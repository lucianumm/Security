# MODULE — API SECURITY (REST, GraphQL, WebSocket, RPC)

Scope: the HTTP/WS surface — per-endpoint controls, CORS, CSRF, rate limiting, payload handling,
response shaping, GraphQL and realtime channels.

Related: `authorization.md`, `backend.md`, `frontend.md`, `webhooks.md`, `business-logic.md`.
Standards: OWASP API Security Top 10:2023, ASVS v5.0.0 V4 (API and Web Service) and V8 (Authorization), CWE-284, CWE-352, CWE-770, CWE-915, CWE-213.

---

## 1. Endpoint inventory

Enumerate every endpoint (see `authorization.md` §2 for the search commands) and fill this table in
`security/ATTACK_SURFACE.md`:

| Method | Path | Auth | AuthZ rule | Input validated | Rate limit | Data returned | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |

Include: versioned/legacy routes, internal routes, health/metrics/debug, OpenAPI/Swagger, GraphQL,
WebSocket, server actions, file endpoints, and anything mounted by a library (admin UIs, queue
dashboards, dev tools).

## 2. Per-endpoint controls

- **Authentication**: required unless the endpoint is intentionally public (justify each public one).
- **Authorization**: the five-part check (`authorization.md` §1).
- **Input validation**: schema-based, server-side, allowlist (`backend.md` §Validation).
- **Rate limiting / quotas**: §5.
- **Payload limits**: maximum body size, array length, string length, nesting depth, file size.
- **Response exposure**: return only the fields the caller needs — see §3.
- **Pagination**: mandatory limits with a maximum page size; no unbounded `limit`.
- **Timeouts**: request and upstream timeouts set; no unbounded waits.
- **Idempotency**: for payments, orders, refunds, credits and webhook processing (`payments.md`).
- **Method restriction**: only the methods the endpoint needs; `TRACE` disabled; `OPTIONS` limited
  to preflight; verify the framework does not auto-expose `PUT`/`DELETE`.
- **Content-Type**: validated on request; correct and explicit on response;
  `X-Content-Type-Options: nosniff` set.
- **HTTP parameter pollution**: duplicated parameters handled deterministically.

## 3. Excessive data exposure

Serializing an entity directly is the most common data-leak source.

```bash
grep -rnE "res\.json\((user|account|order|record|row|entity|\w+)\)|return (user|account|profile)\b|JsonResponse\(.*__dict__|toJSON\(\)|\.serialize\(\)" src app | head -40
```

Check for leaked: password hashes, tokens, reset tokens, internal flags, other users' data in
nested relations, soft-deleted records, audit fields, internal IDs of other tenants, email
addresses in public listings, and full objects in error responses. Use explicit DTOs/serializers
with an allowlist of fields.

Also check list endpoints and search: do they leak counts or existence for records the caller
cannot read?

## 4. Mass assignment

```bash
grep -rnE "create\(req\.body|update\(req\.body|Object\.assign\(|\.\.\.req\.body|save\(req\.body|new \w+\(req\.body|fill\(\$request->all\(\)|\*\*request\.data" src app | head -40
```

Any write built from the whole request body without a DTO/schema/allowlist is a finding. Attempt
the concrete escalation fields relevant to the model: `role`, `isAdmin`, `permissions`, `tenantId`,
`organizationId`, `userId`, `ownerId`, `balance`, `credits`, `price`, `status`, `verified`,
`emailVerified`, `createdAt`, `id`. Severity depends on which fields are writable.

## 5. Rate limiting and quotas

Evaluate **separately** — one global limiter is rarely sufficient:

login · password reset · MFA/OTP verification · registration · email/SMS sending · search ·
upload · download/export · report and PDF generation · AI/LLM calls · payment operations ·
webhook receivers · expensive aggregation endpoints · GraphQL queries · public read APIs.

Dimensions: IP, authenticated user, tenant, API key, endpoint, and combinations. Behind a proxy or
CDN, verify the real client IP is derived from a **trusted** forwarded header (`nginx.md`) —
otherwise the limiter is bypassable by spoofing `X-Forwarded-For`.

Verify: limits are enforced server-side and centrally, the store is shared across instances
(Redis, not in-memory, when horizontally scaled), the response is 429 with `Retry-After`, and the
limiter fails closed or degrades safely if the store is unavailable.

## 6. Resource exhaustion

Check bounds on: request body size, JSON depth and array size, file uploads, query result sets,
export sizes, image/PDF generation dimensions and page counts, regex applied to user input
(`backend.md` §ReDoS), recursive data structures, concurrent long-running jobs per user,
LLM token budgets, and zip/archive extraction (`uploads.md` §Archives).

Apply: quotas, timeouts, concurrency limits, maximum sizes, pagination limits, circuit breakers.

## 7. CORS

```bash
grep -rniE "cors|Access-Control-Allow-(Origin|Credentials|Methods|Headers)" . | head -30
```

| Anti-pattern | Verdict |
| --- | --- |
| Reflecting the `Origin` header with `Allow-Credentials: true` | CRITICAL (any site reads authenticated responses) |
| `Allow-Origin: *` on an authenticated API | HIGH |
| `Allow-Origin: *` on a truly public, credential-free API | Acceptable — verify, then `NOT_APPLICABLE` |
| Regex origin matching with an unanchored pattern (`evil-example.com` matches `example.com`) | HIGH |
| `null` origin allowed | HIGH |
| Wildcard methods/headers with credentials | MEDIUM |

CORS is a browser control; it does not protect against non-browser clients. It is never a
substitute for authorization.

## 8. CSRF

Required when authentication can travel automatically (cookies, HTTP Basic, TLS client certs).

- Synchronizer token or double-submit cookie; token bound to the session and validated on every
  state-changing request.
- `SameSite=Lax|Strict` as defense in depth.
- `Origin`/`Referer` validated on state-changing requests.
- `GET`/`HEAD` must be side-effect free.
- Verify exemptions: webhook endpoints, legacy routes and file uploads are frequently excluded from
  CSRF middleware — each exclusion must be justified and compensated.
- SPA + bearer token: no CSRF token needed **if** there is no cookie fallback anywhere.

## 9. GraphQL

Only when a GraphQL schema exists.

- Introspection and playground/GraphiQL disabled in production.
- Authorization enforced **in resolvers** (including field resolvers and nested relations), not in
  the gateway or the client.
- Query depth limit, complexity/cost analysis, and node/result limits.
- Batching and aliasing abuse limited (a single request can multiply work or bypass per-request
  rate limits).
- Persisted queries / allowlists for public APIs where feasible.
- Errors do not leak stack traces, schema internals or database messages.
- Mutations: same input validation, mass-assignment and idempotency rules as REST.
- File uploads through GraphQL follow `uploads.md`.
- Subscriptions: authenticated and authorized per subscription and per event delivery.

## 10. WebSocket / realtime

- Authentication at connect time (token in the subprotocol/first message, not in the URL query
  where it lands in logs) and re-validated on reconnect.
- Authorization per channel/room on subscribe **and** per message.
- `Origin` header checked on the handshake (no CSWSH).
- Message schema validation, message size and rate limits, and backpressure.
- Tenant isolation on channel names; no wildcard subscriptions.
- Session lifecycle: connection closed when the session is revoked or expires.
- `wss://` only.

## 11. API documentation and discovery

Swagger/OpenAPI, `/graphql` playground, `.well-known` endpoints, `/actuator`, `/metrics`,
`/debug/pprof`, queue dashboards and admin UIs: confirm whether each should be public. Exposure is
at least MEDIUM when it reveals internal endpoints, and HIGH when it allows actions.

## 12. Regression tests

Unauthenticated and cross-user access per endpoint (from the authorization matrix) · mass
assignment attempt · oversized body rejected · unbounded `limit` clamped · rate limit returns 429 ·
CORS preflight from an untrusted origin denied · state-changing request without CSRF token
rejected · GraphQL introspection disabled in the production config · WebSocket connect without a
token rejected.
