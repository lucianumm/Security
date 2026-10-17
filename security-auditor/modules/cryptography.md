# MODULE — CRYPTOGRAPHY

Scope: encryption, hashing, signing, randomness, key management, TLS configuration in application
code.

Related: `authentication.md` §Password storage, `sessions.md` §JWT, `secrets.md`, `nginx.md`.
Standards: ASVS v5.0.0 V11 (Cryptography), V6 (Authentication) and V9 (Self-contained Tokens), OWASP Top 10:2025 A04, CWE-327, CWE-328, CWE-330, CWE-321, CWE-326, CWE-916.

---

## 1. Discovery

```bash
grep -rniE "crypto\.|createCipher|createHash|createHmac|randomBytes|Math\.random|secrets\.|hashlib|Fernet|AES|RSA|ECDSA|Ed25519|openssl_|sodium_|bcrypt|argon2|jwt|sign\(|verify\(|encrypt|decrypt" src app lib | head -60
```

Answer first: **is this code implementing cryptography, or using a vetted library correctly?**
Home-made crypto (custom ciphers, custom KDFs, XOR "encryption", hand-rolled token formats,
"encrypt then base64 and call it a signature") is a finding regardless of apparent strength.

## 2. Algorithms

| Use | Acceptable | Flag |
| --- | --- | --- |
| Password hashing | Argon2id, scrypt, bcrypt, PBKDF2-HMAC-SHA256 (high iterations) | MD5, SHA-1, SHA-256 alone, reversible encryption, custom |
| Data hashing / integrity | SHA-256, SHA-384, SHA-512, BLAKE2/3 | MD5, SHA-1 (flag; acceptable only for non-security checksums, and say so) |
| MAC | HMAC-SHA-256+, Poly1305 | Hash of `secret + message` (length-extension) |
| Symmetric encryption | AES-256-GCM, ChaCha20-Poly1305, XSalsa20-Poly1305 (libsodium), AES-256-CBC **with** a separate HMAC | ECB mode (any), DES/3DES, RC4, Blowfish, CBC without integrity, `createCipher` (deprecated, key-derivation flaw) |
| Asymmetric | RSA ≥ 3072 with OAEP/PSS, ECDSA P-256+, Ed25519, X25519 | RSA < 2048, PKCS#1 v1.5 encryption, custom padding |
| Key exchange / transport | TLS 1.2+ (1.3 preferred) | SSLv3, TLS 1.0/1.1, disabled certificate verification |
| Randomness (security) | `crypto.randomBytes`, `crypto.getRandomValues`, `secrets`, `os.urandom`, `SecureRandom` | `Math.random`, `rand()`, `mt_rand`, `random.random`, timestamps, incrementing counters, UUIDv1 for secrets |

## 3. Mode and parameter correctness

- **IV/nonce**: unique per encryption, generated randomly (or a strict counter for GCM), never
  hardcoded, never reused with the same key. A fixed IV in the source is a finding.
- **GCM**: verify the auth tag is checked on decryption and associated data is used where relevant.
- **CBC**: requires an HMAC over ciphertext+IV (encrypt-then-MAC) and constant-time verification;
  otherwise padding-oracle exposure.
- **Comparisons**: use constant-time comparison for MACs, tokens, signatures and secrets
  (`crypto.timingSafeEqual`, `hmac.compare_digest`, `hash_equals`).
- **Key derivation**: HKDF for deriving keys from a high-entropy secret; a password-based KDF
  (Argon2/scrypt/PBKDF2) when derived from a password. Never use a raw password or a SHA of it as
  an AES key.
- **Encoding is not encryption**: base64, hex, ROT13 and JWT payloads are not confidentiality.

## 4. Key management

- Keys come from environment variables or a secret manager, never from source or the repository.
- Distinct keys per environment and per purpose (signing ≠ encryption ≠ session).
- Rotation is possible: key identifiers/versions stored with the ciphertext, old keys retained for
  decryption, a documented rotation procedure.
- Keys are not logged, not sent to the client, not stored in the database next to the data they
  protect.
- Hardware/KMS backing (AWS KMS, GCP KMS, Azure Key Vault, HSM) where the data class warrants it.
- Private keys have restrictive file permissions and are excluded from the repository and images.

## 5. Signing and verification

- Verify signatures with a pinned algorithm and the correct key; never let the message choose the
  algorithm (`sessions.md` §JWT).
- Webhook signatures: constant-time comparison, timestamp window, replay protection
  (`webhooks.md`).
- Signed URLs: include expiry, method and resource in the signed payload.
- Do not confuse encryption with authentication — encrypted data without integrity is malleable.

## 6. TLS in application code

Flag disabled verification anywhere:

```bash
grep -rnE "rejectUnauthorized: ?false|verify ?= ?False|InsecureSkipVerify|CURLOPT_SSL_VERIFYPEER, ?(0|false)|NODE_TLS_REJECT_UNAUTHORIZED|trustAllCerts|ALLOW_ALL_HOSTNAME_VERIFIER" . | head -20
```

Each occurrence is a finding (HIGH in production paths; MEDIUM in dev-only code with a clear guard).
Also check minimum TLS version, certificate pinning claims, and custom trust stores.

## 7. Data classification alignment

Confirm the crypto matches the data class from the audit's classification phase: identity
documents, health, financial and credential data should be encrypted at rest with managed keys and
access-logged. Tokenization or hashing is preferable where the plaintext is never needed.

## 8. Regression tests

Two encryptions of the same plaintext produce different ciphertext (IV uniqueness) · tampering with
ciphertext or tag causes a decryption failure, not silent acceptance · signature verification
rejects a wrong key and a modified payload · token generator output passes a basic entropy/length
assertion and is not derived from `Math.random` · constant-time comparison used for secret
comparison (unit-level assertion or code review evidence).
