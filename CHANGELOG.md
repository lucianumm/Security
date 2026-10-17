# Changelog

## 1.1.0 — 2026-10-17

- Added strict schemas and starter state that remains explicitly incomplete until an audit runs.
- Added a deterministic source/policy-bound, fail-closed CI state gate and POSIX/PowerShell wrappers.
- Added protected-baseline CI templates for GitHub Actions and GitLab CI, plus a repository test workflow.
- Added adversarial attack-path, evidence, coverage and tool-execution guidance with explicit dynamic-testing boundaries.
- Added local Semgrep starter rules and a machine-readable attack-scenario schema.
- Updated OWASP mappings to the verified Top 10:2025, ASVS v5.0.0, API Top 10:2023, LLM Top 10:2026 and Agentic Top 10:2026 editions.
- Added a responsible vulnerability disclosure policy and this changelog.
- Documented that CI templates require stack-specific adaptation and that the gate validates evidence metadata but does not run or authenticate scanner claims.
