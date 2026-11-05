# Extended surfaces from encyclopedia §5

Read only the relevant sections of `../references/encyclopedia-v1.0.md`. This module routes
domains that cannot be inferred or secured from a web repository alone. Keep an external
verification backlog with owner, evidence needed, proposed action and residual risk. No tests
against people, radios, physical facilities, devices or industrial systems are implied.

| Domain | Inspect when applicable | Defensive verification and implementation proposals |
|---|---|---|
| ENC-D12 — endpoint and persistence | Signed releases, service registration, scheduled tasks, workload permissions and endpoint policy supplied by the owner | Verify update provenance, least privilege, deployment persistence paths, endpoint monitoring and containment evidence. Never install an implant or test a discovered credential. |
| ENC-D13 — communication and social engineering | Email delivery code, sender-domain configuration, account recovery/helpdesk flows and organizational evidence | Propose sender authentication, safe link/attachment handling and independent identity verification for critical changes. DNS/mail-console and training controls remain external until verified. No phishing campaign. |
| ENC-D14 — mobile and desktop | AndroidManifest, entitlements, deep links, exported components, Electron preload/IPC, Tauri capabilities, native key stores and update channels | Trace untrusted URI/IPC to privileged effects; validate caller, arguments and permissions. Propose restricted IPC, secure token storage, transport validation and signed updates with platform-specific negative tests. Do not claim pinning or obfuscation alone secures a client. |
| ENC-D15 — IoT, firmware and OT | Device identity, provisioning, debug interfaces, OTA verification, protocol access and documented safety constraints | Propose unique credentials, signed/versioned updates, safe rollback, segmentation and asset inventory. Verify firmware/configuration offline or in an explicitly authorized lab. Never actuate equipment or fuzz live industrial protocols. |
| ENC-D17 — physical and human operations | Access, custody, offboarding, backups, break-glass and continuity evidence supplied by the owner | Record procedure owners and independent evidence. Propose access reviews, restore exercises and separation of duties. Repository code cannot prove physical access control or staff behavior. |
| ENC-D18 — memory and binary safety | C/C++/unsafe Rust/FFI, parsers, allocations, lifetime and integer conversions, compiler/linker flags | Trace bounds, lengths, ownership and lifetimes across FFI. Propose safe APIs, checked arithmetic, hardening flags and isolated sanitizer/fuzzer regression cases under an approved execution budget. A hardened compiler does not close a demonstrated memory defect. |
| ENC-D19 — wireless and peripherals | Device/network configurations, pairing, BLE permissions, USB/accessory trust and location-input handling | Propose authenticated pairing, current encryption, management-frame protection where supported, narrow device trust and update policy. Inspect configurations and lab fixtures; no deauthentication, jamming, spoofing or nearby-device scan. |

For every applicable imported scenario, document preconditions, the actual trust boundary, existing
controls, evidence, counterevidence and a safe validation method. Use `NOT_VERIFIED`/`INCONCLUSIVE`
when artifacts are unavailable. Absence of a manifest or a source-code keyword does not justify
excluding an organizational or externally managed surface.
