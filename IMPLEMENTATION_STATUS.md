# Security improvement plan — implementation status

Status describes what this repository now contains. A template or checklist is not an active
control in a consumer's project. The status is deliberately explicit where the host platform or a
controlled test target must supply enforcement.

| Milestone | Status | Evidence and boundary |
|---|---|---|
| M01 — Strict schemas and state contracts | Done | Six state schemas, an attack-scenario schema and regression tests cover malformed, incomplete and placeholder state. |
| M02 — Deterministic fail-closed gate | Done | Python standard-library validator checks source and policy digests, scope, coverage, scanner records, control regression and finding lifecycle. |
| M03 — CI aggregation and protected policy | Templates done; external setup required | GitHub Actions and GitLab CI templates pin actions/images, load gate, rules and baseline policy from protected sources, override source-controlled suppressions and fail when a required job is missing or fails. They are not installed as consumer pipelines automatically. Protect workflows, policy and required checks in the host settings. |
| M04 — Secret-safe output | Guidance and templates done | Secret searches return paths only; raw reports stay private. CI uses trusted scanner rules, rejects untrusted suppressions, and suppresses raw output. Scanner behavior must be checked for each pinned version and integration. |
| M05 — Tool and action pinning | Template examples done | CI examples use immutable action SHAs and image digests. Refresh pins through reviewed updates; the examples are not a promise that every upstream scanner is included. |
| M06 — Stack discovery and routing | Partial | Routing guidance covers common runtimes and infrastructure. Detection remains a read-only heuristic; it cannot reliably infer every monorepo, generated framework or externally managed service. |
| M07 — Adversarial reasoning | Done | Attack-chain method, counterevidence, scenario lifecycle, safety bounds and 23 surface families are documented. |
| M08 — Coverage and identity | Done for state model | Scope, applicable/verified control counts, persistent IDs, duplicate detection and baseline regressions are represented and gated. Manual report quality still depends on evidence supplied by an audit. |
| M09 — State integrity | Done with stated trust boundary | The gate binds findings to the current source and trusted policy digests. A digest does not prove who authored the audit or scanner claims; protect the policy and gate in the CI host. |
| M10 — Scanner adapters | Partial | CI examples integrate selected scanners. There is no universal adapter runtime; the state gate never executes arbitrary repository tools. |
| M11 — Tests and evaluations | Partial | Deterministic unit tests cover the gate and state/scenario schemas. A broad, labeled vulnerable/benign repository corpus and model-quality benchmark remain future work. |
| M12 — Standards mapping | Done for listed editions | OWASP editions are recorded in standards.lock.json and referenced by version. Confirm again when mappings are updated. |
| M13 — Enforced scanner sandbox | Not implemented | Cross-platform host isolation, network policy and resource enforcement cannot be guaranteed by a portable Markdown skill. Dynamic execution remains opt-in and bounded by SAFETY.md. |
| M14 — DAST and runtime testing | Procedure only | Tool families and authorized profiles are documented; no target was supplied and no live dynamic scan is run by the gate. Use local mocks or explicitly authorized staging. |
| M15 — Operations and response | Guidance done | The skill requires explicit external-verification limits and adds a responsible disclosure policy. Provider-side alerting, branch protection, secret rotation and restore tests remain external controls. |
| M16 — Versioned release | Done | VERSION and CHANGELOG identify release 1.2.0. |
| M17 — Safe starter templates | Done | State templates contain no sample findings or successful scan claims and remain incomplete by default. |
| M18 — Disclosure and distribution metadata | Partial | SECURITY.md and changelog are present. No LICENSE file was added because the repository owner has not selected a license; publishing reuse terms remains an owner decision. |
| M19 — Encyclopedia inventory | Done for supplied v1.0 source | Original bytes, SHA-256, 136 controls, 507 actual scenario rows and 19 domains; importer detects drift. The source declares 506; none of its 507 rows were dropped. Entries are review seeds, not executable detectors. |
| M20 — Project coverage | Implemented with evidence trust limits | Bounded Git-based discovery seeds all items as unverified. The coverage validator checks exact IDs, source/catalog identity, evidence metadata, exclusions and finding links. New baseline templates require the ledger in CI and cross-check findings controls/counts. Human/model review must still establish evidence quality. |
| M21 — Approved hardening | Workflow and preflight implemented; host consent enforcement required | Every change requires an explicitly approved concrete batch. Schemas and a read-only preflight bind worktree/source/catalog/plan/patch/action IDs and expiry; unsafe paths and repository-local receipts are rejected. The helper never applies a patch or authenticates approval. Trusted receipt storage, actual user consent and prevention of bypass remain host/operator duties. |
| M22 — Extended domains | Guidance implemented | Added review routing for mobile/desktop, endpoints, communications, firmware/OT, memory, wireless and physical/human process surfaces. No live hardware, provider or organizational verification is claimed. |

## Validation boundary

The repository test workflow exercises the validator, schemas and shell syntax. It does not certify a
consumer deployment, prove that scanner outputs are complete, execute DAST, or validate GitHub/GitLab
branch-protection settings. Those claims require evidence from the consuming project and its hosting
platform.
