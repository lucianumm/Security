# Tool catalog and adapter boundaries

This skill selects tools by hypothesis and stack. The families, examples, evidence, and required
adapter metadata are maintained in `../../core/TOOL_EXECUTION.md`. No named tool is guaranteed to be
installed, free, safe to run, or suitable for every repository.

Before recommending a tool, record whether it reads local files, contacts a registry/advisory API,
downloads rules or images, checks credentials against providers, executes project code, writes
files, and uploads reports. Pin versions, image/binary digest and ruleset/template digest. Check the
official version-specific exit-code and data-handling documentation. Missing or failed tools produce
an explicit coverage gap, not an empty finding list.

## Current implementation boundary

`scripts/security_auditor.py` is a deterministic local state validator and gate. It does not execute
Gitleaks, Semgrep, OSV-Scanner, Trivy, CodeQL, ZAP, Burp, Schemathesis, Nuclei or cloud tools, and it
does not authenticate scanner claims. The CI templates show selected integrations that must be
adapted to the consumer's stack and protected baseline. A future sandboxed adapter runner requires
host-level process, filesystem, network and resource controls; this repository does not claim to
provide those controls.
