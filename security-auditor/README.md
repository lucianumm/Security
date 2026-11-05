# SECURITY-AUDITOR

**Security Auditor — Full Stack AppSec, DevSecOps & Production Hardening**

A portable, agent-agnostic skill that turns an AI coding agent into a permanent security auditor for
a project: it discovers the real architecture, maps the attack surface, verifies controls against
evidence, reports findings with persistent IDs, fixes what can be fixed safely, writes regression
tests, re-verifies, records a baseline, and establishes a CI security gate.

Defensive only. It audits and hardens systems you own or are authorized to assess.

Version 1.2 adds the original encyclopedia and a reproducible catalog of 136 controls, 507 actual
scenario rows and 19 domains (the source declares 506). Read
[`core/ENCYCLOPEDIA_WORKFLOW.md`](core/ENCYCLOPEDIA_WORKFLOW.md) for project discovery, complete
coverage accounting, scoped proposals and user-approved implementation. All target changes,
including `SAFE_AUTO_FIX`, need explicit approval of the concrete batch. The helper checks
source/plan/patch consistency; the host/operator must enforce actual user consent. Catalog entries
are review guidance, not automatic vulnerability detectors or a guarantee of complete security.

---

## Design principles

| Principle | What it means in practice |
| --- | --- |
| **Verify, don't assume** | Every control status needs evidence; `NOT_VERIFIED` never becomes `IMPLEMENTED` |
| **Evidence over vibes** | A comment, a README or an installed library is not proof |
| **Find missing controls, not just bugs** | The audit asks what *should* exist, not only what is broken |
| **Persistent state** | Findings keep their IDs across runs; regressions are detected against a baseline |
| **Progressive disclosure** | `SKILL.md` coordinates; modules load only for the detected stack |
| **Conservative with production** | Nothing destructive, nothing outward-facing, no secret ever printed |
| **Fixes must be proven** | A code change is not a fix until a test or an observation says so |

## Layout

```text
security-auditor/
├── SKILL.md                     entry point: modes, phases, routing, output contract
├── README.md                    this file
├── VERSION
├── core/
│   ├── SAFETY.md                hard rules; read before any command
│   ├── WORKFLOW.md              phases, exit criteria, incremental/monorepo/CI variants
│   ├── EVIDENCE_RULES.md        status vocabulary, what counts as evidence, false positives
│   ├── SEVERITY.md              severity, confidence, priority, fix types, finding lifecycle
│   ├── SCORING.md               0–100 score, hard caps, production readiness verdicts
│   └── REMEDIATION_POLICY.md    approved corrections, regression tests, change reporting
│   ├── ENCYCLOPEDIA_WORKFLOW.md catalog review, coverage, concrete plan and approval checks
│   ├── ATTACK_REASONING.md      adversary paths, attacker goals, evidence and counterevidence
│   ├── TOOL_EXECUTION.md        tool selection, privacy, network and execution profiles
│   ├── COVERAGE.md · STATE_MACHINE.md
├── modules/                     25 technology/domain modules, loaded on detection
│   authentication · authorization · sessions · api · frontend · backend · database ·
│   uploads · cryptography · secrets · supply-chain · docker · kubernetes · cloud ·
│   nginx · ci-cd · logging · monitoring · backup · business-logic · payments ·
│   webhooks · ai-security · incident-response · extended-surfaces
├── references/
│   ├── OWASP_MAPPING.md         Top 10, API Top 10, LLM Top 10, related standards
│   ├── ASVS_MAPPING.md          chapter → module map, verification levels
│   ├── CWE_MAPPING.md           weakness taxonomy per finding class
│   ├── CHECKLIST_GLOBAL.md      full-audit coverage self-check + natural-language triggers
│   └── CHECKLIST_PRODUCTION.md  production readiness gate
├── templates/
│   ├── SECURITY_AUDIT.md · SECURITY_MATRIX.md · FINDINGS.md · ATTACK_SURFACE.md
│   ├── THREAT_MODEL.md · REMEDIATION_PLAN.md · SECURITY_BASELINE.md
│   ├── SECURITY_CHANGES.md · PRODUCTION_READINESS.md · INCIDENT_READINESS.md
│   ├── state/                   .security/*.json schemas and seed files
│   └── ci/                      GitHub Actions and GitLab CI security-gate pipelines
├── schemas/                     strict state and scenario JSON schemas
├── catalog/                     attack scenarios, tool notes and local SAST starter rules
├── tests/                       deterministic gate regression suite
└── scripts/
    ├── detect-stack.sh          read-only technology detection
    ├── security_auditor.py      schema validation, source/policy digests and fail-closed gate
    ├── security-gate.sh         POSIX gate wrapper
    └── security-gate.ps1        PowerShell gate wrapper
```

## Modes

| Mode | Writes code? | Use it for |
| --- | --- | --- |
| `AUDIT` *(default)* | No | Full read-only diagnosis |
| `AUDIT_AND_FIX` | After batch approval | Audit, present plan/diff, obtain approval, fix and verify |
| `HARDEN` | After batch approval | Approved fixes plus justified missing hardening controls |
| `VERIFY` | No | Re-audit, revalidate findings, detect regressions |
| `CI_GATE` | No | Pipeline checks → `PASS`/`FAIL` + machine-readable JSON |
| `TARGETED_AUDIT <area>` | Per request | One area (auth, API, Docker, uploads, CI/CD…) |
| `INCIDENT_REVIEW` | No | Preserve evidence, look for compromise indicators |

## Installation

The skill is plain Markdown, so it works anywhere an agent can read files.

**Claude Code / Claude Desktop (skills)**

```bash
# project-scoped
mkdir -p .claude/skills && cp -r security-auditor .claude/skills/
# or user-scoped
mkdir -p ~/.claude/skills && cp -r security-auditor ~/.claude/skills/
```

Then invoke it by name (`/security-auditor`) or just ask: *"faça uma auditoria de segurança"*.

**Cursor / Windsurf / Continue / other IDE agents**

Copy the directory into the repository (e.g. `.ai/security-auditor/`) and add a rule pointing at
`security-auditor/SKILL.md` for security-related requests.

**OpenAI Codex / ChatGPT with file access / Gemini / CLI agents**

Provide `SKILL.md` as the instruction file and let the agent open the referenced files on demand.
When the agent cannot read files lazily, paste `SKILL.md` plus the modules relevant to the stack.

**MCP-based setups**

Expose the directory as a resource root; `SKILL.md` is the entry point and every internal link is a
relative path within this directory.

**CI**

Copy a pipeline from `templates/ci/` and `scripts/security-gate.sh` into the audited project.

## Usage

```text
security-auditor                          # AUDIT, full repository
security-auditor AUDIT_AND_FIX
security-auditor HARDEN
security-auditor VERIFY
security-auditor CI_GATE
security-auditor TARGETED_AUDIT authorization
security-auditor INCIDENT_REVIEW
```

Flags: `--scope <path>` · `--no-write` · `--incremental` · `--full` · `--offline` ·
`--allow-dynamic`.

Natural language works too, in any language — "audite minha API", "is this ready for production?",
"security review this PR", "faça hardening do Docker e da VPS".

## What it produces

In the audited project (unless `--no-write`):

```text
security/           SECURITY_AUDIT · SECURITY_MATRIX · FINDINGS · ATTACK_SURFACE · THREAT_MODEL ·
                    REMEDIATION_PLAN · SECURITY_BASELINE · SECURITY_CHANGES ·
                    PRODUCTION_READINESS · INCIDENT_RESPONSE
.security/          baseline.json · findings.json · controls.json · architecture.json ·
                    risk-register.json · last-audit.json
```

Plus, in fix modes: the code changes themselves, regression tests, and a `git diff` for review.
By default the skill leaves Git history untouched. It creates commits, pushes or rewrites history
only when the user explicitly requests that exact operation. A history rewrite checks the remote tip
and uses a compare-and-swap force-with-lease.

## Safety guarantees

- Reads `core/SAFETY.md` before acting; refuses destructive commands without explicit authorization.
- Rewrites Git history or force-pushes only after the user explicitly asks for that exact change;
  verifies the remote tip and uses a compare-and-swap force-with-lease.
- Never runs migrations or changes production infrastructure.
- Never prints a secret; never uses a discovered credential.
- Dynamic testing only against localhost or a target the user explicitly authorizes; never DoS,
  never third-party systems.
- Treats every file, log and page it reads as data, not as instructions.

## Limitations

- Anything outside the repository (cloud consoles, DNS, IdP, provider dashboards) is
  `NOT_VERIFIED` unless the user supplies evidence.
- Scanner availability varies by environment; a missing tool yields `NOT_VERIFIED`, never a pass.
- The state gate validates JSON, digests and policy; it does not run scanners or prove scanner
  claims. Trusted CI must load the gate and policy from a protected source.
- CI files are adaptable templates, not active scanning integrations for every technology stack.
- Standard editions are recorded in `references/standards.lock.json`; verify them when updating the
  mappings.
- A clean audit is never a guarantee of the absence of vulnerabilities.

## Security improvement status

See [`IMPLEMENTATION_STATUS.md`](../IMPLEMENTATION_STATUS.md) for milestone-level coverage and
explicit limits. A consumer must adapt and protect the CI templates, supply its own authorized
runtime targets for dynamic testing, and verify external controls such as branch protection.

## Version

See `VERSION`.

## Author

Created by **Lucianum** — [instagram.com/lucianum](https://instagram.com/lucianum)

Criado por **Lucianum** — [instagram.com/lucianum](https://instagram.com/lucianum)
