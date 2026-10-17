# Incident Response & Readiness — <project name>

<!--
Template for security/INCIDENT_RESPONSE.md. Create it when the project has no incident procedure
(../modules/incident-response.md). Keep every step defensive and non-destructive, and mark clearly
where a human decision is required.
-->

Version: <n> · Last updated: <YYYY-MM-DD> · Owner: <name/role>

---

## 1. Readiness assessment

| Capability | State | Evidence / gap |
| --- | --- | --- |
| Written procedure | | |
| Named responsible person + out-of-hours contact | | |
| Log coverage and retention | | |
| Session revocation | | |
| Secret rotation procedure | | |
| Account disable / API key revocation | | |
| Deploy rollback | | |
| Traffic blocking (IP/WAF/maintenance mode) | | |
| Forensic snapshot capability | | |
| Validated backups / restore | | |
| Data classification (to scope a breach) | | |
| Notification obligations understood | | |
| Communication plan | | |
| Post-incident process | | |
| Last rehearsal | | |

## 2. Contacts

| Role | Name | Channel | Hours |
| --- | --- | --- | --- |
| Incident lead | | | |
| Technical responder | | | |
| Infrastructure / cloud owner | | | |
| Data protection / legal | | | |
| Communications | | | |
| Key providers (hosting, payments, IdP) | | support channel + account id | |

## 3. Severity and declaration

| Level | Definition | Response |
| --- | --- | --- |
| SEV1 | Confirmed compromise, active data loss, or full outage | Immediate; all hands; notify leadership |
| SEV2 | Probable compromise, single-account takeover, sensitive exposure | Same business day |
| SEV3 | Suspicious activity, contained issue, no confirmed impact | Next business day |

Anyone may declare an incident. Over-declaring is cheap; under-declaring is not.

## 4. Universal first steps

1. **Preserve.** Do not delete logs, containers, images, branches or files. Do not "clean up".
2. Start a timestamped log of observations and actions (this file, appended).
3. Assign an incident lead and a single communication channel.
4. Assess: what is confirmed, what is suspected, what is unknown.
5. Contain with the least destructive effective action.
6. Only then eradicate and recover.
7. Post-incident review within a week; every preventive action becomes a tracked finding.

## 5. Scenario runbooks

### 5.1 Leaked secret

1. Identify the credential, its scope and where it was exposed. Do not use it.
2. Create a replacement credential with least privilege; deploy it.
3. Revoke the old credential.
4. Review the provider's audit log for use of the exposed credential and for objects created by it.
5. If it was in Git history, treat it as compromised regardless of repository visibility; decide on
   history rewriting as a team.
6. Record the finding as `SECRET_ROTATION_REQUIRED` → `FIXED` only after revocation is confirmed.

### 5.2 Compromised user account

Revoke sessions and refresh tokens · force a password reset · check and reset MFA enrollment ·
review the account's recent actions, exports, permission changes and API keys · notify the user ·
check for lateral movement from that account.

### 5.3 Compromised administrative account

All of 5.2, plus: review every action taken with the account · check for new admin users, new API
keys, changed webhooks, changed CI configuration, new SSH keys and new cloud IAM grants · rotate
credentials the account could access · consider full credential rotation.

### 5.4 Database breach / data exposure

Determine scope from logs (what data, how many records, which tenants, over what period) ·
stop the access path · preserve evidence · assess notification obligations with legal ·
prepare customer communication · plan credential resets if credentials were exposed.

### 5.5 Ransomware / destructive attack

Isolate affected systems (network, not power, if forensics matter) · confirm backups are intact and
unreachable from the compromised credentials · restore to a point before the intrusion ·
rebuild rather than clean · rotate all credentials · involve law enforcement/legal per policy.

### 5.6 Supply-chain compromise

Identify the affected package/action and the versions in use (lockfiles, SBOM) · pin to a safe
version or remove · rotate every secret the build or runtime could have exposed · rebuild artifacts
from a clean environment · review what the malicious code could reach · audit CI logs.

### 5.7 Compromised server or container

Snapshot before changing anything · look for persistence (cron, systemd units, SSH keys, modified
binaries, unexpected processes and outbound connections) · rebuild from a known-good image rather
than cleaning · rotate every credential present on the host · review lateral access.

### 5.8 DDoS / abuse

Enable provider protections and stricter rate limits · block the offending sources · scale or shed
load · protect the origin (`../modules/cloud.md` §Origin protection) · review costs.

### 5.9 External vulnerability report

Acknowledge quickly · triage against this skill's severity model · reproduce · fix and verify ·
credit the reporter if they wish · publish a fix note where appropriate.

## 6. Communication templates

**Internal declaration**
```text
[SEV<n>] <short description>
Detected: <time, how>   Lead: <name>   Channel: <where>
Confirmed: <facts>      Suspected: <hypotheses>     Unknown: <gaps>
Immediate actions: <list>       Next update: <time>
```

**Customer notice (draft — legal review before sending)**
```text
What happened, when, what data was involved, what we have done, what you should do,
how to contact us. No speculation. No blame. Facts and actions only.
```

## 7. Incident log

| Timestamp (UTC) | Actor | Observation / action | Evidence |
| --- | --- | --- | --- |

## 8. Post-incident

| Item | Detail |
| --- | --- |
| Root cause | |
| Timeline | |
| Data affected | |
| Detection gap | |
| Response gap | |
| Preventive actions (tracked as findings) | |
| Baseline / test updates | |
