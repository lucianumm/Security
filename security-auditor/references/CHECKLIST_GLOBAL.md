# GLOBAL CHECKLIST

Coverage self-check for a **full** audit. Every applicable line must end with one of:
`IMPLEMENTED` · `PARTIALLY_IMPLEMENTED` · `NOT_IMPLEMENTED` · `MISCONFIGURED` · `NOT_APPLICABLE` ·
`NOT_VERIFIED` — plus evidence (`../core/EVIDENCE_RULES.md`).

Lines marked *(if present)* are skipped with `NOT_APPLICABLE` when the technology is absent.
Do not run this as a questionnaire: it is the closing verification that the modules were covered.

---

## Transport and headers
- [ ] HTTPS everywhere; HTTP→HTTPS redirect
- [ ] Modern TLS (1.2/1.3), no weak ciphers, valid certificate and renewal
- [ ] HSTS
- [ ] No mixed content; `wss://` for realtime
- [ ] Content-Security-Policy (and its directives reviewed individually)
- [ ] X-Content-Type-Options, Referrer-Policy, Permissions-Policy
- [ ] frame-ancestors / X-Frame-Options
- [ ] Cross-Origin-Opener/Resource(/Embedder) policies
- [ ] Cache-Control on authenticated responses

## Authentication and session
- [ ] Login, logout, registration, reset, email/password change flows audited
- [ ] Password storage with an approved KDF
- [ ] Brute force and credential stuffing protection
- [ ] User enumeration resistance
- [ ] MFA (enforced for admin/privileged/financial)
- [ ] OAuth/SSO validation (state, PKCE, nonce, redirect allowlist, token verification) *(if present)*
- [ ] Session ID entropy, rotation on login, invalidation on logout/password change
- [ ] Idle and absolute timeouts; revocation capability
- [ ] Cookie flags: Secure, HttpOnly, SameSite, Path, Domain
- [ ] JWT: signature, algorithm pinning, exp/iss/aud, revocation, storage *(if present)*
- [ ] Client-side token storage risk assessed
- [ ] API keys / service credentials scoped, hashed, revocable *(if present)*

## Authorization
- [ ] Every route/handler/resolver/job enumerated with its authorization rule
- [ ] Deny by default; server-side enforcement
- [ ] Object-level ownership checks (IDOR/BOLA)
- [ ] Function-level role checks (BFLA)
- [ ] Authorization matrix produced
- [ ] Privilege escalation paths (horizontal and vertical) tested
- [ ] Multi-tenant isolation across DB, ORM, cache, storage, search, jobs, WS, exports *(if present)*
- [ ] Admin surface baseline applied
- [ ] Re-authentication for the most sensitive actions

## Input and injection
- [ ] Server-side schema validation on every input channel
- [ ] SQL injection
- [ ] NoSQL injection *(if present)*
- [ ] Command injection
- [ ] XSS (stored, reflected, DOM)
- [ ] Output encoding per context; CSV/log/email injection
- [ ] SSTI *(if templates take user input)*
- [ ] Deserialization *(if present)*
- [ ] XXE *(if XML is parsed)*
- [ ] Prototype pollution *(JavaScript)*
- [ ] ReDoS
- [ ] Mass assignment
- [ ] Path traversal
- [ ] Open redirect
- [ ] SSRF (all URL-accepting features)
- [ ] HTTP method restriction; Content-Type validation; parameter pollution

## API and realtime
- [ ] Endpoint inventory with auth/authz/validation/rate-limit per endpoint
- [ ] Excessive data exposure reviewed (DTOs/serializers)
- [ ] Pagination and payload limits
- [ ] CORS configuration
- [ ] CSRF protection where cookies authenticate
- [ ] Rate limiting per sensitive operation, per dimension
- [ ] Resource exhaustion bounds and timeouts
- [ ] Idempotency on sensitive operations
- [ ] GraphQL: introspection, resolver authz, depth/complexity, batching *(if present)*
- [ ] WebSocket: auth, per-channel authz, Origin, message limits *(if present)*
- [ ] API documentation/playgrounds/debug endpoints exposure reviewed

## Files and storage
- [ ] Upload: authz, extension allowlist, magic bytes, size/count, filename, storage location
- [ ] Dangerous types (SVG, HTML, archives, XML, executables) handled
- [ ] Download: authorization, ownership, path handling, headers, signed URLs
- [ ] Object storage: public access, policies, CORS, encryption, lifecycle, logging *(if present)*

## Data and cryptography
- [ ] Data inventory and classification produced
- [ ] Encryption in transit and at rest per data class
- [ ] Approved algorithms, modes, IV/nonce handling, constant-time comparisons
- [ ] Key management and rotation
- [ ] No home-made cryptography
- [ ] Randomness from a CSPRNG
- [ ] Retention and deletion policy; account deletion propagation

## Secrets
- [ ] Secret scan of the working tree (and history, if authorized)
- [ ] No secrets in client bundles, images, CI logs, artifacts
- [ ] `.env` handling, `.env.example` placeholders, no insecure defaults
- [ ] Secret storage mechanism and access control
- [ ] Rotation plan for anything exposed (`SECRET_ROTATION_REQUIRED`)

## Datastores
- [ ] Network exposure of DB/cache/search
- [ ] Least-privilege database user; no default accounts
- [ ] TLS to the datastore
- [ ] RLS / tenant scoping / Firebase-Supabase rules reviewed *(if present)*
- [ ] Migrations and seeds reviewed (no production admin seeds)
- [ ] Cache key scoping, TTLs, sensitive data in cache
- [ ] Connection pool, statement timeouts

## Frontend
- [ ] No secrets in the bundle; public env prefixes reviewed
- [ ] DOM sinks traced to their sources
- [ ] Client-side-only enforcement identified and paired with server checks
- [ ] Third-party scripts inventoried (necessity, pinning, SRI, CSP)
- [ ] Source maps and build artifacts reviewed
- [ ] Debug output and console leakage

## Business logic and money
- [ ] Critical workflows modeled as state machines
- [ ] Invariants enforced server-side/in the database
- [ ] Race conditions and idempotency
- [ ] Coupons, credits, quotas, referrals, trials abuse-tested
- [ ] Payments: server-side pricing, provider-authoritative status, refunds, payouts *(if present)*
- [ ] Webhooks: signature, timestamp, replay, idempotency, tenant binding *(if present)*

## Infrastructure
- [ ] Reverse proxy configuration (TLS, headers, limits, hidden files, tokens) *(if present)*
- [ ] Docker: base image, pinning, non-root, secrets, privileges, socket, ports, limits *(if present)*
- [ ] Kubernetes: securityContext, RBAC, secrets, NetworkPolicy, admission *(if present)*
- [ ] IaC scanned; open security groups, public resources, missing encryption *(if present)*
- [ ] Cloud IAM least privilege; root/owner protection; MFA; environment separation
- [ ] Network exposure of management ports and dashboards
- [ ] CDN/WAF configuration and origin protection *(if present)*
- [ ] Serverless/edge: env exposure, preview deployments, function permissions *(if present)*
- [ ] VPS/OS hardening: SSH, firewall, users, updates, cron/systemd, permissions *(if accessible)*
- [ ] DNS: DNSSEC, CAA, dangling records, registrar protections *(if verifiable)*
- [ ] Email: SPF, DKIM, DMARC *(if the domain sends mail)*

## Supply chain and CI/CD
- [ ] Dependency audit run and interpreted (reachability, fix availability)
- [ ] Lockfiles committed and enforced in CI
- [ ] Install scripts, typosquatting, abandoned and Git dependencies reviewed
- [ ] Container image scan *(if images are built)*
- [ ] Git hygiene: `.gitignore`, no secrets/dumps, branch protection
- [ ] CI: token permissions, untrusted triggers, script injection, action pinning, runner isolation
- [ ] Secrets in CI scoped to protected environments; OIDC preferred
- [ ] Security gate stages defined and blocking policy documented

## Operations
- [ ] Security event logging coverage
- [ ] No sensitive data in logs; redaction configured
- [ ] Log integrity, retention, off-host shipping, time sync
- [ ] Monitoring and alerting for the security signals list
- [ ] Dashboards/metrics endpoints protected
- [ ] Backups: coverage, frequency, offsite, immutability, encryption, alerting
- [ ] **Restore tested** (otherwise `BACKUP_STATUS = NOT_VALIDATED`)
- [ ] Error handling: generic responses, no stack traces, debug off
- [ ] Incident response readiness assessed
- [ ] Vulnerability disclosure channel *(public products)*

## AI *(if present)*
- [ ] Provider keys server-side; quotas and cost caps
- [ ] Direct and indirect prompt injection mitigations (architecture, not prompting alone)
- [ ] Tool authorization independent of model output; confirmation for irreversible actions
- [ ] RAG retrieval filtered by user/tenant permissions
- [ ] Output validation and safe rendering
- [ ] Sandboxing for code execution tools
- [ ] Data sent to third-party providers reviewed for privacy

## Privacy
- [ ] Is each field necessary? Is it stored? For how long? Who can access it?
- [ ] Does it need to appear in logs, analytics, or leave the server?
- [ ] Deletion and export paths exist and are authorized
- [ ] Third-party processors identified

---

## Natural-language triggers

The skill should activate on requests such as: "faça uma auditoria de segurança" · "verifique se
este projeto está seguro" · "faça hardening" · "revise a segurança" · "analise vulnerabilidades" ·
"corrija os problemas de segurança" · "veja se está pronto para produção" · "verifique autenticação
e autorização" · "audite minha API" · "audite Docker e VPS" · "revalide os findings" · "faça
security review deste Pull Request" · and their English equivalents ("security audit",
"is this safe to deploy", "harden this", "check for vulnerabilities", "review this PR for
security").
