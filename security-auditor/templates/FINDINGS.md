# Findings — <project name>

<!--
Template for security/FINDINGS.md.
One block per finding, most severe first. IDs are persistent across audits — reuse the ID for the
same underlying problem and never reuse an ID for a different one.
Statuses and severities: ../core/SEVERITY.md. Evidence rules: ../core/EVIDENCE_RULES.md.
-->

Legend: Severity `CRITICAL|HIGH|MEDIUM|LOW|INFO` · Priority `P0|P1|P2|P3` ·
Confidence `HIGH|MEDIUM|LOW` · Status `OPEN|FIXED|PARTIALLY_FIXED|MITIGATED|ACCEPTED_RISK|
EXTERNAL_ACTION_REQUIRED|NOT_VERIFIED|REGRESSION` ·
Fix type `SAFE_AUTO_FIX|REVIEW_RECOMMENDED|MANUAL_INFRASTRUCTURE_ACTION|SECRET_ROTATION_REQUIRED|
ARCHITECTURAL_CHANGE`

---

## SEC-0001 — <short, specific title>

| Field | Value |
| --- | --- |
| Severity | CRITICAL |
| Priority | P0 |
| Confidence | HIGH |
| Status | OPEN |
| Layer | BACKEND |
| Category | Broken Access Control |
| CWE | CWE-862 — Missing Authorization |
| OWASP | Top 10:2025 A01 · API Security Top 10:2023 API1 |
| ASVS | v5.0.0 — V8 Authorization |
| First seen | <YYYY-MM-DD> (commit <sha>) |
| Last seen | <YYYY-MM-DD> (commit <sha>) |
| Fix type | REVIEW_RECOMMENDED |

**Affected**

```text
src/api/invoices.ts:82-101
src/api/invoices.ts:140-152   (same root cause, delete path)
```

**Evidence**

```ts
// src/api/invoices.ts:88
const invoice = await db.invoice.findUnique({ where: { id: req.params.id } });
return res.json(invoice);   // no ownership or tenant filter
```

Route registered at `src/routes.ts:31` behind `requireAuth` only; no policy middleware.
Verified there is no upstream filter: `grep -n "tenantId" src/api/invoices.ts` → no match.

**Attack scenario**

1. Attacker authenticates as any valid user (self-registration is open).
2. Requests `GET /api/invoices/<id>` iterating sequential ids.
3. Receives every invoice in the system, including other organizations'.

**Impact**

Full read access to all customers' invoices: names, addresses, tax identifiers and amounts
(`CONFIDENTIAL`/`SENSITIVE` data). Cross-tenant exposure; likely notification obligations.

**Root cause**

Authorization is applied at the route level (authentication only). Object-level ownership and
tenant scoping are not enforced in the data layer, and there is no default-deny policy.

**Recommended fix**

1. Filter every query by the tenant derived from the session:
   `where: { id, tenantId: session.tenantId }`.
2. Return 404 for objects outside the tenant so existence is not disclosed.
3. Introduce a central policy layer so new routes are deny-by-default.
4. Apply the same change to the update and delete handlers (lines 140-152).

**Regression test**

`tests/security/invoices.authz.spec.ts` — user of tenant A requests an invoice of tenant B →
expects 404 and an empty body; repeated for GET, PATCH and DELETE.

**Verification**

<How this was, or will be, proven fixed. Empty until verified — a code change alone is not
verification (`../core/EVIDENCE_RULES.md` §7).>

---

## SEC-0002 — <title>

<!-- repeat the block -->

---

## Closed and carried-over findings

| ID | Title | Severity | Status | Note |
| --- | --- | --- | --- | --- |
| SEC-0000 | <title> | HIGH | FIXED | Verified <date> by <test/observation> |
| SEC-0000 | <title> | ACCEPTED_RISK | — | Accepted by <user> on <date>, review <date> |
| SEC-0000 | <title> | EXTERNAL_ACTION_REQUIRED | — | Blocked on <provider action> |
| SEC-0000 | <title> | REGRESSION | OPEN | Was FIXED on <date>, reappeared in <commit> |
