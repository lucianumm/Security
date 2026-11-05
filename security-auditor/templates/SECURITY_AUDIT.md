# Security Audit — <project name>

<!--
Template for security/SECURITY_AUDIT.md. Replace every <placeholder>.
Delete sections that are genuinely not applicable, and say so in Scope.
Never leave an invented value in place of a real one.
-->

```text
SECURITY AUDIT
Project:            <name>            Commit: <sha>        Branch: <branch>
Date:               <YYYY-MM-DD>      Mode:   <AUDIT | AUDIT_AND_FIX | HARDEN | VERIFY | CI_GATE | TARGETED_AUDIT | INCIDENT_REVIEW>
Auditor:            security-auditor v<version>
Security Score:     <XX>/100          Coverage: <XX>% of applicable controls verified
Production Readiness: <READY_FOR_PRODUCTION | READY_WITH_RESTRICTIONS | NOT_READY_FOR_PRODUCTION | INSUFFICIENT_EVIDENCE>

Findings
  Critical: <n>   High: <n>   Medium: <n>   Low: <n>   Info: <n>
Status
  Fixed: <n>   Open: <n>   External Action Required: <n>   Not Verified: <n>   Regressions: <n>

Top Risks
  1. <SEC-XXXX — one line>
  2. <SEC-XXXX — one line>
  3. <SEC-XXXX — one line>

Immediate Actions
  1. <action, owner>
  2. <action, owner>
  3. <action, owner>
```

---

## 1. Scope of this audit

**Mode:** <mode> · **Requested scope:** <full repository | path | area>
**Environment safety check:** <PASS | PASS_WITH_NOTES | BLOCKED> — <notes>

| Category | Detail |
| --- | --- |
| Inspected | <files, directories, configurations actually read> |
| Executed | <commands and scanners actually run, with versions> |
| Tested | <dynamic tests actually performed and against what target> |
| Externally verified | <what the user confirmed or showed evidence for> |
| Not accessible | <production, cloud console, DNS, provider dashboards…> |
| Not verified | <controls left as NOT_VERIFIED and why> |
| Assumptions | <keep this list as short as possible; each one is a risk> |

### Encyclopedia coverage and approval status

Catalog: <source version/hash> · Source digest: <digest>
Controls reviewed: <n>/136 · Applicable / excluded / unknown: <n>/<n>/<n>
Scenarios reviewed: <n>/507 · Domains accounted for: <n>/19
Source count discrepancy: the original declares 506 scenarios; 507 actual rows are preserved.

List evidence-backed exclusions, unresolved domains, current intelligence sources/dates and the
external verification backlog. Record proposed, approved, applied and verified actions separately,
with plan digest and user-message approval references. Catalog accounting is not a claim that all
vulnerabilities were found. Do not mark the project fully secure because the ledger is complete.

## 2. System overview

**Stack detected:** <languages, frameworks, datastores, infra, CI, cloud>
**Modules loaded:** <list> · **Modules skipped:** <list and why>

### Architecture

```text
<the architecture actually found — no invented components>
```

| Component | Function | Trust | Exposure | Data handled | Auth |
| --- | --- | --- | --- | --- | --- |

### Trust boundaries

| Boundary | Crossing controls | Gaps |
| --- | --- | --- |

### Data classification

| Data | Class | Where stored | Encrypted | Retention |
| --- | --- | --- | --- | --- |

## 3. Attack surface summary

See `ATTACK_SURFACE.md` for the full inventory. Highlights:

- Public entry points: <n> · Authenticated endpoints: <n> · Admin endpoints: <n>
- Unauthenticated endpoints handling sensitive data: <n>
- File upload/download paths: <n> · URL-accepting features: <n> · Webhooks: <n>

## 4. Findings

Full detail in `FINDINGS.md`. Summary table, most severe first:

| ID | Severity | Priority | Confidence | Status | Layer | Title |
| --- | --- | --- | --- | --- | --- | --- |
| SEC-0001 | CRITICAL | P0 | HIGH | OPEN | BACKEND | <title> |

## 5. Security control matrix

Full matrix in `SECURITY_MATRIX.md`. Domain summary:

| Domain | Controls | Implemented | Partial | Missing | Misconfigured | Not verified |
| --- | --- | --- | --- | --- | --- | --- |
| Authentication & session | | | | | | |
| Authorization & tenancy | | | | | | |
| Secrets | | | | | | |
| Input handling | | | | | | |
| Data protection | | | | | | |
| API & transport | | | | | | |
| Infrastructure & containers | | | | | | |
| Supply chain | | | | | | |
| CI/CD & Git | | | | | | |
| Logging & monitoring | | | | | | |
| Backup & recovery | | | | | | |

## 6. Scanners executed

| Tool | Version | Command | Result summary | Interpretation |
| --- | --- | --- | --- | --- |

Tools not available in this environment: <list> → the corresponding controls are `NOT_VERIFIED`.

## 7. Changes applied *(fix modes only)*

See `SECURITY_CHANGES.md`. Summary:

| Finding | Files changed | Fix type | Tests | Status |
| --- | --- | --- | --- | --- |

Validation after changes: lint <PASS/FAIL> · typecheck <PASS/FAIL> · unit <PASS/FAIL> ·
integration <PASS/FAIL> · build <PASS/FAIL> · security regression <PASS/FAIL>.

## 8. Score explanation

```text
Security Score: <XX>/100
Base (weighted domain assessment): <XX>
Penalties: <-XX> (list the largest)
Caps applied: <which, if any>
Coverage: <XX>%
```

Main factors:
1. <factor>
2. <factor>
3. <factor>

## 9. Production readiness

**Verdict:** <verdict>

<justification tied to `../references/CHECKLIST_PRODUCTION.md`; list blockers or restrictions>

Full detail in `PRODUCTION_READINESS.md`.

## 10. Remediation plan

See `REMEDIATION_PLAN.md`. Immediate (P0/P1) items:

| Order | ID | Action | Fix type | Owner | Effort |
| --- | --- | --- | --- | --- | --- |

## 11. Residual risk

<what remains after everything done in this run; be specific>

## 12. Recommendations beyond this audit

<CI gate, restore drill, monitoring, periodic full audit cadence, training gaps — each actionable>

---

### Closing statement

<Use only when it is true:>

> No critical or high severity vulnerabilities were identified within the scope actually inspected
> and the tests actually executed. This is not an absolute guarantee of the absence of
> vulnerabilities.
