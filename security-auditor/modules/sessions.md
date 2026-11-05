# MODULE — SESSIONS, COOKIES AND TOKENS

Scope: how identity is carried between requests — server sessions, cookies, JWTs, refresh tokens,
API tokens, client-side storage.

Related: `authentication.md`, `cryptography.md`, `frontend.md`, `api.md`.
Standards: ASVS v5.0.0 V7 (Session Management), OWASP Top 10:2025 A07, CWE-384, CWE-613, CWE-614, CWE-1004, CWE-539.

---

## 1. Session identifiers

- Generated with a CSPRNG, ≥ 128 bits of entropy; never derived from user data, counters or time.
- Stored server-side (or signed+encrypted if stateless) and looked up in constant time.
- **Rotated on login** (session fixation defense) and on privilege change (e.g. after MFA, after
  impersonation start/stop).
- Never transmitted in URLs, referrers, logs or analytics.

```bash
grep -rniE "express-session|iron-session|cookie-session|session\(|SESSION_SECRET|SECRET_KEY|regenerate|rotateSession" . -l
```

## 2. Lifecycle

| Control | Expected |
| --- | --- |
| Idle timeout | Present and proportionate (e.g. 30 min–8 h for user apps; ≤ 15–30 min for admin) |
| Absolute timeout | Present (e.g. 12–24 h; ≤ 8 h for admin) |
| Logout | Destroys the server-side session, clears the cookie, and invalidates refresh tokens |
| Password change | Invalidates all other sessions |
| Email/MFA change | Invalidates other sessions; notifies the user |
| Account disable/delete | Immediately invalidates sessions |
| Revocation | An administrator or the user can list and revoke active sessions |
| Concurrency | Policy defined (allow, limit, or notify) rather than accidental |

A logout that only deletes the cookie client-side while the server session remains valid is a
finding (HIGH when tokens are long-lived).

## 3. Cookie attributes

For every cookie carrying identity or state:

```text
Secure       required (all environments served over HTTPS)
HttpOnly     required for session/auth cookies
SameSite     Lax (default) or Strict; None only with Secure and a documented cross-site need
Path         narrowest that works
Domain       do not widen to a parent domain unless required (subdomain takeover risk)
Max-Age/Expires  aligned with the session policy; session cookies for short-lived auth
__Host-      prefix recommended for session cookies (implies Secure, Path=/, no Domain)
```

```bash
grep -rniE "set-?cookie|cookies\.set|res\.cookie|SESSION_COOKIE_|SameSite|httpOnly|secure ?:" . | head -40
```

Verify the **effective** header, not just the config default. A framework default can be overridden
by a proxy, a middleware, or a second cookie set elsewhere.

## 4. JWT

Only audit this section if JWTs are actually used.

```bash
grep -rniE "jsonwebtoken|jose|pyjwt|jwt\.(sign|verify|decode)|firebase-admin|jwks" . -l
```

| Check | Requirement |
| --- | --- |
| Signature verification | Always verified server-side; `decode()` without `verify()` is a finding |
| Algorithm | Explicit allowlist (`HS256` **or** `RS256`/`EdDSA`); never accept `alg` from the token; `alg: none` rejected |
| Key confusion | RS→HS confusion prevented by pinning the expected algorithm and key type |
| Secret strength | HMAC secret ≥ 256 bits, random, from the environment; never a default like `secret`, `changeme`, `your-secret-key` |
| `exp` | Present, short for access tokens (5–60 min) |
| `nbf` / `iat` | Validated where relevant; clock skew bounded |
| `iss` / `aud` | Validated against expected values |
| `jti` | Present when revocation or replay protection is needed |
| Claims trust | Authorization claims are issued by the server, never accepted from the client |
| Revocation | A strategy exists (short expiry + refresh rotation, denylist, or session lookup) |
| Key management | Keys from a secret manager/env; rotation supported (`kid`); JWKS cached with TTL |
| Storage | See §5 |
| Sensitive data | No PII/secrets in the payload — a JWT is readable by anyone holding it |

Refresh tokens: long-lived, stored hashed server-side, rotated on use, reuse detection that revokes
the family, bound to the client where possible, revoked on logout and password change.

## 5. Client-side token storage

```bash
grep -rniE "localStorage|sessionStorage|indexedDB|document\.cookie|window\.__" src app --include=*.ts --include=*.tsx --include=*.js --include=*.jsx | head -40
```

Assessment (not a blanket rule — judge the architecture):

- `HttpOnly` cookie + CSRF defense: preferred for browser apps.
- `localStorage`/`sessionStorage`: readable by any injected script; a single XSS becomes full token
  theft. Flag as MEDIUM by default, HIGH when the token is long-lived, refreshable, or grants
  privileged access, and when the app renders user-controlled HTML.
- Tokens in URLs/query strings: finding (leaks via history, referrer, logs, proxies).
- Tokens in `window` globals or embedded in server-rendered HTML: finding if exposed to third-party
  scripts.
- Any secret that must remain secret cannot live in client code at all (`frontend.md` §Secrets).

## 6. Cross-request protection

Cookie-based auth requires CSRF defense (`api.md` §CSRF): a synchronizer token or double-submit
pattern **plus** `SameSite`, with `Origin`/`Referer` checks on state-changing requests.
Bearer-token APIs with no cookie fallback do not need CSRF tokens — verify there is truly no cookie
fallback path.

## 7. Native/mobile and long-lived clients

- Tokens stored in the OS keystore/keychain, not in plain preferences or files.
- Device binding and revocation on logout/uninstall where feasible.
- Long-lived refresh tokens require rotation and reuse detection.

## 8. Evidence to capture

Effective `Set-Cookie` header(s); session store configuration; the rotation call after login; the
logout handler; the JWT verify options object; refresh-token rotation code; timeout configuration.

## 9. Regression tests

- Session ID before login ≠ session ID after login.
- After logout, the old session/token is rejected (401), including the refresh token.
- After a password change, other sessions are rejected.
- `Set-Cookie` asserts `Secure`, `HttpOnly`, `SameSite`.
- A JWT signed with `alg: none` or with a wrong key is rejected.
- An expired JWT is rejected; a token with a tampered `role` claim is rejected.
- A reused refresh token revokes the token family.
