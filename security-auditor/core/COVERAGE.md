# Coverage and evidence accounting

Report coverage with explicit denominators. Do not equate modules loaded, scanners installed, files
enumerated or lines searched with verified security coverage.

Keep separate counts for:

| Measure | Denominator and inclusion rule |
|---|---|
| Components | Deployable applications, services, workers, data stores and control planes discovered; list out-of-repository components separately. |
| Entry points | Routes, resolvers, messages, jobs, webhooks, file paths and privileged operations enumerated for the declared scope. |
| Authorization operations | Applicable actor × resource × action × state combinations; show untested combinations and why. |
| Scenarios | Applicable attack scenarios examined, with status `SUPPORTED`, `REPRODUCED`, `REFUTED` or `INCONCLUSIVE`. |
| Controls | Applicable controls verified with current evidence; `NOT_VERIFIED` is not in the numerator. |
| Scanners | Required tools that ran on the declared source and returned an understood, acceptable outcome. |
| Evidence | Evidence items tied to a path, configuration, test or runtime, with source identity and time. |

For a simple control ratio, state `verified applicable controls / total applicable controls` and list
which controls were excluded as not applicable. Do not count `NOT_APPLICABLE` as verified. Do not
hide a critical unverified control behind a high average. Preserve `INSUFFICIENT_EVIDENCE` when a
required denominator, component or source of evidence is unknown.

For each exclusion, record the boundary and reason. Examples: no payment code or integration found
in the inspected tree; mobile client absent; provider console unavailable; a generated artifact was
outside scope. “No finding found” is not an exclusion reason. A 24-module load count is not 24
completed reviews.

Use static evidence, configuration, tests and runtime observations as distinct evidence classes
(`ATTACK_REASONING.md`). State exact source revision/digest, scope, timestamp, tool and ruleset
versions, skipped components and unresolved questions. See `STATE_MACHINE.md` for digest and trust
limits.
