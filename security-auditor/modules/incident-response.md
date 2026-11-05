# MODULE — INCIDENT RESPONSE READINESS

Scope: whether the project can detect, contain, investigate, recover from and communicate about a
security incident. Readiness is a control; assess it like any other.

Related: `monitoring.md`, `logging.md`, `backup.md`, `secrets.md`.
Standards: NIST SP 800-61 (phases), NIST CSF Respond/Recover, CISA incident guidance.

---

## 1. Readiness assessment

Answer each with evidence, `NOT_IMPLEMENTED`, or `NOT_VERIFIED`:

| Question | Evidence to look for |
| --- | --- |
| Is there a written incident procedure? | A document, runbook or `security/INCIDENT_RESPONSE.md` |
| Who is responsible, and how are they reached out of hours? | On-call rotation, contact list |
| How is an incident declared and by whom? | Severity definitions, declaration criteria |
| Can you tell what happened? | Log coverage and retention (`logging.md`) |
| Can you contain quickly? | Ability to revoke sessions, rotate secrets, disable accounts, block IPs, take a service offline, roll back a deploy |
| Can you recover? | Tested restore (`backup.md`), redeploy from IaC, known-good image |
| Do you know what data would be affected? | Data classification from the audit |
| Are there notification obligations? | LGPD/GDPR/contractual timelines, regulator and customer contacts |
| Is there a communication plan? | Status page, customer template, internal comms |
| Is there a post-incident process? | Blameless post-mortem, action tracking |
| Has any of it been rehearsed? | Tabletop exercise date |

Missing IR readiness for a system holding `SENSITIVE`/`CRITICAL` data is at least MEDIUM, and HIGH
when combined with no monitoring or no validated backups.

## 2. Capabilities to verify concretely

- **Session revocation**: can you invalidate all sessions for one user, and for everyone?
- **Secret rotation**: is every credential rotatable, and is the procedure documented per provider?
- **Account lockdown**: can you disable a compromised account and its API keys immediately?
- **Deploy rollback**: can you deploy the previous known-good version in minutes?
- **Traffic control**: can you block an IP/ASN, enable stricter WAF rules, or turn on maintenance
  mode?
- **Forensic capture**: can you snapshot a compromised host/container before rebuilding?
- **Dependency response**: can you find out within a day whether you use a newly announced
  vulnerable package version (SBOM/lockfile search)?

## 3. Scenario runbooks the project should have

Leaked secret · compromised user account · compromised admin account · database breach or data
exposure · ransomware or destructive attack · supply-chain compromise (malicious dependency or
compromised CI) · compromised server or container · DDoS · insider misuse · third-party provider
breach · vulnerability disclosure from an external researcher.

When absent, create `security/INCIDENT_RESPONSE.md` from
`../templates/INCIDENT_READINESS.md`, with defensive, non-destructive steps and clear
"stop and involve a human" points.

## 4. Vulnerability disclosure

For internet-facing products, recommend a way for researchers to report:
`/.well-known/security.txt` with a contact and policy URL, a `SECURITY.md` in the repository, and a
defined response SLA. Absence is LOW on its own — do not overstate it.

## 5. Operating in `INCIDENT_REVIEW` mode

If the audit is running during a suspected incident:

1. **Preserve first.** Do not delete logs, containers, images, branches or files. Do not "clean up".
2. Capture volatile evidence only if the user authorizes it and it can be done read-only.
3. Establish a timeline: recent commits, deploys, dependency changes, CI runs, new accounts, new
   permissions, configuration changes, new outbound destinations, new cron/systemd units, new
   webhooks, unexpected files in web roots.
4. Search for exposed or used credentials; recommend rotation, do not execute it.
5. Identify persistence: added SSH keys, altered CI workflows, new admin users, scheduled jobs,
   modified dependencies, backdoored middleware.
6. Assess data access scope from logs, and record what cannot be determined.
7. Recommend containment steps for a human to execute; never execute destructive containment
   yourself (`../core/SAFETY.md` §3).
8. Document everything with timestamps in `security/INCIDENT_RESPONSE.md`, appended, never
   overwritten.

Notify the user immediately and plainly if you find evidence suggesting an active compromise.

## 6. After the incident

Root cause, timeline, affected data, actions taken, and preventive changes — each preventive change
becomes a finding with an owner and a deadline so it is tracked like any other. Update the baseline
and add regression tests for the exploited weakness.
