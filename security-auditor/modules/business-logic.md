# MODULE — BUSINESS LOGIC SECURITY

Technical scanners cannot find these. This module is about legitimate operations used in an
illegitimate order, quantity, timing or combination.

Guiding question:

> Can a user gain value, cause loss, or reach a state they should not, purely by changing the
> order, quantity, repetition, timing or parameters of operations they are allowed to perform?

Related: `payments.md`, `authorization.md`, `backend.md` §Concurrency, `api.md` §Rate limiting.
Standards: OWASP WSTG Business Logic Testing, OWASP API Top 10 API6, CWE-840, CWE-841, CWE-362,
CWE-799.

---

## 1. Method

1. Reconstruct each critical workflow as a state machine from the code: states, allowed
   transitions, who may trigger each, and what invariants must hold.
2. For each transition ask: can it be skipped, repeated, reversed, run concurrently, run out of
   order, or triggered by the wrong actor?
3. For each numeric input ask: negative, zero, fractional, enormous, string, null, different
   currency, different unit?
4. For each invariant ask: where is it enforced — client, application, or database constraint?
   Only the last two count.

## 2. Flows to examine

Registration and invitation · trial and plan changes · subscription upgrade/downgrade/cancellation ·
coupon, voucher and referral codes · loyalty points and credits · cart, pricing and shipping ·
stock reservation · order placement, cancellation and refund · withdrawal, payout and transfer ·
approval and multi-step workflows (quote → order → invoice) · document signing · ratings and
reviews · content moderation and reporting · quota and usage metering · file/API rate consumption ·
role assignment and team membership · data export and account deletion.

## 3. Common flaws

| Flaw | Example | Control |
| --- | --- | --- |
| Skipped step | Calling the "confirm order" endpoint without payment | Server-side state machine; verify prerequisites |
| Repeated step | Applying the same coupon twice; redeeming a referral repeatedly | Idempotency, uniqueness constraints, usage counters |
| Reversed step | Requesting a refund then cancelling the return | Transition rules with irreversible states |
| Concurrency | Two simultaneous withdrawals from one balance | Transactions, atomic updates, locking (`backend.md` §12) |
| Negative / overflow values | Quantity `-1` to credit the account; huge quantity to overflow | Range validation and DB constraints |
| Price/discount trust | Price or discount sent by the client | Recompute server-side (`payments.md`) |
| Currency/unit confusion | Paying in a weaker currency for the same product | Bind currency to the price server-side |
| Time manipulation | Client-supplied timestamps to extend a trial or backdate a record | Server clock only |
| Quota bypass | Deleting and recreating records to reset counters; using a second workspace | Count against a durable, per-account meter |
| Enumeration for value | Guessing gift-card, invite or discount codes | High entropy, rate limiting, lockout |
| Free-tier abuse | Unlimited trials via email aliases | Identity checks, device/payment binding, quotas |
| Approval bypass | Self-approving one's own request | Segregation of duties enforced server-side |
| State leakage between tenants | Sequence/counter shared across tenants | Per-tenant scoping |
| Partial failure | Payment captured but the order not created (or vice versa) | Transactional outbox, reconciliation job, idempotency |
| Withdrawal race | Requesting a payout while a refund is processing | Locking + status guards |
| Referral self-dealing | Referring yourself with a second account | Identity/device correlation, delayed payout |

## 4. Invariants to verify explicitly

Balances never go negative unless intended · stock never oversells · totals equal the sum of the
lines including tax and discount · a discount cannot exceed the price · credits granted equal
credits consumed · each coupon's usage count is bounded · a subscription cannot be active without a
valid payment state · an approved record cannot be edited without re-approval · deleted resources
disappear from every read path (search, export, cache, related objects).

Where an invariant is critical, recommend enforcing it in the database (constraint, check,
`SELECT ... FOR UPDATE`) rather than only in application code.

## 5. Abuse and anti-automation

Beyond rate limiting (`api.md` §5), consider: velocity checks per account and per payment
instrument, device fingerprinting where lawful, human verification on high-risk actions, delays on
irreversible operations, notification to the user on sensitive changes, and manual review
thresholds. Balance against usability — recommend proportionately.

## 6. Detection

Business-logic attacks look like normal traffic. Recommend metrics and alerts on: refund rate,
coupon redemption rate, credit issuance, negative balances, order cancellation patterns, unusual
export volume, and accounts consuming quota far above the norm (`monitoring.md`).

## 7. Regression tests

Concurrent double-spend leaves the balance correct · coupon redeemed twice is rejected · negative
and oversized quantities rejected · out-of-order transition rejected (confirm before pay) ·
client-sent price ignored · self-approval rejected · quota reset attempt via delete/recreate does
not reset the meter · trial extension via client timestamp rejected.
