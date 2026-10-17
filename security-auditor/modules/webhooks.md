# MODULE — WEBHOOKS (INBOUND AND OUTBOUND)

A webhook endpoint is an unauthenticated, internet-facing entry point that mutates state. Treat it
with the same rigor as an admin API.

Related: `payments.md`, `api.md`, `backend.md` §SSRF, `cryptography.md`.
Standards: OWASP API Top 10, CWE-345, CWE-347, CWE-294, CWE-918.

---

## 1. Discovery

```bash
grep -rniE "webhook|/hooks?/|stripe.*constructEvent|verifyWebhook|X-Hub-Signature|X-Signature|svix|callback" src app routes | head -40
```

Distinguish **inbound** (a provider calls you) from **outbound** (you call a customer-supplied URL).
They have opposite threat models.

## 2. Inbound webhooks

| Control | Requirement |
| --- | --- |
| Signature verification | Verify the provider's HMAC/asymmetric signature over the **raw body**, using the provider's SDK where available. Body parsers that rewrite the payload break verification — capture the raw body first |
| Constant-time comparison | `timingSafeEqual`/`hmac.compare_digest`/`hash_equals`; never `==` |
| Secret management | Per-provider, per-environment secret from the secret store; rotatable (support two valid secrets during rotation) |
| Timestamp | Reject events outside a tolerance window (commonly ±5 min) to limit replay |
| Replay protection | Store processed event ids; reject or no-op duplicates (also required because providers legitimately retry) |
| Idempotency | Processing the same event twice must not double-charge, double-credit or duplicate records |
| Schema validation | Validate the payload shape and values; never trust field types or nesting |
| Authorization of content | The event must reference an object that belongs to the account the webhook is configured for — a signed event for another tenant must not mutate your data |
| Source verification | Where the provider publishes IP ranges, restrict; signature remains the primary control |
| Transport | HTTPS only; no `http://` endpoints registered |
| Rate limiting | Bounded, with a queue; a provider outage retry storm must not take you down |
| Response | Fast 2xx after durable enqueue; process asynchronously; never do long work in the handler |
| Error handling | Failures logged with the event id; a dead-letter queue with alerting; no sensitive data in responses |
| Out-of-order handling | State machine that ignores stale transitions (`payments.md` §4) |
| CSRF exemption | Justified and narrowly scoped to the webhook path only |

Critical anti-pattern: trusting the payload because "only the provider knows the URL". A webhook
URL is not a secret. An unsigned webhook that grants entitlements is CRITICAL.

## 3. Outbound webhooks (you calling a user-supplied URL)

This is SSRF by design — apply `backend.md` §6 in full:

- Validate the URL at registration and again before each send: `https` only, public IP only, deny
  loopback/private/link-local/metadata ranges, resolve and pin the IP, re-validate on redirects (or
  disable redirects).
- Egress restriction at the network level where possible.
- Do not forward internal headers, credentials or cookies.
- Sign your outgoing requests (HMAC with a per-subscriber secret plus a timestamp) so receivers can
  verify you.
- Timeouts, retry with exponential backoff and a cap, circuit breaker per endpoint, and a maximum
  response size that you ignore anyway.
- Never expose the response body or timing back to the user (blind SSRF hardening).
- Per-subscriber rate limits; disable endpoints that fail persistently.
- Do not include more data in the payload than the subscriber needs (`SENSITIVE` data should be
  fetched authenticated, not pushed).

## 4. Verification checklist for an existing integration

1. Send an unsigned request → must be rejected (401/400), nothing mutated.
2. Send a request signed with a wrong secret → rejected.
3. Replay a valid captured request → no duplicate effect.
4. Send a valid signature with an old timestamp → rejected.
5. Send a valid event referencing another tenant's object → rejected.
6. Send a malformed/oversized payload → rejected cleanly, no crash, no stack trace.
7. Register an outbound webhook pointing to `http://169.254.169.254/` → rejected at registration.

(Only against your own non-production environment — `../core/SAFETY.md` §6.)

## 5. Regression tests

Invalid signature rejected · stale timestamp rejected · duplicate event id processed once ·
raw-body capture preserved through the middleware chain (a regression test here catches a very
common breakage) · outbound URL validator blocks private ranges and redirects to them ·
webhook handler enqueues and returns quickly.
