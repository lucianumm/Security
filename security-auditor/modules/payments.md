# MODULE — PAYMENTS AND FINANCIAL OPERATIONS

Load when the project handles payments, subscriptions, credits, payouts or any monetary value.

Related: `webhooks.md`, `business-logic.md`, `authorization.md`, `logging.md`.
Standards: PCI DSS (scope reduction principles), OWASP API Top 10 API6, CWE-602, CWE-841, CWE-799.

---

## 1. Discovery

```bash
grep -rniE "stripe|paypal|adyen|braintree|mercadopago|mercadopago|pagseguro|asaas|iugu|paddle|lemonsqueezy|square|pix|boleto|checkout|invoice|subscription|refund|payout|charge" . -l | head -30
```

Identify the provider(s), the integration style (hosted checkout, elements/SDK, direct API), and
whether card data ever touches your servers.

## 2. Never handle raw card data

- Card numbers, CVV and full PAN must go directly to the provider (hosted fields, Stripe Elements,
  provider SDK). Any code that receives, logs, stores or forwards raw card data is CRITICAL and
  puts the project in full PCI DSS scope.
- Never store CVV — under any circumstance, encrypted or not.
- Storing a card token/last four/brand for display is fine; storing the PAN is not.

```bash
grep -rniE "card_number|cardNumber|cvv|cvc|pan|expiry|numero_cartao" src app | head -20
```

## 3. Server-side authority

| Value | Rule |
| --- | --- |
| Price | Computed on the server from the catalog — never taken from the request |
| Quantity | Validated (positive integer, bounded, stock-checked) |
| Discount / coupon | Validated server-side: exists, active, applicable, not expired, usage limit not exceeded, belongs to this user/plan |
| Currency | Bound to the product/price record; a client-chosen currency must map to a server-defined price |
| Tax / shipping | Computed server-side |
| Total | Recomputed and compared against the provider's charge amount |
| Success state | Derived from the provider (webhook/API verification), never from a client redirect |

The classic critical bug: the client posts `amount` and the server charges it. The second classic:
the client is redirected to `/success` and the server marks the order paid without verifying with
the provider.

## 4. Payment lifecycle integrity

- **Idempotency**: every charge, refund and payout uses an idempotency key so a retry cannot
  duplicate the operation; the key derives from the business operation, not from a random value
  generated per attempt.
- **Authoritative status**: order/subscription state changes only from a verified provider event or
  a server-side API confirmation.
- **Webhook verification**: signature, timestamp window and replay protection (`webhooks.md`).
- **Out-of-order events**: webhooks arrive out of order and duplicated — process by event id with a
  state machine that ignores stale transitions.
- **Partial failure**: payment captured but the order not persisted (and the reverse) must be
  detectable — use a transactional outbox and a reconciliation job comparing provider records with
  local records daily.
- **Refunds**: authorized, bounded by the original amount minus prior refunds, idempotent, logged,
  and not self-service where fraud risk is material.
- **Payouts/withdrawals**: strong authorization, re-authentication, destination-change cooldown and
  notification, velocity limits, manual review thresholds, and separation of duties.
- **Currency and rounding**: integer minor units (cents) throughout; never floats for money;
  consistent rounding rules.
- **Race conditions**: `business-logic.md` §3 — balance and stock changes must be atomic.

## 5. Authorization on financial objects

Every invoice, receipt, subscription, payment method and payout is an object with an owner and a
tenant. Apply the full five-part check (`authorization.md` §1). Invoice/receipt URLs are frequently
guessable and unauthenticated — verify explicitly, including PDF endpoints and email links.

## 6. Provider credentials and configuration

- Secret keys server-side only; publishable keys are the only ones allowed in the client
  (`frontend.md` §1). A live secret key in a bundle is CRITICAL.
- Test vs live keys separated per environment; no test mode in production and no live keys in
  staging.
- Webhook signing secrets stored in the secret manager and distinct per environment.
- Restricted API keys with the minimum permissions where the provider supports them.
- Provider dashboard access: MFA, least privilege, offboarding.

## 7. Fraud and abuse

Card testing (many small charges with different cards) · stolen-card use · refund abuse ·
promo/coupon farming · chargeback-driven service theft · subscription sharing.

Recommend: provider fraud tooling (Radar/equivalent), velocity limits per account/IP/card,
3-D Secure / SCA where applicable, address and CVV checks by the provider, alerting on failure-rate
and refund-rate spikes (`monitoring.md`), and delayed fulfillment for high-risk orders.

## 8. Audit trail

Every financial event logged immutably with actor, amount, currency, provider reference, before and
after balance, and the reason (`logging.md`). Financial audit records must not be deletable by the
application role. Reconciliation reports retained.

## 9. Regression tests

Client-supplied price is ignored and the catalog price is charged · negative/zero/fractional
quantity rejected · expired, exhausted or foreign-owned coupon rejected · duplicate webhook does not
double-credit · webhook with an invalid signature rejected · refund exceeding the original amount
rejected · concurrent withdrawals cannot overdraw the balance · another user's invoice returns
403/404 · marking an order paid requires a verified provider event.
