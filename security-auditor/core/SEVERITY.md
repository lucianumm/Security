# SEVERITY, CONFIDENCE, PRIORITY, LIFECYCLE

---

## 1. Severity

Severity describes impact **if the finding is real and reachable**. It is independent of confidence.

### CRITICAL

Immediate, severe, often unauthenticated compromise. Typical cases:

- remote code execution, command injection, unsafe deserialization reachable from user input;
- authentication bypass; login as any user; admin takeover;
- authorization bypass granting access to all users' or all tenants' data;
- SQL/NoSQL injection with data access or modification;
- an **active production secret** committed or exposed to clients;
- mass exposure of `SENSITIVE`/`CRITICAL` data (PII dumps, documents, credentials);
- tenant escape in a multi-tenant system;
- arbitrary file write/upload leading to execution;
- SSRF reaching cloud metadata or internal admin services;
- payment/balance manipulation with direct financial loss.

### HIGH

Serious compromise, or CRITICAL impact behind a meaningful precondition:

- IDOR/BOLA on a single sensitive resource; horizontal privilege escalation;
- missing authorization on a privileged but non-catastrophic action (BFLA);
- stored XSS in an authenticated area; XSS that steals session tokens;
- CSRF on a state-changing sensitive action;
- password reset flaws, account enumeration combined with no rate limiting;
- weak password hashing (fast hash, MD5/SHA1) of real user passwords;
- session tokens that never expire or are not invalidated on logout/password change;
- exploitable dependency vulnerability on a reachable path;
- exposed database/cache/admin interface on the public network;
- privileged container / Docker socket exposure; overly broad cloud IAM on production;
- secrets retrievable from the client bundle (non-production or limited scope);
- missing rate limiting on authentication or on an expensive/abusable operation.

### MEDIUM

Real but constrained risk, or a defense-in-depth failure that matters:

- missing or weak security headers with a plausible attack path (no CSP, missing HSTS);
- cookies missing `Secure`/`HttpOnly`/`SameSite` in a cookie-auth application;
- verbose errors leaking stack traces, paths, versions, internal identifiers;
- open redirect; SSRF limited to non-sensitive external targets;
- overly permissive CORS on an authenticated API;
- missing audit logging for security-relevant events;
- unrestricted file type/size on upload without proven execution path;
- outdated dependency with a known but not clearly reachable vulnerability;
- missing tenant scoping in a low-sensitivity query;
- GraphQL introspection/playground exposed in production.

### LOW

Limited risk or meaningful hardening:

- missing `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`;
- server version banners; directory listing of non-sensitive content;
- source maps published in production;
- long but bounded session lifetimes; missing idle timeout;
- non-pinned but non-privileged CI action versions;
- missing `security.txt`; missing DNS CAA.

### INFO

Observations, best practices, documentation gaps, and items requiring the user's confirmation.

### Severity modifiers

Raise one level when: the affected data is `SENSITIVE`/`CRITICAL`; the endpoint is unauthenticated;
the affected account class is administrative; the system is multi-tenant and the flaw crosses
tenants; exploitation is trivially automatable; the issue is already live in production.

Lower one level when: exploitation requires an already-privileged account with legitimate access to
the same data; the path is unreachable in the deployed configuration (state why); a verified
compensating control materially blocks the attack (name the control and its evidence).

Never lower severity because the fix is hard, because the project is small, or because "nobody
knows the URL" (`security by obscurity` is not a control).

## 2. Confidence

| Level | Meaning |
| --- | --- |
| `HIGH` | Verified end to end: the vulnerable path is reachable and the impact is demonstrated or logically certain from the code read. |
| `MEDIUM` | The flaw is clear in code, but reachability or exploitability was not fully proven. |
| `LOW` | Strong indicator only (pattern match, partial read, external dependency behavior assumed). Requires stated follow-up. |

Always state, for `MEDIUM`/`LOW`, the exact check that would raise confidence.

## 3. Priority

| Priority | Rule |
| --- | --- |
| `P0` | Fix now. Any confirmed CRITICAL; any active exposed production secret; any confirmed critical regression. |
| `P1` | Fix before production / urgently. HIGH findings; CRITICAL with LOW confidence pending verification. |
| `P2` | Schedule. MEDIUM findings; HIGH findings that are not reachable in the current deployment. |
| `P3` | Hardening backlog. LOW and INFO. |

Base remediation order (adjust to the project's reality):

1. active exposed secret → 2. RCE → 3. authentication bypass → 4. authorization bypass →
5. privilege escalation → 6. injection → 7. critical SSRF → 8. tenant escape → 9. data exposure →
10. executable upload → 11. critical crypto failure → 12. critical supply chain →
13. production debug/exposure → 14. remaining HIGH → 15. MEDIUM → 16. hardening.

## 4. Fix types

| Type | Definition | Autonomy |
| --- | --- | --- |
| `SAFE_AUTO_FIX` | Deterministic, reversible, low blast radius; no behavior change beyond the security effect. Historical label, not authorization. | Apply only after explicit batch approval |
| `REVIEW_RECOMMENDED` | May affect behavior, compatibility, UX or performance. | Propose; apply only with the user's agreement |
| `MANUAL_INFRASTRUCTURE_ACTION` | Requires a change outside the repository (cloud console, DNS, provider settings, server). | Never apply; write exact steps |
| `SECRET_ROTATION_REQUIRED` | A credential must be revoked/rotated by a human with provider access. | Never apply; write exact steps |
| `ARCHITECTURAL_CHANGE` | Requires structural redesign (auth model, tenancy, trust boundary). | Never apply; write a design proposal |

## 5. Finding lifecycle

```text
                 ┌──────────────────────────────────────────┐
                 ▼                                          │
NEW ──▶ OPEN ──▶ (fix applied) ──▶ NOT_VERIFIED ──▶ verification
                 │                                   │
                 ├─▶ PARTIALLY_FIXED ─────────────────┤
                 ├─▶ MITIGATED ───────────────────────┤
                 ├─▶ EXTERNAL_ACTION_REQUIRED ────────┤
                 ├─▶ ACCEPTED_RISK (user decision, recorded in risk-register.json)
                 └─▶ FIXED ──▶ (reappears in a later audit) ──▶ REGRESSION ──▶ OPEN (priority +1)
```

| Status | Meaning |
| --- | --- |
| `OPEN` | Confirmed, unfixed. |
| `FIXED` | Fixed **and** verified after the change (`EVIDENCE_RULES.md` §7). |
| `PARTIALLY_FIXED` | Some affected paths remain vulnerable; list them. |
| `MITIGATED` | Compensating control reduces risk; root cause remains; record residual risk. |
| `ACCEPTED_RISK` | The user explicitly accepted it. Record who, when, why, and a review date. |
| `EXTERNAL_ACTION_REQUIRED` | Blocked on an action outside this environment. |
| `NOT_VERIFIED` | Could not be confirmed or could not be revalidated this run. |
| `REGRESSION` | Previously `FIXED`, now present again. Raise priority by one level (minimum `P1`). |

Persistence rules:

- Finding IDs (`SEC-0001`, `SEC-0002`, …) are allocated once and never reused for a different issue.
- On every run, correlate current observations with `.security/findings.json` by root cause and
  location, not by wording.
- Never delete an unresolved finding. Closing requires evidence or an explicit `ACCEPTED_RISK`.
- Record `first_seen`, `last_seen`, `fixed_in` (commit/date) and `verification` for each finding.

## 6. Layers

Every finding carries exactly one layer, used for grouping and ownership:

`APPLICATION_CODE` · `FRONTEND` · `BACKEND` · `DATABASE` · `INFRASTRUCTURE` · `CLOUD` ·
`CONTAINER` · `CI_CD` · `SUPPLY_CHAIN` · `OPERATIONAL` · `HUMAN_ACTION`
