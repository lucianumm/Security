#!/usr/bin/env python3
"""Offline discovery, encyclopedia coverage and local-patch approval preflight.

Never executes project code, installs packages, applies patches or grants approval.
JSON goes to stdout; caller controls report storage. Python 3.10+, standard library.
Exit codes: 0 valid/complete, 1 incomplete review, 2 invalid/denied.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True

from build_encyclopedia import BASE, CATALOG, build
from security_auditor import GateError, read_json, source_digest, validate_schema

MAX_FILE = 2 * 1024 * 1024
MAX_TOTAL = 32 * 1024 * 1024
MAX_FILES = 100_000
SKIP = {".git", ".security", "security", "node_modules", "vendor", "dist", "build", ".next", "target", "__pycache__", ".venv", "venv"}
TEXT_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".toml", ".yaml", ".yml", ".go", ".rs", ".java", ".kt", ".swift", ".cs", ".php", ".rb", ".tf", ".xml", ".gradle", ".c", ".h", ".cpp", ".html", ".sql"}
SIGNALS = {
    "python": r"\b(?:django|flask|fastapi|starlette)\b",
    "web": r"\b(?:express|next|react|vue|svelte|django|flask|fastapi|spring-boot|laravel)\b",
    "database": r"\b(?:prisma|sequelize|typeorm|sqlalchemy|psycopg|mongoose|postgresql|mysql|sqlite|redis)\b",
    "ai": r"\b(?:openai|anthropic|langchain|llamaindex|mcp|modelcontextprotocol)\b",
    "payments": r"\b(?:stripe|paypal|mercadopago)\b",
    "mobile": r"\b(?:react-native|flutter|android|swiftui)\b",
    "native": r"\b(?:unsafe|malloc|strcpy|memcpy)\b",
}
DOMAIN_SIGNALS = {
    1: {"web", "mobile"}, 2: {"web", "database", "ai"}, 3: {"web", "native", "database"},
    4: {"web"}, 5: {"web", "ai"}, 6: {"web", "payments"}, 7: {"database", "mobile", "ai"},
    8: {"cloud", "web"}, 9: {"cloud"}, 10: {"docker", "kubernetes"},
    11: {"dependencies", "ci"}, 12: {"native", "ci"}, 13: set(),
    14: {"mobile", "desktop"}, 15: {"iot"}, 16: {"ai"}, 17: set(),
    18: {"native"}, 19: {"iot", "mobile"},
}


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def digest(document: dict) -> str:
    return sha(json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode())


def catalog() -> dict:
    bundled = read_json(CATALOG, BASE)
    if bundled != build():
        raise GateError("bundled encyclopedia differs from its source; maintainer review required")
    return bundled


def checked_json(path: Path, schema_name: str) -> dict:
    document = read_json(path, path.parent.resolve())
    schema = read_json(BASE / "schemas" / schema_name, BASE)
    if validate_schema(document, schema):
        raise GateError("document does not satisfy its schema")
    return document


def safe_relative(value: str) -> str:
    # Reject drive, ADS, traversal, glob and control characters on every platform.
    if (not isinstance(value, str) or not value or "\\" in value or
            any(c in value for c in ":*?[]\x00\r\n") or any(ord(c) < 32 for c in value)):
        raise GateError("unsafe relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in {"", ".", "..", ".git"} for p in value.split("/")):
        raise GateError("unsafe relative path")
    return value


def safe_path(root: Path, relative: str) -> Path:
    safe_relative(relative)
    candidate = root
    for part in relative.split("/"):
        candidate = candidate / part
        if candidate.is_symlink() or getattr(candidate, "is_junction", lambda: False)():
            raise GateError("symlink or junction in project path")
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise GateError("path escapes project")
    return candidate


def inventory(root: Path) -> list[str]:
    # No repository hooks, build tools, package scripts or shell evaluation.
    root = root.resolve()
    try:
        top = subprocess.run(["git", "-c", "core.fsmonitor=false", "-C", str(root), "rev-parse", "--show-toplevel"], capture_output=True, check=True, timeout=15)
        if Path(os.fsdecode(top.stdout).strip()).resolve() != root:
            raise GateError("root must be the Git worktree root")
        result = subprocess.run(["git", "-c", "core.fsmonitor=false", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"], capture_output=True, check=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        raise GateError("cannot enumerate Git project") from None
    if len(result.stdout) > 64 * 1024 * 1024:
        raise GateError("project inventory exceeds limits")
    paths = sorted({os.fsdecode(p) for p in result.stdout.split(b"\0") if p})
    if len(paths) > MAX_FILES:
        raise GateError("project inventory exceeds limits")
    for path in paths:
        safe_relative(path)
    return paths


def profile(root: Path, cat: dict) -> dict:
    root = root.resolve()
    before = source_digest(root)
    paths = inventory(root)
    signals: dict[str, list[str]] = {}
    omissions: dict[str, int] = {}
    total = 0

    def signal(name: str, path: str) -> None:
        if path not in signals.setdefault(name, []) and len(signals[name]) < 20:
            signals[name].append(path)

    for relative in paths:
        parts = PurePosixPath(relative).parts
        name = parts[-1].lower()
        if any(p in SKIP for p in parts[:-1]) or name.startswith(".env") or name.endswith((".pem", ".key", ".p12", ".pfx")):
            omissions["excludedOrSensitivePaths"] = omissions.get("excludedOrSensitivePaths", 0) + 1
            continue
        path = safe_path(root, relative)
        if name in {"package.json", "pyproject.toml", "requirements.txt", "go.mod", "cargo.toml", "composer.json", "pom.xml", "gemfile"}:
            signal("dependencies", relative)
        if ".github" in parts or name in {".gitlab-ci.yml", "jenkinsfile"}:
            signal("ci", relative)
        if name.startswith("dockerfile") or "compose" in name:
            signal("docker", relative)
        if any(p in {"k8s", "charts", "helm"} for p in parts):
            signal("kubernetes", relative)
        if path.suffix == ".tf" or any(p in {"terraform", "pulumi"} for p in parts):
            signal("cloud", relative)
        if path.suffix in {".c", ".h", ".cpp", ".rs"}:
            signal("native", relative)
        if name in {"androidmanifest.xml", "pubspec.yaml"} or path.suffix == ".swift":
            signal("mobile", relative)
        if name in {"platformio.ini", "idf_component.yml"}:
            signal("iot", relative)
        if path.suffix.lower() not in TEXT_SUFFIXES and not name.startswith("dockerfile"):
            continue
        if not path.is_file() or path.stat().st_size > MAX_FILE or total + path.stat().st_size > MAX_TOTAL:
            omissions["unreadableOrBudgetExceeded"] = omissions.get("unreadableOrBudgetExceeded", 0) + 1
            continue
        with path.open("rb") as stream:
            payload = stream.read(MAX_FILE + 1)
        total += len(payload)
        if len(payload) > MAX_FILE:
            raise GateError("project file changed or exceeds profile read limit")
        text = payload.decode("utf-8", errors="replace").lower()
        for key, pattern in SIGNALS.items():
            if re.search(pattern, text):
                signal(key, relative)
        if '"electron"' in text or '"tauri"' in text:
            signal("desktop", relative)
        if re.search(r"(?m)^kind:\s*(deployment|pod|statefulset|service)\s*$", text):
            signal("kubernetes", relative)
    if source_digest(root) != before:
        raise GateError("project changed while profiling; retry on a stable tree")
    return {
        "schemaVersion": 1, "sourceDigest": before, "catalogDigest": digest(cat),
        "scope": ["."], "complete": False,
        "discovery": {"signals": signals, "omissions": omissions,
                      "limits": ["Git-ignored files, history and submodule contents not inspected", "Signals are routing hints, not security findings", "External runtime and provider controls require independent evidence"]},
        "controls": [{"id": c["id"], "status": "NOT_VERIFIED", "applicability": "UNKNOWN", "evidence": [], "reason": "", "findings": []} for c in cat["controls"]],
        "domains": [{"id": d["id"], "candidate": bool(DOMAIN_SIGNALS[int(d["section"].split(".")[1])] & signals.keys()), "modules": d["modules"]} for d in cat["domains"]],
        "scenarios": [{"id": s["id"], "status": "NOT_VERIFIED", "evidence": [], "reason": "", "findings": []} for s in cat["scenarios"]],
    }


def exact_ids(rows: list[dict], expected: set[str]) -> None:
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)) or set(ids) != expected:
        raise GateError("coverage IDs are duplicated, missing or unknown")


def validate_coverage(root: Path, document: dict, cat: dict) -> dict:
    if document["sourceDigest"] != source_digest(root) or document["catalogDigest"] != digest(cat):
        raise GateError("coverage is stale for this source or catalog")
    # Full review only; targeted audits must not pretend to cover the full catalog.
    if document["scope"] != ["."]:
        raise GateError("encyclopedia completeness requires explicit full-project scope")
    exact_ids(document["controls"], {c["id"] for c in cat["controls"]})
    exact_ids(document["scenarios"], {s["id"] for s in cat["scenarios"]})
    exact_ids(document["domains"], {d["id"] for d in cat["domains"]})
    unreviewed = 0
    finding_refs: set[str] = set()
    for row in document["controls"]:
        status, applicability = row["status"], row["applicability"]
        if (status == "NOT_APPLICABLE") != (applicability == "NOT_APPLICABLE"):
            raise GateError("control applicability contradicts status")
        if status == "NOT_VERIFIED" or applicability == "UNKNOWN":
            unreviewed += 1
        if status != "NOT_VERIFIED" and (not row["evidence"] or not row["reason"].strip()):
            raise GateError("reviewed control lacks evidence or rationale")
        if status in {"NOT_IMPLEMENTED", "MISCONFIGURED", "PARTIALLY_IMPLEMENTED"} and not row["findings"]:
            raise GateError("control gap must link a finding or hardening proposal")
        finding_refs.update(row["findings"])
    for row in document["scenarios"]:
        if row["status"] in {"NOT_VERIFIED", "INCONCLUSIVE"}:
            unreviewed += 1
        if row["status"] != "NOT_VERIFIED" and (not row["evidence"] or not row["reason"].strip()):
            raise GateError("reviewed scenario lacks evidence or rationale")
        if row["status"] in {"SUPPORTED", "REPRODUCED"} and not row["findings"]:
            raise GateError("supported scenario lacks a finding reference")
        finding_refs.update(row["findings"])
    if finding_refs:
        from security_auditor import load_checked
        findings = load_checked(".security/findings.json", root, "findings.schema.json", BASE / "scripts")
        if findings["source"]["sourceDigest"] != document["sourceDigest"]:
            raise GateError("referenced findings are stale")
        if not finding_refs <= {f["id"] for f in findings["findings"]}:
            raise GateError("coverage references an unknown finding")
    if document["complete"] and unreviewed:
        raise GateError("complete coverage cannot contain unknown or unverified items")
    return {"result": "COMPLETE" if document["complete"] and not unreviewed else "INCOMPLETE",
            "unreviewed": unreviewed, "controlCount": len(document["controls"]),
            "scenarioCount": len(document["scenarios"]),
            "securityVerdict": "NOT_ASSESSED_BY_COVERAGE_VALIDATOR"}


def external_file(path: Path, root: Path) -> Path:
    # External files are trusted only if the caller's environment actually protects them.
    cursor = path.absolute()
    while cursor != cursor.parent:
        if cursor.is_symlink() or getattr(cursor, "is_junction", lambda: False)():
            raise GateError("approval input path must not contain symlinks or junctions")
        cursor = cursor.parent
    resolved = path.resolve(strict=True)
    if resolved.is_relative_to(root) or not resolved.is_file():
        raise GateError("approval inputs must be regular files outside the audited worktree")
    return resolved


def patch_paths(payload: bytes) -> set[str]:
    # Intentionally accepts only ordinary Git text patches, with simple relative paths.
    # The preflight does not execute Git apply or try to support every patch dialect.
    text = payload.decode("utf-8")
    if any(marker in text for marker in ("GIT binary patch", "Binary files ", "rename from ", "rename to ", "copy from ", "copy to ", "mode 120000", "mode 160000")):
        raise GateError("unsupported binary, rename, copy, symlink or submodule patch")
    paths = set()
    headers = 0
    for line in text.splitlines():
        if line.startswith("diff --git "):
            match = re.fullmatch(r"diff --git a/([^\s]+) b/([^\s]+)", line)
            if not match or match[1] != match[2]:
                raise GateError("patch requires simple identical old/new paths")
            paths.add(safe_relative(match[1]))
            headers += 1
        elif line.startswith(("--- ", "+++ ")):
            value = line[4:]
            if value == "/dev/null":
                continue
            if not value.startswith(("a/", "b/")) or safe_relative(value[2:]) not in paths:
                raise GateError("patch file header differs from declared diff paths")
    if not paths or headers != len(paths):
        raise GateError("patch has no supported changes or duplicates paths")
    return paths


def approval_check(root: Path, plan_path: Path, receipt_path: Path, patch_path: Path, cat: dict, now: dt.datetime | None = None) -> dict:
    root = root.resolve()
    plan_path, receipt_path, patch_path = [external_file(p, root) for p in (plan_path, receipt_path, patch_path)]
    plan = checked_json(plan_path, "remediation-plan.schema.json")
    receipt = checked_json(receipt_path, "approval.schema.json")
    if Path(plan["projectRoot"]).resolve() != root or plan["sourceDigest"] != source_digest(root):
        raise GateError("plan is for another worktree or stale source")
    if plan["catalogDigest"] != digest(cat):
        raise GateError("plan uses a different encyclopedia catalog")
    if receipt["planDigest"] != digest(plan) or receipt["sourceDigest"] != plan["sourceDigest"]:
        raise GateError("approval does not match this plan and source")
    now = now or dt.datetime.now(dt.timezone.utc)
    issued = dt.datetime.fromisoformat(receipt["issuedAt"].replace("Z", "+00:00"))
    expires = dt.datetime.fromisoformat(receipt["expiresAt"].replace("Z", "+00:00"))
    if issued > now or expires <= now or expires <= issued:
        raise GateError("approval is future-dated or expired")
    actions = plan["actions"]
    ids = [a["id"] for a in actions]
    if len(ids) != len(set(ids)) or set(ids) != set(receipt["approvedActions"]):
        raise GateError("approval must cover exactly the reviewed batch; split the plan for partial approval")
    if not receipt["userMessageRef"].strip() or not receipt["approvedBy"].strip():
        raise GateError("approval requires an authenticated user-message reference")
    known_controls = {c["id"] for c in cat["controls"]}
    declared_paths = set()
    for action in actions:
        if not action["findingIds"] and not action["controlIds"]:
            raise GateError("action must reference a finding or a catalog control")
        if not set(action["controlIds"]) <= known_controls:
            raise GateError("action references an unknown catalog control")
        for relative in action["paths"]:
            safe_path(root, relative)
            declared_paths.add(relative)
    if patch_path.stat().st_size > 10 * 1024 * 1024:
        raise GateError("patch exceeds the 10 MiB limit")
    with patch_path.open("rb") as stream:
        patch = stream.read(10 * 1024 * 1024 + 1)
    if len(patch) > 10 * 1024 * 1024 or sha(patch) != plan["patchSha256"]:
        raise GateError("patch differs from the reviewed plan")
    if patch_paths(patch) != declared_paths:
        raise GateError("patch paths differ from the reviewed action scope")
    try:
        subprocess.run(["git", "-c", "core.fsmonitor=false", "-C", str(root), "apply", "--check", "--whitespace=nowarn", "-"],
                       input=patch, check=True, capture_output=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        raise GateError("reviewed patch does not apply cleanly to the current worktree") from None
    return {"result": "PREFLIGHT_VALID", "planDigest": digest(plan), "approvedActions": ids,
            "operation": "PATCH_LOCAL", "applied": False,
            "identityVerifiedByHelper": False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["profile", "validate-coverage", "plan-digest", "approval-check"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--coverage", type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--approval", type=Path)
    parser.add_argument("--patch", type=Path)
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve(strict=True)
        cat = catalog()
        if args.command == "profile":
            result = profile(root, cat)
        elif args.command == "validate-coverage":
            if not args.coverage:
                raise GateError("--coverage is required")
            result = validate_coverage(root, checked_json(args.coverage, "encyclopedia-coverage.schema.json"), cat)
        elif args.command == "plan-digest":
            if not args.plan:
                raise GateError("--plan is required")
            result = {"planDigest": digest(checked_json(args.plan, "remediation-plan.schema.json"))}
        else:
            if not all((args.plan, args.approval, args.patch)):
                raise GateError("--plan, --approval and --patch are required")
            result = approval_check(root, args.plan, args.approval, args.patch, cat)
        print(json.dumps(result, ensure_ascii=True, sort_keys=True))
        return 1 if result.get("result") == "INCOMPLETE" else 0
    except (GateError, OSError, ValueError, KeyError, TypeError, RecursionError):
        # Never echo untrusted content, filenames, secrets or document values.
        print(json.dumps({"result": "DENIED_OR_INVALID", "reason": "Invalid, stale, incomplete or out-of-scope input; inspect locally without exposing secrets."}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
