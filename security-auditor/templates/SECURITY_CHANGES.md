# Security Changes — <project name>

<!--
Template for security/SECURITY_CHANGES.md. Written only in AUDIT_AND_FIX and HARDEN modes.
One block per change. Policy: ../core/REMEDIATION_POLICY.md §7.
Never commit or push as part of the audit; this file is the record the user reviews before doing so.
-->

Audit date: <YYYY-MM-DD> · Mode: <AUDIT_AND_FIX | HARDEN> · Base commit: <sha>
Changes applied: <n> · Findings addressed: <n> · Files touched: <n>

---

## SEC-0012 — Session cookie missing `HttpOnly`

| | |
| --- | --- |
| Fix type | SAFE_AUTO_FIX |
| Files | `src/auth/session.ts:41` |
| Related finding severity | HIGH |

**Before**

```ts
res.cookie('sid', token, { maxAge: 86_400_000 });
```

**After**

```ts
res.cookie('sid', token, {
  maxAge: 86_400_000,
  httpOnly: true,
  secure: true,
  sameSite: 'lax',
  path: '/',
});
```

**Why** — the session cookie was readable by any script on the page, so a single XSS became full
session theft.

**Tests**

```text
tests/auth/session.test.ts  → PASS  (new: "session cookie sets HttpOnly, Secure, SameSite")
```

**Validation** — lint PASS · typecheck PASS · unit PASS · build PASS

**Status** — `FIXED` (verified: `Set-Cookie` header asserted in the new test)

**Behavioral impact** — none expected; no client code reads this cookie
(`grep -rn "document.cookie" src` → no matches).

---

## SEC-00xx — <title>

<!-- repeat the block -->

---

## Changes proposed but NOT applied

| ID | Change | Fix type | Why not applied | Where the proposal is |
| --- | --- | --- | --- | --- |
| SEC-0001 | Introduce a policy layer for object-level authorization | ARCHITECTURAL_CHANGE | Changes request behavior across the API; needs the team's decision | `REMEDIATION_PLAN.md` §1 |
| SEC-0011 | Rotate the exposed key | SECRET_ROTATION_REQUIRED | Requires provider access | `REMEDIATION_PLAN.md` §5 |

## Files changed (summary)

```text
<output of: git diff --stat>
```

Full diff: `git diff` (not committed — review before committing).

## Validation summary after all changes

| Step | Command | Result |
| --- | --- | --- |
| Lint | | |
| Typecheck | | |
| Unit tests | | |
| Integration tests | | |
| Build | | |
| Security regression tests | | |
| Re-scan (SCA) | | |
| Re-scan (secrets) | | |
| Re-scan (SAST) | | |

Pre-existing failures unrelated to these changes: <list, or "none">.

## Rollback

Every change above is contained in the working tree and has not been committed. To discard a single
change, revert the listed file to the base commit; to discard all of them, discard the working-tree
changes for the files listed in the summary. Do not run destructive git commands without reviewing
what else is in the tree.
