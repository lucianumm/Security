# Persistent state (schema v2)

Copy these files into `.security/` only when starting a new project state. The JSON files are
deliberately empty and marked as not audited. They contain no sample finding, scan result, score,
coverage claim or accepted risk.

| File | Purpose | Schema |
|---|---|---|
| `baseline.json` | Trusted scope, required controls and blocking policy | `../../schemas/state/baseline.schema.json` |
| `findings.json` | Current findings plus source and policy digests, audit completeness, coverage and scanner runs | `../../schemas/state/findings.schema.json` |
| `risk-register.json` | Time-bounded exceptions and external actions | `../../schemas/state/risk-register.schema.json` |
| `controls.json` | Evidence-backed control states | `../../schemas/state/controls.schema.json` |
| `architecture.json` | Discovered components, boundaries, data flows and integrations | `../../schemas/state/architecture.schema.json` |
| `last-audit.json` | Latest run summary | `../../schemas/state/last-audit.schema.json` |

Configure the project identity and audit scope before use. `findings.json` must contain the digest
for the exact source tree, a completed audit, nonzero applicable-control count, current scanner
results and sufficient verified coverage. The placeholder `sourceDigest` is intentionally invalid
for any real checkout. The starter baseline requires all listed tools; remove or replace a tool only
after documenting why it is inapplicable and updating the trusted baseline through normal review.
After configuring the baseline, compute `policyDigest` with
`python3 security-auditor/scripts/security_auditor.py policy-digest --root .` and record it alongside
the source digest when the audit is generated.

In CI, load the baseline, risk register, schemas and gate implementation from a protected branch or
another independently trusted location. Do not trust policy or gate files supplied by the same
untrusted pull request that is being evaluated. A digest detects stale source/policy evidence; it
does not prove who authored the findings or approval metadata. Protect workflow files and findings
with repository review controls (for example, required reviewers and branch protection) and keep
scanner jobs independently required.

Finding IDs are persistent: reuse the existing ID for the same root cause, and never reuse an ID for
a different issue. A finding marked `FIXED` requires post-fix verification evidence. `MITIGATED`
requires compensating controls and fails the gate unless the trusted policy explicitly allows it.
`ACCEPTED_RISK` requires a matching, unexpired register entry; a text approval reference remains an
audit pointer, not proof of approver identity.
