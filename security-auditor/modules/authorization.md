# MODULE — AUTHORIZATION (CRITICAL MODULE)

Scope: every decision about whether an authenticated (or anonymous) actor may perform an action on
a resource. This is the most common source of critical findings; never sample — enumerate.

Related: `authentication.md`, `api.md`, `database.md`, `business-logic.md`.
Standards: OWASP Top 10:2025 A01, OWASP API Top 10:2023 API1/API3/API5, ASVS v5.0.0 V8 (Authorization), CWE-285, CWE-639, CWE-862,
CWE-863, CWE-566.

---

## 1. The five-part check

Every privileged operation must verify, **server-side**, all of:

```text
Authentication  — who is the actor?
Permission      — does this role/scope allow this action type?
Ownership       — does this specific resource belong to (or is shared with) the actor?
Tenant          — is the resource inside the actor's organization/tenant?
Action context  — is the action allowed in the resource's current state and the actor's context?
```

Missing **Ownership** is IDOR/BOLA. Missing **Permission** is BFLA. Missing **Tenant** is tenant
escape. Missing **Authentication** on a privileged route is a bypass. All are HIGH or CRITICAL.

## 2. Enumerate every entry point

Do not rely on reading the "auth middleware" file. Build the actual route × control table.

```bash
# Express/Nest/Fastify
grep -rnE "\.(get|post|put|patch|delete)\(|@(Get|Post|Put|Patch|Delete)\(|router\.(get|post|put|patch|delete)" src app routes 2>/dev/null
# Next.js / file-based routing
find . -path ./node_modules -prune -o \( -path "*app/api/*route.*" -o -path "*pages/api/*" \) -print
# server actions / RPC
grep -rn "use server" . --include=*.ts --include=*.tsx | head -40
# Django / Flask / FastAPI
grep -rnE "urlpatterns|@app\.(route|get|post)|@router\.(get|post|put|delete)|path\(" . --include=*.py
# Laravel / Rails / Spring
grep -rnE "Route::(get|post|put|patch|delete)|resources :|@(Get|Post|Put|Delete)Mapping" .
```

Then, for each route, record: method, path, auth required?, permission required?, ownership check?,
tenant scope?, input validated?, rate limited?, data returned. Put this in
`security/ATTACK_SURFACE.md`.

Do not forget these frequently unprotected surfaces:
GraphQL resolvers and field resolvers · WebSocket message handlers · server actions / RPC endpoints ·
background jobs triggered by user input · webhook receivers · file download endpoints ·
export/report generators · admin CLI or management endpoints · health/debug/metrics endpoints ·
"internal" endpoints reachable from the internet · batch/bulk endpoints · search endpoints that
cross tenants · cache-warming and cron endpoints.

## 3. Anti-patterns to flag

| Pattern | Verdict |
| --- | --- |
| Hiding a UI button/menu as the only restriction | Not a control — finding |
| Client-sent role/permission trusted by the server (`if (req.body.isAdmin)`) | CRITICAL |
| JWT claim `role` trusted without verifying signature/issuer | CRITICAL |
| Authorization implemented in the frontend router only | CRITICAL |
| Secret/obscure URL as the access control | Not a control — finding |
| `findById(req.params.id)` with no ownership/tenant filter | IDOR |
| Global middleware with an allowlist of "public" paths where a new route defaults to public | Design flaw — HIGH |
| Permission checked before, but the mutation uses a different id from the body | Bypass |
| Check on the read path but not on the write path (or vice versa) | Partial — HIGH |
| `if (user.role === 'admin')` scattered across handlers | Fragile; drift risk — MEDIUM, recommend centralization |
| Deny list of forbidden roles instead of an allow list | Fails open — HIGH |
| Authorization done in the frontend for GraphQL, resolvers unprotected | CRITICAL |
| Bulk endpoints that filter after fetching all records | Data exposure risk |

Search aids:

```bash
grep -rnE "findById|findOne|findUnique|get_object_or_404|find\(params\[:id\]\)|where\(.?id" src app | head -60
grep -rnE "isAdmin|is_admin|role ?===|role ?==|hasRole|can\(|authorize|permission|ability|policy|guard" src app | head -60
```

For each match: is the actor's identity taken from the **server-side session/token**, and is the
resource filtered by it?

## 4. Authorization matrix

Build the real matrix for the project and put it in `security/SECURITY_MATRIX.md`:

| Resource | Action | Guest | User | Manager | Admin | Enforced at | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Profile | read own | No | Yes | Yes | Yes | `src/api/profile.ts:22` | code |
| Profile | read others | No | No | Team only | Yes | — | **missing** → SEC-00xx |
| Invoice | delete | No | No | No | Yes | — | **missing** → SEC-00xx |

Derive the regression tests directly from this matrix: for every `No` cell, a test that asserts
denial.

## 5. Model quality

- Is there a single, centralized authorization layer (policy/guard/ability/CASL/Oso/OPA/decorators)
  or is it ad hoc? Centralized + default-deny is the target.
- Is the default for a new route **deny**? Test by reasoning about what a newly added route inherits.
- Are permissions data-driven (role → permission table) and auditable?
- Is privilege elevation (role change, ownership transfer, invite to a higher role) itself
  authorized, logged and notified?
- Is there re-authentication for the most dangerous actions (delete account, change email, payout,
  change MFA, add an admin)?
- Are object-level rules expressed once and reused, so read/write/list/export agree?

## 6. Multi-tenancy

If the system serves multiple organizations, customers or workspaces, verify isolation in **every**
layer:

| Layer | Check |
| --- | --- |
| Query | Every query filters by tenant id derived from the session — not from the request body/param |
| ORM | Global scope / row-level security / middleware that cannot be forgotten; check for `raw` escapes |
| Database | RLS policies where available; separate schemas/credentials where claimed |
| Cache | Keys include the tenant id; no cross-tenant key collisions |
| Object storage | Prefix/bucket per tenant; signed URLs scoped; listing disabled |
| Search index | Tenant filter applied at query time and enforced server-side |
| Background jobs | Tenant context propagated; job payloads validated |
| Exports/reports | Scoped, and the generated file is only downloadable by that tenant |
| WebSocket | Subscription channel authorization on join and on each message |
| Logs/metrics | No cross-tenant data leakage in shared dashboards |
| Admin/impersonation | Explicit, logged, time-bounded, and not reachable by tenant users |

Test: authenticate as tenant A and reference an identifier belonging to tenant B in every parameter
position (path, query, body, header, nested object, array element, GraphQL variable). Expected: 403
or 404 consistently — and no difference between "exists in another tenant" and "does not exist"
(that difference is an enumeration oracle).

## 7. Identifiers

- Sequential integer IDs are not a vulnerability by themselves, but they remove the guessing cost;
  where objects are sensitive, recommend UUIDv4/ULID **in addition to** authorization, never instead.
- Check for identifiers leaked in URLs shared externally, emails, invoices and public pages.

## 8. Findings to raise (typical)

`Missing server-side authorization on <route>` · `IDOR on <resource>` · `Cross-tenant data access
via <parameter>` · `Privilege escalation through <field> in mass assignment` ·
`Role check performed only in the client` · `Admin endpoint reachable without authentication` ·
`Authorization enforced on read but not on delete`.

## 9. Regression tests

Generate one test per denied cell of the matrix, plus:

- user A → user B's resource (read, update, delete, list, export) → denied;
- tenant A → tenant B's identifier in every parameter position → denied, identical response for
  "other tenant" and "nonexistent";
- low-privilege user → each privileged action → denied;
- unauthenticated → every non-public route → 401/403;
- role field submitted by the client is ignored on create and update;
- after a user is removed from an organization, their existing session cannot access its data.
