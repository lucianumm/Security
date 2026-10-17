# Security Baseline — <project name>

<!--
Template for security/SECURITY_BASELINE.md.
This document is the expected security state of the project. Future audits (VERIFY / CI_GATE)
compare reality against it; any control that was IMPLEMENTED and no longer is becomes a
SECURITY REGRESSION (../core/SEVERITY.md §5).
Keep it factual and machine-mirrorable into .security/baseline.json.
-->

Established: <YYYY-MM-DD> · Last updated: <YYYY-MM-DD> · Commit: <sha> ·
Baseline version: <n> · Audit that produced it: <mode>, score <XX>/100

---

## 1. Scope of the baseline

Applies to: <repositories, apps, services covered>
Excluded: <what this baseline does not cover, and why>
Target verification level: <ASVS L1 | L2 | L3> — justified by <data classification>

## 2. Expected control state

A future audit finding a **lower** state than recorded here raises a regression finding.

| Control | Expected state | Where enforced | How to verify |
| --- | --- | --- | --- |
| HTTPS + HSTS | IMPLEMENTED | `nginx/app.conf` | response headers on `GET /` |
| Security headers (CSP, nosniff, referrer, frame-ancestors) | IMPLEMENTED | `middleware/headers.ts` | header assertions in `tests/security/headers.spec.ts` |
| Session cookie flags Secure+HttpOnly+SameSite | IMPLEMENTED | `src/auth/session.ts` | `tests/auth/session.test.ts` |
| Session rotation on login | IMPLEMENTED | `src/auth/login.ts` | `tests/auth/session.test.ts` |
| Password hashing: Argon2id | IMPLEMENTED | `src/auth/hash.ts` | unit test asserting the algorithm |
| MFA required for admin roles | IMPLEMENTED | `src/auth/mfa.ts` | `tests/security/admin-mfa.spec.ts` |
| Object-level authorization on every `/api/**` route | IMPLEMENTED | policy layer `src/authz/` | `tests/security/authz.matrix.spec.ts` |
| Tenant scoping in every query | IMPLEMENTED | Prisma middleware | `tests/security/tenant.spec.ts` |
| Input validation schema on every endpoint | IMPLEMENTED | `src/schemas/` | route-schema coverage test |
| Rate limiting on auth endpoints | IMPLEMENTED | `middleware/rateLimit.ts` | `tests/security/rate-limit.spec.ts` |
| No secrets in the repository | IMPLEMENTED | — | gitleaks in CI |
| No secrets in the client bundle | IMPLEMENTED | — | bundle grep step in CI |
| Container runs as non-root | IMPLEMENTED | `Dockerfile` | `docker run … id` check in CI |
| Datastores not publicly exposed | IMPLEMENTED | `docker-compose.yml`, security groups | config assertion / user confirmation |
| Dependency audit clean of critical | IMPLEMENTED | — | `npm audit` in CI |
| Security event logging | IMPLEMENTED | `src/log/security.ts` | log assertions |
| Backups configured | IMPLEMENTED | <provider> | provider console |
| Restore tested | <date or NOT_VALIDATED> | — | drill record |

## 3. Accepted risks

Carried forward into every future audit. Re-evaluate at the review date.

| ID | Risk | Severity | Why accepted | Accepted by | Date | Review date |
| --- | --- | --- | --- | --- | --- | --- |

## 4. Known gaps (open findings at baseline time)

| ID | Title | Severity | Status | Target date |
| --- | --- | --- | --- | --- |

## 5. Blocking policy for CI

Documented decision for this project (`../modules/ci-cd.md` §Blocking policy):

```text
Fail the pipeline on:  CRITICAL findings, active secrets, auth/authz bypass, confirmed RCE/SQLi,
                       critical reachable dependency vulnerabilities, security regressions,
                       failing security regression tests
Block production on:   HIGH findings          <yes | no — project decision>
Report only:           MEDIUM, LOW, INFO
Exception process:     <who approves, for how long, recorded where>
```

## 6. Security regression tests protected by this baseline

| Test file | Protects | Findings |
| --- | --- | --- |
| `tests/security/authz.matrix.spec.ts` | object- and function-level authorization | SEC-0001, SEC-0004 |
| `tests/security/headers.spec.ts` | security headers | SEC-0012, SEC-0013 |
| `tests/security/rate-limit.spec.ts` | authentication rate limiting | SEC-0007 |

Deleting or weakening one of these tests is itself a regression — review test changes in security
review.

## 7. Environment expectations

| Setting | Production value |
| --- | --- |
| Debug mode | off |
| Error detail to clients | generic |
| Default log level | info, with security events at info or above |
| Required environment variables | <list of names> — startup fails if absent |
| Public env prefixes in use | <list> — must contain no secrets |

## 8. Change control

- Update this baseline only through an audit run (`HARDEN` or a completed `AUDIT_AND_FIX`).
- Record the baseline version and the commit each time.
- Lowering an expected state requires an explicit, recorded decision by the user — never do it
  silently to make an audit pass.
