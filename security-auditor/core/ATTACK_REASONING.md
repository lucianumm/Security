# Adversarial reasoning and attack-path analysis

Use this method in every full or targeted audit. “Hacker mindset” means testing assumptions about
identity, boundaries, state and capability; it does not authorize actions against a live or
third-party target. Read `SAFETY.md` before running commands and `EVIDENCE_RULES.md` before turning
a hypothesis into a finding.

## Model the attacker before the bug

For each asset, name the adversary and starting capability: anonymous internet user, authenticated
low-privilege user, another tenant, compromised account or token, malicious contributor, compromised
dependency, insider, or an external service sending callbacks. Do not silently upgrade that actor's
privileges. Record what the actor controls, what they can observe, and which preconditions are
unproven.

Then trace a concrete chain:

```text
attacker goal → controlled input → parsing/normalization → trust boundary →
authentication → authorization → state/data transition → sensitive sink → impact
```

For every arrow, point to code, configuration, a test, or an observation. Include alternate entry
points and asynchronous paths: jobs, queues, exports, webhooks, cached responses, batch APIs,
retries, callbacks, admin tools and recovery flows. A chain is supported only when each prerequisite
is evidenced and the output capability of one step satisfies the next step's precondition.

## Challenge the defensive hypothesis

Before recording a candidate, actively search for counterevidence: middleware or policy checks,
object ownership and tenant filters, row-level security, schema constraints, transaction isolation,
egress policy, output encoding, parser limits, provider-side enforcement, feature flags and tests.
Check that the control executes on the exact route and object, in the deployed configuration, for
all relevant actors and state transitions. A test that covers only the happy path is not proof of a
boundary.

Separate these evidence classes in the report:

| Class | What it supports |
|---|---|
| Static | A possible path in source or configuration; it may not be reachable at runtime. |
| Configuration | An intended setting; deployment may override it. |
| Test | Behavior for the exact fixture, actor and request exercised. |
| Runtime observation | Behavior on the identified, authorized environment at a stated time. |
| External evidence | Provider or operator configuration that cannot be inferred from this repository. |

Record counterevidence alongside supporting evidence. If a required link cannot be established,
keep the path `INCONCLUSIVE`; do not inflate it into a confirmed vulnerability or call it safe.

## Structured attack scenario

For a scenario, capture: stable `scenarioId`; asset/component; attacker and starting capability;
goal; controlled inputs; entry point; trust boundary; preconditions; ordered steps; transformation
and authorization checks; sensitive sink; expected impact; controls found; bypass hypothesis;
counterevidence; evidence references; validation method and scope; confidence; and scenario status.
Keep scenario status separate from finding status:

`HYPOTHESIS` · `SUPPORTED` · `REPRODUCED` · `REFUTED` · `INCONCLUSIVE` · `NOT_APPLICABLE`.

`SUPPORTED` means repository evidence supports the path, not that it has been dynamically exploited.
`REPRODUCED` requires a bounded, authorized test and recorded preconditions. A finding uses the
separate lifecycle in `STATE_MACHINE.md`.

Prioritize operations that grant authority or move sensitive data: create, read, update, delete,
export, approve, pay, refund, invite, change identity, issue credentials, deploy, call a tool, or
change tenant membership. For each operation, map actor × resource × action × state, including
direct API calls and background execution.

## Coverage families

Select families based on the observed stack, assets and exposed operations. Mark applicability and
the reason for every exclusion; a loaded module is not a completed check.

| Family | Adversarial question |
|---|---|
| Reconnaissance and exposed assets | Are forgotten routes, artifacts, environments, debug endpoints or origin services reachable? |
| Login, recovery and identity federation | Can reset, invitation, MFA, OAuth/OIDC/SAML or account-linking swap identity or bypass proof? |
| Sessions and tokens | Can fixation, theft, replay, weak claims, stale keys or incomplete revocation preserve authority? |
| Authorization and tenants | Can a caller cross user, role, object, tenant or administrative boundaries through any route or job? |
| REST, GraphQL, WebSocket and RPC | Do resolvers, batch/alias paths, subscriptions, schemas, pagination and message handlers enforce the same policy? |
| Injection and interpreters | Can controlled data become SQL/NoSQL/LDAP/template/shell/expression syntax or a second-order command? |
| Deserialization and loaders | Can untrusted objects, plugins, archives, parsers or dynamic imports trigger code or unsafe state? |
| Uploads, downloads and archives | Can normalization, symlinks, MIME confusion, decompression or storage names escape limits or authorization? |
| SSRF and egress | Can URL fetchers, PDF, image, webhook or import flows reach internal destinations after redirects and DNS changes? |
| Browser and frontend | Can origin confusion, XSS, CSRF, clickjacking, `postMessage` or client storage expose authority/data? |
| Proxy, CDN and cache | Do parsers, forwarded headers, cache keys and identity vary between edge and origin? |
| Business logic and concurrency | Can steps be skipped/reordered/replayed or raced while preserving a broken invariant? |
| Payments, webhooks and queues | Can signatures, idempotency, ordering, retries or reconciliation be bypassed? |
| Secrets and cryptography | Can credentials leak through history, bundles, logs, artifacts or broad access; are key lifecycle and primitives sound? |
| Dependencies, build and provenance | Can a package, action, cache, build script or artifact introduce unreviewed code or access to credentials? |
| Cloud IAM and serverless | Can identity/policy combinations, event triggers or resource policies grant unexpected access? |
| Containers and orchestration | Can privileges, mounts, service accounts, network paths or admission gaps cross workload boundaries? |
| AI, agents, MCP and RAG | Can untrusted content influence tool selection, authorization, tenant retrieval, destinations or spend? |
| Availability and cost | Can a bounded request amplify CPU, memory, concurrency, queue depth or external spend? |
| Persistence and lateral movement | Could a compromised service identity reach adjacent assets or create durable unauthorized access? |
| Detection, recovery and response | Would security-relevant behavior be logged, alerted, contained and restorable with tested evidence? |
| Human and operational process | Can approval, helpdesk, onboarding, recovery or emergency bypass defeat technical controls? Review the process; do not target people. |
| Mobile, desktop and native code | When present, can IPC, deep links, local storage, update channels or native parsers cross privilege boundaries? |

## Validation boundary

Default to source review and existing tests. Dynamic validation requires explicit user authorization,
an identified local or controlled staging target, a non-destructive test case, synthetic data, a
low request count, a timeout and a cleanup plan. Do not scan broad ranges, test provider-owned
systems, use discovered credentials, trigger real payments, send real emails, mutate production
records, perform load/fuzz/brute-force campaigns, or exfiltrate data. Use local mocks for metadata
services, payment providers, webhooks and external callbacks.

For each proposed test, state what a secure result looks like and a legitimate negative control.
Stop when the precondition is absent, the test exceeds its bound, or the observed target differs
from the authorized target. Keep raw tokens, payload secrets and personal data out of output; redact
before storing scanner or runtime evidence.

## Framework references

Use ATT&CK for adversary behavior, CAPEC for attack patterns, CWE for weakness classes, ASVS for
verification requirements, and WSTG for test procedures. These catalogs complement each other;
map only when the identifier and edition are verified. See `../references/ASVS_MAPPING.md`,
`../references/OWASP_MAPPING.md` and `../references/CWE_MAPPING.md`.
