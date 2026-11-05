# MODULE — MONITORING, DETECTION AND ALERTING

`LOGGING` ≠ `MONITORING` ≠ `ALERTING`. Recording an event, watching for a pattern, and waking
someone up are three separate controls; assess each one separately and never let one imply another.

Related: `logging.md`, `incident-response.md`, `cloud.md` §Cloud logging.
Standards: ASVS v5.0.0 V16 (Security Logging and Error Handling), OWASP Top 10:2025 A09, NIST CSF Detect.

---

## 1. Discovery

```bash
grep -rniE "sentry|datadog|newrelic|prometheus|grafana|opentelemetry|cloudwatch|stackdriver|appinsights|elastic|loki|pagerduty|opsgenie|statuspage" . -l | head
ls -d monitoring grafana prometheus .well-known 2>/dev/null
```

Record: what is collected (logs, metrics, traces, errors), where it goes, who can see it, what is
alerted on, and who receives the alert.

## 2. Detection coverage

Security signals that should raise an alert:

| Signal | Threshold example | Why |
| --- | --- | --- |
| Failed logins for one account | > 10 in 5 min | Brute force |
| Failed logins across many accounts from one source | > 50 in 5 min | Credential stuffing |
| Successful login from a new country/ASN for privileged users | any | Account takeover |
| New admin login, or privilege elevation | any | Insider or takeover |
| MFA disabled or reset | any | Takeover precursor |
| Password reset spike | anomalous | Enumeration/abuse |
| 401/403 spike | anomalous | Authorization probing |
| 5xx spike | > baseline | Exploitation or outage |
| Rate-limit triggers spike | anomalous | Automated abuse |
| Unusual data export / bulk read volume | > baseline per user | Exfiltration |
| Payment failures / refund spikes | anomalous | Fraud, card testing |
| New outbound destination from the server | any | C2 / exfiltration |
| WAF/CDN blocked-request spike | anomalous | Targeted attack |
| Secret scanner or dependency scanner critical finding | any | Supply chain |
| Cloud IAM change, key creation, security-group change | any | Persistence |
| Certificate expiring | < 14 days | Outage prevention |
| Backup job failure | any | Recoverability |
| Disk/CPU/memory saturation | thresholds | Availability |
| Queue depth / job failure rate | thresholds | Silent data loss |

## 3. Alerting quality

- Every alert has: a named owner, a delivery channel that reaches a human out of hours where
  warranted, a severity, and a runbook link (`incident-response.md`).
- Alerts are actionable — noisy alerts get muted, which is equivalent to having none. Review the
  current noise level with the user.
- Escalation path defined; on-call rotation if the service warrants it.
- Alert delivery tested (a channel nobody reads is `NOT_IMPLEMENTED` in practice).
- Health checks and synthetic monitoring for the login path and critical business flows.

## 4. Observability hygiene

- Dashboards and metrics endpoints are authenticated and not publicly exposed (`/metrics`,
  Grafana, Prometheus, Kibana, Jaeger, queue dashboards) — public exposure is at least MEDIUM and
  often leaks tenant data or internal topology.
- Error trackers scrub PII and secrets (`logging.md` §3) and their access is restricted.
- Traces do not carry tokens or personal data in span attributes.
- Third-party observability vendors: data processing agreement, region, retention.
- Cost/quota limits so log volume cannot become an outage or a bill incident.

## 5. Verification with the user

Much of this is outside the repository. Ask specifically, and record the answers as user-reported
(`NOT_VERIFIED` unless evidence is shown):

1. If someone brute-forces an account right now, who finds out and how?
2. If a server starts sending data to an unknown host, would anything notice?
3. When did an alert last fire, and what happened?
4. Who is on call, and what is the response-time expectation?
5. Are cloud audit logs enabled in every region and retained?

## 6. Regression / verification

Trigger a benign detectable event on a non-production system (e.g. 20 failed logins) and confirm the
alert fires end-to-end · assert the metrics endpoint requires authentication · assert the error
tracker's scrubbing configuration in a unit test · confirm the backup-failure alert path by
simulating a failure in staging.
