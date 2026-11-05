# Production Readiness — <project name>

<!--
Template for security/PRODUCTION_READINESS.md.
Criteria: ../references/CHECKLIST_PRODUCTION.md. Verdict rules: ../core/SCORING.md §2.
The verdict follows the evidence, never the score alone and never the deadline.
-->

Date: <YYYY-MM-DD> · Commit: <sha> · Audit mode: <mode> ·
Security score: <XX>/100 · Coverage: <XX>%

```text
Production Readiness: <READY_FOR_PRODUCTION | READY_WITH_RESTRICTIONS |
                       NOT_READY_FOR_PRODUCTION | INSUFFICIENT_EVIDENCE>
```

---

## 1. Basis for the verdict

<Two to five sentences: what was verified, what blocks or restricts, what remains unknown.>

## 2. Blockers

| # | ID | Blocker | Why it blocks | Required to clear |
| --- | --- | --- | --- | --- |

*(Empty for `READY_FOR_PRODUCTION`. Any single row forces `NOT_READY_FOR_PRODUCTION`.)*

## 3. Restrictions *(for `READY_WITH_RESTRICTIONS`)*

| # | Restriction | Risk if ignored | Owner | Due |
| --- | --- | --- | --- | --- |
| 1 | <e.g. do not enable public signup until SEC-0007 rate limiting ships> | | | |
| 2 | <e.g. run a restore drill before onboarding customer data> | | | |

## 4. Checklist result

| Section | Result | Notes |
| --- | --- | --- |
| Blockers (none present) | | |
| Application controls | | |
| Data | | |
| Secrets and configuration | | |
| Infrastructure | | |
| Supply chain and delivery | | |
| Operations | | |
| Evidence and process | | |

Full detail: `../references/CHECKLIST_PRODUCTION.md` walked item by item during this audit.

## 5. Evidence coverage

| | |
| --- | --- |
| Applicable controls | <n> |
| Verified | <n> (<XX>%) |
| Not verified | <n> — listed below |

| Not verified | Why | What would settle it |
| --- | --- | --- |

If coverage is below 60%, or authentication, authorization or secrets could not be assessed, the
verdict is `INSUFFICIENT_EVIDENCE` regardless of what was found.

## 6. Recoverability statement

| | |
| --- | --- |
| Backups configured | <yes/no — mechanism> |
| Offsite / immutable copy | <yes/no> |
| Encryption | <yes/no> |
| Failure alerting | <yes/no> |
| **Last successful restore test** | <date / NEVER> |
| Measured RTO / target RTO | <x / y> |
| Stated RPO / achievable RPO | <x / y> |
| `BACKUP_STATUS` | `VALIDATED` \| `NOT_VALIDATED` |

## 7. Residual risk after remediation

```text
Residual risk: <LOW | MEDIUM | HIGH>
 - <ID> <what remains, why, who owns it>
 - <ID> <…>
```

## 8. Conditions for re-assessment

Re-run `security-auditor VERIFY` when: the blockers above are addressed · external actions are
confirmed · the restore drill is completed · before the release · after any change to
authentication, authorization, payment or infrastructure code.

## 9. Sign-off

| Role | Name | Date | Note |
| --- | --- | --- | --- |
| Prepared by | security-auditor v<version> | <date> | Automated audit; scope in `SECURITY_AUDIT.md` §1 |
| Reviewed by | | | |
| Accepted by | | | Accepting the residual risk above |
