# MODULE — BACKEND SECURITY

Scope: server-side input handling, injection classes, output encoding, file and process access,
outbound requests, concurrency, error handling, admin surfaces.

Related: `api.md`, `database.md`, `authorization.md`, `uploads.md`, `logging.md`.
Standards: OWASP Top 10:2025 A01/A02/A05/A06/A08/A10, ASVS v5.0.0 V1 (Encoding and Sanitization), V2 (Validation and Business Logic), V15 (Secure Coding and Architecture), CWE-20, CWE-78, CWE-89, CWE-22, CWE-918,
CWE-502, CWE-1321, CWE-1333.

---

## 1. Input validation

Every input is untrusted: body, query, path params, headers, cookies, WebSocket messages, webhook
payloads, file names and contents, imported data, values read back from the database that
originated with a user, and LLM output.

Requirements: schema-based validation at the boundary (Zod/Joi/Yup, Pydantic, DRF serializers,
FormRequest, Bean Validation, `encoding/json` + explicit structs), with **type, length, range,
enum, format and allowlist** constraints, applied server-side, before business logic, failing
closed with a generic error.

Anti-patterns: validation only in the frontend; validating some fields; blocklists of "bad
characters"; `parseInt` without bounds; accepting arbitrary objects; trusting `Content-Type`;
trusting headers such as `X-Forwarded-For`, `X-Real-IP`, `Host` or `X-User-Id` without a trusted
proxy configuration.

## 2. SQL injection

```bash
grep -rnE "query\(|execute\(|raw\(|rawQuery|createQueryBuilder|\\\$queryRaw|\\\$executeRaw|db\.exec|sequelize\.query|DB::(raw|select|statement)|cursor\.execute|SELECT .*\+|f\"SELECT|`SELECT .*\$\{" src app lib | head -60
```

For each hit, determine whether untrusted data reaches the statement. Findings for: string
concatenation or interpolation of user input; dynamic `WHERE`/`ORDER BY`/`LIMIT` built from
parameters (parameter binding does not cover identifiers — require an allowlist for column and
direction names); `LIKE` patterns built unsafely; raw escapes inside an otherwise safe ORM;
stored procedures concatenating input; second-order injection (value stored safely, later
concatenated).

Fix: parameterized queries / prepared statements everywhere; allowlists for identifiers; ORM used
without raw escapes; least-privilege database user (`database.md`).

## 3. NoSQL injection

```bash
grep -rnE "\$where|\$ne|\$gt|\$regex|\$expr|find\(req\.(body|query)|filter ?= ?req\.|new Function|mapReduce" src app | head -40
```

Findings: user-supplied objects passed straight into a query (`{ password: { $ne: null } }`),
`$where`/`$expr` with user data, unvalidated `$regex` (also a ReDoS vector), and dynamic keys.
Fix: cast/validate to primitives, use schema validation, sanitize operators, avoid `$where`.

## 4. Command injection

```bash
grep -rnE "child_process|exec\(|execSync|spawn\(|shell ?= ?True|os\.system|subprocess\.(run|call|Popen)|Runtime\.getRuntime\(\)\.exec|system\(|popen\(|passthru|shell_exec|proc_open|`.*\$" src app lib | head -40
```

Any untrusted data reaching a shell is CRITICAL until proven otherwise. Also check the arguments of
tools frequently invoked with user data: `ffmpeg`, `imagemagick`/`convert`, `pdftk`, `wkhtmltopdf`,
`git`, `tar`, `unzip`, `curl`, `wget`, `sendmail`.

Fix: avoid the shell (`execFile`/`spawn` with an argument array, `shell=False`); validate against an
allowlist; never interpolate; drop privileges; consider sandboxing.

## 5. Output encoding (server-rendered)

Contextual escaping for HTML body, HTML attributes, JavaScript, URL, CSS, and for non-HTML sinks:
CSV/Excel formula injection (`=`, `+`, `-`, `@`, tab, CR prefixes), log injection (CR/LF), email
header injection, LDAP filters, XML/XPath, and shell (see §4).

Check template auto-escaping is enabled and where it is bypassed (`|safe`, `{!! !!}`, `Html.Raw`,
`template.HTML`, `mark_safe`, `raw`).

## 6. SSRF

Audit every feature that fetches a URL supplied or influenced by a user: remote downloads, image
import, link previews and unfurling, webhook testers, proxies, scrapers, PDF/screenshot generation,
avatar-from-URL, RSS/OPML import, OAuth discovery URLs, file import from URL, LLM tool browsing,
and any `redirect_uri`-like value that is fetched server-side.

```bash
grep -rnE "axios\.(get|post)\(|fetch\(|requests\.(get|post)|http\.get|HttpClient|curl_exec|file_get_contents\(|urlopen|Net::HTTP|RestTemplate" src app lib | head -60
```

Required defenses (all of them, not one):
scheme allowlist (`https` only, no `file:`, `gopher:`, `ftp:`, `data:`); host allowlist where
possible; DNS resolution followed by IP checks blocking `127.0.0.0/8`, `::1`, `10/8`, `172.16/12`,
`192.168/16`, `169.254/16` (cloud metadata `169.254.169.254`), `100.64/10`, `0.0.0.0`, IPv6 ULA and
mapped IPv4; re-validation after each redirect (or redirects disabled); protection against DNS
rebinding (resolve once and connect to that IP, or re-check before connect); timeouts and response
size limits; no credential forwarding; egress restricted at the network level where possible; and
never returning the raw upstream response body to the caller unfiltered.

SSRF that reaches cloud metadata or an internal admin service is CRITICAL.

## 7. Path traversal and file access

```bash
grep -rnE "readFile|writeFile|createReadStream|sendFile|res\.download|open\(|os\.path\.join|Path\(|File\(|include|require\(.*\+|unlink|rmdir" src app lib | head -50
```

Untrusted data in a path must be: validated against an allowlist or a strict pattern, resolved
(`path.resolve`/`realpath`) and confirmed to remain inside the intended base directory, with no
symlink escape. Handle encoded traversal (`%2e%2e%2f`, `..\\`, unicode variants, null bytes).
Never serve files by a raw client-provided path. Never use user input in `require`/`include`
(local file inclusion → RCE).

## 8. Deserialization

```bash
grep -rnE "pickle\.loads|yaml\.load\(|marshal\.loads|unserialize\(|ObjectInputStream|readObject|BinaryFormatter|Marshal\.load|node-serialize|JSON\.parse\(.*eval" . | head -30
```

Untrusted data through an unsafe deserializer is CRITICAL. Fix: `yaml.safe_load`, JSON with a
schema, signed payloads, or a data format without code execution semantics.

## 9. SSTI

User input placed into a template **string** (not passed as a variable) allows server-side template
injection. Check Jinja2, Twig, Freemarker, Velocity, Handlebars, EJS, Pug, Liquid, Thymeleaf, and
any "custom email/report template" feature. User-editable templates require a sandboxed engine with
an allowlist of filters and no access to objects, classes or the environment.

## 10. Prototype pollution (JavaScript)

```bash
grep -rnE "__proto__|constructor\[|prototype\[|merge\(|deepMerge|extend\(|assignDeep|qs\.parse|Object\.assign\(\{\}, ?req" src app | head -30
```

Check recursive merges of user-controlled objects, query-string parsers with nested syntax, and
config loaders. Fix: reject `__proto__`/`constructor`/`prototype` keys, use `Object.create(null)`,
`Map`, or a vetted merge implementation, and freeze prototypes where practical.

## 11. ReDoS

Look for regexes with nested quantifiers or overlapping alternation (`(a+)+`, `(\w+\s?)*`,
`(.*,)*`) applied to user input, especially on validation of emails, URLs, and uploaded text.
Also flag user-supplied regexes. Fix: simplify the pattern, bound the input length, use a
linear-time engine (RE2), or apply a timeout.

## 12. Concurrency and race conditions

Identify operations where two simultaneous requests can break an invariant: balance and credit
changes, stock reservation, coupon/voucher redemption, quota consumption, invite acceptance,
idempotent job creation, "check then act" sequences, file writes, and counters.

Fix: database transactions with an appropriate isolation level, atomic operations
(`UPDATE ... SET x = x - 1 WHERE x >= 1`), unique constraints, optimistic locking with a version
column, pessimistic locks (`SELECT ... FOR UPDATE`), distributed locks, or idempotency keys.
Also consider TOCTOU on the filesystem and on permission checks.

## 13. Outbound requests and integrations

Timeouts, retries with backoff and a cap, circuit breakers, TLS verification enabled (never
`rejectUnauthorized: false`, `verify=False`, `InsecureSkipVerify: true`), response size limits,
schema validation of third-party responses (a compromised or changed provider is untrusted input),
and credentials from the secret store.

## 14. Error handling

- Clients receive a generic message and, ideally, a correlation ID; details go to the logs.
- No stack traces, SQL fragments, file paths, framework versions, internal hostnames or object
  dumps in responses (check 4xx and 5xx, and error pages served by the proxy).
- Framework debug mode off in production (`DEBUG=False`, `APP_DEBUG=false`, `NODE_ENV=production`,
  detailed errors disabled) — verify the deployed configuration, not the default.
- Errors fail closed: an exception in an authorization check must deny, not allow.
- Unhandled promise rejections/panics do not crash-loop the service or leak state.

## 15. Debug and development leftovers

```bash
grep -rniE "DEBUG ?= ?true|APP_DEBUG=true|console\.log\(|print\(|dd\(|var_dump|phpinfo|pdb\.set_trace|debugger;|TODO ?:? ?security|FIXME|/debug|/__|test ?account|admin:admin|changeme|password123" . | head -60
```

Look for: debug endpoints, mock/bypass routes ("skip auth in dev"), seeded test accounts and default
passwords, feature flags that disable security in a way reachable in production, `phpinfo`,
profilers, and verbose SQL logging.

Any code path of the form `if (env !== 'production') { skipAuth() }` is a finding — verify how the
environment is determined and whether it can be influenced.

## 16. Admin panel baseline

Mandatory MFA · role-based access with least privilege · shorter session and idle timeout ·
re-authentication for destructive actions · full audit logging of who did what to whom ·
stricter rate limits · CSRF protection · notification on new admin logins and privilege changes ·
network restriction (VPN, IP allowlist, zero-trust proxy) where feasible · no shared accounts ·
no impersonation without logging and consent policy.

## 17. Regression tests

Injection payloads treated as data (SQL, NoSQL, command, template) · traversal payloads rejected ·
SSRF blocklist enforced including a redirect to an internal address · oversized/malformed input
rejected · error responses contain no stack trace · concurrent double-spend attempt leaves the
invariant intact · debug mode off in the production configuration.
