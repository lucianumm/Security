# Security Control Matrix — <project name>

<!--
Template for security/SECURITY_MATRIX.md.
Every applicable control from ../references/CHECKLIST_GLOBAL.md appears here exactly once, with a
status and evidence. Statuses: IMPLEMENTED | PARTIALLY_IMPLEMENTED | NOT_IMPLEMENTED |
MISCONFIGURED | NOT_APPLICABLE | NOT_VERIFIED (../core/EVIDENCE_RULES.md).
"Risk" is the residual risk of the current state, not the severity of a hypothetical failure.
-->

Date: <YYYY-MM-DD> · Commit: <sha> · Coverage: <XX>% of applicable controls verified

Legend — Evidence must be a concrete pointer (`path:line`, config excerpt, observed response,
scanner run) or the reason it could not be obtained.

---

## Transport and headers

| Control | Status | Evidence | Risk | Finding |
| --- | --- | --- | --- | --- |
| HTTPS enforced | IMPLEMENTED | `nginx/app.conf:12` (301 redirect) | — | — |
| TLS 1.2/1.3 only | IMPLEMENTED | `nginx/app.conf:24` | — | — |
| HSTS | NOT_IMPLEMENTED | response headers, `GET /` | Medium | SEC-0012 |
| CSP | PARTIALLY_IMPLEMENTED | `middleware/headers.ts:18` (`unsafe-inline`) | Medium | SEC-0013 |
| X-Content-Type-Options | IMPLEMENTED | `middleware/headers.ts:21` | — | — |
| Referrer-Policy | NOT_IMPLEMENTED | response headers | Low | SEC-0021 |
| Permissions-Policy | NOT_IMPLEMENTED | response headers | Low | SEC-0022 |
| frame-ancestors / X-Frame-Options | IMPLEMENTED | `middleware/headers.ts:23` | — | — |
| Cache-Control on sensitive responses | NOT_VERIFIED | not inspected — no access to CDN config | Unknown | — |

## Authentication and session

| Control | Status | Evidence | Risk | Finding |
| --- | --- | --- | --- | --- |
| Password hashing (approved KDF) | | | | |
| Brute force protection | | | | |
| User enumeration resistance | | | | |
| MFA for administrators | NOT_VERIFIED | external IdP, no access | High | SEC-0014 |
| Session rotation on login | | | | |
| Session invalidation on logout | | | | |
| Idle / absolute timeout | | | | |
| Cookie flags (Secure/HttpOnly/SameSite) | | | | |
| JWT validation (alg, exp, iss, aud) | | | | |
| Token storage on the client | | | | |

## Authorization

| Control | Status | Evidence | Risk | Finding |
| --- | --- | --- | --- | --- |
| Deny by default | | | | |
| Server-side enforcement on every privileged route | | | | |
| Object-level ownership (IDOR/BOLA) | | | | |
| Function-level roles (BFLA) | | | | |
| Tenant isolation — database | | | | |
| Tenant isolation — cache/storage/search/jobs | | | | |
| Re-authentication for sensitive actions | | | | |
| Admin surface baseline | | | | |

### Authorization matrix

| Resource | Action | Guest | User | Manager | Admin | Enforced at | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Profile | read own | No | Yes | Yes | Yes | | |
| Profile | read others | No | No | Team | Yes | | |
| Invoice | read | No | Own | Team | Yes | | |
| Invoice | delete | No | No | No | Yes | | |
| Users | manage roles | No | No | No | Yes | | |

## Input handling and injection

| Control | Status | Evidence | Risk | Finding |
| --- | --- | --- | --- | --- |
| Server-side schema validation | | | | |
| SQL injection defenses | | | | |
| NoSQL injection defenses | | | | |
| Command injection defenses | | | | |
| XSS defenses (stored/reflected/DOM) | | | | |
| Output encoding per context | | | | |
| Deserialization safety | | | | |
| Prototype pollution | | | | |
| ReDoS | | | | |
| Mass assignment | | | | |
| Path traversal | | | | |
| Open redirect | | | | |
| SSRF | | | | |

## API and realtime

| Control | Status | Evidence | Risk | Finding |
| --- | --- | --- | --- | --- |
| Endpoint inventory complete | | | | |
| Excessive data exposure | | | | |
| Pagination and payload limits | | | | |
| CORS configuration | | | | |
| CSRF protection | | | | |
| Rate limiting (per operation) | | | | |
| Resource exhaustion bounds | | | | |
| Idempotency on sensitive operations | | | | |
| GraphQL controls | | | | |
| WebSocket controls | | | | |

## Files, data and cryptography

| Control | Status | Evidence | Risk | Finding |
| --- | --- | --- | --- | --- |
| Upload validation (type, size, name, storage) | | | | |
| Download authorization | | | | |
| Object storage access policy | | | | |
| Encryption in transit (datastores) | | | | |
| Encryption at rest | | | | |
| Approved algorithms and modes | | | | |
| Key management and rotation | | | | |
| CSPRNG for security values | | | | |
| Retention and deletion | | | | |

## Secrets

| Control | Status | Evidence | Risk | Finding |
| --- | --- | --- | --- | --- |
| No secrets in the repository | | | | |
| No secrets in the client bundle | | | | |
| No secrets in images / CI logs | | | | |
| Secret storage mechanism | | | | |
| No insecure default fallbacks | | | | |
| Rotation procedure | | | | |

## Infrastructure

| Control | Status | Evidence | Risk | Finding |
| --- | --- | --- | --- | --- |
| Reverse proxy hardening | | | | |
| Container non-root / unprivileged | | | | |
| No Docker socket / privileged mode | | | | |
| Datastore not publicly exposed | | | | |
| Cloud IAM least privilege | | | | |
| IaC misconfiguration scan | | | | |
| CDN/WAF and origin protection | | | | |
| DNS (DNSSEC, CAA, dangling records) | | | | |
| Email (SPF, DKIM, DMARC) | | | | |
| Server hardening (SSH, firewall, updates) | | | | |

## Supply chain and CI/CD

| Control | Status | Evidence | Risk | Finding |
| --- | --- | --- | --- | --- |
| Dependency audit clean / triaged | | | | |
| Lockfile committed and enforced | | | | |
| Install scripts reviewed | | | | |
| Container image scan | | | | |
| Git hygiene (.gitignore, no secrets) | | | | |
| CI token least privilege | | | | |
| Third-party actions pinned | | | | |
| Untrusted-trigger safety | | | | |
| Security gate in CI | | | | |

## Operations

| Control | Status | Evidence | Risk | Finding |
| --- | --- | --- | --- | --- |
| Security event logging | | | | |
| No sensitive data in logs | | | | |
| Log retention and off-host shipping | | | | |
| Alerting on security signals | | | | |
| Dashboards/metrics protected | | | | |
| Backups configured | | | | |
| **Restore tested** | NOT_VERIFIED | no restore evidence → `BACKUP_STATUS = NOT_VALIDATED` | | |
| Error handling / debug disabled | | | | |
| Incident response readiness | | | | |

## AI *(if applicable)*

| Control | Status | Evidence | Risk | Finding |
| --- | --- | --- | --- | --- |
| Provider keys server-side | | | | |
| Cost and rate quotas | | | | |
| Prompt-injection mitigations (architectural) | | | | |
| Tool authorization independent of model output | | | | |
| RAG retrieval permission filtering | | | | |
| Output validation and safe rendering | | | | |

---

## Not applicable

| Control | Reason |
| --- | --- |
| <control> | <why this system cannot have it> |

## Not verified

| Control | What is missing to verify it |
| --- | --- |
| <control> | <access, tool, authorization, or environment needed> |
