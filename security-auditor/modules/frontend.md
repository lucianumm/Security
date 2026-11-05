# MODULE — FRONTEND SECURITY

Governing rule: **everything shipped to the browser is readable and modifiable by the user.**
The frontend can improve safety and UX; it can never be the enforcement point.

Scope: XSS, DOM sinks, CSP and security headers, HTTPS/mixed content, client-side secrets,
third-party scripts, source maps, client-side routing and hidden features.

Related: `sessions.md` §Client-side storage, `api.md`, `nginx.md`.
Standards: OWASP Top 10:2025 A02/A05, ASVS v5.0.0 V1 (Encoding and Sanitization), V3 (Web Frontend Security), V12 (Secure Communication), V14 (Data Protection), CWE-79, CWE-1021, CWE-1004, CWE-829.

---

## 1. Secrets in the client

```bash
grep -rniE "sk_live|sk_test|api[_-]?key|secret|token|password|private[_-]?key|bearer " \
  src app public assets --include=*.ts --include=*.tsx --include=*.js --include=*.jsx --include=*.vue --include=*.svelte --include=*.html | head -40
grep -rnE "NEXT_PUBLIC_|VITE_|REACT_APP_|PUBLIC_|VUE_APP_|NUXT_PUBLIC_" . | head -40
# built output, if present
grep -rniE "sk_live|-----BEGIN|api_key" dist build .next/static out 2>/dev/null | head -20
```

Any credential reaching the bundle is exposed. `NEXT_PUBLIC_*`/`VITE_*`-style variables are
**public by definition** — flag every sensitive value using that prefix (CRITICAL for server-side
API secrets, payment secret keys, database URLs, admin tokens; INFO for genuinely publishable keys
such as a Stripe publishable key or a public Supabase anon key **when** row-level security is
verified).

Also check: hardcoded internal hostnames, staging URLs, employee emails, feature-flag payloads
revealing unreleased functionality, and comments containing credentials.

## 2. XSS

### Sinks

```bash
grep -rnE "innerHTML|outerHTML|insertAdjacentHTML|document\.write|dangerouslySetInnerHTML|v-html|\[innerHTML\]|\{@html|bypassSecurityTrust|new Function|eval\(|setTimeout\(['\"]|setInterval\(['\"]" src app components pages --include=* | head -60
```

For each hit, trace the data source. Static, developer-controlled content is not a finding
(`../core/EVIDENCE_RULES.md` §5). User-, URL-, API- or database-derived content is.

### Sources to trace

`location.*`, `document.URL`, `document.referrer`, `window.name`, `postMessage` data, URL query and
hash params, `localStorage`, cookies, API responses, WebSocket messages, file contents, Markdown
and rich-text fields, user-supplied SVG, and any field rendered in an email or PDF.

### Types

- **Stored**: persisted then rendered — highest impact, especially in admin views.
- **Reflected**: from the request into the response.
- **DOM**: entirely client-side, invisible to server-side scanners; audit by reading the sinks.

### Defenses to verify

Framework auto-escaping is on and not bypassed; HTML sanitization (DOMPurify or equivalent,
server-side where possible) with a strict allowlist for legitimate rich text; contextual encoding
(HTML body vs attribute vs JavaScript vs URL vs CSS — one generic `escape()` is not enough);
`javascript:`/`data:` URLs blocked in `href`/`src` (check link rendering in Markdown);
attribute injection through unquoted templates; `postMessage` handlers validating `event.origin`
and the message schema; Trusted Types where supported.

Special cases: user-uploaded SVG rendered inline (`uploads.md`), Markdown renderers with raw HTML
enabled, template literals building HTML, and third-party widget embeds.

## 3. Content Security Policy

Verify the **delivered** header (or meta tag), not the config file.

Directives to review: `default-src`, `script-src`, `style-src`, `img-src`, `connect-src`,
`font-src`, `frame-src`, `object-src`, `base-uri`, `form-action`, `frame-ancestors`,
`upgrade-insecure-requests`, `report-uri`/`report-to`.

| Issue | Verdict |
| --- | --- |
| No CSP at all on an app that renders user content | MEDIUM–HIGH |
| `script-src` with `'unsafe-inline'` | Weakens CSP substantially — MEDIUM; prefer nonces/hashes |
| `script-src` with `'unsafe-eval'` | MEDIUM; identify what requires it |
| `*` or broad wildcards in `script-src`/`connect-src` | MEDIUM |
| Missing `object-src 'none'` and `base-uri 'self'` | LOW–MEDIUM (base-uri enables injection pivots) |
| Missing `frame-ancestors` | Clickjacking exposure — MEDIUM |
| CSP in report-only mode only | Not enforced — `PARTIALLY_IMPLEMENTED` |
| Allowlisting a CDN that hosts arbitrary user content (JSONP endpoints, `unpkg`-style hosts) | Bypassable CSP — MEDIUM |

Practical target: nonce- or hash-based `script-src` with `strict-dynamic`, `object-src 'none'`,
`base-uri 'self'`, `frame-ancestors` set, and a report endpoint.

## 4. Other response headers

Checked here or in `nginx.md`, wherever they are actually set:

```text
Strict-Transport-Security: max-age=31536000; includeSubDomains   (preload only when deliberate)
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin (or no-referrer)
Permissions-Policy: disable unused features (camera, microphone, geolocation, payment, usb)
X-Frame-Options: DENY|SAMEORIGIN   (legacy; frame-ancestors preferred, both is fine)
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin | same-site
Cross-Origin-Embedder-Policy: require-corp   (only when cross-origin isolation is needed)
Cache-Control: no-store  on authenticated/sensitive responses
```

Verify per response type: HTML pages, API responses, static assets and error pages can be served by
different layers with different headers.

## 5. Transport

- HTTPS everywhere; HTTP redirects to HTTPS; HSTS present.
- No mixed content (`http://` scripts, images, XHR, iframes) — check the built output too.
- `ws://` upgraded to `wss://`.
- No absolute `http://` API base URLs in configuration.
- External links with `target="_blank"` carry `rel="noopener noreferrer"`.

## 6. Third-party JavaScript

Inventory every external script, font, style, pixel, tag manager, chat widget, analytics and A/B
tool. For each: is it necessary, who controls it, what data does it see, is it pinned, does it have
Subresource Integrity, and is it allowed by the CSP? A tag manager effectively grants script
execution to whoever can log into it — note that as a supply-chain risk (`supply-chain.md`).

Any third-party script on a page that handles payments, credentials or personal data is a
significant risk; recommend isolation (iframe, separate origin) or removal.

## 7. Client-side enforcement anti-patterns

Flag whenever the client is the only gate:

```text
if (user.isAdmin) { showAdminPanel() }         // UI only — server must enforce
if (formValid) { submit() }                     // server must revalidate
price computed in the browser and posted        // server must recompute (payments.md)
role/permission list fetched and trusted         // server must decide
feature flag hides a working endpoint            // endpoint is still reachable
"secret" admin route in the SPA router           // discoverable in the bundle
```

Each occurrence without a verified server-side counterpart is a finding
(severity per `authorization.md`).

## 8. Build output and source maps

- Are source maps published in production? Judge the content: maps for a public SPA reveal code
  structure (usually LOW), maps revealing server-side code, comments, internal URLs or credentials
  are higher. Do not report reflexively — read what is exposed.
- Are `.env`, `.git`, backup files, editor files or dumps served from the public directory?
  (`nginx.md` §Hidden files) — CRITICAL when `.env` or `.git` is reachable.
- Is `console.log` leaking tokens, PII or internal state in production?
- Are debug tools (React DevTools hooks, Redux DevTools, Vue devtools, verbose error overlays)
  enabled in production builds?

## 9. Miscellaneous client risks

- Clickjacking on sensitive actions → `frame-ancestors`.
- Prototype pollution in client-side merge/query-parsing libraries (`backend.md` §Prototype
  pollution).
- Open redirect implemented in the client router (`backend.md` §Open redirect).
- Autocomplete on sensitive fields; password fields inside forms posting cross-origin.
- Sensitive data in URLs (tokens, IDs of private resources) leaking via referrer and history.
- Service worker caching authenticated responses in a shared browser context.
- `postMessage` targets set to `*` when sending sensitive data.

## 10. Regression tests

Assert the delivered security headers · assert a stored XSS payload renders escaped · assert
sanitizer strips `<script>`, `on*` handlers and `javascript:` URLs · assert no `sk_`/secret pattern
exists in the built bundle (grep in CI) · assert `postMessage` handler rejects a foreign origin ·
assert the app does not fetch over plain HTTP.
