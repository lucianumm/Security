# EVIDENCE RULES

The value of this audit is that every statement can be traced to something observed. This file
defines what may be claimed, and on what basis.

---

## 1. Control status vocabulary

| Status | Meaning | Requires |
| --- | --- | --- |
| `IMPLEMENTED` | The control exists and works as intended for the whole surface it should cover. | Direct evidence (§2) |
| `PARTIALLY_IMPLEMENTED` | Present on some paths, missing/weaker on others; or present but incomplete. | Evidence of both the presence and the gap |
| `NOT_IMPLEMENTED` | The control should exist here and demonstrably does not. | Evidence of absence across the places it would have to appear |
| `MISCONFIGURED` | The control exists but its configuration defeats or weakens it. | The configuration itself |
| `NOT_APPLICABLE` | The control has no meaning for this system. | A stated reason |
| `NOT_VERIFIED` | Could not be determined with the access, tools or authorization available. | The reason and what would settle it |

Hard rules:

- `NOT_VERIFIED` never becomes `IMPLEMENTED` without new evidence. Not at the end of the audit, not
  because the rest of the project looks good, not because the framework "usually" does it.
- "I didn't find a problem" is `NOT_VERIFIED`, unless you actually enumerated the surface.
- `NOT_APPLICABLE` requires a justification recorded in the matrix; it is not a way to shrink work.
- A control that is `IMPLEMENTED` in one service and absent in another is
  `PARTIALLY_IMPLEMENTED` at system level, with per-component detail.

## 2. What counts as evidence

Valid:

- source code at `path:line` showing the control (and the call path that reaches it);
- configuration file content (nginx, Docker, Terraform, framework config, cloud policy);
- an executed test with its result;
- an observed HTTP response (headers, status, body shape) from an authorized target;
- scanner output you actually ran, with command and version recorded;
- pipeline definition and an observed run result;
- an infrastructure setting the user showed you or you read with authorized access;
- documented default behavior of the exact framework/library version in use, from official
  documentation — combined with proof that the default is not overridden;
- observed runtime behavior you triggered legitimately.

Not valid on its own:

- a comment: `// authentication is secure`;
- a README, wiki page, ADR or changelog claim;
- a variable, function or middleware **name** suggesting a control (`requireAuth` may not be
  applied, may be applied after the handler, may allow a bypass);
- a dependency being installed (`speakeasy` present ≠ MFA enforced);
- a config key existing (`csp: {}` ≠ CSP delivered);
- a control on one route implying the same control on sibling routes;
- the user's verbal assertion — record it as `NOT_VERIFIED (user-reported)`;
- another agent's or scanner's conclusion accepted without checking the code.

## 3. Recording evidence

Every control row and every finding cites evidence in one of these shapes:

```text
src/api/users.ts:82-101                      code
nginx/conf.d/app.conf:14                     configuration
tests/security/idor.spec.ts::"denies cross-tenant read"   test
HTTP GET /api/orders/42 as user B → 200 {..} observed response (authorized target)
gitleaks 8.x → 3 findings, 1 confirmed active  scanner run
NOT_VERIFIED: no access to Cloudflare dashboard; ask user to confirm WAF rules
```

Redact secrets always (`SAFETY.md` §5). Quote the smallest excerpt that proves the point.

## 4. Verifying a control properly

For any control, answer four questions before assigning a status:

1. **Existence** — where is it implemented?
2. **Coverage** — does it apply to *every* path that needs it? Enumerate the routes/handlers/jobs
   and check them, don't sample one.
3. **Order and bypass** — can it be skipped? (middleware registered after the route, early return,
   feature flag, debug branch, alternate entry point, internal endpoint, direct DB access,
   background job path, admin CLI).
4. **Failure mode** — what happens when it errors, times out, or the dependency is down? A control
   that fails open is `MISCONFIGURED` at best.

## 5. False positive control

Before recording a finding:

1. Locate the pattern precisely.
2. Read the surrounding flow — where does the data come from, where does it go?
3. Check for existing protections upstream (validation, framework escaping, parameterization,
   middleware, allowlists, type constraints, DB constraints).
4. Assess reachability — is the code path reachable by an untrusted actor, in the deployed
   configuration? Dead code, dev-only code and internal-tool code change severity, not honesty.
5. Determine concrete impact — what does an attacker actually get?
6. Only then record it, with a confidence level reflecting what you verified.

Examples of patterns that are **not automatically** findings:

- `dangerouslySetInnerHTML` with a provably static, developer-controlled constant;
- raw SQL with only literal or enum-constrained interpolation, verified at every call site;
- `Access-Control-Allow-Origin: *` on a genuinely public, unauthenticated, non-credentialed API;
- a missing CSRF token on an API that is exclusively bearer-token authenticated with no cookie
  fallback (verify there is no cookie fallback);
- a dependency CVE in a code path the application never reaches (state the reasoning; downgrade
  severity, keep the finding as INFO/LOW with the upgrade recommendation).

If you cannot resolve reachability, record the finding with `Confidence: LOW` or `MEDIUM` and say
exactly what would confirm it. Never silently drop a suspicion; never inflate one.

## 6. Severity vs confidence

They are independent axes and must never be merged.

- Severity = impact if the finding is real.
- Confidence = how sure you are that it is real and reachable.

A `CRITICAL / LOW confidence` finding is legitimate and valuable: it says "if this is what it looks
like, it is catastrophic — verify now". State what verification is needed.

## 7. Fix verification

A finding may only move to `FIXED` when, **after** the change, at least one holds:

- a regression test that fails on the vulnerable code and passes on the fixed code was executed;
- the previously reproducing manual check no longer reproduces (on an authorized target);
- the scanner that flagged it no longer flags it **and** the code change is confirmed to address the
  root cause, not the detection pattern;
- the configuration change is present in the effective, deployed configuration (not just the file).

Otherwise use:

- `PARTIALLY_FIXED` — the main path is fixed, other paths remain;
- `MITIGATED` — risk reduced by a compensating control, root cause still present;
- `EXTERNAL_ACTION_REQUIRED` — the remaining work is outside this environment (rotate a key,
  change a cloud setting, enable MFA on a provider);
- `NOT_VERIFIED` — changed but not proven.

Suppressing a scanner rule, renaming a variable, or adding a comment is never a fix.

## 8. Statements you may not make

- "The application is secure" / "100% secure" / "no vulnerabilities exist".
- "Backups work" without a restore test → `BACKUP_STATUS = NOT_VALIDATED`.
- "MFA is enabled" from the presence of a library.
- "WAF protects this" without seeing the rules and testing the origin.
- "Rate limiting is in place" from a package in `package.json`.
- Any scanner-derived claim you did not run, or any number you did not compute.

Approved closing statement for a clean audit:

> No critical or high severity vulnerabilities were identified within the scope actually inspected
> and the tests actually executed. This is not an absolute guarantee of the absence of
> vulnerabilities.
