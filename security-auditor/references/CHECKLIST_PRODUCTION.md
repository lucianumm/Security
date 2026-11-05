# PRODUCTION READINESS CHECKLIST

Gate for `READY_FOR_PRODUCTION`. Every line must be satisfied **with evidence**, explicitly accepted
by the user as a recorded risk, or the verdict cannot be `READY_FOR_PRODUCTION`
(`../core/SCORING.md` §2).

---

## Blockers — any single one forces `NOT_READY_FOR_PRODUCTION`

- [ ] No open CRITICAL finding
- [ ] No active production secret exposed in code, history, client bundle, image or CI logs
- [ ] No authentication bypass
- [ ] No authorization bypass, IDOR or tenant escape on sensitive data
- [ ] No injection with data access or modification impact
- [ ] No unauthenticated access to personal or business-critical data
- [ ] No database, cache, admin panel or management interface reachable from the public internet
- [ ] Debug mode disabled in the production configuration; no dev bypass reachable in production
- [ ] No default or seeded administrative credentials

## Application

- [ ] Authentication verified end to end, including reset and MFA where required
- [ ] Passwords stored with an approved KDF
- [ ] Sessions: rotation, expiry, revocation, secure cookie flags
- [ ] Authorization enforced server-side on every privileged path; matrix produced and tested
- [ ] Input validated server-side on every channel
- [ ] Output encoded contextually; XSS defenses verified
- [ ] CSRF protection where cookies authenticate
- [ ] File upload and download controls in place
- [ ] Rate limiting on authentication and on abusable/expensive operations
- [ ] Error responses generic; no stack traces or internal details
- [ ] Business-logic invariants enforced server-side (pricing, quantities, balances, state machine)

## Data

- [ ] Data classified; sensitive classes identified
- [ ] Encryption in transit everywhere; at rest per data class
- [ ] Least-privilege database credentials; no superuser at runtime
- [ ] Tenant isolation verified in every layer *(multi-tenant systems)*
- [ ] Retention and deletion behavior defined
- [ ] No production data in development/test environments without anonymization

## Secrets and configuration

- [ ] All secrets external to the codebase and to client bundles
- [ ] Separate credentials per environment
- [ ] Application fails fast when a required secret is missing (no insecure defaults)
- [ ] Secret storage with access control and a rotation procedure
- [ ] `.env` and key files untracked; `.env.example` contains placeholders only

## Infrastructure

- [ ] TLS with a modern configuration and automated renewal
- [ ] Security headers delivered (verified on a real response)
- [ ] Only intended ports exposed; management access restricted
- [ ] Containers run as non-root, unprivileged, with resource limits *(if containerized)*
- [ ] Cloud IAM least privilege; MFA on human accounts; root/owner protected *(if cloud)*
- [ ] IaC scanned clean of critical misconfigurations *(if IaC)*
- [ ] CDN/WAF configured and the origin not directly reachable *(if applicable)*
- [ ] Preview/staging deployments isolated from production data *(if applicable)*

## Supply chain and delivery

- [ ] Dependency audit clean of unmitigated critical/high reachable vulnerabilities
- [ ] Lockfiles committed; CI installs from the lockfile
- [ ] Container images scanned *(if applicable)*
- [ ] CI: least-privilege tokens, pinned third-party actions, no untrusted-trigger execution with
      secrets
- [ ] Production build verified (lint, typecheck, tests, build all pass)
- [ ] Security gate active in CI with a documented blocking policy
- [ ] Rollback path documented and exercised

## Operations

- [ ] Security event logging in place; no sensitive data in logs
- [ ] Monitoring and alerting for the key security signals, delivered to a human who reads them
- [ ] Metrics/dashboards/tracing endpoints protected
- [ ] Backups configured, encrypted, offsite, and alerting on failure
- [ ] **Restore tested** with a recorded date and result — otherwise `BACKUP_STATUS = NOT_VALIDATED`
      and the verdict is at best `READY_WITH_RESTRICTIONS`
- [ ] RPO/RTO stated and achievable
- [ ] Incident response procedure exists with named responsibilities
- [ ] Contact path for vulnerability reports *(public products)*

## Evidence and process

- [ ] Coverage ≥ 80% of applicable controls verified; the remainder listed as `NOT_VERIFIED`
- [ ] All findings recorded with IDs and statuses in `.security/findings.json`
- [ ] Baseline written (`security/SECURITY_BASELINE.md`) so drift can be detected
- [ ] Regression tests exist for every fixed CRITICAL and HIGH finding, and they pass
- [ ] Remaining risks accepted explicitly by the user, with owners and review dates
- [ ] Scope and limitations documented in the report

---

## Verdict statement template

```text
Production Readiness: READY_WITH_RESTRICTIONS

Satisfied: application controls, secrets, TLS, container hardening, CI gate.
Restrictions:
 1. SEC-0011 — Stripe key rotation pending (EXTERNAL_ACTION_REQUIRED, owner: user, due: <date>)
 2. Backups configured but never restored → BACKUP_STATUS = NOT_VALIDATED; run a restore drill
    before onboarding customer data.
 3. No alerting on repeated authentication failures (SEC-0019, P2).
Not verified: production infrastructure (no access), Cloudflare WAF rules (no access).
```
