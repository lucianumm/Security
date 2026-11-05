from __future__ import annotations

import copy
import datetime as dt
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True
import encyclopedia as enc
import build_encyclopedia as importer
from security_auditor import GateError, validate_schema


class EncyclopediaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp.name).resolve()
        self.root = self.workspace / "app"
        self.root.mkdir()
        self.trusted = self.workspace / "trusted"
        self.trusted.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.root)], check=True)
        (self.root / "src").mkdir()
        (self.root / "src" / "app.py").write_text("print('example')\n", encoding="utf-8")
        self.cat = enc.catalog()
        self.now = dt.datetime.now(dt.timezone.utc)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, value):
        path = self.trusted / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def package(self):
        patch = b"diff --git a/src/app.py b/src/app.py\n--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1 @@\n-print('example')\n+print('updated')\n"
        patch_path = self.trusted / "changes.patch"
        patch_path.write_bytes(patch)
        plan = {
            "schemaVersion": 1, "projectRoot": str(self.root),
            "sourceDigest": enc.source_digest(self.root), "catalogDigest": enc.digest(self.cat),
            "patchSha256": enc.sha(patch),
            "actions": [{"id": "PLAN-0001", "operation": "PATCH_LOCAL", "findingIds": [],
                         "controlIds": ["APP-01"], "paths": ["src/app.py"], "summary": "Fixture change",
                         "risk": "Fixture only", "regressionTests": ["Local assertion"], "rollback": "Reverse the approved patch"}],
        }
        receipt = {"schemaVersion": 1, "decision": "APPROVED", "planDigest": enc.digest(plan),
                   "sourceDigest": plan["sourceDigest"], "approvedActions": ["PLAN-0001"],
                   "approvedBy": "Fixture user", "userMessageRef": "fixture:explicit-approval",
                   "issuedAt": (self.now - dt.timedelta(minutes=1)).isoformat(),
                   "expiresAt": (self.now + dt.timedelta(hours=1)).isoformat()}
        return plan, receipt, patch_path

    def check(self, plan, receipt, patch_path):
        return enc.approval_check(self.root, self.write("plan.json", plan), self.write("approval.json", receipt), patch_path, self.cat, self.now)

    def reviewed(self):
        ledger = enc.profile(self.root, self.cat)
        for row in ledger["controls"]:
            row.update(status="NOT_APPLICABLE", applicability="NOT_APPLICABLE", evidence=["fixture:scope-review"], reason="Synthetic fixture excludes this control")
        ledger["controls"][0].update(status="IMPLEMENTED", applicability="APPLICABLE", reason="Synthetic fixture inventory reviewed")
        for row in ledger["scenarios"]:
            row.update(status="NOT_APPLICABLE", evidence=["fixture:scope-review"], reason="Synthetic fixture excludes this scenario")
        ledger["complete"] = True
        return ledger

    def test_import_is_lossless_and_ids_and_lines_resolve(self):
        self.assertEqual(self.cat, importer.build())
        self.assertEqual([len(self.cat[k]) for k in ("controls", "scenarios", "domains")], [136, 507, 19])
        lines = importer.SOURCE.read_text(encoding="utf-8-sig").splitlines()
        for key in ("controls", "scenarios"):
            self.assertEqual(len(self.cat[key]), len({r["id"] for r in self.cat[key]}))
            for row in self.cat[key]:
                self.assertIn(row["title"], lines[row["sourceLine"] - 1])
        self.assertEqual(self.cat["source"]["sha256"], enc.sha(importer.SOURCE.read_bytes()))
        self.assertEqual(self.cat["source"]["declaredScenarioCount"], 506)

    def test_nested_discovery_never_executes_scripts_or_leaks_secret_contents(self):
        nested = self.root / "apps" / "api"
        nested.mkdir(parents=True)
        (nested / "package.json").write_text(json.dumps({"dependencies": {"express": "1.0", "openai": "1.0"}, "scripts": {"postinstall": "touch SHOULD_NOT_EXIST"}}))
        secret = "SENSITIVE_FIXTURE_VALUE"
        (self.root / ".env").write_text("TOKEN=" + secret)
        before = enc.source_digest(self.root)
        ledger = enc.profile(self.root, self.cat)
        self.assertIn("apps/api/package.json", ledger["discovery"]["signals"]["ai"])
        self.assertEqual({c["status"] for c in ledger["controls"]}, {"NOT_VERIFIED"})
        self.assertEqual({s["status"] for s in ledger["scenarios"]}, {"NOT_VERIFIED"})
        self.assertFalse(ledger["complete"])
        self.assertNotIn(secret, json.dumps(ledger))
        self.assertFalse((self.root / "SHOULD_NOT_EXIST").exists())
        self.assertEqual(before, enc.source_digest(self.root))
        self.assertEqual(enc.validate_coverage(self.root, ledger, self.cat)["result"], "INCOMPLETE")

    def test_profile_satisfies_schema_but_cannot_claim_complete(self):
        ledger = enc.profile(self.root, self.cat)
        schema = json.loads((enc.BASE / "schemas" / "encyclopedia-coverage.schema.json").read_text())
        self.assertEqual(validate_schema(ledger, schema), [])
        ledger["complete"] = True
        with self.assertRaises(GateError):
            enc.validate_coverage(self.root, ledger, self.cat)

    def test_complete_review_is_not_a_security_verdict(self):
        result = enc.validate_coverage(self.root, self.reviewed(), self.cat)
        self.assertEqual(result["result"], "COMPLETE")
        self.assertEqual(result["securityVerdict"], "NOT_ASSESSED_BY_COVERAGE_VALIDATOR")

    def test_missing_duplicate_unknown_or_unsubstantiated_coverage_is_rejected(self):
        ledger = self.reviewed()
        mutations = [
            lambda d: d["controls"].pop(),
            lambda d: d["scenarios"].append(copy.deepcopy(d["scenarios"][0])),
            lambda d: d["controls"][0].update(id="APP-99"),
            lambda d: d["controls"][0].update(evidence=[]),
            lambda d: d["controls"][0].update(reason=" "),
            lambda d: d["controls"][0].update(applicability="UNKNOWN"),
            lambda d: d["scenarios"][0].update(status="SUPPORTED"),
            lambda d: d.update(scope=["src"]),
            lambda d: d.update(catalogDigest="0" * 64),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                candidate = copy.deepcopy(ledger)
                mutate(candidate)
                with self.assertRaises(GateError):
                    enc.validate_coverage(self.root, candidate, self.cat)

    def test_inconclusive_and_stale_reviews_do_not_complete(self):
        ledger = self.reviewed()
        ledger["scenarios"][0]["status"] = "INCONCLUSIVE"
        with self.assertRaises(GateError):
            enc.validate_coverage(self.root, ledger, self.cat)
        ledger = self.reviewed()
        (self.root / "src" / "app.py").write_text("changed\n")
        with self.assertRaises(GateError):
            enc.validate_coverage(self.root, ledger, self.cat)

    def test_valid_preflight_neither_applies_patch_nor_authenticates_user(self):
        plan, receipt, patch = self.package()
        before = enc.source_digest(self.root)
        result = self.check(plan, receipt, patch)
        self.assertEqual(result["result"], "PREFLIGHT_VALID")
        self.assertFalse(result["applied"])
        self.assertFalse(result["identityVerifiedByHelper"])
        self.assertEqual(enc.source_digest(self.root), before)

    def test_receipt_cannot_be_replayed_after_approved_patch_is_applied(self):
        plan, receipt, patch = self.package()
        self.assertEqual(self.check(plan, receipt, patch)["result"], "PREFLIGHT_VALID")
        subprocess.run(["git", "-C", str(self.root), "apply", str(patch)], check=True)
        with self.assertRaises(GateError):
            self.check(plan, receipt, patch)

    def test_matching_digest_does_not_approve_malformed_patch(self):
        plan, receipt, patch = self.package()
        patch.write_bytes(b"diff --git a/src/app.py b/src/app.py\n--- a/src/app.py\n+++ b/src/app.py\n@@ nonsense @@\n")
        plan["patchSha256"] = enc.sha(patch.read_bytes())
        receipt["planDigest"] = enc.digest(plan)
        with self.assertRaises(GateError):
            self.check(plan, receipt, patch)

    def test_symlinked_receipt_or_target_parent_cannot_escape_scope(self):
        plan, receipt, patch = self.package()
        real_receipt = self.write("receipt-real.json", receipt)
        linked_receipt = self.trusted / "receipt-link.json"
        try:
            linked_receipt.symlink_to(real_receipt)
        except OSError:
            self.skipTest("host does not permit symlink creation")
        with self.assertRaises(GateError):
            enc.approval_check(self.root, self.write("plan.json", plan), linked_receipt, patch, self.cat)
        link_dir = self.root / "linked"
        link_dir.symlink_to(self.trusted, target_is_directory=True)
        with self.assertRaises(GateError):
            enc.safe_path(self.root, "linked/outside.py")

    def test_absent_or_repo_controlled_approval_is_rejected(self):
        plan, receipt, patch = self.package()
        plan_path = self.write("plan.json", plan)
        with self.assertRaises((GateError, OSError)):
            enc.approval_check(self.root, plan_path, self.trusted / "missing.json", patch, self.cat)
        local_receipt = self.root / ".security" / "approval.json"
        local_receipt.parent.mkdir()
        local_receipt.write_text(json.dumps(receipt))
        with self.assertRaises(GateError):
            enc.approval_check(self.root, plan_path, local_receipt, patch, self.cat)

    def test_changed_source_plan_patch_catalog_or_worktree_invalidates_approval(self):
        plan, receipt, patch = self.package()
        for field, value in [("projectRoot", str(self.workspace)), ("sourceDigest", "0" * 64), ("catalogDigest", "0" * 64), ("patchSha256", "0" * 64)]:
            with self.subTest(field=field):
                candidate = copy.deepcopy(plan)
                candidate[field] = value
                with self.assertRaises(GateError):
                    self.check(candidate, receipt, patch)
        altered = copy.deepcopy(plan)
        altered["actions"][0]["summary"] = "Different reviewed change"
        with self.assertRaises(GateError):
            self.check(altered, receipt, patch)
        patch.write_bytes(patch.read_bytes() + b"\n")
        with self.assertRaises(GateError):
            self.check(plan, receipt, patch)
        plan, receipt, patch = self.package()
        (self.root / "src" / "app.py").write_text("changed\n")
        with self.assertRaises(GateError):
            self.check(plan, receipt, patch)

    def test_expiry_wrong_batch_and_rejection_block(self):
        plan, receipt, patch = self.package()
        mutations = [
            {"decision": "REJECTED"}, {"approvedActions": ["PLAN-0002"]},
            {"expiresAt": (self.now - dt.timedelta(seconds=1)).isoformat()},
            {"issuedAt": (self.now + dt.timedelta(minutes=1)).isoformat()},
            {"userMessageRef": " "}, {"approvedActions": ["PLAN-0001", "PLAN-0001"]},
        ]
        for values in mutations:
            candidate = {**receipt, **values}
            with self.subTest(values=values), self.assertRaises(GateError):
                self.check(plan, candidate, patch)

    def test_undeclared_paths_and_traversal_block_even_with_matching_digests(self):
        plan, receipt, patch = self.package()
        for relative in ["other.py", "../outside.py", "C:/outside.py", ".git/config", "src/../../outside.py"]:
            candidate = copy.deepcopy(plan)
            candidate["actions"][0]["paths"] = [relative]
            updated = {**receipt, "planDigest": enc.digest(candidate)}
            with self.subTest(relative=relative), self.assertRaises(GateError):
                self.check(candidate, updated, patch)

    def test_supported_patch_paths_exclude_symlink_binary_rename_and_hidden_headers(self):
        for patch in [b"GIT binary patch\n", b"diff --git a/a b/a\nnew file mode 120000\n", b"diff --git a/a b/b\nrename from a\nrename to b\n", b"diff --git a/a b/a\n--- a/a\n+++ b/../../outside\n"]:
            with self.subTest(patch=patch), self.assertRaises(GateError):
                enc.patch_paths(patch)

    def test_cli_invalid_input_fails_without_echoing_sensitive_content(self):
        bad = self.trusted / "bad.json"
        bad.write_text('{"SECRET_FIXTURE":NaN}')
        result = subprocess.run([sys.executable, str(SCRIPTS / "encyclopedia.py"), "plan-digest", "--plan", str(bad)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SECRET_FIXTURE", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
