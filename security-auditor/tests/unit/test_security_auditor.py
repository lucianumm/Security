from __future__ import annotations

import copy
import datetime as dt
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "security_auditor.py"
SPEC = importlib.util.spec_from_file_location("security_auditor", SCRIPT)
assert SPEC and SPEC.loader
auditor = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = auditor
SPEC.loader.exec_module(auditor)


class GateFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "src").mkdir()
        (self.root / "src" / "app.py").write_text("print('safe')\n", encoding="utf-8")
        (self.root / ".security").mkdir()
        self.tool_dir = SCRIPT.parent
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "security-test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Security Gate Test"], check=True)
        subprocess.run(["git", "-C", str(self.root), "add", "src/app.py"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-q", "-m", "fixture"], check=True)
        self.findings = {
            "schemaVersion": 2,
            "project": "fixture-app",
            "source": {
                "sourceDigest": auditor.source_digest(self.root),
                "scope": ["."],
                "generatedAt": self.now().isoformat().replace("+00:00", "Z"),
                "complete": True,
            },
            "coverage": {"applicableControls": 1, "verifiedControls": 1},
            "scanners": [{"tool": "gitleaks", "version": "8.24.0", "ran": True, "exitCode": 0}],
            "controls": [{"id": "authz.server-side", "status": "IMPLEMENTED", "evidence": ["src/app.py:1"]}],
            "findings": [],
        }
        self.baseline = {
            "schemaVersion": 2,
            "project": "fixture-app",
            "scope": {"included": ["."], "excluded": []},
            "controls": [{"id": "authz.server-side", "expected": "IMPLEMENTED"}],
            "blockingPolicy": {
                "failPipelineOn": ["ACTIVE_SECRET", "AUTHORIZATION"],
                "blockProductionOnHigh": True,
                "blockOnIncomplete": True,
                "allowMitigated": False,
                "minimumCoverage": 0.8,
                "maxFindingAgeDays": 30,
                "requiredTools": [{"tool": "gitleaks", "successExitCodes": [0]}],
            },
        }
        self.findings["source"]["policyDigest"] = auditor.policy_digest(self.baseline)
        self.risks = {"schemaVersion": 2, "risks": []}
        self.write_state()

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def now() -> dt.datetime:
        return dt.datetime.now(dt.timezone.utc)

    def write_state(self) -> None:
        for name, value in (("findings.json", self.findings), ("baseline.json", self.baseline), ("risk-register.json", self.risks)):
            (self.root / ".security" / name).write_text(json.dumps(value), encoding="utf-8")

    def finding(self, *, status: str = "OPEN", severity: str = "HIGH", category: str = "AUTHORIZATION") -> dict:
        today = self.now().date().isoformat()
        return {
            "id": "SEC-0001",
            "title": "Potential cross-tenant access",
            "severity": severity,
            "priority": "P1",
            "confidence": "HIGH",
            "status": status,
            "layer": "BACKEND",
            "category": category,
            "affected": ["src/app.py:1"],
            "evidence": "A request path reaches the object lookup without a tenant check.",
            "impact": "A user may read another tenant's record.",
            "fixType": "REVIEW_RECOMMENDED",
            "regressionTest": "tests/authz/test_tenant_isolation.py",
            "verification": None,
            "firstSeen": today,
            "lastSeen": today,
            "fixedIn": None,
            "history": [],
        }

    def evaluate(self) -> dict:
        self.findings["source"]["policyDigest"] = auditor.policy_digest(self.baseline)
        self.write_state()
        return auditor.evaluate(self.root, self.tool_dir)


class SecurityAuditorGateTests(GateFixture):
    def test_complete_current_audit_with_clean_findings_passes(self) -> None:
        self.assertEqual(self.evaluate()["result"], "PASS")

    def test_empty_object_is_invalid(self) -> None:
        (self.root / ".security" / "findings.json").write_text("{}", encoding="utf-8")
        with self.assertRaises(auditor.GateError):
            auditor.load_checked(".security/findings.json", self.root, "findings.schema.json", self.tool_dir)

    def test_incomplete_audit_cannot_pass(self) -> None:
        self.findings["source"]["complete"] = False
        with self.assertRaisesRegex(auditor.GateError, "incomplete"):
            self.evaluate()

    def test_stale_source_digest_cannot_pass(self) -> None:
        (self.root / "src" / "app.py").write_text("print('changed')\n", encoding="utf-8")
        with self.assertRaisesRegex(auditor.GateError, "do not match"):
            self.evaluate()

    def test_scope_mismatch_cannot_pass(self) -> None:
        self.baseline["scope"]["included"] = ["src"]
        with self.assertRaisesRegex(auditor.GateError, "scope differs"):
            self.evaluate()

    def test_policy_digest_binds_findings_to_the_trusted_baseline(self) -> None:
        self.write_state()
        self.baseline["blockingPolicy"]["blockProductionOnHigh"] = False
        (self.root / ".security" / "baseline.json").write_text(json.dumps(self.baseline), encoding="utf-8")
        with self.assertRaisesRegex(auditor.GateError, "different security policy"):
            auditor.evaluate(self.root, self.tool_dir)

    def test_nonstandard_json_numbers_and_duplicate_keys_are_rejected(self) -> None:
        path = self.root / ".security" / "findings.json"
        path.write_text('{"schemaVersion":2,"schemaVersion":2}', encoding="utf-8")
        with self.assertRaisesRegex(auditor.GateError, "cannot be read or parsed"):
            auditor.read_json(path, self.root)
        path.write_text('{"value":NaN}', encoding="utf-8")
        with self.assertRaisesRegex(auditor.GateError, "cannot be read or parsed"):
            auditor.read_json(path, self.root)

    def test_project_identity_must_match_and_be_configured(self) -> None:
        self.baseline["project"] = "another-project"
        with self.assertRaisesRegex(auditor.GateError, "identity"):
            self.evaluate()
        for placeholder in ("<configure project>", "<custom text>", " TODO ", "[Project Name]", "n/a"):
            with self.subTest(placeholder=placeholder):
                self.baseline["project"] = placeholder
                self.findings["project"] = placeholder
                with self.assertRaisesRegex(auditor.GateError, "identity"):
                    self.evaluate()
        self.baseline["project"] = "fixture-app"
        self.findings["project"] = "fixture-app"

    def test_expired_or_future_audit_timestamp_cannot_pass(self) -> None:
        old = self.now() - dt.timedelta(days=31)
        self.findings["source"]["generatedAt"] = old.isoformat().replace("+00:00", "Z")
        with self.assertRaisesRegex(auditor.GateError, "expired"):
            self.evaluate()
        self.findings["source"]["generatedAt"] = (self.now() + dt.timedelta(minutes=10)).isoformat().replace("+00:00", "Z")
        with self.assertRaisesRegex(auditor.GateError, "future"):
            self.evaluate()

    def test_invalid_coverage_counts_are_rejected(self) -> None:
        self.findings["coverage"]["verifiedControls"] = 2
        with self.assertRaisesRegex(auditor.GateError, "exceeds"):
            self.evaluate()

    def test_zero_applicable_controls_cannot_pass(self) -> None:
        self.findings["coverage"] = {"applicableControls": 0, "verifiedControls": 0}
        with self.assertRaises(auditor.GateError):
            self.evaluate()

    def test_missing_failed_or_unversioned_required_scanner_blocks(self) -> None:
        self.findings["scanners"] = []
        with self.assertRaisesRegex(auditor.GateError, "required security tool"):
            self.findings["scanners"] = [{"tool": "semgrep", "version": "1.0", "ran": True, "exitCode": 0}]
            self.evaluate()
        self.findings["scanners"] = [{"tool": "gitleaks", "version": "8.24.0", "ran": True, "exitCode": 2}]
        with self.assertRaisesRegex(auditor.GateError, "required security tool"):
            self.evaluate()
        self.findings["scanners"][0]["exitCode"] = 0
        self.findings["scanners"][0]["version"] = "unknown"
        with self.assertRaisesRegex(auditor.GateError, "required security tool"):
            self.evaluate()

    def test_duplicate_scanner_and_control_identity_blocks(self) -> None:
        self.findings["scanners"].append({"tool": "gitleaks", "version": "different", "ran": True, "exitCode": 0})
        with self.assertRaisesRegex(auditor.GateError, "duplicate tool"):
            self.evaluate()
        self.findings["scanners"].pop()
        self.findings["controls"].append({"id": "authz.server-side", "status": "NOT_VERIFIED", "evidence": []})
        with self.assertRaisesRegex(auditor.GateError, "duplicate identities"):
            self.evaluate()

    def test_control_regression_blocks(self) -> None:
        self.findings["controls"][0]["status"] = "NOT_VERIFIED"
        with self.assertRaisesRegex(auditor.GateError, "regressed"):
            self.evaluate()

    def test_duplicate_finding_ids_block(self) -> None:
        self.findings["findings"] = [self.finding(), self.finding()]
        with self.assertRaisesRegex(auditor.GateError, "duplicate"):
            self.evaluate()

    def test_pending_statuses_block(self) -> None:
        for status in ("OPEN", "PARTIALLY_FIXED", "REGRESSION", "NOT_VERIFIED", "EXTERNAL_ACTION_REQUIRED"):
            with self.subTest(status=status):
                self.findings["findings"] = [self.finding(status=status)]
                result = self.evaluate()
                self.assertEqual(result["result"], "FAIL")

    def test_critical_and_policy_selected_categories_block(self) -> None:
        self.findings["findings"] = [self.finding(status="OPEN", severity="CRITICAL", category="OTHER")]
        self.baseline["blockingPolicy"]["failPipelineOn"] = []
        self.assertEqual(self.evaluate()["result"], "FAIL")
        self.findings["findings"] = [self.finding(status="OPEN", severity="MEDIUM", category="AUTHORIZATION")]
        self.assertEqual(self.evaluate()["result"], "FAIL")

    def test_fixed_requires_post_fix_verification(self) -> None:
        item = self.finding(status="FIXED", severity="CRITICAL")
        self.findings["findings"] = [item]
        self.assertEqual(self.evaluate()["result"], "FAIL")
        item["verification"] = {"verifiedAt": self.now().isoformat().replace("+00:00", "Z"), "method": "regression_test", "evidence": ["test passed"]}
        self.assertEqual(self.evaluate()["result"], "PASS")

    def test_mitigated_requires_controls_and_explicit_policy(self) -> None:
        item = self.finding(status="MITIGATED", severity="HIGH")
        self.findings["findings"] = [item]
        item["compensatingControls"] = ["Temporary scoped deny rule"]
        self.assertEqual(self.evaluate()["result"], "FAIL")
        self.baseline["blockingPolicy"]["allowMitigated"] = True
        self.assertEqual(self.evaluate()["result"], "PASS")
        del item["compensatingControls"]
        self.assertEqual(self.evaluate()["result"], "FAIL")

    def test_accepted_risk_requires_valid_auditable_exception(self) -> None:
        self.findings["findings"] = [self.finding(status="ACCEPTED_RISK", severity="CRITICAL")]
        self.assertEqual(self.evaluate()["result"], "FAIL")
        start = self.now() - dt.timedelta(days=1)
        expiry = self.now() + dt.timedelta(days=3)
        self.risks["risks"] = [{
            "id": "RISK-0001", "finding": "SEC-0001", "decision": "ACCEPTED_RISK", "acceptedBy": "security-owner",
            "acceptedAt": start.isoformat().replace("+00:00", "Z"), "reviewAt": expiry.isoformat().replace("+00:00", "Z"),
            "approvalRef": "SEC-APPROVAL-42", "rationale": "Temporary exception with a tracked review date.",
            "compensatingControls": ["Restricted to synthetic test accounts"],
        }]
        self.assertEqual(self.evaluate()["result"], "PASS")
        self.risks["risks"][0]["reviewAt"] = (self.now() - dt.timedelta(seconds=1)).isoformat().replace("+00:00", "Z")
        self.assertEqual(self.evaluate()["result"], "FAIL")

    def test_malformed_json_and_missing_state_fail_closed(self) -> None:
        path = self.root / ".security" / "findings.json"
        path.write_text("{broken", encoding="utf-8")
        with self.assertRaises(auditor.GateError):
            auditor.evaluate(self.root, self.tool_dir)
        path.unlink()
        with self.assertRaises(auditor.GateError):
            auditor.evaluate(self.root, self.tool_dir)

    def test_state_templates_match_schemas_and_start_unverified(self) -> None:
        templates = self.tool_dir.parent / "templates" / "state"
        schema_dir = self.tool_dir.parent / "schemas" / "state"
        for name in ("findings", "baseline", "risk-register", "controls", "architecture", "last-audit"):
            with self.subTest(name=name):
                document = json.loads((templates / f"{name}.json").read_text(encoding="utf-8"))
                schema = json.loads((schema_dir / f"{name}.schema.json").read_text(encoding="utf-8"))
                self.assertEqual(auditor.validate_schema(document, schema), [])
        findings = json.loads((templates / "findings.json").read_text(encoding="utf-8"))
        self.assertFalse(findings["source"]["complete"])
        self.assertEqual(findings["findings"], [])

    def test_attack_scenario_schema_accepts_and_rejects_records(self) -> None:
        schema_path = self.tool_dir.parent / "catalog" / "attack-scenarios" / "scenario.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        record = {
            "schemaVersion": 1, "scenarioId": "AS-01", "asset": "invoice API",
            "attacker": {"actor": "authenticated tenant user", "startingCapability": "Can request own invoices", "controlledInputs": ["invoice id"]},
            "objective": "Read another tenant's invoice", "entryPoint": "GET /api/invoices/{id}",
            "boundary": "request handler to database", "preconditions": ["two tenants exist"],
            "steps": [{"action": "request a foreign invoice id", "evidence": ["src/api/invoices.py:20"], "resultingCapability": "Potential cross-tenant read"}],
            "controls": ["session authentication"], "counterevidence": ["tenant filter present in query"],
            "sink": "invoice database row", "impact": "Confidential invoice data could be exposed",
            "evidence": ["src/api/invoices.py:20"],
            "validation": {"profile": "offline-static", "method": "trace query and authorization", "authorized": True, "result": "HYPOTHESIS"},
            "confidence": "LOW", "status": "HYPOTHESIS", "limitations": ["No dynamic request was made"]
        }
        self.assertEqual(auditor.validate_schema(record, schema), [])
        record["validation"]["profile"] = "unauthorized-live-test"
        self.assertTrue(auditor.validate_schema(record, schema))

    def test_output_does_not_echo_finding_text(self) -> None:
        item = self.finding()
        item["title"] = "CANARY-PRIVATE-DESCRIPTION"
        self.findings["findings"] = [item]
        self.write_state()
        completed = subprocess.run([sys.executable, str(SCRIPT), "gate", "--root", str(self.root)], capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 1)
        self.assertNotIn("CANARY-PRIVATE-DESCRIPTION", completed.stdout + completed.stderr)
        self.assertIn("OPEN", completed.stdout)

    def test_trusted_baseline_can_live_outside_untrusted_checkout(self) -> None:
        trusted = self.root.parent / f"{self.root.name}-trusted-baseline.json"
        try:
            trusted.write_text(json.dumps(self.baseline), encoding="utf-8")
            untrusted = copy.deepcopy(self.baseline)
            untrusted["project"] = "attacker-controlled-policy"
            (self.root / ".security" / "baseline.json").write_text(json.dumps(untrusted), encoding="utf-8")
            self.assertEqual(auditor.evaluate(self.root, self.tool_dir, trusted)["result"], "PASS")
        finally:
            trusted.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
