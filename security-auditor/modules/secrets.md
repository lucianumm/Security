# MODULE — SECRETS AND CREDENTIALS

Scope: discovery of hardcoded and leaked credentials, environment configuration, secret storage,
and the compromise/rotation lifecycle.

**Never print a secret in full.** Redaction format: `STRIPE_SECRET_KEY=sk_live_****[REDACTED]`.

Related: `../core/SAFETY.md` §5, `supply-chain.md`, `ci-cd.md`, `cloud.md`.
Standards: ASVS v5.0.0 V6 (Authentication), V11 (Cryptography) and V14 (Data Protection), OWASP Top 10:2025 A02/A07, CWE-798, CWE-259, CWE-522, CWE-312, CWE-532.

---

## 1. Where to look

```bash
# Candidate paths only. Never print matching source lines or secret values.
rg -li --hidden --glob '!**/.git/**' --glob '!**/node_modules/**' --glob '!**/dist/**' \
  --glob '!**/build/**' --glob '!**/vendor/**' --glob '!**/.next/**' \
  "(api[_-]?key|secret|token|passwd|password|pwd|credential|private[_-]?key|access[_-]?key)['\"]? ?[:=]" . | head -60

# high-signal provider patterns
rg -li --hidden --glob '!**/.git/**' --glob '!**/node_modules/**' --glob '!**/dist/**' \
  --glob '!**/build/**' --glob '!**/vendor/**' \
  "sk_live_|sk_test_|rk_live_|pk_live_|AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|ya29\.|ghp_|gho_|ghu_|ghs_|github_pat_|glpat-|xox[baprs]-|SG\.[A-Za-z0-9_-]{22}|EAACEdEose0cBA|-----BEGIN [A-Z ]*PRIVATE KEY-----|eyJhbGciOi" . | head -40

# files that should never be tracked
git ls-files | grep -iE "^\.env|\.env\.|\.pem$|\.key$|\.p12$|\.pfx$|\.jks$|id_rsa|\.kdbx$|credentials|serviceaccount.*\.json|\.npmrc$|\.pypirc$|\.netrc$|terraform\.tfstate"

# Scanner output can contain secrets even when it is JSON. Set PRIVATE_SCAN_DIR to a new local
# directory outside the project with owner-only permissions; inspect it without echoing raw fields,
# then remove it after triage.
umask 077
PRIVATE_SCAN_DIR=$(mktemp -d)
chmod 700 "$PRIVATE_SCAN_DIR"
gitleaks detect --source . --log-opts=--all --no-banner --redact \
  --report-format json --report-path "$PRIVATE_SCAN_DIR/gitleaks.json" > "$PRIVATE_SCAN_DIR/gitleaks.log" 2>&1
trufflehog filesystem . --no-verification --no-update --json \
  > "$PRIVATE_SCAN_DIR/trufflehog.jsonl" 2>&1
```

Also inspect: config files, `docker-compose*.yml`, Kubernetes manifests and ConfigMaps, CI workflow
files, Terraform variables and state, test fixtures, seed scripts, notebooks, documentation and
READMEs, log files committed by accident, build output, mobile app bundles, and browser-visible
files (`frontend.md` §1).

Git history may be inspected read-only during an audit. Rewriting it is a separate destructive
operation and requires the user's explicit request for that exact change (`../core/SAFETY.md` §3).

```bash
git log --all --full-history --format='%H' -- .env '*.pem' '*credentials*' 2>/dev/null | head
git log --all --format='%H' -S 'sk_live_' -- . 2>/dev/null | head -20
# Use the private-output wrapper above; never print scanner reports or upload them as artifacts.
gitleaks detect --source . --log-opts=--all --no-banner --redact \
  --report-format json --report-path "$PRIVATE_SCAN_DIR/gitleaks-history.json" \
  > "$PRIVATE_SCAN_DIR/gitleaks-history.log" 2>&1
```

## 2. Triage each hit

For every candidate answer:

1. **Is it real?** Placeholder, example, test fixture, public key, or a live credential?
2. **What does it unlock?** Provider, scope, environment, blast radius.
3. **Where is it exposed?** Working tree only, committed, pushed to a public remote, in a published
   package, in a client bundle, in a container image layer, in CI logs?
4. **Is it active?** Do not test it by using it — reason from context and ask the user to check the
   provider's dashboard.

Severity: active production credential in a public repository or client bundle = CRITICAL;
active credential committed to a private repository = HIGH–CRITICAL by blast radius;
test/sandbox credential = MEDIUM (still requires rotation); placeholder = INFO/no finding.

## 3. Compromise lifecycle

Deleting the string does **not** resolve the finding. Required, in order:

1. Remove the value from code/config; load it from the environment or a secret manager.
2. Add the pattern to `.gitignore`; ensure `.env.example` has placeholders only.
3. Mark the finding `SECRET_ROTATION_REQUIRED` and provide provider-specific revocation steps.
4. If it was committed and pushed, treat it as **already compromised** regardless of repository
   visibility; explain that rotation/revocation is primary. History removal (BFG/`filter-repo` plus
   a coordinated force-with-lease rewrite) requires the user's explicit request for that exact
   operation; without it, propose the steps but do not execute them (`../core/SAFETY.md` §3).
5. Status stays `EXTERNAL_ACTION_REQUIRED` until the user confirms rotation with evidence
   (new credential in use, old credential revoked). Only then `FIXED`.
6. Recommend reviewing provider audit logs for use of the exposed credential.

## 4. Environment configuration

- `.env`, `.env.local`, `.env.production` and equivalents are git-ignored and absent from
  `git ls-files`.
- `.env.example` documents every required variable with **placeholder** values and no real data.
- No fallback defaults for secrets in code:
  `process.env.JWT_SECRET || 'dev-secret'` is a finding (HIGH — it silently ships an insecure
  default). The application should fail fast at startup when a required secret is missing.
- Environment separation: distinct credentials for dev, staging and production; a developer laptop
  must not hold production secrets.
- Secrets are not baked into container images (`docker.md` §Build secrets) or into build-time
  client variables (`frontend.md` §1).
- `.dockerignore` excludes `.env`, `.git`, keys and local state.

## 5. Storage and distribution

Preferred: a managed secret store (AWS Secrets Manager/Parameter Store, GCP Secret Manager, Azure
Key Vault, Vault, Doppler, 1Password/Infisical) or the platform's encrypted variables
(GitHub/GitLab secrets, Vercel/Netlify/Cloudflare env vars, Kubernetes Secrets with encryption at
rest and RBAC).

Verify: least-privilege access to each secret, rotation capability and schedule, audit logging of
access, no secret shared over chat/email, no secret in a ticket or a wiki, no long-lived static
cloud keys where short-lived OIDC federation is available (`ci-cd.md` §OIDC).

## 6. Secrets in logs and telemetry

```bash
# Report candidate file paths only; inspect locally without copying matching values into logs.
rg -li "console\.log\(.*(token|password|secret|authorization)|logger\.(info|debug)\(.*(token|password|secret)|print\(.*(password|token)" src app | head -30
```

Also check: error trackers (Sentry scrubbing configured), APM payload capture, HTTP client debug
logging, request/response logging middleware, and CI job output (`ci-cd.md`).

## 7. Prevention controls to recommend/implement

- Pre-commit secret scanning (`gitleaks` hook, `pre-commit`, `husky`).
- Secret scanning in CI on every PR and on push (`ci-cd.md` §Security gate).
- Provider-side push protection (GitHub Secret Scanning + push protection).
- A documented rotation procedure and owner per credential.
- Onboarding/offboarding: revoke access when a person leaves.

## 8. Regression tests / CI checks

CI fails when a secret pattern is detected in the diff · application fails to start when a required
secret is missing instead of using a default · built client bundle contains no `sk_`, `-----BEGIN`,
or `AKIA` pattern (grep step) · `.env` is not tracked (`git ls-files` assertion).
