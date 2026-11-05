# Attack scenario catalog

The complete imported inventory is [`../encyclopedia.json`](../encyclopedia.json): 507 scenario
rows across 19 domains plus 136 controls, with exact source-line pointers. The original source
declares 506 scenarios; the catalog records the discrepancy and preserves all rows. These entries
are coverage seeds, not implemented detectors or confirmed findings. Follow
[`../../core/ENCYCLOPEDIA_WORKFLOW.md`](../../core/ENCYCLOPEDIA_WORKFLOW.md) for applicability,
evidence, coverage validation and user-approved implementation. The AS-* families below remain
useful cross-cutting reasoning prompts; do not double-count them as additional verified checks.

Use these prompts as coverage seeds, then tailor them to the discovered architecture. They are
questions for defensive review, not claims that the project is vulnerable. Link every applicable
scenario to code/configuration and counterevidence. Add a project-specific scenario when an asset or
trust boundary is missing here.

| ID | Surface | Scenario seed |
|---|---|---|
| AS-01 | Recon/exposure | Compare declared routes, deployment config, docs and artifacts; look for a stale or debug entry point that reaches a privileged operation. |
| AS-02 | Authentication/recovery | Trace login, reset, invitation, MFA and account-linking as one identity state machine; test one-use, expiry and revocation with synthetic users. |
| AS-03 | Federation/session | Check issuer, audience, callback, nonce/state/PKCE, session rotation and key rollover at every protocol boundary that exists. |
| AS-04 | Authorization/tenant | Compare same request for owner, other user, other tenant, low-privilege role and anonymous actor across list/detail/write/export paths. |
| AS-05 | APIs/realtime | Compare REST, GraphQL, batch/alias, WebSocket subscription and RPC authorization, schemas, field filtering and cost limits where present. |
| AS-06 | Injection | Trace untrusted values through normalization to query/template/interpreter sinks; confirm parameterization and contextual encoding at the final sink. |
| AS-07 | Process/deserialization | Trace filenames, options, serialized objects, plugins and parser inputs; inspect argument separation, allowed formats and isolation. |
| AS-08 | Upload/archive | Follow bytes through type checks, extraction, generated paths, storage, scanning and download authorization; inspect size/expansion/timeout bounds. |
| AS-09 | SSRF/egress | Follow URL inputs through redirects and DNS resolution to the final connection; verify private/metadata egress is denied by policy or a local mock. |
| AS-10 | Browser | Trace attacker-controlled content to DOM, URL and message sinks; verify origin checks, server-side state authorization, CSRF defenses and output context. |
| AS-11 | Proxy/cache | Compare edge and origin parsing, forwarded headers, cache keys and authenticated response behavior; use static config or a local test pair. |
| AS-12 | Business logic | Enumerate operation preconditions and state transitions; check skip, replay, duplicate, reorder and bounded concurrency against invariants. |
| AS-13 | Payment/webhook/queue | Verify original-body signature, timestamp, replay/idempotency, tenant binding, ordering and reconciliation in a mock provider flow. |
| AS-14 | Secrets/crypto | Search working tree, Git history and outputs with redaction; map credential scope and rotation ownership without testing a found secret. |
| AS-15 | Supply chain/build | Trace contribution and package inputs through build scripts, actions, caches, credentials, artifact digest and deployment provenance. |
| AS-16 | Cloud/IAM | Build principal-to-resource/action paths from IaC and external evidence; assess trust conditions, role chaining and resource policies. |
| AS-17 | Container/orchestration | Check privilege, mounts, namespaces, service accounts, RBAC, admission and east-west network edges for each workload. |
| AS-18 | AI/agent/MCP/RAG | Treat retrieved text and model output as hostile; verify tool authorization, destination allowlist, tenant filters, confirmation and budget outside the model. |
| AS-19 | Availability/cost | Trace unbounded input, fan-out, recursion, concurrency and retries; inspect limits and cancellation. Do not run load or exhaustion tests. |
| AS-20 | Persistence/lateral movement | Inspect service identities, scheduled jobs, CI, integrations and adjacent trust boundaries for durable or transitive access; no implants or credential use. |
| AS-21 | Detection/recovery | Follow a simulated security event into logs, alerts, owner, containment procedure and isolated restore evidence. |
| AS-22 | Human/process | Review approval, helpdesk, emergency and offboarding controls as process evidence; do not phish, impersonate or target people. |
| AS-23 | Mobile/desktop/native | When present, inspect IPC/deep links, local permissions, update verification, local secrets and parser memory safety. |

## Scenario record

Use `scenario.schema.json` and keep a small record with: attacker capability; objective; asset;
entry point; boundary; preconditions; ordered steps; controls; counterevidence; sensitive sink and
impact; evidence; validation profile; confidence; state; and explicit limits. A possible sequence
without a supported link remains `HYPOTHESIS` or `INCONCLUSIVE`.

Validation profiles and stop conditions are in `../../core/ATTACK_REASONING.md` and
`../../core/SAFETY.md`. Do not include real credentials, customer data or destructive proof material.
