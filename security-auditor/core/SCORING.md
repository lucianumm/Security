# SCORING AND PRODUCTION READINESS

The score is a communication device, not the verdict. The verdict is the readiness classification
plus the findings list. Never let the score soften a critical finding.

---

## 1. Security score (0–100)

Never a plain average of a checklist. Compute it as a weighted domain assessment with hard caps.

### Step 1 — Domain assessment

Score each applicable domain 0–100 based on the status of its controls (`IMPLEMENTED` = full
credit, `PARTIALLY_IMPLEMENTED` = half, `MISCONFIGURED` = quarter, `NOT_IMPLEMENTED` = 0,
`NOT_APPLICABLE` = excluded from the domain, `NOT_VERIFIED` = excluded from the score **and**
counted separately as coverage loss).

| Domain | Weight |
| --- | --- |
| Authentication & session | 12 |
| Authorization & tenancy | 15 |
| Secrets management | 12 |
| Input handling & injection defense | 12 |
| Data protection (crypto, storage, exposure, privacy) | 10 |
| API & transport security (TLS, headers, CORS, rate limiting) | 9 |
| Infrastructure & containers | 8 |
| Supply chain & dependencies | 7 |
| CI/CD & Git hygiene | 5 |
| Logging, monitoring & alerting | 5 |
| Backup & recoverability | 5 |

Renormalize the weights over the applicable domains only (drop weights for domains that are truly
`NOT_APPLICABLE`, e.g. containers in a project with no container).

`base = Σ(domain_score × weight) / Σ(weights)`

### Step 2 — Finding penalties

Subtract penalties only for findings that still describe current risk. `FIXED` findings contribute
zero only after the verification required by `STATE_MACHINE.md`; `OPEN`, `PARTIALLY_FIXED`,
`REGRESSION` and `EXTERNAL_ACTION_REQUIRED` findings retain their full penalty. `MITIGATED` and
`ACCEPTED_RISK` findings retain half their severity penalty to reflect residual exposure. A
`NOT_VERIFIED` finding is not evidence that the risk is absent: keep the conservative severity,
mark the affected control unverified, and let coverage/readiness rules reflect the uncertainty.
Confirmed means `Confidence: HIGH` or `MEDIUM`:

| Severity | Penalty each | Cap |
| --- | --- | --- |
| CRITICAL | 25 | no cap |
| HIGH | 10 | 40 total |
| MEDIUM | 3 | 20 total |
| LOW | 1 | 8 total |
| INFO | 0 | — |
| REGRESSION | +5 extra on top of its severity | 15 total |

`LOW` confidence findings count at half penalty.

### Step 3 — Hard caps

Apply the lowest applicable cap:

| Condition | Score cannot exceed |
| --- | --- |
| Any confirmed CRITICAL open | 40 |
| Active production secret exposed and not rotated | 35 |
| Authentication or authorization bypass open | 30 |
| More than 3 open HIGH | 55 |
| Any open HIGH | 75 |
| Backups absent or `NOT_VALIDATED` for a system holding `SENSITIVE`/`CRITICAL` data | 80 |
| No security logging at all | 85 |
| No applicable controls were assessed | report `INSUFFICIENT_EVIDENCE` instead of a score |
| Coverage loss > 40% (too much `NOT_VERIFIED`) | report `INSUFFICIENT_EVIDENCE` instead of a score |
| Authentication, authorization or secrets could not be assessed | report `INSUFFICIENT_EVIDENCE` |

### Step 4 — Coverage statement

Always publish alongside the score:

```text
Security Score: 72/100
Coverage: 81% of applicable controls verified (19% NOT_VERIFIED — see Scope & Limitations)
```

A high score with low coverage is meaningless and must be labeled as such.

### Step 5 — Explain the score

List the three to five factors that moved it most, e.g.:

```text
Main factors:
 -25  SEC-0003 missing server-side authorization on /api/invoices (CRITICAL)
 -10  SEC-0007 no rate limiting on login (HIGH)
 -10  SEC-0011 secrets in .env committed to git (HIGH, rotation pending)
  cap 40 applied (open CRITICAL)
```

## 2. Production readiness

Exactly one verdict, derived from evidence — never from the score alone.

### `READY_FOR_PRODUCTION`

All of:
- no open CRITICAL, no open HIGH (or every HIGH explicitly `ACCEPTED_RISK` by the user with a
  recorded rationale);
- no active exposed secret;
- authentication and authorization verified on every privileged path;
- `../references/CHECKLIST_PRODUCTION.md` fully satisfied or its gaps explicitly accepted;
- coverage ≥ 80% of applicable controls;
- backups configured **and** a restore evidence statement exists.

### `READY_WITH_RESTRICTIONS`

No open CRITICAL, but material risks remain (open HIGH/MEDIUM, pending external actions, missing
monitoring or unvalidated restore). State the restrictions concretely: what must be watched, what
must not be enabled yet, and the deadline for each item.

### `NOT_READY_FOR_PRODUCTION`

Any of: open CRITICAL; active exposed production secret; authentication/authorization bypass;
injection with data impact; unauthenticated access to sensitive data; publicly exposed database or
admin interface; debug mode on in the production configuration.

### `INSUFFICIENT_EVIDENCE`

Access, tooling or authorization were too limited to judge (coverage < 60%, no applicable controls,
or auth/authorization/secrets could not be assessed). List exactly what access is needed to complete
the assessment. Do not compute a score from a zero-control denominator or present missing evidence
as a clean result.

## 3. Residual risk

After remediation, restate the risk that remains:

```text
Residual risk: MEDIUM
 - SEC-0011 secret rotation pending (EXTERNAL_ACTION_REQUIRED, owner: user)
 - SEC-0019 no alerting on repeated auth failures (OPEN, P2)
 - Coverage: production infrastructure not accessible (NOT_VERIFIED)
```

## 4. CI gate result

In `CI_GATE` mode the score is secondary; the gate is binary. See `../modules/ci-cd.md`
§Blocking policy. Emit:

```json
{
  "result": "PASS",
  "score": 84,
  "critical": 0,
  "high": 0,
  "medium": 3,
  "low": 6,
  "regressions": 0,
  "secrets": 0,
  "coverage": 0.86,
  "readiness": "READY_WITH_RESTRICTIONS"
}
```
