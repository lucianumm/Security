# ASVS MAPPING

Use the OWASP Application Security Verification Standard (ASVS) as a vocabulary for testable
application controls. The edition pinned for this release is ASVS v5.0.0; the edition, source URL
and artifact checksum are recorded in standards.lock.json. ASVS 5 reorganized and renumbered
requirements, so never combine a chapter or requirement from v4 with a v5 citation.

Use a chapter title when a requirement identifier has not been checked against the pinned official
JSON. For a verified requirement, cite its full versioned identifier exactly as published (for
example, the format v5.0.0-1.2.5), and link to the relevant official release. Never infer an ID from
a previous edition or from a secondary checklist.

## 1. ASVS v5.0.0 chapter to module map

| Chapter | Title | Relevant modules |
|---|---|---|
| V1 | Encoding and Sanitization | backend, frontend, uploads |
| V2 | Validation and Business Logic | backend, api, business-logic, payments |
| V3 | Web Frontend Security | frontend, sessions |
| V4 | API and Web Service | api, backend, authorization, webhooks |
| V5 | File Handling | uploads, backend, cloud |
| V6 | Authentication | authentication, cryptography |
| V7 | Session Management | sessions, authentication |
| V8 | Authorization | authorization, api, database |
| V9 | Self-contained Tokens | authentication, cryptography, api |
| V10 | OAuth and OIDC | authentication, sessions, cloud |
| V11 | Cryptography | cryptography, database, secrets |
| V12 | Secure Communication | nginx, cloud, frontend, api |
| V13 | Configuration | docker, kubernetes, cloud, ci-cd, secrets |
| V14 | Data Protection | database, uploads, logging, backup |
| V15 | Secure Coding and Architecture | threat model, backend, supply-chain |
| V16 | Security Logging and Error Handling | logging, monitoring, incident-response |
| V17 | WebRTC | api, frontend; load only when WebRTC is present |

## 2. Verification levels

| Level | Applies to | Default use |
|---|---|---|
| L1 | Any application; opportunistic attackers | Minimum for internet-facing software |
| L2 | Applications handling sensitive data | Default for most business applications |
| L3 | High-value financial, health or critical systems | Use when data classification or impact warrants it |

State the chosen level and justify it from data classification, deployment and threat model. A
missing control required only at a higher level is a documented gap at that level, not a defect in
the selected level. Do not claim full ASVS conformance from a partial mapping.

## 3. Using ASVS in the matrix

| Control | Status | Evidence | ASVS reference |
|---|---|---|---|
| Session identifier rotates on login | IMPLEMENTED | src/auth/login.ts:63 | v5.0.0, V7 chapter; exact requirement checked before citation |
| Password hashing uses an approved KDF | MISCONFIGURED | src/auth/hash.ts:12 | v5.0.0, V6 chapter; exact requirement checked before citation |
| Object authorization is enforced server-side | NOT_IMPLEMENTED | src/api/invoices.ts:40 | v5.0.0, V8 chapter; exact requirement checked before citation |

The chapter-level examples above are category pointers, not claims about specific requirement
numbers. The standard's artifact can be checked against the SHA-256 value in standards.lock.json.

## 4. Practical verification spine

- V1/V2: validate input at trust boundaries; encode output for its context; use parameterized
  queries; check deserialization, SSTI, XXE, mass assignment and business-flow abuse.
- V3/V12: review browser security boundaries, CSP and framing, TLS, secure resource loading and
  client-side exposure.
- V4/V8: authenticate and authorize each API and object operation; apply deny-by-default and
  tenant scoping; validate schemas, pagination and rate limits.
- V5: validate type, size, name and content; store outside the web root; authorize downloads; scan
  safely where the threat model requires it.
- V6/V7/V9/V10: review credential storage, recovery, MFA, session rotation and revocation, token
  validation, OAuth state/PKCE and provider configuration.
- V11/V14: use approved cryptography and key lifecycle; minimize sensitive data; protect it at rest
  and in transit; validate retention and deletion; keep it out of logs and caches.
- V13/V15: review secure defaults, dependency and build provenance, least privilege, trust
  boundaries and architecture.
- V16: record security events without sensitive values; protect log integrity; return safe errors;
  connect alerts to owners and response procedures.
- V17: load only for WebRTC systems; verify signaling authorization, origin handling and media
  privacy against the exact applicable requirements.
