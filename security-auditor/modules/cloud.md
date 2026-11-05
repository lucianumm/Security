# MODULE — CLOUD, IaC, SERVERLESS, NETWORK AND SERVERS

Scope: cloud accounts and IAM, infrastructure as code, serverless and edge platforms, network
exposure, VPS/OS hardening, DNS and email domain security.

Related: `docker.md`, `kubernetes.md`, `nginx.md`, `secrets.md`, `uploads.md` §Object storage.
Standards: CIS Benchmarks (AWS/GCP/Azure), NIST 800-53 selected controls, CISA Secure by Default.

Much of this layer lives outside the repository. Audit what the repository proves (IaC, config,
deploy scripts), ask the user for the rest, and record `NOT_VERIFIED` for anything you cannot see —
never assume a control exists because it is a provider default.

---

## 1. Identity and access management

- No long-lived static access keys where short-lived credentials or workload identity are possible
  (OIDC federation for CI, IRSA/Workload Identity for workloads, instance/managed identities).
- No wildcard policies: `Action: "*"`, `Resource: "*"`, `Effect: Allow` on a broad principal;
  `roles/owner`, `roles/editor`, `Contributor` at subscription scope for an application.
- Root/owner account: MFA enabled, no access keys, not used for daily work, alerting on use.
- MFA for every human account; SSO with a central IdP; offboarding procedure.
- Separate accounts/projects/subscriptions per environment; production isolated.
- Service accounts scoped per service; keys rotated; unused credentials removed.
- Permission boundaries / SCPs / deny policies for the highest-risk actions where available.
- Cross-account trust relationships reviewed (`sts:AssumeRole` with a weak `ExternalId` or a
  wildcard principal is CRITICAL).

## 2. Infrastructure as Code

```bash
ls -d terraform infra iac pulumi cdk .aws-sam serverless.yml template.y*ml 2>/dev/null
grep -rniE "0\.0\.0\.0/0|::/0|publicly_accessible|acl *= *\"public|allUsers|allAuthenticatedUsers|\"\\*\"" . --include=*.tf --include=*.y*ml --include=*.json | head -40
git ls-files | grep -E "terraform\.tfstate|\.tfvars$"     # state and tfvars often contain secrets
```

Scan:

```bash
checkov -d . -o json
tfsec . --format json
trivy config .
```

Look for: security groups open to `0.0.0.0/0` on management or database ports; public storage
buckets; unencrypted volumes, databases, queues and snapshots; disabled logging (CloudTrail,
flow logs, audit logs); secrets in variables, state or defaults; overly broad IAM; public IPs on
internal resources; missing deletion protection and backups on stateful resources; drift between
IaC and reality (ask the user to run `plan` — never `apply`).

`terraform.tfstate` committed to the repository is a finding (it commonly contains plaintext
secrets) — treat per `secrets.md`.

## 3. Network exposure

Enumerate what is reachable from the internet and why:

| Port/service | Expectation |
| --- | --- |
| 22 SSH | Restricted to a VPN/bastion/IP allowlist; key-only auth |
| 3306 / 5432 / 27017 / 6379 / 9200 / 8123 | Never public |
| 2375/2376 Docker API, 10250 kubelet | Never public |
| Admin panels, queue dashboards, metrics, tracing UIs | Authenticated and restricted |
| 80 | Redirect to 443 only |
| 443 | The application, behind TLS |

Verification without scanning third parties: read security groups/firewall rules, `docker ps`
port bindings, `ss -tulpn` on a server the user controls, provider console output the user shares.
Do not port-scan hosts you were not authorized to test (`../core/SAFETY.md` §6).

Also check: default VPC/public subnets used for private workloads, missing egress restrictions
(exfiltration and SSRF pivot), peering/VPN configuration, and management interfaces bound to
`0.0.0.0`.

## 4. Serverless and edge platforms

(Vercel, Netlify, Cloudflare Workers/Pages, AWS Lambda, Cloud Run, Azure Functions, Deno Deploy,
Supabase Edge Functions.)

- Environment variables: which are exposed to the client build (`frontend.md` §1), which are
  server-only, and are preview/branch deployments using production secrets?
- Preview/branch deployments: are they publicly reachable, indexed, and connected to production
  data? A public preview with production credentials is HIGH–CRITICAL.
- Function execution role scoped to what the function needs.
- Timeouts, memory and concurrency limits set (cost and DoS containment).
- Cold-start secrets fetched from a secret manager, not embedded.
- Public function URLs authenticated; API Gateway authorizers verified.
- Edge middleware performing authorization: verify it cannot be bypassed by calling the origin
  directly, and that it runs for every matching path (config-driven matchers are easy to get wrong).
- Platform-level protections: DDoS, bot management, rate limiting, WAF rules — record what is
  actually enabled, not what the plan offers.

## 5. CDN, WAF and origin protection

- WAF present? Which ruleset, in blocking or detection mode, with what exceptions?
- Rate limiting and bot protection configured for login and expensive endpoints.
- Cache rules: authenticated responses must not be cached; `Cache-Control: private, no-store` on
  sensitive routes; cache key includes anything that varies the response (cache poisoning and cache
  deception risks — test a `/account.css`-style suffix if authorized).
- **Origin protection**: can the origin be reached directly, bypassing the CDN/WAF? Verify origin
  firewall rules allow only CDN IP ranges, or authenticated origin pulls (Cloudflare Authenticated
  Origin Pulls / Tunnel). A discoverable origin IP negates the WAF — MEDIUM–HIGH.
- A WAF is never a substitute for fixing the application (`../core/EVIDENCE_RULES.md` §8).

## 6. VPS / server hardening

When the user gives access or configuration to review (read-only):

OS supported and patched; unattended security updates configured · no unnecessary services listening ·
SSH: key-only (`PasswordAuthentication no`), no root login (`PermitRootLogin no`), non-default port
optional (not a control), `AllowUsers`/`AllowGroups`, idle timeout, fail2ban or equivalent ·
firewall default-deny inbound with explicit allows · separate non-root service users with minimal
privileges · sudo restricted and logged · file permissions on config, keys and web roots (no
world-writable, no `777`) · cron and systemd units reviewed for untrusted scripts and injected
persistence · time synchronization enabled (log correlation) · logs shipped off-host and rotated ·
disk encryption where the data class warrants it · backup agent configured (`backup.md`) ·
monitoring agent (`monitoring.md`).

## 7. DNS

- DNSSEC enabled where the registrar and zone support it.
- CAA records restricting which CAs may issue certificates.
- Registrar account: MFA, registrar lock, transfer protection, and an owner who is not a single
  departed employee.
- **Dangling DNS / subdomain takeover**: enumerate CNAMEs pointing at deprovisioned services
  (`*.s3`, `*.azurewebsites.net`, `*.herokuapp.com`, `*.github.io`, old SaaS vendors). Any record
  pointing at an unclaimed resource is HIGH.
- Old staging/dev subdomains exposing non-production systems to the internet.
- Wildcard records and their implications.

## 8. Email domain security

- SPF: a single record, no `+all`, sensible includes, within the DNS-lookup limit.
- DKIM: signing enabled with a ≥ 2048-bit key, per-sender selectors.
- DMARC: published, moving from `p=none` to `p=quarantine`/`p=reject`, with `rua` reporting.
- MTA-STS/TLS-RPT and BIMI are optional hardening.
- Transactional email provider credentials scoped and rotated (`secrets.md`).

## 9. Cloud logging and detection

CloudTrail / Cloud Audit Logs / Azure Activity Log enabled in all regions, immutable and
centralized · VPC/NSG flow logs where warranted · GuardDuty / Security Command Center / Defender
enabled or a documented decision not to · alerting on root usage, IAM policy changes, key creation,
security group changes, and unusual data egress · log retention meeting the organization's needs.

## 10. Regression / verification

IaC scan gate in CI (`ci-cd.md`) · a rule opening `0.0.0.0/0` on port 22/5432 fails the policy test ·
storage bucket public-access assertion · deployment fails if a required secret is absent ·
origin reachable only via the CDN (verified by the user) · `terraform plan` shows no drift.
