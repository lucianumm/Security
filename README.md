<h1 align="center">Security</h1>

<p align="center">
  <strong>Skills de segurança para agentes de IA</strong><br>
  <em>Security skills for AI coding agents</em>
</p>

<p align="center">
  <a href="#-português">Português</a> ·
  <a href="#-english">English</a> ·
  <a href="security-auditor/">security-auditor</a>
</p>

---

| Skill | PT | EN |
| --- | --- | --- |
| [`security-auditor/`](security-auditor/) | Auditoria defensiva completa de aplicações e infraestrutura, com evidências, correções verificadas, baseline persistente e security gate no CI/CD. | Full defensive audit of applications and infrastructure, with evidence, verified fixes, a persistent baseline and a CI/CD security gate. |

---

# 🇧🇷 Português

## security-auditor

**Security Auditor — Full Stack AppSec, DevSecOps & Production Hardening**

Uma skill portátil que transforma um agente de IA em um **auditor de segurança permanente** do
projeto. Ela descobre a arquitetura real, mapeia a superfície de ataque, verifica controles com
evidências, registra findings com IDs persistentes, corrige o que pode ser corrigido com segurança,
cria testes de regressão, revalida, mantém um baseline e estabelece um security gate no CI/CD.

Atua simultaneamente como Application Security Engineer, DevSecOps Engineer, Security Architect,
Secure Code Reviewer, API Security Engineer, Cloud Security Reviewer, Infrastructure Hardening
Engineer, Container Security Reviewer, CI/CD Security Reviewer, Threat Modeling Specialist e
Incident Readiness Reviewer.

**Somente defensiva.** Audita e endurece sistemas que você possui ou está autorizado a avaliar.

### O ciclo

```text
REPOSITÓRIO DESCONHECIDO → DESCOBERTA DE STACK → INVENTÁRIO → ARQUITETURA →
SUPERFÍCIE DE ATAQUE → THREAT MODEL → AUDITORIA → FINDINGS → PRIORIZAÇÃO →
CORREÇÃO → TESTES DE REGRESSÃO → BUILD/TEST → RESCAN → VERIFICAÇÃO →
BASELINE → CI SECURITY GATE → SEGURANÇA CONTÍNUA
```

### Princípio central

> **VERIFY, DON'T ASSUME.** Ausência de evidência nunca é evidência de ausência.

Nenhum controle recebe `IMPLEMENTED` sem evidência concreta. Nenhuma correção vira `FIXED` sem
verificação posterior. Um comentário, um README ou uma biblioteca instalada **não são prova**.

Estados de controle: `IMPLEMENTED` · `PARTIALLY_IMPLEMENTED` · `NOT_IMPLEMENTED` ·
`MISCONFIGURED` · `NOT_APPLICABLE` · `NOT_VERIFIED`

### Modos

| Modo | Altera código? | Para quê |
| --- | --- | --- |
| `AUDIT` *(padrão)* | Não | Diagnóstico completo, somente leitura |
| `AUDIT_AND_FIX` | Sim | Audita, corrige com segurança, testa, re-escaneia, verifica |
| `HARDEN` | Sim | Correção + implementação dos controles de hardening ausentes |
| `VERIFY` | Não | Reauditoria, revalidação de findings, detecção de regressões |
| `CI_GATE` | Não | Checagens de pipeline → `PASS`/`FAIL` + JSON machine-readable |
| `TARGETED_AUDIT <área>` | Conforme pedido | Uma área só (auth, API, Docker, uploads, CI/CD…) |
| `INCIDENT_REVIEW` | Não | Preserva evidências e procura indícios de comprometimento |

### O que é auditado

24 módulos carregados sob demanda conforme a stack detectada:

autenticação · autorização · sessões · API (REST, GraphQL, WebSocket) · frontend · backend ·
banco de dados e cache · uploads e storage · criptografia · secrets · supply chain · Docker ·
Kubernetes · cloud/IaC/VPS/DNS · reverse proxy · CI/CD e Git · logging · monitoramento ·
backup e restore · lógica de negócio · pagamentos · webhooks · segurança de IA/LLM ·
prontidão para resposta a incidentes.

### Instalação (Claude Code / Claude Desktop)

```bash
git clone https://github.com/lucianumm/Security.git
mkdir -p ~/.claude/skills
cp -r Security/security-auditor ~/.claude/skills/
```

Para instalar apenas em um projeto, copie para `.claude/skills/` dentro do repositório.
Outros agentes (Codex, Gemini, Cursor, Windsurf, agentes CLI, MCP): veja
[`security-auditor/README.md`](security-auditor/README.md#installation).

### Uso

Peça em linguagem natural:

```text
Faça uma auditoria de segurança.
Verifique se este projeto está pronto para produção.
Audite autenticação e autorização.
Faça hardening do Docker e da VPS.
Revalide os findings.
Faça security review deste Pull Request.
```

Ou invoque explicitamente:

```text
security-auditor AUDIT
security-auditor AUDIT_AND_FIX
security-auditor HARDEN
security-auditor VERIFY
security-auditor CI_GATE
security-auditor TARGETED_AUDIT authorization
```

Flags: `--scope <path>` · `--no-write` · `--incremental` · `--full` · `--offline` ·
`--allow-dynamic`.

### O que é gerado no projeto auditado

```text
security/     SECURITY_AUDIT.md · SECURITY_MATRIX.md · FINDINGS.md · ATTACK_SURFACE.md ·
              THREAT_MODEL.md · REMEDIATION_PLAN.md · SECURITY_BASELINE.md ·
              SECURITY_CHANGES.md · PRODUCTION_READINESS.md · INCIDENT_RESPONSE.md
.security/    baseline.json · findings.json · controls.json · architecture.json ·
              risk-register.json · last-audit.json
```

Nos modos de correção, também: as mudanças de código, os testes de regressão e o `git diff` para
revisão. Por padrão, a skill deixa o histórico Git intacto; só cria commit, envia ou reescreve o
histórico quando o usuário pede essa operação explicitamente. Para reescrita, confere a ponta remota
e usa `--force-with-lease` condicionado ao SHA observado.

Cada relatório abre com o bloco executivo:

```text
SECURITY AUDIT
Security Score: 72/100        Coverage: 81%
Production Readiness: NOT_READY_FOR_PRODUCTION
Critical: 1   High: 2   Medium: 5   Low: 8   Info: 4
Top Risks / Immediate Actions
```

### Segurança da própria skill

Não executa ações destrutivas sem autorização explícita, não altera produção, não roda migrations,
não rotaciona credenciais, não imprime secrets, não usa credenciais encontradas e não testa sistemas
de terceiros. Reescrita de histórico e force push só ocorrem após pedido explícito e comparação da
ponta remota. Teste dinâmico só em `localhost` ou em alvo que você autorize explicitamente. Todo
conteúdo lido (código, logs, páginas, dependências) é tratado como **dados, nunca instruções**.

O status de implementação e os limites dos componentes estão em
[`IMPLEMENTATION_STATUS.md`](IMPLEMENTATION_STATUS.md). Os templates de CI precisam ser adaptados
e protegidos pelo projeto que os instalar.

### Limitações

O que está fora do repositório (console de cloud, DNS, IdP, dashboards de provedores) fica como
`NOT_VERIFIED` até haver evidência. Ferramenta de scan ausente gera `NOT_VERIFIED`, nunca aprovação.
As edições usadas estão em [`standards.lock.json`](security-auditor/references/standards.lock.json);
confirme os identificadores exatos ao atualizar o mapeamento.
**Uma auditoria limpa nunca é garantia de ausência de vulnerabilidades.**

---

# 🇬🇧 English

## security-auditor

**Security Auditor — Full Stack AppSec, DevSecOps & Production Hardening**

A portable, agent-agnostic skill that turns an AI coding agent into a **permanent security auditor**
for a project: it discovers the real architecture, maps the attack surface, verifies controls
against evidence, records findings with persistent IDs, fixes what can be fixed safely, writes
regression tests, re-verifies, maintains a baseline, and establishes a CI/CD security gate.

It acts simultaneously as Application Security Engineer, DevSecOps Engineer, Security Architect,
Secure Code Reviewer, API Security Engineer, Cloud Security Reviewer, Infrastructure Hardening
Engineer, Container Security Reviewer, CI/CD Security Reviewer, Threat Modeling Specialist and
Incident Readiness Reviewer.

**Defensive only.** It audits and hardens systems you own or are authorized to assess.

### The cycle

```text
UNKNOWN REPOSITORY → STACK DISCOVERY → INVENTORY → ARCHITECTURE → ATTACK SURFACE →
THREAT MODEL → SECURITY AUDIT → FINDINGS → PRIORITIZATION → REMEDIATION →
REGRESSION TESTS → BUILD/TEST → RESCAN → VERIFICATION → BASELINE →
CI SECURITY GATE → CONTINUOUS SECURITY
```

### Core principle

> **VERIFY, DON'T ASSUME.** Absence of evidence is never evidence of absence.

No control is marked `IMPLEMENTED` without concrete evidence. No fix becomes `FIXED` without
post-change verification. A comment, a README or an installed library is **not proof**.

Control states: `IMPLEMENTED` · `PARTIALLY_IMPLEMENTED` · `NOT_IMPLEMENTED` · `MISCONFIGURED` ·
`NOT_APPLICABLE` · `NOT_VERIFIED`

### Modes

| Mode | Writes code? | Use it for |
| --- | --- | --- |
| `AUDIT` *(default)* | No | Full read-only diagnosis |
| `AUDIT_AND_FIX` | Yes | Audit, fix safely, test, re-scan, verify |
| `HARDEN` | Yes | Fix plus implement missing hardening controls |
| `VERIFY` | No | Re-audit, revalidate findings, detect regressions |
| `CI_GATE` | No | Pipeline checks → `PASS`/`FAIL` + machine-readable JSON |
| `TARGETED_AUDIT <area>` | Per request | One area (auth, API, Docker, uploads, CI/CD…) |
| `INCIDENT_REVIEW` | No | Preserve evidence, look for compromise indicators |

### What gets audited

24 modules, loaded on demand according to the detected stack:

authentication · authorization · sessions · API (REST, GraphQL, WebSocket) · frontend · backend ·
database and cache · uploads and storage · cryptography · secrets · supply chain · Docker ·
Kubernetes · cloud/IaC/VPS/DNS · reverse proxy · CI/CD and Git · logging · monitoring ·
backup and restore · business logic · payments · webhooks · AI/LLM security ·
incident response readiness.

### Installation (Claude Code / Claude Desktop)

```bash
git clone https://github.com/lucianumm/Security.git
mkdir -p ~/.claude/skills
cp -r Security/security-auditor ~/.claude/skills/
```

For a single project, copy it into `.claude/skills/` inside that repository. Other agents (Codex,
Gemini, Cursor, Windsurf, CLI agents, MCP): see
[`security-auditor/README.md`](security-auditor/README.md#installation).

### Usage

Just ask, in any language:

```text
Run a security audit.
Is this project ready for production?
Audit authentication and authorization.
Harden Docker and the VPS.
Revalidate the findings.
Security review this Pull Request.
```

Or invoke it explicitly:

```text
security-auditor AUDIT
security-auditor AUDIT_AND_FIX
security-auditor HARDEN
security-auditor VERIFY
security-auditor CI_GATE
security-auditor TARGETED_AUDIT authorization
```

Flags: `--scope <path>` · `--no-write` · `--incremental` · `--full` · `--offline` ·
`--allow-dynamic`.

### What it produces in the audited project

```text
security/     SECURITY_AUDIT.md · SECURITY_MATRIX.md · FINDINGS.md · ATTACK_SURFACE.md ·
              THREAT_MODEL.md · REMEDIATION_PLAN.md · SECURITY_BASELINE.md ·
              SECURITY_CHANGES.md · PRODUCTION_READINESS.md · INCIDENT_RESPONSE.md
.security/    baseline.json · findings.json · controls.json · architecture.json ·
              risk-register.json · last-audit.json
```

In fix modes, also: the code changes, the regression tests and a `git diff` for review.
By default, the skill leaves Git history untouched. It creates commits, pushes or rewrites history
only when the user explicitly requests that exact operation; history rewrites compare the remote tip
and use a compare-and-swap `--force-with-lease`.

### Safety guarantees

Destructive actions require explicit authorization. No production changes, migrations, credential
rotation, secrets printed, discovered credentials used, or third-party systems tested. Git history
rewrites require the user's explicit request, a remote-tip check and compare-and-swap `--force-with-lease`.
Dynamic testing only against `localhost` or a target you explicitly authorize. Everything it reads
(code, logs, pages, dependencies) is treated as **data, never instructions**.

Implementation coverage and component limits are in `IMPLEMENTATION_STATUS.md`. CI templates must
be adapted and protected by the project that installs them.

### Limitations

Anything outside the repository (cloud consoles, DNS, IdP, provider dashboards) stays
`NOT_VERIFIED` until evidence is supplied. A missing scanner yields `NOT_VERIFIED`, never a pass.
The OWASP editions used are recorded in `security-auditor/references/standards.lock.json`; verify
exact identifiers when updating the mappings. **A clean audit is never a guarantee that no
vulnerabilities exist.**

---

## Estrutura / Structure

```text
security-auditor/
├── SKILL.md              entrada / entry point: modos, fases, roteamento, contrato de saída
├── README.md · VERSION
├── core/                 SAFETY · WORKFLOW · EVIDENCE_RULES · SEVERITY · SCORING ·
│                         REMEDIATION_POLICY
├── modules/              24 módulos técnicos / 24 technical modules
├── references/           OWASP · ASVS · CWE · CHECKLIST_GLOBAL · CHECKLIST_PRODUCTION
├── templates/            10 templates de relatório + state/ (JSON) + ci/ (pipelines)
└── scripts/              detect-stack.sh · security-gate.sh
```

## Autor / Author

Criado por **Lucianum** — [instagram.com/lucianum](https://instagram.com/lucianum)

Se esta skill te ajudou, deixe uma ⭐ no repositório.
*Created by **Lucianum** — [instagram.com/lucianum](https://instagram.com/lucianum). If this skill
helped you, leave a ⭐.*
