# MODULE — BACKUP AND RECOVERABILITY

Rule of this module: **a backup is not validated until a restore has been tested.** Configuration
alone yields `BACKUP_STATUS = NOT_VALIDATED`, never `IMPLEMENTED`.

Related: `database.md`, `cloud.md`, `incident-response.md`.
Standards: NIST CSF Recover, ASVS v5.0.0 V14 (Data Protection), ISO 27001 A.8.13 (reference only).

---

## 1. Scope of what must be recoverable

| Asset | Typical mechanism |
| --- | --- |
| Primary database | Managed automated backups + PITR, or `pg_dump`/`mysqldump` jobs |
| Uploaded files / object storage | Versioning + cross-region replication or scheduled copies |
| Cache/queues | Usually rebuildable — confirm nothing durable lives only there |
| Configuration and secrets | Secret manager backup / documented re-provisioning |
| Infrastructure definition | IaC in Git (this is your infrastructure backup) |
| Code | Git remote + a second copy for critical projects |
| CI/CD configuration and runners | IaC or documented setup |
| DNS zone | Exported zone file |
| Logs and audit trail | Retention policy, separate from the primary system |

Anything that exists only inside a single running server is a finding.

## 2. Backup controls

| Control | Requirement |
| --- | --- |
| Coverage | Every asset above has a defined owner and mechanism, or a documented "not needed" |
| Frequency | Matches the tolerable data loss (RPO). State the RPO explicitly |
| Retention | Multiple restore points, not just the last one (ransomware and slow corruption) |
| Offsite | A copy in a different account/region/provider — a backup in the same account an attacker compromises is not a backup |
| Immutability | Object lock / write-once / delayed deletion so a compromised credential cannot erase history |
| Encryption | At rest and in transit; key stored separately from the backup |
| Access control | Least privilege; the application's runtime credential must not be able to delete backups |
| Monitoring | Backup success/failure alerting (`monitoring.md`) — silent failure is the norm without it |
| Integrity | Checksums, and periodic verification that the file is readable |
| Documentation | Where backups live, how to restore, who is authorized |

## 3. Restore testing

Ask for, and record, evidence of the last successful restore:

- date of the last restore test;
- what was restored (full database, single table, a file, the whole environment);
- how long it took (measured RTO vs target RTO);
- whether the restored system was verified as functional and consistent;
- who performed it and whether the runbook was followed and updated.

If none exists: `BACKUP_STATUS = NOT_VALIDATED`, severity MEDIUM normally, HIGH when the system
holds `SENSITIVE`/`CRITICAL` data or has no other redundancy. Recommend a scheduled restore drill
(quarterly is a reasonable default) into an isolated environment.

Never perform a restore yourself over a live system.

## 4. RPO / RTO

State both, agreed with the user:

```text
RPO (max acceptable data loss): 1 hour   → hourly PITR or continuous WAL archiving
RTO (max acceptable downtime):  4 hours  → documented runbook, tested restore, pre-provisioned target
```

A backup schedule that cannot meet the stated RPO is a finding.

## 5. Ransomware and destructive-attack resilience

- Backups unreachable from the production credentials that could be stolen.
- Delete protection / MFA-delete / object lock on backup storage.
- At least one copy that is offline or logically isolated.
- Ability to restore to a **point before** an intrusion — requires enough retention and the ability
  to determine when the intrusion started (`logging.md`).

## 6. Data lifecycle interactions

Backups extend the life of deleted personal data — document the retention window in the privacy
statement and account for it in deletion requests. Backups of production data used to seed
development environments must be anonymized (`database.md` §7).

## 7. Regression / verification

Backup job alerting verified by simulating a failure · a restore drill executed in an isolated
environment with the result recorded in `security/PRODUCTION_READINESS.md` · the application
database role cannot delete backup objects (permission test) · backup encryption confirmed ·
retention policy asserted in IaC.
