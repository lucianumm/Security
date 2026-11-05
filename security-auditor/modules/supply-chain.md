# MODULE — DEPENDENCIES AND SOFTWARE SUPPLY CHAIN

Scope: third-party packages, lockfiles, install scripts, build artifacts, container base images,
CI actions, and the integrity of everything you did not write.

Related: `ci-cd.md`, `docker.md`, `frontend.md` §Third-party JavaScript, `secrets.md`.
Standards: OWASP Top 10 A06/A08, NIST SSDF, CWE-1104, CWE-1357, CWE-494, CWE-829.

---

## 1. Inventory

```bash
ls package.json pnpm-lock.yaml yarn.lock package-lock.json requirements*.txt poetry.lock \
   Pipfile.lock composer.lock go.sum Cargo.lock Gemfile.lock pom.xml build.gradle* 2>/dev/null
```

Record: package manager, direct vs transitive counts, whether a lockfile exists and is committed,
Node/Python/etc. runtime versions, and whether the runtime version itself is still supported
(an end-of-life runtime is a finding — no security patches).

## 2. Vulnerability scanning

Run what is available; record the exact command and interpret, do not paste raw output.

```bash
npm audit --json            # or: pnpm audit --json / yarn npm audit --json
pip-audit -f json           # or: safety check --json
composer audit --format=json
cargo audit --json
govulncheck ./...           # reachability-aware
bundler-audit check --update
osv-scanner --format json -r .     # language-agnostic fallback
trivy fs --scanners vuln --format json .
```

For each reported vulnerability, decide with evidence:

| Question | Why it matters |
| --- | --- |
| Direct or transitive? | Determines who can fix it and how |
| Is the vulnerable function/path reachable from our code? | Reachability, not CVSS, drives priority |
| Is the affected feature enabled in our configuration? | Many CVEs need a non-default option |
| Is it exploitable in our deployment (server vs build-time vs dev-only)? | A dev-only tool CVE is not production risk |
| Is there a fixed version, and what does upgrading break? | Determines fix type |
| Is there a mitigation if we cannot upgrade? | Config change, WAF rule, removing the feature |

`govulncheck` (Go) and reachability-aware scanners give strong evidence; for other ecosystems, do
the reachability analysis by reading the call sites. Downgrade to LOW/INFO with a written rationale
when unreachable — never silently drop.

Dev-dependency vulnerabilities still matter: they run on developer machines and CI runners with
access to source and secrets. Rate them by that blast radius, not as "not production".

## 3. Lockfiles and version discipline

- A lockfile exists, is committed, and is used in CI (`npm ci`, `pnpm i --frozen-lockfile`,
  `yarn --immutable`, `pip install -r requirements.txt --require-hashes`, `bundle install
  --deployment`). Installing without the lockfile in CI is a finding.
- Floating specifiers on security-relevant packages (`*`, `latest`, `^` on a major-zero package,
  unpinned Git refs, `main` branch dependencies) — flag with the risk of unreviewed code entering
  the build.
- Integrity hashes present in the lockfile and not stripped.
- Private registry configuration: check for dependency-confusion exposure — an internal package name
  that also resolves on the public registry. Scope internal packages and pin the registry per scope.

## 4. Package trust

For each direct dependency that is unusual, recently added, or security-relevant:

- Is the name a typosquat of a popular package (`reqeusts`, `crossenv`, `lodahs`)?
- Maintenance status: last release, open critical issues, single-maintainer risk, archived/deprecated.
- Does it run install scripts (`preinstall`, `install`, `postinstall`)? Those execute arbitrary code
  at install time, including in CI.
  ```bash
  grep -rn "\"\(pre\|post\)\?install\"" package.json
  # consider: npm ci --ignore-scripts (verify nothing legitimately needs them)
  ```
- Does it pull binaries at install time from a non-registry URL?
- Does it need the permissions/network access it has (Node has no per-package sandbox — the whole
  dependency tree runs with your process's privileges)?
- Is a much smaller alternative (or the standard library) sufficient?

## 5. Build and artifact integrity

- Reproducible, scripted build; no manual steps that could inject content.
- Build runs from a clean checkout, not from a developer machine's working tree.
- Artifacts are versioned and, where feasible, signed (Sigstore/cosign) with provenance
  (SLSA-style attestation).
- SBOM generation (`syft`, `cdxgen`, `npm sbom`) recommended for anything distributed.
- Published packages: `.npmignore`/`files` reviewed so source secrets, `.env` and internal docs are
  not published; 2FA required on the publishing account; automation tokens scoped.
- Container base images pinned by digest (`docker.md`).

## 6. Third-party code in the browser

Every external script, font, style, widget and tag manager is a supply-chain dependency with
execution rights on your origin (`frontend.md` §6). Require: necessity, pinned version, Subresource
Integrity where possible, CSP restriction, and a documented owner.

## 7. CI dependencies

Third-party GitHub Actions / GitLab includes / Jenkins plugins execute in a context with repository
access and secrets. Pin to a full commit SHA, review what they do, and prefer first-party or
widely-audited actions (`ci-cd.md`).

## 8. Update policy to recommend

- Automated dependency updates (Dependabot/Renovate) with grouped, tested PRs.
- Patch updates: propose the advisory-specific patch and lockfile change (`SAFE_AUTO_FIX` risk
  label); apply only after batch approval. Green CI does not authorize merging or publication.
- Minor updates: reviewed (`REVIEW_RECOMMENDED`).
- Major updates: planned work with a changelog review (`MANUAL_ACTION`).
- A defined SLA for critical advisories (e.g. patch or mitigate within 72 h).
- Re-run tests and build after every update; never bump versions without validating.

## 9. Regression / CI checks

Dependency audit runs on every PR and fails on unmitigated critical advisories (`ci-cd.md`
§Blocking policy) · lockfile drift detected (`git diff --exit-code` after an install) ·
license/dependency allowlist enforced if the organization requires it · SBOM generated for releases.
