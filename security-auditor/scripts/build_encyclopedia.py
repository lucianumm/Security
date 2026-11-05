#!/usr/bin/env python3
"""Reproducibly import the user-supplied encyclopedia; never execute its content."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / "references" / "encyclopedia-v1.0.md"
CATALOG = BASE / "catalog" / "encyclopedia.json"

# Routing hints are editorial, not verified applicability or normative mappings.
ROUTES = {
    1: ["authentication", "sessions"], 2: ["authorization", "database"],
    3: ["backend", "uploads", "database"], 4: ["frontend", "nginx", "sessions"],
    5: ["api", "webhooks"], 6: ["business-logic", "payments"],
    7: ["cryptography", "secrets", "database", "logging"],
    8: ["cloud", "nginx", "monitoring"], 9: ["cloud", "secrets"],
    10: ["docker", "kubernetes"], 11: ["supply-chain", "ci-cd"],
    12: ["incident-response", "extended-surfaces"], 13: ["extended-surfaces"],
    14: ["extended-surfaces"], 15: ["extended-surfaces"], 16: ["ai-security"],
    17: ["backup", "incident-response", "extended-surfaces"],
    18: ["extended-surfaces"], 19: ["extended-surfaces"],
}
CONTROL_ROUTES = {
    "GOV": ["business-logic", "incident-response"],
    "IAM": ["authentication", "authorization", "sessions"],
    "APP": ["backend", "frontend", "uploads"], "API": ["api", "webhooks"],
    "DAT": ["cryptography", "database", "secrets"],
    "NET": ["cloud", "docker", "kubernetes", "nginx"],
    "SDLC": ["supply-chain", "ci-cd"], "OPS": ["logging", "monitoring", "backup", "incident-response"],
}


def build() -> dict:
    payload = SOURCE.read_bytes()
    controls, domains, scenarios = [], [], []
    section = ""
    domain = None
    for number, line in enumerate(payload.decode("utf-8-sig").splitlines(), 1):
        if line.startswith("## "):
            section = line
            domain = None
        match = re.fullmatch(r"### 5\.(\d+) (.+)", line)
        if match:
            index = int(match[1])
            domain = {"id": f"ENC-D{index:02}", "section": f"5.{index}",
                      "title": match[2], "sourceLine": number, "modules": ROUTES[index]}
            domains.append(domain)
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if section.startswith("## 4.") and re.fullmatch(r"[A-Z]+-\d{2}", cells[0]):
            if len(cells) != 3:
                raise ValueError("unexpected control row")
            controls.append({"id": cells[0], "title": cells[1], "requirement": cells[2],
                             "sourceLine": number, "modules": CONTROL_ROUTES[cells[0].split("-")[0]]})
        if section.startswith("## 5.") and domain and cells[0] not in {"Ataque ou abuso", "---"}:
            if len(cells) != 3:
                raise ValueError("unexpected scenario row")
            ordinal = 1 + sum(s["domainId"] == domain["id"] for s in scenarios)
            scenarios.append({"id": f"{domain['id']}-S{ordinal:03}", "domainId": domain["id"],
                              "title": cells[0], "preconditionImpact": cells[1],
                              "defenseValidation": cells[2], "sourceLine": number})
    if (len(controls), len(domains), len(scenarios)) != (136, 19, 507):
        raise ValueError(f"encyclopedia counts changed: {len(controls)}/{len(domains)}/{len(scenarios)}; review importer and ID migration")
    return {"schemaVersion": 1, "source": {"file": "references/encyclopedia-v1.0.md",
            "version": "1.0.0", "referenceDate": "2026-11-04",
            "sha256": hashlib.sha256(payload).hexdigest(),
            "origin": "User-supplied reference, not independently verified standards or executable rules",
            "declaredScenarioCount": 506, "importedScenarioCount": 507,
            "countNote": "The source declares 506 scenarios but contains 507 data rows; none were discarded."},
            "controls": controls, "domains": domains, "scenarios": scenarios}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="maintainer-only: regenerate the bundled catalog")
    args = parser.parse_args()
    catalog = build()
    if args.write:
        CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    elif json.loads(CATALOG.read_text(encoding="utf-8")) != catalog:
        parser.exit(1, "Catalog drift: inspect the source and rebuild explicitly.\n")
    print("Catalog verified: 136 controls, 507 scenarios (source declares 506), 19 domains.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
