# Helper scripts

## Stack detection

Run `sh security-auditor/scripts/detect-stack.sh [project-root]`. It reads repository metadata and
manifest names/content, reports detected signals and never changes files or contacts services. The
result is heuristic: inspect the relevant source and configuration before selecting modules.

## State validator and CI gate

Requires Python 3.10+ and the standard library. From the consumer repository root:

```sh
python3 security-auditor/scripts/security_auditor.py validate --root .
python3 security-auditor/scripts/security_auditor.py source-digest --root .
python3 security-auditor/scripts/security_auditor.py policy-digest --root .
python3 security-auditor/scripts/security_auditor.py gate --root .
```

The `validate` command checks all six state documents against the bundled schemas. `source-digest`
binds the audit to tracked and non-ignored untracked source files while excluding only generated
root `security/` reports and `.security/` state. `policy-digest` canonically hashes the baseline.
`gate` returns 0 for PASS, 1 for a policy FAIL, and 2 for invalid or incomplete state. POSIX and
PowerShell wrappers are also provided.

For untrusted pull requests, load the script, schemas, baseline and risk register from a protected
branch or other trusted source. The digest proves content correspondence, not audit authorship or
scanner authenticity. This script does not run scanners or provide an operating-system sandbox.

## Encyclopedia discovery, coverage and approval preflight

Run from an installed/trusted copy of the skill, replacing paths with the actual project and local
artifacts. All commands below only read inputs and emit JSON:

```text
python <skill>/scripts/encyclopedia.py profile --root <project>
python <skill>/scripts/encyclopedia.py validate-coverage --root <project> --coverage <ledger.json>
python <skill>/scripts/encyclopedia.py plan-digest --plan <plan.json>
python <skill>/scripts/encyclopedia.py approval-check --root <project> --plan <plan.json> --approval <approval.json> --patch <changes.patch>
```

The profile seeds 136 controls and 507 scenarios as unverified, using bounded local discovery
signals. It does not run SAST/SCA, find every vulnerability or implement controls. Coverage validation
checks full-catalog accounting and evidence metadata; it cannot prove evidence is true. The optional
protected baseline policy `requireEncyclopediaCoverage` connects it to the existing CI gate.

Approval preflight checks root/source/catalog/plan/patch identity, paths, exact batch and expiry. It
never records consent, authenticates a user or applies changes. The operator must have actual user
approval and protect the external plan/receipt/patch storage. See
[`../core/ENCYCLOPEDIA_WORKFLOW.md`](../core/ENCYCLOPEDIA_WORKFLOW.md) for the complete contract and
supported patch restrictions. No `--approve`, `--auto-fix` or arbitrary command execution exists.

## Maintainer-only catalog import

`python <skill>/scripts/build_encyclopedia.py` checks reproducibility against the bundled original.
Only maintainers updating the reference run it with `--write`. The source declares 506 scenarios;
the importer preserves all 507 actual rows and records the discrepancy. Do not regenerate catalogs
during consumer audits or silently alter IDs. This is the only new helper that writes a bundled file,
and only with the explicit maintainer flag.
