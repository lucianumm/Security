# WORKFLOW — phases, exit criteria and variants

The canonical order is in `../SKILL.md` §3. This file defines what each phase must produce and when
it may be considered complete. Track progress internally; on large repositories, work phase by
phase and keep a running phase log so an interrupted audit can resume.

---

## Phase 0 — Environment safety

See `SAFETY.md` §2. Exit criterion: `ENVIRONMENT_SAFETY_CHECK` recorded, prior state
(`.security/`, `security/`) loaded if present.

On a repeat audit, load in this order: `baseline.json` → `findings.json` → `controls.json` →
`architecture.json` → `risk-register.json` → `last-audit.json`. Every prior finding starts this run
as `NOT_VERIFIED` and must be revalidated before it may be reported as `FIXED` or `OPEN`.

## Phase 1 — Stack discovery

See `../SKILL.md` §4. Exit criterion: languages, frameworks, package managers, datastores, infra,
CI, cloud and integrations identified from files (not from the README), and the module set selected
and recorded.

Deliberately record what you could **not** determine (e.g. "hosting provider unknown — no IaC or
deploy config in repo") — these become `NOT_VERIFIED` items, not assumptions.

## Phase 2 — System inventory

Enumerate: applications, services, APIs, databases, caches, object storage, queues, cron jobs,
workers, webhooks (in and out), third-party integrations, containers, servers, domains and known
subdomains, proxies, CDNs, WAFs, CI/CD pipelines, cloud accounts/projects, secrets consumed by the
system (names only), and categories of data handled.

Output: `SYSTEM_INVENTORY` section of `security/ATTACK_SURFACE.md` and `architecture.json`.

## Phase 3 — Architecture and trust boundaries

Draw the architecture that actually exists — no invented components. For each component record:
function, trust level, inputs, outputs, data handled, authentication, exposure (public/internal).

Then enumerate trust boundaries explicitly, e.g.:

```text
Public Internet → CDN/WAF → Reverse proxy → Frontend
Browser → Backend API
Backend → Database / Cache / Object storage
Backend → Third-party API
Webhook provider → Application
Tenant A → Shared application → Tenant B data
CI runner → Production credentials
LLM output → Tool execution
```

Every crossing is an attack surface. Each boundary must have: an authentication answer, an
authorization answer, a validation answer, and a failure-mode answer.

## Phase 4 — Data classification

Discover the data the system handles and classify: `PUBLIC` `INTERNAL` `CONFIDENTIAL` `SENSITIVE`
`CRITICAL`. Look for national IDs (CPF/CNPJ/SSN), emails, phones, addresses, credentials, tokens,
financial data, health data, legal documents, private files, biometrics, precise location.

For each sensitive class map: `input → processing → storage → transmission → deletion`.
Data class raises severity: the same IDOR is HIGH on a display name and CRITICAL on identity
documents.

## Phase 5 — Attack surface

Enumerate every entry point: pages, forms, all HTTP routes, login/register/reset/admin, API, GraphQL,
WebSocket, uploads, downloads, remote-URL inputs, webhooks, importers/exporters, callbacks,
redirects, payments, search, AI endpoints, PDF/report generation, background jobs, internal
endpoints, health checks, debug endpoints, Swagger/OpenAPI, playgrounds, metrics and management
endpoints.

For each: method, auth requirement, authorization rule, input shape, rate limiting, data returned.
Output: `security/ATTACK_SURFACE.md` (template provided).

## Phase 6 — Threat model

Per relevant asset: asset, threat, attacker profile, vector, precondition, impact, likelihood,
existing control, missing control, mitigation. Cover STRIDE plus account takeover, session
hijacking, credential stuffing, privilege escalation, data exfiltration, supply-chain compromise,
insider misuse, tenant escape, API abuse and LLM prompt injection where applicable.
Output: `security/THREAT_MODEL.md`.

## Phase 7 — Control audit

Work through the selected modules. For each control: determine status, capture evidence
(`path:line`, config excerpt, observed response), and open findings for gaps. Do not stop at the
first problem in an area — enumerate the whole area.

Order that maximizes early signal: secrets → authentication → session → authorization →
input handling → API → data layer → files/storage → frontend → infra/containers → CI/CD →
operations → business logic.

## Phase 8 — Scanners

Run what is available; never invent output. Record the exact command and version.

Read `TOOL_EXECUTION.md` before selecting commands. Choose the scanner and command for the detected
stack; the alternatives below are separate examples, never a shell pipeline of competing tools.
Load scanner rules and exceptions from this skill or another protected source, never the project
under audit. Disable telemetry/update checks where supported, pin versions, keep raw reports in a
local owner-only directory outside the project, and record only sanitized summaries. Network-backed
dependency scans disclose package identities and versions to their advisory service; confirm that
this is allowed before running.

```bash
# Examples; select only the command that matches the repository and approved disclosure policy.
umask 077
PRIVATE_SCAN_DIR=$(mktemp -d)
chmod 700 "$PRIVATE_SCAN_DIR"
npm audit --audit-level=high
pip-audit --strict
composer audit
cargo audit
govulncheck ./...
bundler-audit check

# Secrets and source history; capture reports privately, then inspect only sanitized fields.
# PRIVATE_SCAN_DIR must be a new owner-only directory outside the project, created with umask 077.
gitleaks detect --source . --log-opts=--all --no-banner --redact \
  --report-format json --report-path "$PRIVATE_SCAN_DIR/gitleaks.json" \
  > "$PRIVATE_SCAN_DIR/gitleaks.log" 2>&1
trufflehog filesystem . --no-verification --no-update --json \
  > "$PRIVATE_SCAN_DIR/trufflehog.jsonl" 2>&1

# Use the ruleset bundled with this skill or a protected policy path; never a project-controlled
# ruleset or .semgrepignore. If a repository-controlled .semgrepignore exists, stop and review it
# against the protected policy before scanning. Keep source output private while triaging.
semgrep scan --config /path/to/security-auditor/catalog/tools/semgrep-rules.yaml \
  --no-git-ignore --metrics off --quiet . > "$PRIVATE_SCAN_DIR/semgrep.log" 2>&1

# Split source dependency and IaC scans; use an explicit empty or protected ignore policy.
trivy --config /path/to/protected-trivy.yaml fs --ignorefile /path/to/protected-trivyignore \
  --scanners vuln,misconfig --format json --output "$PRIVATE_SCAN_DIR/trivy.json" . > /dev/null 2>&1
trivy --config /path/to/protected-trivy.yaml image <image>:<tag> --scanners vuln \
  --format json --output "$PRIVATE_SCAN_DIR/trivy-image.json" > /dev/null 2>&1
checkov -d . --quiet > /dev/null 2>&1
tfsec . --no-color > /dev/null 2>&1
```

Interpret results; do not paste them. For every dependency finding assess: is it reachable, is it a
direct or transitive dependency, is the vulnerable code path used, is a fixed version available,
what breaks if we upgrade. Scanner severity is an input, not a verdict.

Missing tool → the corresponding control is `NOT_VERIFIED`, with the reason and the command a human
can run.

## Phase 9 — Consolidation and false positives

Apply `EVIDENCE_RULES.md` §False positive control to every candidate. Merge duplicates. Correlate
with prior findings to reuse IDs. Mark reappearing fixed issues as `REGRESSION`.

## Phase 10 — Prioritization

Apply `SEVERITY.md`. Produce the ordered remediation list (`security/REMEDIATION_PLAN.md`).

## Phase 11 — Remediation (fix modes only)

Apply `REMEDIATION_POLICY.md`. One logical fix at a time; keep the working tree coherent.

## Phase 12 — Regression tests

Every CRITICAL and HIGH fix gets a test when technically possible. Patterns in
`REMEDIATION_POLICY.md` §Regression tests. Place them where the project's tests already live and
follow its existing conventions and runner.

## Phase 13 — Build validation

Run the project's own commands, in this order, and report real results:
lint → typecheck → unit tests → integration tests → build. If something was already failing before
your changes, say so explicitly and do not claim to have broken or fixed it.

## Phase 14 — Rescan and verification

Re-run the scanners that were relevant to the fixes, re-execute the manual checks, and only then
update finding statuses. Code change alone never justifies `FIXED` (`EVIDENCE_RULES.md` §Fix
verification).

## Phase 15 — Score and readiness

Apply `SCORING.md`. Produce `security/PRODUCTION_READINESS.md`.

## Phase 16 — Baseline and state

Write/update `security/SECURITY_BASELINE.md` and the `.security/*.json` files. The baseline records
the expected state of each control so a future run can detect drift.

## Phase 17 — CI security gate

Propose (or implement, in `HARDEN`) the pipeline in `../modules/ci-cd.md` §Security gate using
`../templates/ci/`. Respect the project's existing CI platform.

## Phase 18 — Final report

Executive block, findings, matrix, plan, scope and limitations. Never omit limitations.

---

## Variant: change-aware / incremental audit (`--incremental`, PR review)

Use when a baseline exists and the user asks for a PR or delta review.

1. `git diff --stat <base>...HEAD` and `git diff <base>...HEAD` to get the real change set.
2. Identify: new/changed endpoints, new dependencies, migrations, new permissions or roles, new
   file handling, new external calls, new secrets usage, changed auth/authorization code,
   changed CI configuration, changed Docker/IaC.
3. Audit the changed surface fully, plus every control the change could affect.
4. Always re-run: secret scan on the diff, dependency audit if any manifest changed, and the
   baseline regression comparison.
5. Apply `NEW FEATURE SECURITY REVIEW` to each new feature: data, trust boundary, auth,
   authorization, input, output, rate limiting, logging, abuse potential, secrets, dependencies,
   privacy.
6. State clearly in the report that this was incremental, and what was **not** re-examined.

A full audit remains available and is recommended: before a significant release, periodically,
after an incident, and after major architectural change.

## Variant: monorepos

Detect workspaces (`apps/*`, `packages/*`, `services/*`, `pnpm-workspace.yaml`, `turbo.json`,
`nx.json`, Lerna, Go workspaces, Cargo workspaces). Audit each deployable unit as its own system
with its own attack surface and trust level, then audit the seams: shared session/token formats,
internal APIs assumed to be trusted, shared database access, shared secrets, cross-package
type-only validation, and a public app importing code intended for an internal one.

## Variant: large repositories

Split into the phase list above and process the codebase by area rather than file-by-file. Use
targeted searches for high-signal patterns first (auth decorators, route definitions, raw SQL,
`exec`, `innerHTML`, upload handlers, `process.env` usage), then read the surrounding flow. Record
partial coverage honestly: "audited `apps/api` fully; `services/reporting` sampled only".

## Variant: `CI_GATE`

Minimal, fast, non-interactive. Run: secret scan, dependency audit, SAST (if configured), IaC and
container scan (if applicable), security regression tests, baseline comparison. Emit both a human
summary and:

```json
{ "result": "FAIL", "critical": 1, "high": 2, "regressions": 1, "secrets": 0 }
```

Blocking policy: `../modules/ci-cd.md` §Blocking policy.

## Variant: `INCIDENT_REVIEW`

Preserve evidence first; change nothing. Inventory recent deploys and commits, look for unexpected
modifications, exposed or leaked secrets, new accounts and permissions, suspicious dependencies,
new outbound endpoints, persistence mechanisms (cron, systemd units, startup scripts, webhooks,
CI changes), and log gaps. Never delete logs. Never run destructive containment on your own.
Output goes to `security/INCIDENT_RESPONSE.md` as an appended, timestamped record.
