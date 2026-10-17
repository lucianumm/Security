# OWASP MAPPING

The editions in standards.lock.json were checked on 2026-10-17. Cite the full edition with every
category identifier. A mapping helps organize evidence; it does not establish exploitability or
severity. Prefer the exact vulnerability class (CWE) and source evidence in the finding.

## 1. OWASP Top 10:2025 for web applications

| ID | Category | Relevant audit areas |
|---|---|---|
| A01:2025 | Broken Access Control | authorization, API object/function access, tenant boundaries, SSRF |
| A02:2025 | Security Misconfiguration | cloud, Docker, Kubernetes, reverse proxy, security headers, secrets/configuration |
| A03:2025 | Software Supply Chain Failures | dependency, build, CI/CD, artifact and distribution integrity |
| A04:2025 | Cryptographic Failures | cryptography, authentication, database, secrets and transport |
| A05:2025 | Injection | backend, frontend, database, deserialization and command execution |
| A06:2025 | Insecure Design | threat model, business logic, payments and abuse controls |
| A07:2025 | Authentication Failures | authentication, sessions, recovery and identity federation |
| A08:2025 | Software or Data Integrity Failures | CI/CD, supply chain, deserialization and trusted updates |
| A09:2025 | Security Logging & Alerting Failures | logging, monitoring, alerting and incident response |
| A10:2025 | Mishandling of Exceptional Conditions | error handling, fail-open behavior, resource cleanup and boundary failures |

The 2025 edition moves SSRF into A01:2025. Injection remains in A05:2025. Do not carry a 2021
identifier forward when the category changed; historical reports should retain their original
edition rather than being relabeled retroactively.

## 2. OWASP API Security Top 10:2023

| ID | Category | Audit areas |
|---|---|---|
| API1:2023 | Broken Object Level Authorization | authorization, IDOR/BOLA, tenant isolation |
| API2:2023 | Broken Authentication | authentication, sessions, tokens |
| API3:2023 | Broken Object Property Level Authorization | API schemas, mass assignment, excessive data exposure |
| API4:2023 | Unrestricted Resource Consumption | API limits, expensive queries, upload and workflow budgets |
| API5:2023 | Broken Function Level Authorization | role and administrative action checks |
| API6:2023 | Unrestricted Access to Sensitive Business Flows | business logic, payments, automation and anti-abuse |
| API7:2023 | Server Side Request Forgery | URL fetchers, webhooks, integrations and parsers |
| API8:2023 | Security Misconfiguration | CORS, TLS, errors, default endpoints and configuration |
| API9:2023 | Improper Inventory Management | endpoint discovery, versions, environments and retirement |
| API10:2023 | Unsafe Consumption of APIs | third-party response validation, timeouts and trust boundaries |

## 3. OWASP GenAI Top 10 for LLM Applications:2026

Use the current 2026 identifiers for LLM components. The official guide includes detailed scenarios,
mitigations and mappings; use the pinned source in standards.lock.json for exact requirements.

| ID | Category | Audit areas |
|---|---|---|
| LLM01:2026 | Prompt Injection | direct/indirect input, RAG, multimodal content, memory and tool output |
| LLM02:2026 | Sensitive Information Disclosure | model output, retrieval access, logs and external channels |
| LLM03:2026 | Excessive Agency | permissions, tool access, autonomy and approval boundaries |
| LLM04:2026 | Supply Chain | models, datasets, tools, registries and build provenance |
| LLM05:2026 | Data and Model Poisoning | training, fine-tuning, retrieval corpora and persistent memory |
| LLM06:2026 | Unbounded Consumption | inference cost, token limits, queueing and denial of service |
| LLM07:2026 | Misinformation | unsafe reliance, validation and consequential decisions |
| LLM08:2026 | Hidden Context Exposure | prompts, hidden context, reasoning or internal metadata |
| LLM09:2026 | Vector and Embedding Weaknesses | vector stores, retrieval isolation and embedding pipelines |
| LLM10:2026 | Improper Output Handling | output validation, rendering, code execution and downstream sinks |

## 4. OWASP Top 10 for Agentic Applications:2026

For systems where models can plan and take actions, pair the LLM mapping above with the agentic
categories below. Review goal boundaries, identity, tool authorization, memory, inter-agent messages,
human approvals, runtime containment and cascading impact.

| ID | Category |
|---|---|
| ASI01 | Agent Goal Hijack |
| ASI02 | Tool Misuse and Exploitation |
| ASI03 | Identity and Privilege Abuse |
| ASI04 | Agentic Supply Chain Vulnerabilities |
| ASI05 | Unexpected Code Execution (RCE) |
| ASI06 | Memory & Context Poisoning |
| ASI07 | Insecure Inter-Agent Communication |
| ASI08 | Cascading Failures |
| ASI09 | Human-Agent Trust Exploitation |
| ASI10 | Rogue Agents |

## 5. Other OWASP resources

| Resource | Use |
|---|---|
| ASVS v5.0.0 | Testable application requirements; see ASVS_MAPPING.md |
| Web Security Testing Guide | Test procedures for authentication, authorization, business logic and web behavior |
| Cheat Sheet Series | Implementation guidance for a specific control |
| Software Assurance Maturity Model | Organizational process maturity where in scope |
| Proactive Controls | Developer-facing secure design and implementation guidance |
| Top 10 CI/CD Security Risks | Pipeline threat modeling and hardening |
| Agent Control Standard | Agent visibility, traceability and runtime control; check edition before citing |

## 6. Other standards

- CWE is the weakness taxonomy; see CWE_MAPPING.md.
- CVE, NVD, OSV and GitHub Security Advisories identify specific vulnerable versions. Confirm the
  affected range against the advisory and package ecosystem, not just a scanner summary.
- NIST SSDF (SP 800-218) supports secure development process findings.
- NIST SP 800-61 supports incident handling; NIST SP 800-63 supports digital identity controls.
- CISA Secure by Design and CIS Benchmarks inform secure defaults and infrastructure review.
- SLSA supports build provenance and supply-chain assurance.

Official documentation for the language, framework, database, library and cloud provider in use
takes precedence over a general checklist. See standards.lock.json before using any identifier.
