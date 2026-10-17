# State vocabulary and gate invariants

Control, scenario, finding and gate states describe different things. Do not merge them into one
status or infer one from another.

## Controls

`IMPLEMENTED` · `PARTIALLY_IMPLEMENTED` · `NOT_IMPLEMENTED` · `MISCONFIGURED` ·
`NOT_APPLICABLE` · `NOT_VERIFIED`.

Every status has an evidence pointer or a concise reason. `NOT_APPLICABLE` requires a reason tied to
the discovered architecture. `NOT_VERIFIED` is an explicit gap. A control is not `IMPLEMENTED`
because a scanner returned zero findings or a library is present.

## Attack scenarios

`HYPOTHESIS` → `SUPPORTED` → `REPRODUCED`, or `REFUTED`, `INCONCLUSIVE`, `NOT_APPLICABLE`.
`SUPPORTED` means static/configuration evidence makes the path plausible; `REPRODUCED` requires an
authorized bounded test. A scenario can be tracked without a vulnerability finding.

## Findings

Canonical finding IDs are `SEC-0001` through `SEC-99999999`, persistent for the underlying root
cause. Status meanings:

| Status | Meaning | Gate treatment |
|---|---|---|
| `OPEN` | Validated issue remains | Blocks |
| `PARTIALLY_FIXED` | Some paths or impact remain | Blocks |
| `REGRESSION` | Previously fixed issue has returned | Blocks |
| `NOT_VERIFIED` | Current evidence cannot establish the state | Blocks |
| `EXTERNAL_ACTION_REQUIRED` | A person/provider must complete an action | Blocks |
| `FIXED` | Remediation is verified after the change | Passes only with dated verification evidence |
| `MITIGATED` | Root cause remains under compensating controls | Blocks unless trusted policy explicitly permits it and evidence names the controls |
| `ACCEPTED_RISK` | Named owner has approved a time-limited exception | Passes only with a matching current register entry and protected policy process |

Do not delete resolved findings or recycle IDs. Record a status transition in history. When a fixed
issue returns, reuse the ID and mark `REGRESSION`.

## Deterministic gate

The Python standard-library CLI validates the v2 finding, baseline and risk schemas. It checks
project identity, source digest, scope, audit completion, control coverage, evidence age, required
scanner outcomes, duplicate identities, control regressions, finding state, fix verification,
mitigation evidence, exceptions, high/critical severity and configured categories. It exits `0` for
`PASS`, `1` for policy `FAIL`, and `2` for invalid or unavailable evidence. `ERROR` is not `PASS`.

The source digest hashes Git-tracked and non-ignored untracked project files, including file paths,
modes and bytes; it excludes the generated root `.security/` and `security/` directories to avoid a
self-referential report hash. This conservative whole-tree digest can invalidate a scoped audit when
an out-of-scope file changes. It is a freshness check, not proof of scan identity, authorship or
policy trust.

In CI, use `--trusted-baseline` to load policy from a separately protected source, and make the
scanner and test jobs independently required. A finding file, baseline or exception record editable
by the same untrusted contribution cannot authenticate itself. Use branch protection/review policy
outside this CLI. A text approval reference is traceability, not identity verification.

The CLI does not run scanners or verify that a recorded scanner binary actually produced the
recorded result. CI must rely on the scanner jobs' exit states and artifacts as separate evidence.
The included templates are starter integrations and must be adapted to the consuming project's
stack and protected branches before they become required checks.
