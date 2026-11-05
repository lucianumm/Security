# CWE MAPPING

Common Weakness Enumeration identifiers for the weakness classes this skill reports. Use the most
specific CWE that fits; when unsure, cite the parent class rather than guessing a number. Verify at
`https://cwe.mitre.org/` when you have network access.

Format in a finding: `CWE: CWE-89 (Improper Neutralization of Special Elements used in an SQL
Command)`.

---

## Access control

| CWE | Weakness | Module |
| --- | --- | --- |
| CWE-284 | Improper Access Control (parent) | `../modules/authorization.md` |
| CWE-285 | Improper Authorization | `../modules/authorization.md` |
| CWE-862 | Missing Authorization | `../modules/authorization.md` |
| CWE-863 | Incorrect Authorization | `../modules/authorization.md` |
| CWE-639 | Authorization Bypass Through User-Controlled Key (IDOR) | `../modules/authorization.md` |
| CWE-566 | Authorization Bypass Through User-Controlled SQL Primary Key | `../modules/database.md` |
| CWE-269 | Improper Privilege Management | `../modules/authorization.md`, `../modules/docker.md` |
| CWE-1220 | Insufficient Granularity of Access Control | `../modules/authorization.md` |
| CWE-425 | Direct Request / Forced Browsing | `../modules/api.md` |
| CWE-352 | Cross-Site Request Forgery | `../modules/api.md` §8 |
| CWE-601 | URL Redirection to Untrusted Site (open redirect) | `../modules/backend.md` |
| CWE-1021 | Improper Restriction of Rendered UI Layers (clickjacking) | `../modules/frontend.md` |

## Authentication, session and credentials

| CWE | Weakness | Module |
| --- | --- | --- |
| CWE-287 | Improper Authentication | `../modules/authentication.md` |
| CWE-306 | Missing Authentication for Critical Function | `../modules/authentication.md`, `../modules/api.md` |
| CWE-307 | Improper Restriction of Excessive Authentication Attempts | `../modules/authentication.md` |
| CWE-521 | Weak Password Requirements | `../modules/authentication.md` |
| CWE-522 | Insufficiently Protected Credentials | `../modules/secrets.md` |
| CWE-640 | Weak Password Recovery Mechanism | `../modules/authentication.md` |
| CWE-916 | Use of Password Hash With Insufficient Computational Effort | `../modules/authentication.md` |
| CWE-798 | Use of Hard-coded Credentials | `../modules/secrets.md` |
| CWE-259 | Use of Hard-coded Password | `../modules/secrets.md` |
| CWE-384 | Session Fixation | `../modules/sessions.md` |
| CWE-613 | Insufficient Session Expiration | `../modules/sessions.md` |
| CWE-614 | Sensitive Cookie Without `Secure` | `../modules/sessions.md` |
| CWE-1004 | Sensitive Cookie Without `HttpOnly` | `../modules/sessions.md` |
| CWE-347 | Improper Verification of Cryptographic Signature (JWT, webhooks) | `../modules/sessions.md`, `../modules/webhooks.md` |
| CWE-345 | Insufficient Verification of Data Authenticity | `../modules/webhooks.md` |
| CWE-294 | Authentication Bypass by Capture-Replay | `../modules/webhooks.md` |
| CWE-204 | Observable Response Discrepancy (user enumeration) | `../modules/authentication.md` |

## Injection and input handling

| CWE | Weakness | Module |
| --- | --- | --- |
| CWE-20 | Improper Input Validation | `../modules/backend.md` |
| CWE-89 | SQL Injection | `../modules/backend.md`, `../modules/database.md` |
| CWE-943 | Improper Neutralization in a Data Query (NoSQL) | `../modules/backend.md` |
| CWE-78 | OS Command Injection | `../modules/backend.md` |
| CWE-77 | Command Injection (parent) | `../modules/backend.md` |
| CWE-79 | Cross-site Scripting | `../modules/frontend.md` |
| CWE-1336 | Server-Side Template Injection | `../modules/backend.md` |
| CWE-611 | XML External Entity (XXE) | `../modules/uploads.md`, `../modules/backend.md` |
| CWE-502 | Deserialization of Untrusted Data | `../modules/backend.md` |
| CWE-1321 | Prototype Pollution | `../modules/backend.md` |
| CWE-1333 | Inefficient Regular Expression Complexity (ReDoS) | `../modules/backend.md` |
| CWE-915 | Improperly Controlled Modification of Object Attributes (mass assignment) | `../modules/api.md` |
| CWE-22 | Path Traversal | `../modules/backend.md`, `../modules/uploads.md` |
| CWE-73 | External Control of File Name or Path | `../modules/uploads.md` |
| CWE-434 | Unrestricted Upload of File with Dangerous Type | `../modules/uploads.md` |
| CWE-918 | Server-Side Request Forgery | `../modules/backend.md`, `../modules/webhooks.md` |
| CWE-1236 | Formula Injection in a CSV File | `../modules/backend.md` §5 |
| CWE-117 | Improper Output Neutralization for Logs | `../modules/logging.md` |
| CWE-444 | HTTP Request Smuggling | `../modules/nginx.md` |
| CWE-113 | HTTP Response Splitting | `../modules/backend.md` |

## Cryptography and data protection

| CWE | Weakness | Module |
| --- | --- | --- |
| CWE-327 | Use of a Broken or Risky Cryptographic Algorithm | `../modules/cryptography.md` |
| CWE-328 | Use of Weak Hash | `../modules/cryptography.md` |
| CWE-326 | Inadequate Encryption Strength | `../modules/cryptography.md` |
| CWE-330 | Use of Insufficiently Random Values | `../modules/cryptography.md` |
| CWE-338 | Use of Cryptographically Weak PRNG | `../modules/cryptography.md` |
| CWE-321 | Use of Hard-coded Cryptographic Key | `../modules/cryptography.md`, `../modules/secrets.md` |
| CWE-323 | Reusing a Nonce/Key Pair | `../modules/cryptography.md` |
| CWE-311 | Missing Encryption of Sensitive Data | `../modules/database.md`, `../modules/cryptography.md` |
| CWE-319 | Cleartext Transmission of Sensitive Information | `../modules/nginx.md`, `../modules/frontend.md` |
| CWE-312 | Cleartext Storage of Sensitive Information | `../modules/secrets.md`, `../modules/database.md` |
| CWE-359 | Exposure of Private Personal Information | privacy items, `../modules/api.md` §3 |
| CWE-200 | Exposure of Sensitive Information to an Unauthorized Actor | `../modules/api.md`, `../modules/backend.md` §14 |
| CWE-532 | Insertion of Sensitive Information into Log File | `../modules/logging.md` |
| CWE-209 | Generation of Error Message Containing Sensitive Information | `../modules/backend.md` §14 |
| CWE-524 | Use of Cache Containing Sensitive Information | `../modules/cloud.md` §CDN, `../modules/database.md` §Cache |

## Configuration, infrastructure and supply chain

| CWE | Weakness | Module |
| --- | --- | --- |
| CWE-16 | Configuration | `../modules/nginx.md`, `../modules/cloud.md` |
| CWE-1188 | Insecure Default Initialization of Resource | `../modules/database.md`, `../modules/docker.md` |
| CWE-732 | Incorrect Permission Assignment for Critical Resource | `../modules/cloud.md`, `../modules/docker.md` |
| CWE-250 | Execution with Unnecessary Privileges | `../modules/docker.md`, `../modules/kubernetes.md` |
| CWE-693 | Protection Mechanism Failure (missing headers, missing gate) | `../modules/frontend.md`, `../modules/ci-cd.md` |
| CWE-942 | Permissive Cross-domain Policy (CORS) | `../modules/api.md` §7 |
| CWE-1104 | Use of Unmaintained Third Party Components | `../modules/supply-chain.md` |
| CWE-1395 | Dependency on Vulnerable Third-Party Component | `../modules/supply-chain.md` |
| CWE-494 | Download of Code Without Integrity Check | `../modules/supply-chain.md` |
| CWE-829 | Inclusion of Functionality from Untrusted Control Sphere | `../modules/frontend.md` §6, `../modules/ci-cd.md` |
| CWE-1357 | Reliance on Insufficiently Trustworthy Component | `../modules/supply-chain.md` |
| CWE-489 | Active Debug Code | `../modules/backend.md` §15 |
| CWE-215 | Insertion of Sensitive Information Into Debugging Code | `../modules/backend.md` §15 |
| CWE-548 | Exposure of Information Through Directory Listing | `../modules/nginx.md` |
| CWE-527 | Exposure of Version-Control Repository to an Unauthorized Control Sphere | `../modules/nginx.md` |

## Availability, logic and operations

| CWE | Weakness | Module |
| --- | --- | --- |
| CWE-770 | Allocation of Resources Without Limits or Throttling | `../modules/api.md` §5–6 |
| CWE-400 | Uncontrolled Resource Consumption | `../modules/api.md` §6 |
| CWE-409 | Improper Handling of Highly Compressed Data (zip bomb) | `../modules/uploads.md` |
| CWE-362 | Race Condition | `../modules/backend.md` §12, `../modules/business-logic.md` |
| CWE-367 | Time-of-check Time-of-use (TOCTOU) | `../modules/backend.md` §12 |
| CWE-799 | Improper Control of Interaction Frequency | `../modules/api.md`, `../modules/business-logic.md` |
| CWE-840 | Business Logic Errors | `../modules/business-logic.md` |
| CWE-841 | Improper Enforcement of Behavioral Workflow | `../modules/business-logic.md` |
| CWE-602 | Client-Side Enforcement of Server-Side Security | `../modules/frontend.md` §7, `../modules/payments.md` |
| CWE-778 | Insufficient Logging | `../modules/logging.md` |
| CWE-223 | Omission of Security-relevant Information | `../modules/logging.md` |
| CWE-1427 | Improper Neutralization of Input Used for LLM Prompting | `../modules/ai-security.md` |
