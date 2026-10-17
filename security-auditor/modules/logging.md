# MODULE — LOGGING AND AUDIT TRAIL

Logging, monitoring and alerting are three different controls. This module covers logging and the
audit trail; `monitoring.md` covers detection and alerting.

Related: `monitoring.md`, `incident-response.md`, `secrets.md`, `backend.md` §Error handling.
Standards: ASVS v5.0.0 V16 (Security Logging and Error Handling), OWASP Top 10:2025 A09, CWE-778, CWE-532, CWE-117, CWE-223.

---

## 1. Discovery

```bash
grep -rniE "winston|pino|bunyan|morgan|logging\.|logger|log4j|logback|slf4j|serilog|monolog|Rails\.logger|structlog" . -l | head
grep -rn "console\.log\|print(" src app 2>/dev/null | wc -l
ls -d logs var/log storage/logs 2>/dev/null
```

Determine: is there a structured logger, or ad-hoc printing? Where do logs go — stdout, files, a
central platform? Are they retained, rotated and searchable?

## 2. Events that must be logged

| Event | Fields |
| --- | --- |
| Login success / failure | user id or attempted identifier, IP, user agent, timestamp, result |
| Logout | user id, session id (hashed) |
| MFA enroll / challenge / failure / removal | user id, method, result |
| Password reset requested / completed | user id, IP, token id (not the token) |
| Email / phone change | user id, old→new (masked), confirmation state |
| Privilege or role change | actor, target, old role, new role |
| Permission denied on a privileged action | actor, resource, action |
| Admin actions | actor, action, target, before/after where feasible |
| Account creation / deletion / lock / unlock | actor, target, reason |
| Data export / bulk read | actor, scope, record count |
| Payment, refund, payout, credit change | actor, amount, currency, reference, result |
| Deletion of business records | actor, entity, id |
| API key / token creation and revocation | actor, key id, scopes |
| Webhook received / signature failure | source, event id, result |
| Configuration and feature-flag changes | actor, setting, old→new |
| Security control failures | rate limit triggered, validation rejected at scale, CSP violations |
| Infrastructure access | SSH logins, sudo, container exec (`cloud.md`) |

Every entry: UTC timestamp, event type, actor (id, not just IP), source IP, target resource,
outcome, correlation/request id, and service/version.

## 3. What must never be logged

Passwords (including failed attempts) · session identifiers or full tokens · full `Authorization`
headers · API keys · refresh tokens · private keys · card numbers, CVV, full PAN · full national
identity numbers · health data beyond what is required · complete request/response bodies
containing personal data · secrets in stack traces or URLs.

```bash
grep -rniE "log.*(password|token|secret|authorization|api[_-]?key|cpf|ssn|card)" src app | head -30
```

Where a sensitive value must be referenced, log a stable hash or a masked form
(`user@***.com`, `****1234`, `sha256:ab12…`). Configure redaction in the logger (pino `redact`,
Serilog destructuring policies, structlog processors) **and** in the error tracker (Sentry
`beforeSend`, data-scrubbing rules) and APM.

## 4. Integrity and availability of the trail

- Logs shipped off the host (a compromised host must not control its own evidence).
- Append-only or write-once storage for the audit trail where the data class warrants it.
- Application accounts cannot delete or edit audit records; separate retention policy.
- Rotation configured so disks do not fill (an availability incident and a self-inflicted outage).
- Retention aligned with legal/operational needs (commonly 90 days hot, 1 year cold — record what
  the project actually needs).
- Time synchronization (NTP) so events correlate across systems.
- Access to logs is itself restricted and logged (logs contain personal data).

## 5. Log injection and safe formatting

Untrusted input written into logs must be encoded so it cannot forge entries (CR/LF injection) or
break the parser. Use structured logging (JSON) rather than string concatenation. Beware of log
formatters that evaluate placeholders in user input (the Log4Shell class of bug) — keep logging
libraries patched and message lookup disabled.

## 6. Error handling interface

Application errors: generic message plus a correlation id to the user; full context to the log
(`backend.md` §14). Verify the correlation id is actually usable to find the entry.

## 7. Privacy

Logs are a data store: they fall under the same classification, retention, access-control and
deletion obligations as the database. Account deletion should account for logs
(anonymization or documented retention justification). Do not ship personal data to third-party log
platforms without a processing agreement — flag as a privacy note, not a vulnerability, unless the
data class is sensitive.

## 8. Regression / verification

A failed login produces a log entry with no password field · a log line containing a token pattern
fails a unit test on the redaction configuration · an admin action writes an audit record with
actor and target · the correlation id returned in an error response appears in the log · the audit
table cannot be updated or deleted by the application role (database permission test).
