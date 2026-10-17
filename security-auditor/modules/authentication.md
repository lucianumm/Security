# MODULE — AUTHENTICATION

Scope: account creation, login, logout, password reset, password change, email change, MFA,
"remember me", OAuth/SSO, passkeys, recovery codes, machine-to-machine authentication.

Related: `sessions.md`, `authorization.md`, `cryptography.md`, `logging.md`.
Standards: OWASP ASVS v5.0.0 V6 (Authentication), V7 (Session Management), V9 (Self-contained Tokens), V10 (OAuth and OIDC); OWASP Top 10:2025 A07; CWE-287, CWE-307, CWE-521, CWE-640.

---

## 1. Locate the implementation

```bash
grep -rniE "passport|next-auth|auth0|clerk|supabase.auth|firebase.auth|cognito|keycloak|devise|django.contrib.auth|laravel/(sanctum|passport|breeze|jetstream)|spring-security" --include=* -l .
grep -rniE "sign ?in|log ?in|authenticate|login|register|signup|reset.?password|forgot.?password|verify.?email|change.?password|mfa|totp|otp|webauthn|passkey" src app lib routes controllers pages api 2>/dev/null | head -60
```

Identify: is authentication self-implemented, framework-provided, or delegated to an external IdP?
Delegated auth moves controls outside the repository — audit the integration and mark provider-side
controls `NOT_VERIFIED` unless the user gives evidence.

## 2. Registration

- Is email/identity ownership verified before privileges are granted?
- Can registration create privileged accounts (`role` accepted from the body → mass assignment,
  see `api.md`)?
- Is registration rate limited and abuse resistant (disposable domains, automation)?
- Does the response differ for an existing vs new account (enumeration)?
- Are password rules enforced **server-side**: minimum length (≥ 12 recommended for humans, ≥ 8
  absolute floor), no arbitrary maximum below 64, no forced composition rules that reduce entropy,
  and a breached-password check where feasible?
- Is invitation/onboarding token generation random, single-use and expiring?

## 3. Login

Check, for every login path (web form, API, mobile, OAuth callback, admin panel, legacy endpoint):

| Control | What to verify |
| --- | --- |
| Credential comparison | Constant-time comparison for tokens; verified hash comparison for passwords |
| Brute force protection | Per-account and per-IP throttling, progressive delay or lockout with recovery |
| Credential stuffing | Rate limiting across accounts, breached-credential detection, bot protection |
| User enumeration | Identical message and timing for unknown user vs wrong password; same for reset and registration |
| Generic error | "Invalid credentials" — never "user not found" / "wrong password" |
| Session establishment | New session ID after login (`sessions.md`) |
| MFA enforcement | Applied before the session becomes fully privileged |
| Logging | Success and failure logged with user id, IP, user agent, timestamp — never the password |
| Timing | No obviously different response time revealing account existence |
| Account state | Disabled/locked/unverified accounts cannot authenticate |

Common bypasses to look for: an alternate login route without throttling; a "login as" / impersonate
feature without authorization; a dev/test account seeded in production; an SSO callback that trusts
an email claim without verifying issuer/audience/signature; a legacy API key path.

## 4. Password storage

Acceptable: **Argon2id** (preferred), **scrypt**, **bcrypt** (cost ≥ 10, note the 72-byte input
limit), **PBKDF2-HMAC-SHA256** with a high iteration count where required by compliance.

```bash
grep -rniE "argon2|bcrypt|scrypt|pbkdf2|hashSync|password_hash|make_password|BCryptPasswordEncoder" . --include=* -l
grep -rniE "md5|sha1\(|sha256\(|createHash\(['\"](md5|sha1|sha256)|crypt\(|base64.*password|encrypt.*password" . -l
```

Findings (all HIGH or CRITICAL when real user passwords are affected):
plaintext storage; reversible encryption; MD5/SHA1/SHA256 without a KDF; a home-made scheme;
a global/static salt; cost parameters below current guidance; passwords logged or emailed;
password comparison with `==` against a plain value.

Migration path when a weak algorithm is in use: rehash on next successful login, force reset for
inactive accounts, never leave both paths accepted indefinitely. Fix type: `REVIEW_RECOMMENDED`.

## 5. Password reset and account recovery

- Token: cryptographically random (≥ 128 bits), stored hashed, single-use, short expiry (≤ 1 h).
- The token must not be guessable, sequential, derived from user data, or reused across requests.
- Reset must invalidate all existing sessions and refresh tokens.
- Reset must not reveal whether the account exists.
- Reset link host must come from configuration, not from a request `Host`/`X-Forwarded-Host` header
  (host header poisoning → CRITICAL when it leaks the token to an attacker domain).
- MFA must not be bypassable through the reset flow.
- Email/phone change requires re-authentication and confirmation to the **old** address.
- Recovery codes: generated randomly, stored hashed, single-use, regenerable, count limited.

## 6. MFA

Preference order: WebAuthn/passkeys → hardware keys → TOTP → push. SMS is a fallback, not a target
state; document its weaknesses if used.

Verify the **flow**, not the dependency:

- Is MFA enforced for administrators, support staff, finance operations and sensitive actions?
- Is the pre-MFA session unable to access protected resources (no partially authenticated token that
  already works)?
- Is the OTP verification rate limited and are codes single-use with a short window?
- Is TOTP replay prevented (used-code cache)?
- Is there an enrollment step that requires re-authentication?
- Can MFA be removed without re-authentication or notification?
- Are recovery codes and "trusted device" cookies a bypass path? Are trusted devices bound and
  expiring?

`Installed library ≠ IMPLEMENTED` (`../core/EVIDENCE_RULES.md` §2).

## 7. OAuth / OIDC / SSO

- `state` parameter present, random, bound to the session, and verified (CSRF on the callback).
- PKCE for public clients; `nonce` verified for OIDC.
- Redirect URI validated against an exact allowlist — no wildcard, no prefix matching.
- ID token signature, `iss`, `aud`, `exp` and `azp` verified against the provider's JWKS.
- Email claim: only trusted when the provider asserts verification; otherwise account linking by
  email is an account-takeover vector (CRITICAL).
- Account linking requires proof of ownership of the existing account.
- Provider tokens stored server-side, encrypted at rest, never exposed to the browser.

## 8. Machine and service authentication

- API keys: random, hashed at rest, scoped, revocable, rotatable, per-consumer, logged on use.
- No shared "master" key across environments or tenants.
- mTLS / signed requests where appropriate for internal service traffic (zero trust between
  services — do not treat "internal network" as authentication).

## 9. Administrative accounts

Apply the stricter baseline from `../modules/backend.md` §Admin panel: mandatory MFA, shorter
sessions, re-authentication for sensitive actions, audit logging, alerting on new admin logins,
network restriction where feasible, and no shared admin accounts.

## 10. Evidence to capture

Route table with the auth middleware applied to each; the hashing call site; the throttling
configuration; the reset token generation and validation code; the MFA enforcement check; the
OAuth callback validation; test output for the regression tests below.

## 11. Regression tests

- Unauthenticated request to a protected endpoint → 401/403.
- Wrong password and unknown user produce identical status, body and (roughly) timing.
- N failed logins → throttled/429/locked.
- Reset token: expired → rejected; reused → rejected; another user's token → rejected.
- After password change: previously issued session/refresh token → rejected.
- MFA-enabled account cannot complete a privileged request with a pre-MFA token.
- Registration body containing `role=admin` does not create an admin.
