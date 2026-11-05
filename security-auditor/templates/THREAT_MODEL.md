# Threat Model — <project name>

<!--
Template for security/THREAT_MODEL.md. Built in phase 6 of ../core/WORKFLOW.md, after the
architecture, data classification and attack surface are known.
Model the system that exists, not an idealized one.
-->

Date: <YYYY-MM-DD> · Commit: <sha> · Method: STRIDE + attacker-goal analysis

---

## 1. Assets

| # | Asset | Class | Why an attacker wants it | Where it lives |
| --- | --- | --- | --- | --- |
| A1 | User credentials | CRITICAL | Account takeover, credential reuse | `users` table, session store |
| A2 | Customer personal data | SENSITIVE | Resale, fraud, extortion | database, backups, logs, exports |
| A3 | Financial records | SENSITIVE | Fraud, manipulation | database, provider |
| A4 | Uploaded documents | CONFIDENTIAL | Exposure, extortion | object storage |
| A5 | Production secrets | CRITICAL | Full compromise | env vars, secret manager, CI |
| A6 | Service availability | — | Extortion, competitive harm | infrastructure |
| A7 | Admin capability | CRITICAL | Total control | admin panel, cloud IAM |

## 2. Attacker profiles

| Profile | Access | Motivation | Capability |
| --- | --- | --- | --- |
| Anonymous internet user | Public endpoints | Opportunistic, automated | Scanners, known exploits, credential lists |
| Authenticated customer | Own account | Data theft, privilege gain, free usage | Manual API manipulation |
| Malicious tenant | Own organization | Competitor data | Systematic parameter testing |
| Compromised account | A legitimate user's session | Whatever that user can reach | Normal-looking traffic |
| Insider / contractor | Internal access | Data theft, sabotage | Legitimate credentials |
| Supply-chain attacker | A dependency or CI action | Broad compromise | Code execution at build/run time |
| Targeted attacker | Persistent, researched | Specific data or disruption | Chained vulnerabilities, social engineering |

## 3. Threats

One row per meaningful threat. Likelihood and impact are judgments — state the reasoning in the
finding, not just a label.

| # | Asset | Threat (STRIDE) | Attacker | Vector | Precondition | Impact | Likelihood | Existing control | Missing control | Finding |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | A2 | Information disclosure | Authenticated customer | `GET /api/invoices/:id` without ownership check | Any account | All customers' invoices | High | Authentication only | Object-level authorization | SEC-0001 |
| T2 | A1 | Spoofing | Anonymous | Credential stuffing on `/login` | Leaked password lists | Account takeover | High | Password hashing | Rate limiting, MFA | SEC-0007 |
| T3 | A5 | Information disclosure | Anonymous | Secret committed to a public repository | — | Full backend compromise | Medium | — | Secret scanning, rotation | SEC-0011 |
| T4 | A6 | Denial of service | Anonymous | Unbounded export endpoint | Public access | Outage, cost | Medium | — | Rate limits, quotas, timeouts | SEC-0016 |
| T5 | A7 | Elevation of privilege | Authenticated customer | `role` accepted in the update body | Any account | Admin access | Medium | — | Field allowlist | SEC-0004 |

### STRIDE coverage check

| Category | Considered for | Notes |
| --- | --- | --- |
| Spoofing | authentication, sessions, webhooks, service-to-service | |
| Tampering | inputs, stored data, CI artifacts, dependencies | |
| Repudiation | audit logging of privileged and financial actions | |
| Information disclosure | API responses, errors, logs, storage, backups | |
| Denial of service | rate limits, resource bounds, dependencies | |
| Elevation of privilege | authorization, mass assignment, container/cloud privileges | |

### Additional threat classes considered

Account takeover · session hijacking · credential stuffing · horizontal and vertical privilege
escalation · data exfiltration · supply-chain compromise · insider misuse · tenant escape ·
API abuse and business-flow abuse · LLM prompt injection *(if AI is present)* ·
ransomware / destructive attack · third-party provider compromise.

## 4. Attack chains

Realistic multi-step paths matter more than isolated findings.

```text
Chain 1 — from anonymous to full data access
  open registration (no verification)
    → authenticated session
    → SEC-0001 missing object-level authorization
    → enumerate sequential invoice ids
    → export all customer data
  Broken by fixing SEC-0001; partially mitigated by rate limiting and anomaly alerting.
```

```text
Chain 2 — from a leaked secret to production
  SEC-0011 committed API key
    → provider access
    → <what that key reaches>
  Broken by rotation + least-privilege scoping + secret scanning in CI.
```

## 5. Trust boundary analysis

For each boundary in `ATTACK_SURFACE.md` §5, state what would happen if the other side were fully
malicious:

| Boundary | If the other side is hostile | Current resilience |
| --- | --- | --- |
| Browser → API | Any request can be forged | <deny-by-default? validation? authorization?> |
| Provider → Webhook | Forged events | <signature verification?> |
| Dependency → Build | Arbitrary code at build/run | <pinning, review, isolation?> |
| LLM output → Tools | Attacker-authored tool calls | <independent authorization?> |

## 6. Prioritized risk register

| Risk | Severity | Likelihood | Priority | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |

Mirror this into `.security/risk-register.json` for future audits.

## 7. Out of scope / accepted

| Threat | Why out of scope or accepted | Accepted by | Review date |
| --- | --- | --- | --- |
