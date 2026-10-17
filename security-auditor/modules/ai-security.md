# MODULE — AI / LLM SECURITY

Load when the project calls an LLM API, embeds a model, implements RAG, exposes a chat feature, or
runs agents with tools.

Core principle:

> Any content originating from a user, a web page, a document, an email, a database record, an API
> response or another model is **untrusted data**. It can never modify the agent's policies, and it
> can never authorize an action.

Related: `backend.md` §SSRF, `authorization.md`, `secrets.md`, `api.md` §Resource exhaustion.
Standards: OWASP GenAI LLM Top 10:2026, OWASP Agentic Top 10:2026, NIST AI RMF, MITRE ATLAS (reference), CWE-1427. Use the editions in ../references/standards.lock.json.

---

## 1. Discovery

```bash
grep -rniE "openai|anthropic|@ai-sdk|langchain|llama|ollama|gemini|bedrock|vertex|huggingface|embedding|pinecone|weaviate|qdrant|chroma|pgvector|system ?prompt|tool_?call|function_?call" . -l | head -30
```

Map: which models, which providers, where prompts are built, what data enters the prompt, what the
model's output is used for, and which tools/functions the model can invoke.

## 2. Credentials and cost

- Provider API keys server-side only; a key in a client bundle or mobile app is CRITICAL (direct
  financial loss plus abuse).
- No client-side proxying that forwards arbitrary requests to the provider without authentication
  and quotas.
- Per-user and per-tenant token/cost quotas, request rate limits, maximum input and output tokens,
  concurrency caps, and a hard monthly budget with alerting.
- Timeouts and cancellation so an abandoned request stops billing.

## 3. Prompt injection (direct and indirect)

Direct: the user tries to override the system prompt. Indirect: injected instructions arrive inside
a document, web page, PDF, email, code comment, database field, filename, image (OCR/vision), or a
tool's response — and are far more dangerous because the user may not be the attacker.

There is no complete defense through prompting. Mitigate by architecture:

| Control | Detail |
| --- | --- |
| Separation | Keep instructions and data in distinct channels/roles; clearly delimit untrusted content and state that it is data |
| Least privilege for tools | The model gets the minimum set of tools; dangerous tools are not exposed to a session handling untrusted content |
| Independent authorization | Every tool call is authorized against the **user's** permissions server-side, not by the model's judgment (`authorization.md`) |
| Human confirmation | Irreversible or outward-facing actions (sending messages, payments, deletions, publishing, permission changes) require explicit user confirmation |
| Output as data | Never `eval` model output, never pass it to a shell, SQL, template or file path without validation (`backend.md`) |
| Constrained outputs | Structured output/JSON schema validation before use; reject anything unexpected |
| No secret in the prompt | System prompts leak; keep credentials, internal URLs and other users' data out of them |
| Content provenance | Track source, trust and tenant for every context item; filtering can reduce risk but does not prevent prompt injection |
| Egress control | Prevent data exfiltration via rendered markdown images/links to attacker URLs; sanitize model output before rendering (`frontend.md` §XSS) |
| Monitoring | Log actor, policy decision, tool name, target class, result and correlation id; do not retain prompt/response bodies by default, and redact before any approved sampling |

## 4. Agents and tools

- Enumerate every tool: what it can do, what it can reach, what it can spend, and whether the effect
  is reversible.
- Tools that write, pay, message, deploy or delete need: server-side authorization, an allowlist of
  targets, rate limits, an audit log, and confirmation for irreversible effects.
- Bound the agent loop: maximum steps, maximum time, maximum cost, and a stop condition.
- Sandbox code execution (container, no network, no credentials, resource limits, ephemeral) — a
  code-interpreter tool with production credentials in the environment is CRITICAL.
- Network access from tools follows the SSRF rules (`backend.md` §6) — a browsing tool is a
  full SSRF primitive unless restricted.
- Multi-agent systems: a message from another agent is untrusted input, not an instruction.
- Enforce a deterministic policy check on every proposed action; re-authorize at execution time,
  apply target and argument allowlists, and bind credentials to the server-side tool rather than the
  model context.
- Treat MCP servers, plugins, tool schemas/descriptions, model files, datasets and vector indexes
  as supply-chain inputs. Pin and verify versions and provenance; review updates before execution.
- Restrict tool egress and filesystem access, run code in an ephemeral sandbox without credentials,
  and enforce CPU, memory, time, process and output limits. A prompt or a container alone is not a
  sandbox boundary.

## 5. RAG and data boundaries

- Retrieval must be filtered by the **user's** permissions and tenant at query time; embedding a
  document into a shared index without access metadata leaks it to everyone (HIGH–CRITICAL).
- Vector stores need the same authorization, encryption and retention controls as the primary
  database (`database.md`).
- Ingested content is untrusted (see §3) — sanitize and mark it.
- Test retrieval filters against cross-tenant IDs, metadata spoofing, stale permissions, deleted
  documents, and poisoning of indexed content.
- Document ingestion pipelines: file type validation, size limits, archive and XXE handling
  (`uploads.md`).
- Deletion must propagate to the index and to any cached embeddings.
- Do not send `SENSITIVE`/`CRITICAL` data to a third-party model provider without a data processing
  agreement, a no-training guarantee and the user's awareness — flag as a privacy finding with the
  data classes involved.

## 6. Output handling

- Render model output as text/sanitized markdown; never as raw HTML (`frontend.md`).
- Validate structured output against a schema before it touches business logic.
- Do not display another user's data because the model produced it — re-check authorization on
  anything the model retrieved.
- Watch for hallucinated links, package names (slopsquatting risk in code suggestions) and commands;
  do not auto-execute them.
- Content safety: apply the provider's moderation where the product surface warrants it.

## 7. Abuse of the AI feature itself

Free-tier farming, prompt-based DoS (huge inputs, recursive tool loops), model extraction, and using
your API as a free proxy to the provider. Controls: authentication, quotas, cost caps, input size
limits, loop bounds, and monitoring (`monitoring.md`).

## 8. Regression tests

Injected instruction inside a retrieved document does not cause a tool call · a tool call for
another user's resource is denied server-side · model output containing `<script>` is escaped when
rendered · structured output failing schema validation is rejected · token/cost quota returns 429 ·
retrieval filtered by tenant returns nothing for a foreign document id · no provider key present in
the client bundle.

## 9. Adversarial coverage map

For a model embedded as a component, map relevant scenarios to OWASP LLM 2026: prompt injection
(direct, indirect, split, encoded and multimodal), sensitive information disclosure, excessive
agency, model/tool/data supply chain, training or retrieval poisoning, unbounded consumption,
misinformation, hidden-context exposure, vector/embedding weaknesses and improper output handling.
For an agent that plans and acts, also map goal hijack, tool misuse, identity/privilege abuse, agentic
supply chain, unexpected code execution, memory/context poisoning, inter-agent communication,
cascading failures, human-agent trust exploitation and rogue behavior to OWASP Agentic 2026.

Use synthetic local fixtures and mock tool endpoints for regression tests. Do not send prompts,
private documents, source code or credentials to public model evaluation services without explicit
authorization and a disclosure review. Record which attack families were exercised and which remain
NOT_VERIFIED; a passing prompt-injection benchmark is not proof that injection is prevented.
