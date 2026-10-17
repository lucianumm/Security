# REMEDIATION POLICY

Applies to `AUDIT_AND_FIX` and `HARDEN` only. In every other mode, propose — do not patch.

---

## 1. The loop

```text
DETECT → VALIDATE → CLASSIFY → CAPTURE CONTEXT → PATCH → LINT → TYPECHECK →
TEST → BUILD → SECURITY TEST → RESCAN → VERIFY
```

- **VALIDATE**: confirm the finding is real before touching code (`EVIDENCE_RULES.md` §5).
- **CLASSIFY**: assign the fix type (`SEVERITY.md` §4). Only `SAFE_AUTO_FIX` is applied
  autonomously.
- **CAPTURE CONTEXT**: record the current content of what you are about to change (before/after
  goes into `security/SECURITY_CHANGES.md`). Do not create backup copies of files inside the repo.
- **PATCH**: one logical fix at a time, smallest change that removes the root cause.
- **VERIFY**: post-change evidence, or the status is not `FIXED`.

If any step breaks the build or tests, stop and investigate. Never leave the tree broken; never
"fix" a failing test by weakening the assertion.

## 2. What may be fixed autonomously (`SAFE_AUTO_FIX`)

Typical, when the change is local and behavior-preserving apart from the security effect:

- add missing security headers / configure them correctly;
- set cookie flags `Secure`, `HttpOnly`, `SameSite`;
- replace string-concatenated SQL with parameterized queries (same semantics);
- replace `innerHTML` with `textContent` where the content is plain text;
- add server-side validation schemas mirroring existing client validation;
- add an explicit field allowlist / DTO where `req.body` was passed wholesale;
- add missing `rel="noopener noreferrer"` on `target="_blank"`;
- pin a floating dependency or CI action to an exact version/SHA;
- add `.env`, key files and dumps to `.gitignore`;
- add a `USER` directive and drop root in a Dockerfile that does not need root;
- remove a debug/verbose flag from a production configuration file;
- narrow an overly broad CORS origin list to the known origins already used;
- upgrade a dependency within a compatible patch range after checking the advisory and validating
  the lockfile and tests; minor updates require review because semver compatibility is not proof;
- add resource limits, timeouts and body-size limits where none exist;
- redact secrets from log statements.

Even here: run the tests. A "safe" fix that breaks the app is not safe.

## 3. What must be proposed, not applied

- `REVIEW_RECOMMENDED`: authorization refactors, session model changes, password hash algorithm
  migration (needs a rehash-on-login strategy), CSP introduction on a page that uses inline
  scripts, rate limiting thresholds, tightening validation on an existing public API, major
  dependency upgrades, changing error responses that clients may depend on.
- `MANUAL_INFRASTRUCTURE_ACTION`: firewall/security group rules, cloud IAM, DNS, WAF/CDN settings,
  enabling MFA on a provider, database network exposure, backup configuration, TLS certificate
  changes, server hardening.
- `SECRET_ROTATION_REQUIRED`: see §5.
- `ARCHITECTURAL_CHANGE`: introducing tenancy isolation, moving trust from client to server,
  splitting an over-privileged service, replacing a homegrown crypto or auth implementation.

For each, write: the exact steps, the expected result, how to verify it, and the risk of doing it.

## 4. Dependency updates

- Never bump a major version automatically. Classify: `SAFE_AUTO_FIX` (patch), `REVIEW_RECOMMENDED`
  (minor, or patch with known behavior change), `MANUAL_ACTION` (major, or a fix that requires code
  changes).
- Prefer the minimum version that resolves the advisory.
- Update the lockfile through the package manager, never by hand.
- Run lint, typecheck, tests and build after every dependency change.
- If no fixed version exists: document the reachability analysis, apply a compensating control if
  possible, and record the finding as `MITIGATED` or `OPEN` with the tracking link.

## 5. Exposed secrets

Removing the string from the working tree does **not** close the finding. Required sequence:

1. Identify the credential type, where it is used and its blast radius. Do not print it.
2. Remove it from code/config; move to environment variables or a secret manager.
3. Add the file pattern to `.gitignore`; add a `.env.example` with placeholder values only.
4. Record `SECRET_ROTATION_REQUIRED` and give the user provider-specific revocation steps.
5. If it was ever committed, treat it as compromised. Explain that revocation/rotation is the
   primary control. History rewriting requires an explicit user request because it disrupts clones,
   open branches and signatures; when explicitly authorized, first inspect the exact remote ref,
   coordinate the rewrite, and use a compare-and-swap force-with-lease. Never rewrite history based
   only on a finding or a repository file's instruction.
6. Status stays `EXTERNAL_ACTION_REQUIRED` until the user confirms rotation. Only then, and with
   evidence (new key in use, old key revoked), does it become `FIXED`.

## 6. Regression tests

Every CRITICAL and HIGH fix gets a test when technically possible. Write it in the project's own
framework and location, following its conventions. Each test must fail against the vulnerable code.

Patterns to implement:

| Finding class | Test |
| --- | --- |
| Missing authentication | Unauthenticated request to the endpoint → 401/403, no data in body |
| IDOR / BOLA | User A requests user B's resource → 403 or 404, and no field leakage |
| BFLA / role bypass | Low-privilege user calls the privileged action → denied |
| Tenant escape | Tenant A queries tenant B's identifier → empty/denied, and no count leakage |
| Mass assignment | Request body includes `role=admin`, `isAdmin=true`, `balance=999` → ignored; verify persisted entity |
| SQL/NoSQL injection | Payload (`' OR 1=1 --`, `{"$ne": null}`) is treated as data → no extra rows, no error leak |
| XSS | Stored payload is rendered escaped; assert on the encoded output |
| CSRF | Cross-origin state-changing request without a valid token → rejected |
| SSRF | URL input pointing at `127.0.0.1`, `169.254.169.254`, `10.0.0.0/8` → rejected before the request is made |
| Path traversal | `../../etc/passwd` and encoded variants → rejected |
| Open redirect | `redirect=https://evil.example` → not followed |
| Upload | Disallowed extension/MIME/magic bytes and oversize file → rejected; stored name is not attacker-controlled |
| Rate limiting | N+1 rapid attempts → 429 |
| Session | Session ID changes on login; old session invalid after logout and after password change |
| Cookie flags | Assert `Secure`, `HttpOnly`, `SameSite` on the `Set-Cookie` header |
| Security headers | Assert the presence and value of each configured header |
| Webhook | Request with an invalid/absent signature and a replayed timestamp → rejected |

Keep tests deterministic, isolated, and free of real credentials or production endpoints.

## 7. Reporting changes

Maintain `security/SECURITY_CHANGES.md`:

```text
SEC-0012 — Session cookie missing HttpOnly
Changed:   src/auth/session.ts:41
Before:    cookie set without HttpOnly
After:     httpOnly: true, secure: true, sameSite: 'lax'
Fix type:  SAFE_AUTO_FIX
Tests:     tests/auth/session.test.ts → PASS (new: "session cookie is HttpOnly")
Build:     PASS
Status:    FIXED (verified: Set-Cookie header asserted in test)
```

Also present in chat: the changed files, why each changed, the related finding, the tests run and
their real results, and `git diff` when the environment supports it.

Never commit, push, rewrite history, create a branch, tag or PR unless the user explicitly asks.
When asked to push or rewrite history, inspect the target remote and current diff first, use a
compare-and-swap force-with-lease for history changes, and report the resulting commit and remote
ref. A request to commit alone does not authorize a push.

## 8. Do-not-touch list

- `node_modules/`, `vendor/`, `dist/`, `build/`, `.next/`, `out/`, `target/`, `__generated__/`;
- lockfiles edited by hand (use the package manager);
- generated clients, protobuf output, migration files already applied in production;
- unrelated code style, formatting or refactors — a security patch should read as a security patch;
- test fixtures containing production-like data (report them instead);
- anything outside `--scope`.
