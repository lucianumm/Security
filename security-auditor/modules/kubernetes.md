# MODULE — KUBERNETES

Load only when manifests, Helm charts, Kustomize overlays or a cluster context are present.

Related: `docker.md`, `cloud.md`, `secrets.md`, `ci-cd.md`.
Standards: CIS Kubernetes Benchmark, NSA/CISA Kubernetes Hardening Guidance, Pod Security Standards.

---

## 1. Discovery

```bash
ls -d k8s manifests charts helm deploy kustomize 2>/dev/null
grep -rlnE "^kind: (Deployment|StatefulSet|DaemonSet|Pod|Ingress|Service|Role|ClusterRole|Secret)" . --include=*.y*ml | head -40
kubectl config current-context 2>/dev/null    # read-only, only if the user authorizes cluster access
```

Never run mutating `kubectl` commands. `get`/`describe` only, and only with explicit authorization.

## 2. Workload security context

For every Pod template:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 10001
  fsGroup: 10001
  seccompProfile: { type: RuntimeDefault }
containers:
  - securityContext:
      allowPrivilegeEscalation: false
      privileged: false
      readOnlyRootFilesystem: true
      capabilities: { drop: ["ALL"] }
```

Flag: `privileged: true` (CRITICAL), `allowPrivilegeEscalation: true`, missing `runAsNonRoot`,
`hostNetwork`/`hostPID`/`hostIPC: true`, `hostPath` volumes (especially `/`, `/var/run/docker.sock`,
`/etc`), added capabilities (`SYS_ADMIN`, `NET_ADMIN`, `SYS_PTRACE`), and missing resource
`requests`/`limits` (noisy-neighbor and DoS containment).

## 3. Pod Security and admission control

- Pod Security Admission enabled per namespace with `restricted` (or `baseline` with a documented
  reason): `pod-security.kubernetes.io/enforce: restricted`.
- Or a policy engine (OPA Gatekeeper, Kyverno) with enforced constraints — check the policies are
  in `enforce`, not `audit`/`warn` only.
- Image provenance/signature verification at admission where the organization requires it.
- Deny `:latest` tags and require digests in production namespaces.

## 4. RBAC and identity

```bash
grep -rn "kind: \(Role\|ClusterRole\|RoleBinding\|ClusterRoleBinding\|ServiceAccount\)" . --include=*.y*ml
```

- No `cluster-admin` bindings for application workloads or CI; no wildcard rules
  (`apiGroups: ["*"], resources: ["*"], verbs: ["*"]`).
- Dedicated ServiceAccount per workload; `automountServiceAccountToken: false` when the pod does not
  call the API server.
- Beware of permissions that are equivalent to cluster admin: `create pods` (with a privileged spec),
  `create pods/exec`, `get secrets` cluster-wide, `escalate`/`bind`, `impersonate`,
  `patch nodes`.
- Human access through SSO with short-lived credentials; no shared kubeconfigs with static tokens.
- Cloud IAM binding (IRSA / Workload Identity) scoped per service account, not per node.

## 5. Secrets

- Kubernetes `Secret` objects are base64, **not encrypted** by default — verify encryption at rest
  (`EncryptionConfiguration`) or an external store (External Secrets Operator, Vault, cloud secret
  manager, Sealed Secrets).
- Secrets not committed to Git in plaintext (a `kind: Secret` with real `data:` in the repository is
  a finding — see `secrets.md`).
- Mounted as files rather than env vars where possible; least-privilege RBAC on secret reads;
  rotation procedure defined.

## 6. Network

- `NetworkPolicy` present: default-deny ingress **and** egress per namespace, with explicit allows.
  A cluster with no NetworkPolicy means any pod can reach any pod (and often the cloud metadata
  endpoint) — MEDIUM–HIGH depending on data class.
- Cloud metadata endpoint (`169.254.169.254`) blocked from pods that do not need it (SSRF pivot).
- Services: no accidental `type: LoadBalancer`/`NodePort` for internal services.
- Ingress: TLS configured, certificates managed and renewed, security headers set at the ingress or
  the app, rate limiting/WAF where available, no wildcard host routing to an unintended backend.
- mTLS between services (service mesh) where the threat model warrants it.

## 7. Cluster and node posture

Verify with the user or the cloud console (mark `NOT_VERIFIED` if inaccessible):
API server not publicly reachable (or restricted by IP/private endpoint) · anonymous auth disabled ·
audit logging enabled and shipped · kubelet authentication/authorization enforced · nodes patched
and using a hardened OS · etcd encrypted and access-restricted · control-plane and node autoupgrade
policy · namespace separation between environments (separate clusters preferred for production) ·
no shared cluster between production and untrusted workloads.

## 8. Scanning

```bash
trivy config ./k8s
kubescape scan framework nsa
checkov -d ./k8s -o json
polaris audit --audit-path ./k8s
kube-bench          # node/CIS checks, on the cluster, read-only
```

## 9. Helm

- Chart values do not carry secrets; `values.yaml` reviewed for `privileged`, `hostPath`, broad RBAC.
- Third-party charts pinned and reviewed (`supply-chain.md`); avoid charts that install
  cluster-admin components without need.
- `helm template` output audited, since defaults change between versions.

## 10. Regression / CI checks

`trivy config` / `kubescape` gate in CI · a manifest with `privileged: true` or `hostPath: /` fails
the policy test · NetworkPolicy presence asserted per namespace · no `kind: Secret` with real data
in the repository (secret scan) · RBAC diff reviewed on every change.
