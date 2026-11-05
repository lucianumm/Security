# Changelog

## 1.2.0 — 2026-11-04

- Imported the supplied encyclopedia without altering its bytes and generated a source-bound catalog
  with 136 controls, 19 domains and all 507 actual scenario rows; recorded the source's declared 506.
- Added bounded, offline project discovery and an initially unverified full-catalog review ledger,
  strict schemas, evidence/finding cross-checks and opt-in encyclopedia enforcement for existing CI
  policies. New baseline templates enable that enforcement; protected CI bundles include its runtime.
- Required explicit approval of concrete batches for every fix and hardening implementation,
  including the historical `SAFE_AUTO_FIX` category. Added plan/approval schemas and a read-only
  preflight binding source, catalog, worktree, patch, paths, action IDs and expiry.
- Added extended-surface review guidance, report traceability and deterministic regression cases
  for stale/tampered approvals, coverage gaps and the existing CI integration.
- Kept the trust limits explicit: catalog entries are not detectors; evidence metadata is not proof;
  the host must enforce actual consent. No automatic patch executor or 100%-security claim is added.

## 1.1.0 — 2026-10-17

- Added strict schemas and starter state that remains explicitly incomplete until an audit runs.
- Added a deterministic source/policy-bound, fail-closed CI state gate and POSIX/PowerShell wrappers.
- Added protected-baseline CI templates for GitHub Actions and GitLab CI, plus a repository test workflow.
- Added adversarial attack-path, evidence, coverage and tool-execution guidance with explicit dynamic-testing boundaries.
- Added local Semgrep starter rules and a machine-readable attack-scenario schema.
- Updated OWASP mappings to the verified Top 10:2025, ASVS v5.0.0, API Top 10:2023, LLM Top 10:2026 and Agentic Top 10:2026 editions.
- Added a responsible vulnerability disclosure policy and this changelog.
- Documented that CI templates require stack-specific adaptation and that the gate validates evidence metadata but does not run or authenticate scanner claims.
