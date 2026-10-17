#!/usr/bin/env python3
"""Validate Security Auditor state and evaluate its fail-closed CI gate.

Uses only the Python standard library. Never runs discovered tools or prints
finding descriptions/evidence. Exit codes: 0 PASS, 1 policy FAIL, 2 INVALID/ERROR.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

VERSION = "1.1.0"
MAX_DOCUMENT_BYTES = 10 * 1024 * 1024
FINDING_ID = re.compile(r"^SEC-[0-9]{4,8}$")
BLOCKING_STATUSES = {"OPEN", "PARTIALLY_FIXED", "REGRESSION", "NOT_VERIFIED", "EXTERNAL_ACTION_REQUIRED"}
ALLOWED_STATUSES = BLOCKING_STATUSES | {"FIXED", "MITIGATED", "ACCEPTED_RISK"}
ALLOWED_SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"}
PLACEHOLDER_PROJECTS = {
    "", "project", "project name", "configure project", "example", "unknown",
    "placeholder", "todo", "tbd", "n/a", "changeme", "change me", "replace me",
    "your project", "project slug",
}


class GateError(Exception):
    """Safe, user-facing validation error without untrusted document content."""


def read_json(path: Path, root: Path, *, allow_outside_root: bool = False) -> Any:
    root = root.resolve()
    if path.is_symlink():
        raise GateError("security state must not be a symlink")
    try:
        resolved = path.resolve(strict=True)
        if (not allow_outside_root and not resolved.is_relative_to(root)) or not resolved.is_file():
            raise GateError("security state path is outside the project")
        if not allow_outside_root:
            cursor = path.absolute()
            while cursor != root and cursor != cursor.parent:
                if cursor.is_symlink():
                    raise GateError("security state path must not contain symlinked directories")
                cursor = cursor.parent
        before = resolved.stat()
        if before.st_size > MAX_DOCUMENT_BYTES:
            raise GateError("security state exceeds the 10 MiB limit")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(resolved, flags)
        with os.fdopen(descriptor, "rb") as stream:
            opened = os.fstat(stream.fileno())
            if (opened.st_dev, opened.st_ino, opened.st_size) != (before.st_dev, before.st_ino, before.st_size):
                raise GateError("security state changed while it was being read")
            payload = stream.read(MAX_DOCUMENT_BYTES + 1)
            if len(payload) > MAX_DOCUMENT_BYTES:
                raise GateError("security state exceeds the 10 MiB limit")
            finished = os.fstat(stream.fileno())
            if (finished.st_dev, finished.st_ino, finished.st_size, finished.st_mtime_ns) != (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns):
                raise GateError("security state changed while it was being read")
        return json.loads(payload.decode("utf-8-sig"), object_pairs_hook=_unique_object_pairs, parse_constant=_reject_json_constant)
    except GateError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GateError(f"security state cannot be read or parsed ({type(exc).__name__})") from None
    except (ValueError, RecursionError) as exc:
        raise GateError(f"security state cannot be read or parsed ({type(exc).__name__})") from None


def _unique_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise ValueError("non-standard JSON number")


def _json_type(value: Any, expected: str) -> bool:
    return {
        "object": lambda: isinstance(value, dict),
        "array": lambda: isinstance(value, list),
        "string": lambda: isinstance(value, str),
        "integer": lambda: isinstance(value, int) and not isinstance(value, bool),
        "number": lambda: isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": lambda: isinstance(value, bool),
        "null": lambda: value is None,
    }.get(expected, lambda: False)()


def _resolve_ref(ref: str, schema: dict[str, Any]) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise GateError("schema contains an unsupported reference")
    target: Any = schema
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(target, dict) or part not in target:
            raise GateError("schema reference is unresolved")
        target = target[part]
    if not isinstance(target, dict):
        raise GateError("schema reference is invalid")
    return target


def validate_schema(value: Any, schema: dict[str, Any], path: str = "$", document_schema: dict[str, Any] | None = None) -> list[str]:
    root_schema = document_schema or schema
    if "$ref" in schema:
        return validate_schema(value, _resolve_ref(schema["$ref"], root_schema), path, root_schema)
    issues: list[str] = []
    expected = schema.get("type")
    if isinstance(expected, list):
        matches = any(_json_type(value, item) for item in expected)
    elif isinstance(expected, str):
        matches = _json_type(value, expected)
    else:
        matches = True
    if not matches:
        return [f"{path}: wrong type"]
    if "enum" in schema and value not in schema["enum"]:
        issues.append(f"{path}: value outside the allowed set")
    if "const" in schema and value != schema["const"]:
        issues.append(f"{path}: constant value mismatch")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                issues.append(f"{path}: required property missing")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False and any(key not in properties for key in value):
            issues.append(f"{path}: unexpected property")
        for key, child_schema in properties.items():
            if key in value:
                issues.extend(validate_schema(value[key], child_schema, f"{path}.{key}", root_schema))
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", MAX_DOCUMENT_BYTES):
            issues.append(f"{path}: array length outside limits")
        if schema.get("uniqueItems"):
            try:
                canonical = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in value]
                if len(canonical) != len(set(canonical)):
                    issues.append(f"{path}: duplicate array item")
            except (TypeError, ValueError):
                issues.append(f"{path}: array item cannot be compared")
        if "items" in schema:
            for index, child in enumerate(value):
                issues.extend(validate_schema(child, schema["items"], f"{path}[{index}]", root_schema))
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or len(value) > schema.get("maxLength", 1_000_000):
            issues.append(f"{path}: string length outside limits")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            issues.append(f"{path}: string format mismatch")
        if schema.get("format") == "date-time":
            try:
                parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    raise ValueError
            except ValueError:
                issues.append(f"{path}: timestamp must include a timezone")
        elif schema.get("format") == "date":
            try:
                dt.date.fromisoformat(value)
            except ValueError:
                issues.append(f"{path}: date format mismatch")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            issues.append(f"{path}: number below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            issues.append(f"{path}: number above maximum")
    return issues


def load_checked(relative: str, root: Path, schema_name: str, tool_dir: Path) -> dict[str, Any]:
    document = read_json(root / relative, root)
    if not isinstance(document, dict):
        raise GateError(f"{relative} must contain a JSON object")
    schema_path = tool_dir.parent / "schemas" / "state" / schema_name
    schema = read_json(schema_path, tool_dir.parent)
    errors = validate_schema(document, schema)
    if errors:
        raise GateError(f"{relative} failed schema validation ({len(errors)} error(s); first: {errors[0]})")
    return document


def source_digest(root: Path) -> str:
    """Hash source content; exclude reports/state to avoid a self-referential digest."""
    try:
        listing = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            check=True, capture_output=True, timeout=30, shell=False,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        raise GateError("cannot enumerate project files for source verification") from None
    digest = __import__("hashlib").sha256()
    total = 0
    if len(listing) > 64 * 1024 * 1024:
        raise GateError("project source inventory exceeds the 64 MiB listing limit")
    paths = sorted(set(os.fsdecode(item) for item in listing.split(b"\0") if item))
    included = [p for p in paths if p.replace("\\", "/") not in {".security", "security"} and not p.replace("\\", "/").startswith((".security/", "security/"))]
    if not included:
        raise GateError("project source inventory is empty")
    if len(included) > 100_000:
        raise GateError("project source inventory exceeds 100,000 files")
    for relative in included:
        normalized = relative.replace("\\", "/")
        parts = normalized.split("/")
        if normalized.startswith("/") or any(part in {"", ".", ".."} for part in parts):
            raise GateError("project source inventory contains an unsafe path")
        candidate = root.joinpath(*parts)
        try:
            cursor = root
            for part in parts[:-1]:
                cursor = cursor / part
                is_junction = getattr(cursor, "is_junction", lambda: False)()
                if cursor.is_symlink() or is_junction:
                    raise GateError("project source contains a symlinked directory")
            resolved_candidate = candidate.resolve(strict=True)
            if not resolved_candidate.is_relative_to(root.resolve()):
                raise GateError("project source contains a path outside the project")
            stat = candidate.lstat()
            digest.update(normalized.encode("utf-8", "surrogateescape") + b"\0")
            digest.update(str(stat.st_mode & 0o777).encode("ascii") + b"\0")
            if candidate.is_symlink():
                target = candidate.resolve(strict=True)
                if not target.is_relative_to(root.resolve()):
                    raise GateError("project source contains a symlink outside the project")
                payload = os.readlink(candidate).encode("utf-8", "surrogateescape")
                total += len(payload)
                if total > 2 * 1024 * 1024 * 1024:
                    raise GateError("project source exceeds the 2 GiB hashing limit")
                digest.update(b"L" + str(len(payload)).encode("ascii") + b"\0" + payload)
            elif candidate.is_file():
                if stat.st_size > 512 * 1024 * 1024:
                    raise GateError("a source file exceeds the 512 MiB limit")
                digest.update(b"F")
                flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
                descriptor = os.open(candidate, flags)
                with os.fdopen(descriptor, "rb") as stream:
                    opened = os.fstat(stream.fileno())
                    if (opened.st_dev, opened.st_ino, opened.st_size) != (stat.st_dev, stat.st_ino, stat.st_size):
                        raise GateError("a project source file changed during verification")
                    while chunk := stream.read(1024 * 1024):
                        total += len(chunk)
                        if total > 2 * 1024 * 1024 * 1024:
                            raise GateError("project source exceeds the 2 GiB hashing limit")
                        digest.update(chunk)
                    finished = os.fstat(stream.fileno())
                    if (finished.st_dev, finished.st_ino, finished.st_size, finished.st_mtime_ns) != (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns):
                        raise GateError("a project source file changed during verification")
                digest.update(b"\0")
            else:
                raise GateError("project source contains a non-regular file")
        except GateError:
            raise
        except OSError:
            raise GateError("a project source file cannot be hashed") from None
    return digest.hexdigest()


def policy_digest(baseline: dict[str, Any]) -> str:
    payload = json.dumps(baseline, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    return __import__("hashlib").sha256(payload).hexdigest()


def _accepted_risks(risk_doc: dict[str, Any], finding: dict[str, Any], now: dt.datetime) -> bool:
    for risk in risk_doc["risks"]:
        if risk["finding"] != finding["id"] or risk["decision"] != "ACCEPTED_RISK":
            continue
        try:
            if not risk["acceptedAt"] or not risk["reviewAt"] or not risk["approvalRef"]:
                return False
            accepted = dt.datetime.fromisoformat(risk["acceptedAt"].replace("Z", "+00:00"))
            expires = dt.datetime.fromisoformat(risk["reviewAt"].replace("Z", "+00:00"))
        except ValueError:
            return False
        if accepted.tzinfo is None or expires.tzinfo is None:
            return False
        if accepted > now or expires <= accepted or expires <= now or not risk["acceptedBy"].strip() or not risk["approvalRef"].strip() or not risk["compensatingControls"]:
            return False
        return True
    return False


def evaluate(
    root: Path,
    tool_dir: Path,
    trusted_baseline: Path | None = None,
    trusted_risk_register: Path | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    findings_doc = load_checked(".security/findings.json", root, "findings.schema.json", tool_dir)
    if trusted_baseline is None:
        baseline = load_checked(".security/baseline.json", root, "baseline.schema.json", tool_dir)
    else:
        baseline = read_json(trusted_baseline, root, allow_outside_root=True)
        if not isinstance(baseline, dict):
            raise GateError("trusted baseline must contain a JSON object")
        schema = read_json(tool_dir.parent / "schemas" / "state" / "baseline.schema.json", tool_dir.parent)
        errors = validate_schema(baseline, schema)
        if errors:
            raise GateError(f"trusted baseline failed schema validation ({len(errors)} error(s); first: {errors[0]})")
    if trusted_risk_register is None:
        risk_doc = load_checked(".security/risk-register.json", root, "risk-register.schema.json", tool_dir)
    else:
        risk_doc = read_json(trusted_risk_register, root, allow_outside_root=True)
        if not isinstance(risk_doc, dict):
            raise GateError("trusted risk register must contain a JSON object")
        schema = read_json(tool_dir.parent / "schemas" / "state" / "risk-register.schema.json", tool_dir.parent)
        errors = validate_schema(risk_doc, schema)
        if errors:
            raise GateError(f"trusted risk register failed schema validation ({len(errors)} error(s); first: {errors[0]})")
    raw_project_identity = findings_doc["project"].strip()
    project_identity = raw_project_identity.strip("<>[] ").casefold()
    bracketed_placeholder = (raw_project_identity.startswith("<") and raw_project_identity.endswith(">")) or (raw_project_identity.startswith("[") and raw_project_identity.endswith("]"))
    if bracketed_placeholder or project_identity in PLACEHOLDER_PROJECTS or findings_doc["project"] != baseline["project"]:
        raise GateError("project identity is missing or differs from the trusted baseline")
    current = source_digest(root).lower()
    if not re.fullmatch(r"[0-9a-f]{64}", current):
        raise GateError("expected source digest has an invalid format")
    if findings_doc["source"]["sourceDigest"].lower() != current:
        raise GateError("findings do not match the evaluated project source")
    if findings_doc["source"]["policyDigest"].lower() != policy_digest(baseline):
        raise GateError("findings were prepared under a different security policy")
    if set(findings_doc["source"]["scope"]) != set(baseline["scope"]["included"]):
        raise GateError("audit scope differs from the trusted baseline scope")
    if len({item["tool"] for item in baseline["blockingPolicy"]["requiredTools"]}) != len(baseline["blockingPolicy"]["requiredTools"]):
        raise GateError("trusted baseline contains duplicate required tool identities")
    if len({item["id"] for item in baseline["controls"]}) != len(baseline["controls"]):
        raise GateError("trusted baseline contains duplicate control identities")
    if len({item["id"] for item in risk_doc["risks"]}) != len(risk_doc["risks"]) or len({item["finding"] for item in risk_doc["risks"]}) != len(risk_doc["risks"]):
        raise GateError("risk register contains duplicate identities")
    if not findings_doc["source"]["complete"]:
        raise GateError("audit is incomplete; PASS is unavailable")
    minimum = baseline["blockingPolicy"]["minimumCoverage"]
    coverage = findings_doc["coverage"]
    if coverage["verifiedControls"] > coverage["applicableControls"]:
        raise GateError("verified control count exceeds the applicable control count")
    if coverage["applicableControls"] == 0:
        raise GateError("audit has no applicable controls; PASS is unavailable")
    ratio = coverage["verifiedControls"] / coverage["applicableControls"]
    if ratio < minimum:
        raise GateError("verified control coverage is below the configured minimum")
    source_age = dt.datetime.fromisoformat(findings_doc["source"]["generatedAt"].replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    max_age = baseline["blockingPolicy"]["maxFindingAgeDays"]
    if (now - source_age).total_seconds() > max_age * 86400:
        raise GateError("audit evidence has expired")
    if (source_age - now).total_seconds() > 300:
        raise GateError("audit evidence timestamp is too far in the future")

    scanner_runs = {item["tool"]: item for item in findings_doc["scanners"]}
    if len(scanner_runs) != len(findings_doc["scanners"]):
        raise GateError("scanner results contain duplicate tool identities")
    for required in baseline["blockingPolicy"]["requiredTools"]:
        scan = scanner_runs.get(required["tool"])
        if scan is None or not scan["ran"] or scan["version"].strip().lower() in {"unknown", "not-run", "unavailable"} or scan["exitCode"] not in required["successExitCodes"]:
            raise GateError("a required security tool is missing, failed, or has no version")

    observed_controls = {item["id"]: item for item in findings_doc["controls"]}
    if len(observed_controls) != len(findings_doc["controls"]):
        raise GateError("control results contain duplicate identities")
    for expected in baseline["controls"]:
        actual = observed_controls.get(expected["id"])
        if actual is None:
            raise GateError("a baseline control is missing from the current audit")
        if expected["expected"] == "IMPLEMENTED" and actual["status"] != "IMPLEMENTED":
            raise GateError("a control regressed from its required baseline state")
        if actual["status"] in {"NOT_VERIFIED", "PARTIALLY_IMPLEMENTED", "NOT_IMPLEMENTED", "MISCONFIGURED"}:
            if baseline["blockingPolicy"]["blockOnIncomplete"]:
                raise GateError("a required control is incomplete or unverified")

    blocking = []
    seen_findings = set()
    statuses = set()
    for finding in findings_doc["findings"]:
        fid = finding["id"]
        if not FINDING_ID.fullmatch(fid):
            raise GateError("finding ID has an invalid format")
        if fid in seen_findings:
            raise GateError("findings contain duplicate identities")
        seen_findings.add(fid)
        status = finding["status"]
        severity = finding["severity"]
        statuses.add(status)
        if status not in ALLOWED_STATUSES or severity not in ALLOWED_SEVERITIES:
            raise GateError("finding contains an unsupported status or severity")
        if status == "ACCEPTED_RISK" and not _accepted_risks(risk_doc, finding, now):
            blocking.append((fid, "INVALID_OR_EXPIRED_EXCEPTION"))
            continue
        if status == "FIXED":
            verification = finding.get("verification")
            if not isinstance(verification, dict) or not verification.get("evidence") or not verification.get("verifiedAt"):
                blocking.append((fid, "MISSING_FIX_VERIFICATION"))
                continue
        if status == "MITIGATED":
            if not finding.get("compensatingControls"):
                blocking.append((fid, "MISSING_COMPENSATING_CONTROL"))
                continue
            if not baseline["blockingPolicy"]["allowMitigated"]:
                blocking.append((fid, "MITIGATED_RISK_REQUIRES_REVIEW"))
                continue
        if status in BLOCKING_STATUSES:
            blocking.append((fid, status))
            continue
        if severity == "CRITICAL" or (severity == "HIGH" and baseline["blockingPolicy"]["blockProductionOnHigh"]):
            if status not in {"FIXED", "MITIGATED", "ACCEPTED_RISK"}:
                blocking.append((fid, severity))
        category = finding.get("category", "").upper().replace(" ", "_")
        if category in baseline["blockingPolicy"]["failPipelineOn"] and status not in {"FIXED", "MITIGATED", "ACCEPTED_RISK"}:
            blocking.append((fid, category))

    result = "FAIL" if blocking else "PASS"
    return {
        "result": result,
        "sourceDigest": current,
        "coverage": round(ratio, 4),
        "findings": len(findings_doc["findings"]),
        "blocking": [{"id": fid, "reason": reason} for fid, reason in blocking],
        "auditCompletedAt": findings_doc["source"]["generatedAt"],
        "toolCount": len(findings_doc["scanners"]),
    }


def cli() -> int:
    parser = argparse.ArgumentParser(description="Validate security state and evaluate a fail-closed security gate.")
    parser.add_argument("--version", action="version", version=f"security-auditor {VERSION}")
    commands = parser.add_subparsers(dest="command", required=True)
    gate = commands.add_parser("gate", help="validate state and evaluate blocking policy")
    gate.add_argument("--root", type=Path, default=Path.cwd())
    gate.add_argument("--trusted-baseline", type=Path, help="load policy from a separately protected baseline file")
    gate.add_argument("--trusted-risk-register", type=Path, help="load exceptions from a separately protected risk register")
    validate = commands.add_parser("validate", help="validate security state without applying policy")
    validate.add_argument("--root", type=Path, default=Path.cwd())
    hash_command = commands.add_parser("source-digest", help="compute the source digest for the current project tree")
    hash_command.add_argument("--root", type=Path, default=Path.cwd())
    policy_command = commands.add_parser("policy-digest", help="compute a canonical digest for the configured baseline")
    policy_command.add_argument("--root", type=Path, default=Path.cwd())
    policy_command.add_argument("--baseline", type=Path, default=Path(".security/baseline.json"))
    args = parser.parse_args()
    root = args.root.resolve()
    tool_dir = Path(__file__).resolve().parent
    try:
        if args.command == "source-digest":
            print(json.dumps({"sourceDigest": source_digest(root)}, separators=(",", ":")))
            return 0
        if args.command == "policy-digest":
            baseline = read_json(args.baseline if args.baseline.is_absolute() else root / args.baseline, root)
            if not isinstance(baseline, dict):
                raise GateError("baseline must contain a JSON object")
            schema = read_json(tool_dir.parent / "schemas" / "state" / "baseline.schema.json", tool_dir.parent)
            errors = validate_schema(baseline, schema)
            if errors:
                raise GateError(f"baseline failed schema validation ({len(errors)} error(s); first: {errors[0]})")
            print(json.dumps({"policyDigest": policy_digest(baseline)}, separators=(",", ":")))
            return 0
        if args.command == "gate":
            result = evaluate(root, tool_dir, args.trusted_baseline, args.trusted_risk_register)
            print(json.dumps(result, sort_keys=True, separators=(",", ":")))
            return 0 if result["result"] == "PASS" else 1
        for relative, schema_name in [
            (".security/findings.json", "findings.schema.json"),
            (".security/baseline.json", "baseline.schema.json"),
            (".security/risk-register.json", "risk-register.schema.json"),
            (".security/controls.json", "controls.schema.json"),
            (".security/architecture.json", "architecture.schema.json"),
            (".security/last-audit.json", "last-audit.schema.json"),
        ]:
            load_checked(relative, root, schema_name, tool_dir)
        print(json.dumps({"result": "VALID"}, separators=(",", ":")))
        return 0
    except GateError as exc:
        print(json.dumps({"result": "ERROR", "reason": str(exc)}, separators=(",", ":")))
        return 2
    except (KeyError, TypeError, ValueError, ZeroDivisionError, RecursionError):
        print(json.dumps({"result": "ERROR", "reason": "security state is inconsistent"}, separators=(",", ":")))
        return 2


if __name__ == "__main__":
    sys.exit(cli())
