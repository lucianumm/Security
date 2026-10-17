# Security tool selection and execution contract

Choose the smallest set of tools that can test the audit hypotheses. Tool output is evidence to
triage, not a verdict. A missing tool, timeout, parser error, unsupported file or incomplete scan is
`NOT_VERIFIED` and cannot silently become a clean result.

## Tool families

| Question | Candidates when applicable | Evidence to retain |
|---|---|---|
| Secret exposure | Gitleaks; TruffleHog filesystem/history mode with credential verification disabled | Redacted detector, path/commit and rule ID; never the candidate value |
| Source patterns and data flow | Semgrep with a fixed local ruleset; CodeQL where configured; native language analyzers | Tool/ruleset version, exact scope, exit status and triaged rule/path |
| Dependencies | OSV-Scanner and ecosystem-native audit tools | Lockfile digest, package version, advisory, affected range and reachability reasoning |
| IaC, containers and filesystem | Trivy; Checkov for IaC; configuration-specific scanners | Image/config digest, scanner database date, rule and affected resource |
| SBOM and artifact provenance | Syft; signature/provenance verifier appropriate to the build | Artifact digest, package inventory and verifiable origin/attestation |
| HTTP and API behavior | Burp Suite or ZAP; Schemathesis for a supplied schema; application tests | Authorized target, actors, request/response minimized, seed, bounds and result |
| Template-based checks | Nuclei only with individually reviewed and pinned templates | Template digest, scope and each selected check |
| Shell and pipeline correctness | ShellCheck, actionlint and the platform's YAML/lint validator | Exact tool version, file scope and output summary |
| Cloud, network, mobile and native code | Provider/IaC tools or stack-specific analyzers selected after discovery | Identity, scope, permission, data-sharing and execution profile |

Names above are selection examples, not a mandate to install or run every scanner. Prefer existing
lockfile-native tools and offline/local modes. Verify tool support against its official documentation
for the exact version in use.

Scanner rules, config and suppression files are security policy. Load them from a protected branch
or reviewed location, never from the untrusted change being scanned. Override repository defaults
explicitly; reject unreviewed ignore files when the scanner cannot disable them. A clean result from
attacker-controlled rules or ignore paths is not evidence of a clean scan.

## Required adapter metadata

Before an adapter is used, record its executable and version, binary/container digest, ruleset or
template digest, accepted input types, fixed argument vector, working directory, environment
variables, network access, code-execution behavior, writes, timeout, memory/parallelism bounds,
exit-code meaning, parser version, redaction behavior, output format, license and relevant
limitations. Never construct a shell command from a repository value. Pass an argument array and
keep paths within the authorized scope.

Distinguish these profiles in the report:

| Profile | Network/data behavior |
|---|---|
| `offline-static` | Reads local files; no network and no dynamic target. |
| `advisory-update` | Contacts named public advisory/rule sources; package names/versions may be disclosed. |
| `authorized-local-test` | Bounded traffic to a local target or mock explicitly authorized by the user. |
| `authorized-staging-test` | Bounded traffic to the exact controlled staging host named by the user. |

Turning telemetry off does not prove that a tool is offline. Check registry/rule downloads, advisory
lookups, credential verification, update checks and remote image pulls independently. Do not send
private source, scan results, credentials, logs or customer data to third-party services without
explicit authorization and a clear data-handling decision. A scanner finding is not reproduced
behavior unless the evidence says it is.

## Exit handling and evidence

Treat `clean`, `finding`, `partial`, `timeout`, `error`, `unsupported` and `not run` as distinct
outcomes. A tool's nonzero status may mean “finding” or “could not scan”; read its pinned-version
documentation and parse its output before classifying. Invalid or truncated output is an error.
Do not suppress failures with `|| true`, pipeline fallbacks or warnings that still let the gate
pass.

Scanner output can contain secrets and personal data even in JSON/SARIF. Redact before stdout,
artifacts, chat or saved findings. Keep only the minimum evidence needed to reproduce the conclusion.
Use synthetic test data and local mocks. Never use a discovered credential to verify a scanner hit.

This skill currently defines the tool contract and CI examples; it does not provide a sandboxed
universal runner or adapters for every scanner. Running an arbitrary scanner under the agent's host
permissions is not isolation. If no enforceable sandbox is available, inspect commands and inputs,
keep dynamic testing disabled, and record that limitation.
