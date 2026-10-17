# MODULE — DOCKER AND CONTAINERS

Scope: Dockerfiles, compose files, image contents, runtime privileges, networking and registry
hygiene.

Related: `kubernetes.md`, `cloud.md`, `supply-chain.md`, `secrets.md`.
Standards: CIS Docker Benchmark, ASVS v5.0.0 V13 (Configuration), OWASP Top 10:2025 A02, CWE-250, CWE-269, CWE-732, CWE-798.

---

## 1. Discovery

```bash
ls Dockerfile* docker-compose*.y*ml .dockerignore 2>/dev/null
grep -rn "" Dockerfile 2>/dev/null | head -60
docker images 2>/dev/null | head          # only if a daemon is available and the user allows it
```

## 2. Dockerfile review

| Check | Requirement | Typical finding |
| --- | --- | --- |
| Base image | Minimal (distroless, alpine, slim) and from a trusted source | Fat images increase attack surface |
| Tag pinning | Pinned to a specific version **and** ideally a digest (`node:20.11.1-alpine@sha256:…`) | `FROM node:latest` → MEDIUM (unreproducible, silent changes) |
| User | Non-root `USER` after installing dependencies | No `USER` → container runs as root → HIGH |
| Secrets | Never `ENV`/`ARG` for credentials; use BuildKit `--mount=type=secret` or runtime env | Secret in a layer is permanent even if deleted later → HIGH/CRITICAL |
| Layer hygiene | Copied files reviewed; `.dockerignore` excludes `.git`, `.env`, keys, `node_modules`, tests | `COPY . .` without `.dockerignore` → often ships `.env` and `.git` → HIGH |
| Package install | Pinned versions, `--no-install-recommends`, cache cleaned, no `curl \| sh` from unverified sources | Unpinned installs |
| Build stage | Multi-stage so build tools, source and dev dependencies stay out of the runtime image | Compilers/shells in production images |
| Ports | Only what is needed (`EXPOSE` is documentation; the real exposure is at run time) | — |
| Healthcheck | Present for orchestrated services | Missing → availability, not security, but note it |
| Signals/PID 1 | Proper init/signal handling so the app shuts down cleanly | Zombie processes |
| Filesystem | Application directories not world-writable; no `chmod 777` | `chmod -R 777` → MEDIUM |
| Entrypoint | No shell interpolation of untrusted env vars | Command injection at start-up |

Verify what actually ends up in the image:

```bash
docker history --no-trunc <image> | head -30
docker run --rm -it --entrypoint sh <image> -c 'id; ls -la /; env | sed -E "s/=(.{0,4}).*/=\1****/"'
```

(Only against images built locally, with the user's agreement; redact env output.)

## 3. Runtime configuration (compose / run flags)

| Setting | Requirement |
| --- | --- |
| `privileged: true` | Forbidden unless justified — effectively root on the host → CRITICAL |
| `/var/run/docker.sock` mounted | Equivalent to host root → CRITICAL unless it is a deliberately isolated CI runner with compensating controls |
| `cap_add` | Only the specific capabilities needed; drop all by default (`cap_drop: [ALL]`) |
| `security_opt` | Keep seccomp/AppArmor enabled; flag `seccomp:unconfined`, `apparmor:unconfined` |
| `user:` | Non-root UID; `user: root` flagged |
| `read_only: true` | Recommended, with `tmpfs` for writable paths |
| `no-new-privileges` | Enabled |
| Resource limits | `mem_limit`/`cpus`/`pids_limit` set (DoS containment) |
| Volumes | Minimal, read-only where possible; never mount `/`, `/etc`, the Docker socket, or the host home directory |
| Ports | Bind to `127.0.0.1` for services that must not be public: `"127.0.0.1:5432:5432"` not `"5432:5432"` |
| Networks | Segmented; databases and caches on an internal network with no published ports |
| Env/secrets | From an env file that is git-ignored, or from the orchestrator's secret mechanism; never inline production secrets in compose |
| Restart policy | Defined; a crash-looping container leaking errors is an availability and disclosure issue |
| Host namespaces | `network_mode: host`, `pid: host`, `ipc: host` flagged |

Publishing a database port to `0.0.0.0` on a public VPS is one of the most common real-world
critical exposures — check it explicitly against the host's firewall (`server-hardening` items in
`cloud.md` §VPS).

## 4. Image scanning

```bash
trivy image --scanners vuln,secret,misconfig --format json <image>:<tag>
grype <image>:<tag> -o json
docker scout cves <image>:<tag>
trivy config .        # Dockerfile/compose misconfiguration
hadolint Dockerfile
```

Interpret: distinguish OS-package CVEs with no fix available from application-layer vulnerabilities
you can patch; prioritize by reachability and whether the component is used at runtime. Recommend a
smaller base image when the CVE count is driven by unused packages.

## 5. Registry and distribution

- Private images in a private registry with authentication and least-privilege pull/push tokens.
- Image tags immutable for releases; deploy by digest.
- Registry credentials in a secret store, rotated, not in compose files.
- Image signing/attestation (cosign) where the organization requires provenance.
- Old vulnerable tags cleaned up; no `latest` in production manifests.

## 6. Build pipeline

- Images built in CI from a clean checkout, not on a developer machine.
- Build args never carry secrets (they persist in image metadata).
- Base images refreshed on a schedule so OS patches land.
- Scan gate in CI (`ci-cd.md` §Security gate).

## 7. Regression / verification checks

`docker run` of the built image reports a non-root `id` · `trivy config` and `hadolint` pass in CI ·
no secret pattern in `docker history` · database ports are not published to `0.0.0.0` (compose
assertion) · container starts with a read-only root filesystem · image scan gate fails on
unmitigated critical vulnerabilities.
