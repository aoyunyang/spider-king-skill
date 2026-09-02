# MCP Routing Playbook

Use this file when choosing which MCP family to activate next. It does not replace Startup Gate, family triage, browser handoff, or delivery gates.

## Contents

- [Purpose](#purpose)
- [Auto judge](#auto-judge)
- [Role binding](#role-binding)
- [Hard sequence W1](#hard-sequence-w1)
- [Triage table](#triage-table)
- [Capability and availability](#capability-and-availability)
- [Passive wire stores](#passive-wire-stores)
- [Environment providers](#environment-providers)
- [Wire visibility](#wire-visibility)
- [Stop rules](#stop-rules)
- [Out of scope platforms](#out-of-scope-platforms)
- [Anti-patterns](#anti-patterns)

## Purpose

Map installed MCP families onto existing Spider King concepts:

- intake: `live-target`, `artifact-only`, `continuation`
- evidence roles: `fingerprint-baseline`, `debugger-trace`, `cdp-bridge`
- baseline hosts: stock Chromium via `chrome-devtools` (default), Camoufox or managed profile (upgrade on fingerprint pressure)
- route owners: `evidence-reuse`, `chromium-recon`, `browser-hook`, `static-ast`, `env-patch`, `transport`, `verifier`, `pure-python-rebuild`, `python-collector`
- browser ownership: single `TARGET_ACTIVE` family with sequential handoff

MCP tools gather evidence only. Final `compact-replay` and `collector` paths stay browser-free and MCP-runtime-free.


## Auto judge

Choose the path from signals. Do not open a tool family first and invent the reason later.

| Priority | Signal | Auto decision |
|---|---|---|
| 1 | HAR / request text / JS / WASM / cookie-token sample / fixed vectors are enough, and fresh live acceptance is not required | `artifact-only`; no Camoufox, Chrome, or `js-reverse` ceremony |
| 2 | Bare URL, or current page/endpoint/session proof is required | `live-target` |
| 3 | Same target, env, and goal continue | `continuation`; reuse gate; reopen only changed surfaces |
| 4 | Live needed and fingerprint pressure is low or unknown | baseline host = `chrome-devtools` |
| 5 | Live needed and fingerprint pressure is high | baseline host = Camoufox or managed profile first |
| 6 | Candidate business request found and mutation/initiator needed | handoff to `js-reverse` if debug attach exists |
| 7 | Baseline succeeded but no debug attach surface | export artifacts, record `debugger_attach_gap`, continue offline |
| 8 | Mutation and moving fields are rebuildable offline | stop browser hosts; pure Python delivery only |

Fingerprint-pressure signals (upgrade baseline host when one is strong):

- explicit fingerprint / anti-bot / environment-risk gate on the clean path
- stock or automation-marked browser rejected while ordinary browsing is expected to pass
- repeated contaminated-environment failures on the same exit path
- user requires anti-detect or managed profile
- prior same-family evidence that a managed host is required

Default is conservative: when unsure, use `chrome-devtools`, not Camoufox.

## Role binding

| Role or surface | Preferred means | Alternate means | Concurrent rule |
|---|---|---|---|
| `fingerprint-baseline` ACTIVE | `chrome-devtools` on stock/attachable Chromium | Camoufox or managed-profile clean baseline when fingerprint pressure is high | only browser ACTIVE owner |
| `debugger-trace` ACTIVE | `js-reverse` after baseline handoff | none as a second parallel browser | only after baseline handoff; requires debug attach |
| `cdp-bridge` | attach/debug endpoint under current ACTIVE owner | same | never a third parallel owner |
| passive wire-store | `reqable`, HAR files, saved `network.jsonl` | same | may coexist with ACTIVE |
| wire-visibility | `WireMCP`, PCAP files | same | optional; does not prove signers |
| ENV / host provider | Camoufox, AdsPower Local API, other managed profile launcher | same | prepares host only; does not own final collector |
| offline routes | static-ast, env-patch, pure-python rebuild | same | no browser MCP required |

Camoufox is a **baseline host / ENV surface**, not a replacement for `js-reverse` and not a collector runtime.

## Hard sequence W1

Default web live path when the user needs fresh page or endpoint evidence:

```text
capability snapshot (no dual target prewarm)
  -> Auto Judge: intake + fingerprint-pressure + attach availability
  -> optional host/ENV open (Camoufox or managed profile) only when pressure is high or user-required
  -> fingerprint-baseline TARGET_ACTIVE:
       default means: chrome-devtools clean baseline + candidate business requests
       upgraded means: Camoufox/managed host clean baseline + candidate business requests
  -> sequential handoff (BASELINE_PARKED or RETAINED_EXCEPTION)
  -> js-reverse TARGET_ACTIVE when debug attach exists: initiator, mutation point, scripts, WS as needed
  -> if no attach: export artifacts + debugger_attach_gap + offline continue
  -> optional passive wire-store correlation
  -> offline rebuild (no browser MCP / no Camoufox runtime)
  -> fixed-input proof + repeated live HTTP replay
  -> delivery gate for declared shape
```

Do not place baseline-host actions and `js-reverse` target actions in the same parallel tool batch.

## Triage table

| Situation | Intake / route bias | Baseline host / ACTIVE | Passive / ENV |
|---|---|---|---|
| HAR, request text, cookie/token sample, or reqable history; explain or draft replay | `artifact-only` + `evidence-reuse` | none | reqable / files |
| JS/WASM file restore or fixed vectors | `artifact-only` + static-ast / pure-python-rebuild | none | fixtures |
| Bare URL or unknown site; low fingerprint pressure | `live-target` + `chromium-recon` | `chrome-devtools` first, then `js-reverse` | optional reqable later |
| Bare URL or unknown site; high fingerprint pressure | `live-target` + host-first baseline | Camoufox/managed host baseline, then `js-reverse` only if attach exists | Camoufox/AdsPower host |
| Request known; fields rotate or sign fails | after baseline, `debugger-trace` | `js-reverse` | reqable for egress truth |
| Strong multi-profile / anti-detect need already stated | `live-target` with host/ENV first | judged baseline host, then attach debugger | Camoufox or AdsPower |
| Browser works, stdlib/script fails before app semantics | `transport` | often none | optional Wire visibility |
| Verifier / warm-up / sidecar heavy | `verifier-gated` live chain | baseline then `js-reverse` for ordered transcript | reqable to freeze order |
| Deliver collector | `python-collector` | none | historical evidence only |

If URL and sufficient offline artifacts both exist, stay artifact-led until live acceptance, mutation proof, or fresh session evidence is required.

## Capability and availability

Before routing:

1. Inspect the active agent tool registry or schema.
2. Record `available_mcp` and `missing_mcp` for browser and optional families.
3. Record browser mode: `launch`, `attach`, or `unavailable`.
4. Record baseline host options: stock Chromium, Camoufox, managed profile, or none.
5. Record whether a debuggable endpoint is already known.
6. Choose only from confirmed available means (`available_mcp` plus local host providers actually reachable).

Rules:

- Presence of source trees on disk is not availability.
- Local Python env scripts cannot prove MCP plugin availability.
- If a required web live first-pass role cannot be satisfied by any available means, report the blocker before claiming the live target is understood.
- Missing Camoufox does not block low-pressure live work that can use `chrome-devtools`.
- Missing debug attach after a Camoufox-only baseline is a `debugger_attach_gap`, not silent paired success.
- Refresh the snapshot only when the registry, browser mode, or target context changes.

## Passive wire stores

Use reqable or HAR when:

- traffic is already captured or is being ingested locally
- you need ordered HTTP/WS search after a browser pass
- the user asked for artifact-led analysis

Do not use passive stores to:

- skip web live first-pass when intake is truly `live-target`
- replace initiator or mutation proof
- act as the final collector runtime

When browser state and captured egress disagree, trust wire egress.

## Environment providers

Use Camoufox, AdsPower, or another profile/host manager only to create a target-compatible baseline environment.

Required bridge when debugger work is still needed:

```text
open host/profile (Camoufox or managed profile)
  -> collect clean baseline requests when this host owns fingerprint-baseline
  -> obtain debuggable endpoint or browser URL when available
  -> js-reverse / chrome-devtools attach only
  -> forbid launching a second anonymous browser for the same job
```

Rules:

- Host/profile start alone is not protocol proof and not collector delivery.
- If no debuggable endpoint is obtained, keep the clean baseline artifacts, record `debugger_attach_gap` or ENV blocker, and continue offline instead of inventing initiator proof.
- Camoufox may satisfy `fingerprint-baseline` on high-pressure targets even when later debugger attach is unavailable; still do not claim full paired debugger understanding without attach evidence.
- Portable local endpoints and launch placeholders belong in `references/local-mcp-environment.md`; machine-private paths stay outside the shared skill package.

## Wire visibility

Use WireMCP or PCAP for:

- packet capture review
- coarse conversation or protocol hierarchy
- supporting a transport suspicion

Do not treat WireMCP success as:

- JA3 or full transport-profile proof by itself
- signer recovery
- business acceptance

Route transport admission work through `references/transport-pre-gate-playbook.md` and related transport references.

## Stop rules

Stop browser MCP and host use when:

- canonical mutation point and moving fields are known well enough for offline rebuild
- fixed-input vectors exist and only Python parity remains

Refuse to label `collector` when:

- success still requires live page driving, manual clicks, Camoufox/Chrome profile state, or MCP browser state
- only one lucky browser-backed success exists
- helper load success is the only proof

Always allowed stop shapes: honest `evidence`, `local-proof`, or a named external blocker.

## Out of scope platforms

Spider King is pure-web. These are out of primary scope here:

- Android / native app reverse families such as jadx, ida, frida
- mini-program unpackers such as wedecode

If the user's primary target is APK, native app, or mini-program:

- do not invent web paired-browser first-pass as ceremony
- do not pretend platform MCP success is a Spider King web collector path
- report an out-of-scope or unmet-constraint blocker instead of forcing the web live sequence

Keep using this skill only when the real business path is still a web/H5/browser-originated protocol problem.

## Anti-patterns

See also `references/anti-patterns-playbook.md` entries for MCP misuse. Immediate bans:

- open all MCP families at once
- run baseline-host and `js-reverse` target actions in parallel
- force dual browser first-pass on pure HAR/artifact jobs, or on out-of-scope APK/app/mini-program primary tasks
- default Camoufox on low-risk or artifact-only work
- treat Camoufox/ENV start or passive capture as collector delivery
- treat Camoufox as a replacement for `js-reverse`
- claim paired debugger success when only a non-attachable host baseline exists
- invent initiator, mutation, or live acceptance after a missing MCP surface
