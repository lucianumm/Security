# Remediation Plan — <project name>

<!--
Template for security/REMEDIATION_PLAN.md.
Ordered by ../core/SEVERITY.md §3. Every item is actionable by a specific person; nothing here
should read as "improve security".
-->

Date: <YYYY-MM-DD> · Findings covered: <n> · Mode of the audit: <mode>

---

## 1. Immediate — P0 (start now)

### 1. SEC-0001 — <title>

| | |
| --- | --- |
| Severity / Confidence | CRITICAL / HIGH |
| Layer | BACKEND |
| Fix type | REVIEW_RECOMMENDED |
| Owner | <person or team> |
| Effort | <S/M/L or hours> |
| Depends on | <nothing / SEC-XXXX> |
| Blocks production | Yes |

**Action**

1. <concrete step, with the file to change>
2. <concrete step>
3. <concrete step>

**Verification**

<the test to write or run, the request to make, the scanner to re-run — what will prove it>

**Risk of the change**

<what could break; how to roll back>

---

## 2. Urgent — P1 (before production / this sprint)

| Order | ID | Title | Fix type | Owner | Effort | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | SEC-00xx | | | | | |

## 3. Scheduled — P2

| Order | ID | Title | Fix type | Owner | Target | Verification |
| --- | --- | --- | --- | --- | --- | --- |

## 4. Hardening backlog — P3

| ID | Title | Benefit | Effort |
| --- | --- | --- | --- |

---

## 5. External actions required

Actions this audit cannot perform. Each needs a named owner and a completion date; findings stay
`EXTERNAL_ACTION_REQUIRED` until the user confirms with evidence.

| ID | Action | System | Steps | Owner | Due | Confirmed |
| --- | --- | --- | --- | --- | --- | --- |
| SEC-0011 | Rotate the exposed API key | <provider> | 1. Create a new restricted key 2. Deploy it 3. Revoke the old key 4. Review provider audit logs for use of the old key | <user> | <date> | ☐ |

## 6. Architectural changes proposed

| ID | Change | Problem it solves | Impact | Recommendation |
| --- | --- | --- | --- | --- |

## 7. Suggested sequence

```text
Week 1  SEC-0001, SEC-0004 (authorization), SEC-0011 (secret rotation)
Week 2  SEC-0007 (rate limiting + MFA for admins), regression tests, CI security gate
Week 3  SEC-0012..0016 (headers, limits, logging), dependency updates
Later   P3 hardening, restore drill, monitoring coverage
```

Group changes that touch the same code to reduce regression risk, but never delay a P0 to batch it
with lower-priority work.

## 8. Definition of done for this plan

- [ ] Every P0 and P1 finding is `FIXED` with post-change verification, or explicitly
      `ACCEPTED_RISK` by the user
- [ ] Regression tests exist and pass for each fixed CRITICAL/HIGH finding
- [ ] lint / typecheck / tests / build all pass
- [ ] Scanners re-run and the results interpreted
- [ ] `security/SECURITY_BASELINE.md` and `.security/*.json` updated
- [ ] External actions confirmed by the owner
- [ ] A `VERIFY` run has been executed and its report attached
