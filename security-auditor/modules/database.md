# MODULE — DATABASE, CACHE AND DATA LAYER

Scope: relational and NoSQL databases, ORM usage, migrations, network exposure, credentials,
encryption, retention, plus Redis/Memcached and search indexes.

Related: `backend.md` §SQL/NoSQL injection, `authorization.md` §Multi-tenancy, `secrets.md`,
`backup.md`.
Standards: ASVS v5.0.0 V1 (Encoding and Sanitization), V8 (Authorization), V11 (Cryptography), V14 (Data Protection), CWE-89, CWE-311, CWE-256, CWE-566, CWE-1188.

---

## 1. Discovery

```bash
grep -rniE "postgres|mysql|mariadb|mongodb|sqlite|redis|memcached|elasticsearch|opensearch|clickhouse|dynamodb|firestore|supabase|planetscale|neon" \
  --include=*.json --include=*.yml --include=*.yaml --include=*.env* --include=*.ts --include=*.py --include=*.php . -l | head
ls -d prisma migrations db/migrate alembic knex drizzle 2>/dev/null
grep -rniE "DATABASE_URL|DB_HOST|DB_USER|MONGO_URI|REDIS_URL" . -l | head
```

Record for each datastore: engine and version, where it runs, who can reach it, which credentials
the app uses, what data it holds (`SENSITIVE`/`CRITICAL` classes), and whether it is shared with
other systems or environments.

## 2. Network exposure

- Is the database reachable from the public internet? Check bind address (`0.0.0.0`), published
  container ports (`docker.md`), cloud security groups / firewall rules (`cloud.md`), and managed
  service network settings.
- Public exposure of Postgres 5432, MySQL 3306, MongoDB 27017, Redis 6379, Elasticsearch 9200,
  ClickHouse 8123 is HIGH; with weak/absent authentication it is CRITICAL.
- Prefer private networking, VPC peering, or an SSH/VPN tunnel; never "it's on a random port".

## 3. Authentication and privileges

- The application uses a dedicated, non-superuser account. Flag `root`, `postgres`, `sa`, `admin`
  and any account with `SUPERUSER`, `GRANT ALL`, or DDL rights it does not need at runtime.
- Separate credentials per environment and per service; no shared password across environments.
- Migration credentials separate from runtime credentials where feasible.
- Password strength and storage (`secrets.md`); no credentials in code, compose files or client
  bundles.
- Managed-service IAM auth or certificate auth preferred where available.
- Default accounts removed; anonymous access disabled (MongoDB without auth, Redis without
  `requirepass`, Elasticsearch with security disabled).

## 4. Transport and at-rest encryption

- TLS enforced for client connections (`sslmode=require|verify-full`, `ssl: true`, `tls: true`);
  certificate verification not disabled.
- Encryption at rest enabled (managed service setting or disk encryption).
- Application-level encryption for the most sensitive columns where warranted (identity documents,
  financial identifiers, health data, tokens) — see `cryptography.md`.
- Field-level hashing for values that never need to be read back.

## 5. Query safety

Covered in depth in `backend.md` §2–3. Additionally at this layer:

- Are raw queries centralized and reviewable, or scattered?
- Does the ORM's escape hatch get used with user input (`$queryRaw`, `DB::raw`, `literal`,
  `Sequelize.literal`, `extra()`)?
- Are dynamic `ORDER BY`/column names allowlisted?
- Are statement timeouts and connection pool limits configured (a slow query is an availability
  issue and a resource-exhaustion vector)?
- Are transactions used where invariants require them (`backend.md` §Concurrency)?

## 6. Tenant and ownership enforcement at the data layer

- Row-level security (Postgres RLS, Supabase policies) enabled where the architecture relies on it —
  **verify the policies**, not just that RLS is "on"; a permissive `USING (true)` policy is
  equivalent to no policy.
- Global query scopes / repository-level filters that cannot be bypassed by a new query.
- Soft-deleted records excluded from reads.
- Views and materialized views inherit the same restrictions.
- Direct database access from a client (Supabase/Firebase style) is only safe with verified rules —
  audit the rules file as application authorization, and treat missing rules as CRITICAL.

Firebase/Firestore rules and Supabase policies deserve line-by-line review; a rule of
`allow read, write: if true;` or `if request.auth != null;` on tenant data is a finding.

## 7. Migrations

- Migrations are versioned, reviewed and reversible where possible.
- Destructive migrations (drop column/table, type narrowing, data backfill) are flagged for human
  execution; never run them automatically (`../core/SAFETY.md` §3).
- Migration jobs do not run with superuser rights in production if avoidable.
- Seeds do not create default admin accounts or test users in production
  (`admin@example.com/admin123` in a production seed is CRITICAL).
- No production data copied into development/test environments without anonymization.

## 8. Logging and monitoring at the data layer

- Slow query log and error log enabled, without logging parameter values that contain secrets/PII.
- Failed authentication attempts to the database are logged and alerted.
- Audit logging for schema changes and privileged operations where the engine supports it.
- Application logs must not contain full queries with personal data (`logging.md`).

## 9. Retention and privacy

- Is there a retention policy per data class? Are old records, soft-deleted rows, audit trails and
  exports ever purged?
- Does account deletion actually delete or anonymize the data (including backups policy, caches,
  search indexes, analytics and third-party processors)?
- Are analytics/BI copies of personal data governed by the same controls?
- See `../references/CHECKLIST_GLOBAL.md` §Privacy for the minimization questions.

## 10. Cache (Redis / Memcached)

- Not exposed publicly; `requirepass`/ACL configured; TLS where supported; `protected-mode` on.
- Dangerous commands restricted where possible (`FLUSHALL`, `CONFIG`, `KEYS`, `DEBUG`,
  `SCRIPT`/`EVAL` if untrusted input can reach it).
- Cache keys include tenant/user scoping — a missing scope is a cross-user data leak (HIGH).
- Sensitive values (sessions, tokens, PII) have a TTL and, where relevant, are encrypted.
- Cache stampede/poisoning: can a user influence the key or the cached value for another user?
- Persistence files (`dump.rdb`, `appendonly.aof`) are protected and not inside a web root.
- Session store separated from a general-purpose cache that gets flushed.

## 11. Search indexes and analytics stores

Elasticsearch/OpenSearch/Meilisearch/Algolia: authentication enabled, not publicly exposed,
tenant filtering enforced **server-side** (an API key in the browser with search-only rights still
searches every tenant unless filters are enforced by the key), and no sensitive fields indexed
unnecessarily.

## 12. Regression tests

Cross-tenant query returns nothing · a raw-query endpoint rejects an injection payload · the app
cannot connect with the migration/superuser credential · RLS policy denies a foreign tenant row ·
cache key includes the tenant id (unit test on the key builder) · connection uses TLS.
