# MODULE — REVERSE PROXY AND WEB SERVER

Covers Nginx, Apache, Caddy, Traefik, HAProxy, IIS and platform-managed edges. Load when a proxy
configuration exists in the repository or the user provides one.

Related: `frontend.md` §Headers, `cloud.md` §CDN/WAF, `api.md` §Rate limiting.
Standards: ASVS v5.0.0 V12 (Secure Communication) and V13 (Configuration), OWASP Top 10:2025 A02, CIS Nginx/Apache Benchmarks, CWE-16, CWE-693, CWE-444.

---

## 1. Discovery

```bash
ls nginx.conf nginx/ Caddyfile .htaccess httpd.conf traefik*.y*ml haproxy.cfg 2>/dev/null
grep -rn "server_name\|listen\|location\|proxy_pass\|ssl_" nginx* conf* 2>/dev/null | head -60
```

Also check the effective behavior when possible: request the deployed site and read the real
response headers (authorized targets only).

## 2. TLS

| Control | Requirement |
| --- | --- |
| Protocols | TLS 1.2 and 1.3 only (`ssl_protocols TLSv1.2 TLSv1.3;`); TLS 1.0/1.1 and SSLv3 disabled |
| Ciphers | Modern suite, forward secrecy, no RC4/3DES/EXPORT/NULL/anonymous |
| Certificate | Valid, matching every served name, complete chain, auto-renewal configured and monitored |
| HTTP → HTTPS | 301 redirect for all hosts; no mixed serving |
| HSTS | `max-age=31536000; includeSubDomains`; `preload` only when the whole domain is HTTPS-ready |
| OCSP stapling | Enabled where applicable |
| Session tickets | Rotated keys or disabled |
| Default server | A catch-all server block that rejects unknown hosts (prevents host-header abuse and accidental exposure) |

## 3. Security headers at the edge

Set (or verify the application sets) `Strict-Transport-Security`, `Content-Security-Policy`,
`X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, `X-Frame-Options`/
`frame-ancestors`, and the `Cross-Origin-*` policies (`frontend.md` §3–4).

Nginx pitfall: `add_header` inside a `location` block **replaces** the parent's headers — verify
each location, especially error pages, static asset locations and proxied routes. Prefer
`always` on `add_header` so headers are present on error responses too.

## 4. Request handling limits

```nginx
client_max_body_size 10m;        # aligned with the application's upload limit
client_body_timeout 10s;
client_header_timeout 10s;
send_timeout 30s;
keepalive_timeout 30s;
large_client_header_buffers 4 8k;
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
limit_conn_zone $binary_remote_addr zone=perip:10m;
```

Check: body size limits (both too permissive and mismatched with the app), slowloris protections,
timeouts on proxied upstreams (`proxy_read_timeout`, `proxy_connect_timeout`), buffering settings,
and rate limiting for authentication and expensive endpoints.

## 5. Proxy correctness

- `proxy_set_header Host $host;` and the `X-Forwarded-*` chain set deliberately.
- The application must trust forwarded headers **only** from the known proxy
  (`trust proxy` configuration, `ProxyFix`, `TrustedProxies`) — otherwise clients spoof their IP
  and defeat rate limiting, logging and IP allowlists (MEDIUM–HIGH).
- No request smuggling exposure: consistent HTTP versions and header handling between proxy and
  upstream; reject conflicting `Content-Length`/`Transfer-Encoding`; keep proxy and app on
  compatible parsers.
- `proxy_pass` with a variable or user-influenced path can create SSRF/path confusion — review.
- Missing trailing-slash/normalization mismatches can bypass location-based access rules; verify
  protected prefixes cannot be reached via encoded paths (`/admin%2f`, `//admin`, `/./admin`).
- WebSocket upgrade headers passed correctly and only where needed.

## 6. Exposure hygiene

- `server_tokens off;` (Nginx) / `ServerTokens Prod` + `ServerSignature Off` (Apache);
  remove `X-Powered-By` at the app or proxy.
- Directory listing disabled (`autoindex off;`, `Options -Indexes`).
- Hidden and sensitive files unreachable — verify explicitly:
  `/.env`, `/.git/config`, `/.git/HEAD`, `/config.php.bak`, `/*.sql`, `/*.log`, `/docker-compose.yml`,
  `/backup.zip`, editor swap files, `/.DS_Store`, `/.svn`, `/vendor`, `/storage`.
  A reachable `.env` or `.git` is CRITICAL.
- Only the intended document root is served; no symlinks escaping it.
- Error pages are generic and do not reveal versions, paths or stack traces.
- Status/metrics endpoints (`/nginx_status`, `/server-status`, Traefik dashboard, HAProxy stats)
  restricted to localhost or authenticated.
- Deny access to dotfiles as a default rule, with explicit exceptions for `/.well-known/`.

## 7. Access control at the edge

- IP allowlists for admin paths where appropriate (defense in depth, never the only control).
- Basic auth for staging environments, plus `X-Robots-Tag: noindex` and no production data.
- mTLS for machine-to-machine endpoints where warranted.
- Blocking of obviously malicious paths is optional noise reduction, not a control to rely on.

## 8. Logging

Access and error logs enabled, rotated, shipped (`logging.md`), with sensitive query parameters and
`Authorization` headers excluded. Log the real client IP once the trusted-proxy configuration is
correct.

## 9. Regression / verification

Request the deployed site (authorized) and assert: HTTP redirects to HTTPS · every expected security
header present on both a 200 and a 404 · `/.env` and `/.git/HEAD` return 404/403 · directory listing
disabled · server version not disclosed · a request exceeding the body limit returns 413 · rate
limiting returns 429 on the login path · `TRACE` disabled.
