# Attack Surface & System Inventory — <project name>

<!--
Template for security/ATTACK_SURFACE.md. Produced in phases 2 and 5 of ../core/WORKFLOW.md.
Only list what actually exists. Mark anything inferred as "inferred" and verify it.
-->

Date: <YYYY-MM-DD> · Commit: <sha>

---

## 1. System inventory

### Applications and services

| Name | Type | Language/Framework | Deployed to | Public | Notes |
| --- | --- | --- | --- | --- | --- |

### Datastores

| Store | Engine/Version | Location | Public | Data classes | Credential scope |
| --- | --- | --- | --- | --- | --- |

### Infrastructure

| Component | Detail | Managed by | Exposure |
| --- | --- | --- | --- |
| Reverse proxy | | | |
| CDN / WAF | | | |
| Containers / orchestration | | | |
| Cloud accounts / projects | | | |
| CI/CD | | | |
| Domains and known subdomains | | | |

### Background processing

| Job / worker / cron | Trigger | Runs as | Handles user input | Notes |
| --- | --- | --- | --- | --- |

### External integrations

| Provider | Purpose | Direction | Auth method | Data shared | Credential location |
| --- | --- | --- | --- | --- | --- |

### Secrets consumed *(names only — never values)*

| Name | Purpose | Source | Environments | Rotatable |
| --- | --- | --- | --- | --- |

## 2. Data handled

| Data | Class | Collected where | Stored where | Transmitted to | Retention |
| --- | --- | --- | --- | --- | --- |

Classes: `PUBLIC` `INTERNAL` `CONFIDENTIAL` `SENSITIVE` `CRITICAL`.

## 3. Entry points

### HTTP routes

| Method | Path | Auth | Authorization rule | Input validation | Rate limit | Returns | Risk notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GET | /api/invoices/:id | session | **none** | — | none | full invoice | SEC-0001 |

Include every route: public pages, authenticated pages, API, admin, legacy/versioned, internal,
health, metrics, debug, docs/playgrounds, static file serving.

### Non-HTTP entry points

| Type | Identifier | Auth | Authorization | Validation | Notes |
| --- | --- | --- | --- | --- | --- |
| WebSocket | | | | | |
| GraphQL operation | | | | | |
| Server action / RPC | | | | | |
| Webhook (inbound) | | | | | |
| Queue consumer | | | | | |
| Scheduled job | | | | | |
| CLI / admin script | | | | | |
| Email/file ingestion | | | | | |

### High-risk feature classes present

| Feature | Where | Module to apply |
| --- | --- | --- |
| File upload | | `../modules/uploads.md` |
| File download | | `../modules/uploads.md` |
| URL fetched server-side | | `../modules/backend.md` §SSRF |
| Redirect with a user-supplied target | | `../modules/backend.md` §Open redirect |
| HTML/Markdown rendering of user content | | `../modules/frontend.md` §XSS |
| Report / PDF generation | | `../modules/api.md` §Resource exhaustion |
| Search | | `../modules/api.md`, `../modules/database.md` |
| Bulk export / import | | `../modules/authorization.md`, `../modules/business-logic.md` |
| Payments | | `../modules/payments.md` |
| AI / LLM | | `../modules/ai-security.md` |
| Impersonation / support tooling | | `../modules/authorization.md` |

## 4. Architecture

```text
<real architecture diagram in text — components, direction of calls, protocols>
```

| Component | Function | Trust level | Inputs | Outputs | Data handled | Auth | Exposure |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 5. Trust boundaries

| # | Boundary | What crosses it | Authentication | Authorization | Validation | Failure mode |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Internet → Edge | HTTP requests | — | — | | |
| 2 | Browser → API | requests + session | | | | |
| 3 | API → Database | queries | | | | |
| 4 | API → Third party | outbound calls | | | | |
| 5 | Provider → Webhook | signed events | | | | |
| 6 | Tenant A → Shared app | identifiers | | | | |
| 7 | CI → Production | deploy credentials | | | | |
| 8 | LLM output → Tools | tool calls | | | | |

## 6. Exposure summary

- Publicly reachable without authentication: <n> endpoints — list the ones returning data.
- Reachable only with authentication: <n>.
- Administrative: <n> — protection level.
- Undocumented/legacy endpoints found: <list>.
- Endpoints with no rate limiting on an expensive operation: <list>.
- Ports/services exposed at the network level: <list> (source of evidence).

## 7. Gaps in this inventory

<What could not be enumerated and why — e.g. "routes registered dynamically by a plugin loader",
"cloud resources not visible without console access". These become `NOT_VERIFIED` controls.>
