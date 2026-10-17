# Helper scripts

## Stack detection

Run `sh security-auditor/scripts/detect-stack.sh [project-root]`. It reads repository metadata and
manifest names/content, reports detected signals and never changes files or contacts services. The
result is heuristic: inspect the relevant source and configuration before selecting modules.

## State validator and CI gate

Requires Python 3.9+ and the standard library. From the consumer repository root:

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
