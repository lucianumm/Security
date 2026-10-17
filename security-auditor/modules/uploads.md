# MODULE — FILE UPLOAD, DOWNLOAD AND OBJECT STORAGE

Scope: accepting files from users, storing them, serving them back, and the storage services behind
that (S3, R2, GCS, Azure Blob, Supabase, Firebase, local disk).

Related: `backend.md` §Path traversal, `authorization.md`, `cloud.md`, `frontend.md`.
Standards: ASVS v5.0.0 V5 (File Handling) and V14 (Data Protection), CWE-434, CWE-22, CWE-73, CWE-409, OWASP Top 10:2025 A01/A02/A05.

---

## 1. Discovery

```bash
grep -rniE "multer|formidable|busboy|multipart|FileInterceptor|request\.files|\$_FILES|MultipartFile|ActiveStorage|CarrierWave|upload|putObject|getSignedUrl|createPresignedPost|blob|bucket" src app lib config | head -50
```

Map every upload path (including avatar, attachment, import, logo, document, bulk import, drag-drop,
rich-text image paste, and API-only endpoints) and every download/serve path.

## 2. Upload controls

| Control | Requirement |
| --- | --- |
| Authentication | Required unless deliberately public; anonymous upload needs strong justification and quotas |
| Authorization | The user may upload **to this resource**; verify ownership/tenant |
| Extension | Allowlist, never a blocklist; check the final extension after normalization |
| Declared MIME | Validated, but **never trusted** — the client sets it |
| Content sniffing | Magic-byte/type detection server-side (`file-type`, `python-magic`, `Tika`), and it must agree with the extension |
| Size | Per-file and per-request limits enforced at the proxy **and** the application |
| Count / quota | Per request, per user, per tenant, per time window |
| Filename | Never used as-is: generate a UUID/ULID; store the original name separately, escaped; strip path separators, null bytes, control chars, unicode tricks; cap length |
| Storage location | Outside the web root, or in object storage; never in a directory that executes code |
| Execution | The storage path must not be able to run PHP/JSP/CGI; disable execution at the server level too |
| Overwrite | A user cannot overwrite another user's (or a system) object |
| Malware | Scan where feasible (ClamAV, provider scanning) for user-shared files |
| Image handling | Re-encode/normalize images; strip EXIF (privacy: GPS) ; validate dimensions before decoding |
| Processing | Run heavy conversion out of the request path, with timeouts and resource limits |

## 3. Dangerous file types

- **SVG**: contains scripts and external references. Never serve inline from the app origin unless
  sanitized (allowlist-based, e.g. DOMPurify with SVG profile) — otherwise serve as an attachment
  from a separate origin, with `Content-Disposition: attachment` and `nosniff`.
- **HTML/HTM/XHTML/MHTML**: stored XSS on your origin if served inline. Force download or a
  sandboxed, separate domain.
- **Archives (zip, tar, gz, 7z, rar)**: zip-slip path traversal on extraction, decompression bombs,
  symlink entries, nested archives. Validate each entry's resolved path, cap the total uncompressed
  size, entry count and nesting depth, and refuse symlinks.
- **PDF/Office**: may contain scripts, macros and remote content. Do not render in a privileged
  context; consider CDR/flattening for high-risk workflows.
- **Polyglots**: a file valid as both image and script/HTML — magic-byte checking plus re-encoding
  plus a separate serving origin defeats most of these.
- **Executables and scripts** (`.php`, `.jsp`, `.asp`, `.exe`, `.sh`, `.bat`, `.js`, `.jar`): reject
  unless the product genuinely requires them; if it does, store them where nothing executes them.
- **XML** (including `.docx`, `.svg`, `.xlsx` internals): XXE — disable external entities and DTD
  processing in every XML parser (`libxml_disable_entity_loader`, `defusedxml`,
  `XMLConstants.FEATURE_SECURE_PROCESSING`, `noent: false`).

## 4. Serving files back

| Control | Requirement |
| --- | --- |
| Authorization | Checked on every download, including thumbnails, previews and direct object URLs |
| Ownership / tenant | Enforced; an object key must not be guessable *and* unprotected |
| Path handling | No user-supplied path; resolve and confine (`backend.md` §7) |
| `Content-Type` | Set explicitly from the validated type; never echo the stored client value |
| `X-Content-Type-Options` | `nosniff` on every file response |
| `Content-Disposition` | `attachment` for anything not intentionally rendered; sanitize the filename parameter (RFC 5987 encoding, no CRLF) |
| Origin separation | User content served from a distinct domain/subdomain (cookieless) where possible |
| Caching | Private/sensitive files must not be cached by CDN or shared caches (`Cache-Control: private, no-store`) |
| Signed URLs | Short expiry, scoped to one object and one method, not reusable across users, not logged |
| Range/large files | Streaming with limits; no unbounded memory reads |

## 5. Object storage configuration

Audit the bucket/container itself (`cloud.md` for provider specifics):

- Public access blocked at the account and bucket level unless the bucket is intentionally a public
  CDN origin; list permissions denied.
- Bucket policy/ACL grants only the roles that need it; no `Principal: *` with write.
- Presigned upload policies constrain content type, size and key prefix — otherwise a user can
  upload anywhere in the bucket or upload arbitrary types.
- CORS configuration on the bucket restricted to your origins.
- Versioning and lifecycle rules defined; deletion protection where needed.
- Encryption at rest enabled; SSE-KMS where the data class warrants it.
- Access logging enabled.
- Separate buckets per environment; production credentials never in a client app.
- Firebase/Supabase storage rules reviewed line by line (`database.md` §6).

## 6. Common critical findings

Upload endpoint without authentication · file written into the web root with the client's filename ·
`.php`/`.jsp` upload accepted and reachable · download endpoint that accepts a path
(`/download?file=../../.env`) · presigned URL generated for any key the client requests ·
public bucket containing customer documents · SVG served inline from the application origin ·
zip extraction without path validation · unbounded file size enabling disk exhaustion.

## 7. Regression tests

Disallowed extension rejected · declared MIME lying about content rejected (magic bytes checked) ·
oversized file rejected · traversal filename (`../../evil.sh`, `..\\evil`) neutralized · another
user's object id/key returns 403/404 · uploaded `.svg` is served with `attachment` +`nosniff`
(or sanitized) · zip entry escaping the target directory is refused · presigned URL expires and
cannot be reused for a different key.
