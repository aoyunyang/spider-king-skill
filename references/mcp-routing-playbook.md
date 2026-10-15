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
- debugger-trace means: default `js-reverse` when attach exists; `silent-value-capture` is a first-class alternate/upgrade means (including no-attach when a backend is available)
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
| 4 | Live needed, fingerprint pressure is low or unknown, and DP/initiator is not already required | baseline host = `chrome-devtools` |
| 5 | Live needed and fingerprint pressure is high | baseline host = Camoufox or managed profile first |
| 6 | Candidate business request found and mutation/initiator needed, or the user asked to open DP | one host: `js-reverse` may own baseline + debugger-trace; attach/select the current page; do not launch a second Chrome |
| 7 | Baseline succeeded but no debug attach surface, or MCP `select_page`/attach times out | record `debugger_attach_gap`; harvest scripts over ordinary HTTP; if silent backend available, continue via `silent-value-capture`; else offline |
| 8 | Attach/hooks cannot yield correlated fixed-input values without observer damage, or JSVM public-boundary values are missing | enable `silent-value-capture` immediately; if unavailable, record `silent_value_capture_gap` |
| 9 | Mutation and moving fields are rebuildable offline | stop browser/engine hosts; pure Python delivery only |

Fingerprint-pressure signals (upgrade baseline host when one is strong):

- explicit fingerprint / anti-bot / environment-risk gate on the clean path
- stock or automation-marked browser rejected while ordinary browsing is expected to pass
- MCP `launch` Chrome / `chrome-devtools` already marked automation while ordinary browsing is expected to pass
- repeated contaminated-environment failures on the same exit path
- user requires anti-detect or managed profile
- prior same-family evidence that a managed host is required

Default is conservative: when unsure, use `chrome-devtools`, not Camoufox.
If DP/initiator work is already required, start `js-reverse` as the single owner instead of launching `chrome-devtools` first. Record browser mode `launch|attach|unavailable` and the installed curl impersonate max chrome in the capability snapshot.

## Role binding

| Role or surface | Preferred means | Alternate means | Concurrent rule |
|---|---|---|---|
| `fingerprint-baseline` ACTIVE | `chrome-devtools` on stock/attachable Chromium; `js-reverse` on the same host when DP is already required | Camoufox or managed-profile clean baseline when fingerprint pressure is high | only browser ACTIVE owner |
| `debugger-trace` ACTIVE | `js-reverse` after baseline handoff when attach exists; same-host continue when `js-reverse` already owns baseline | `silent-value-capture` on upgrade triggers, or when attach is missing but a backend is available | one browser/engine TARGET_ACTIVE; skip `chrome-devtools` launch when DP already required; role complete via initiator proof and/or correlated silent-value cards; never collector runtime |
| `cdp-bridge` | attach/debug endpoint under current ACTIVE owner | same | never a third parallel owner |
| passive wire-store | `reqable`, HAR files, saved `network.jsonl` | same | may coexist with ACTIVE |
| wire-visibility | `WireMCP`, PCAP files | same | optional; does not prove signers |
| ENV / host provider | Camoufox, AdsPower Local API, other managed profile launcher | same | prepares host only; does not own final collector |
| offline routes | static-ast, env-patch, pure-python rebuild | same | no browser MCP required |

Camoufox is a **baseline host / ENV surface**, not a replacement for `js-reverse` and not a collector runtime.

`silent-value-capture` is a **first-class debugger-trace means**, not a baseline host and not a collector runtime. Prefer `js-reverse` first when attach exists. On upgrade triggers, or when attach is missing but a backend is available, use it under `references/silent-value-capture-playbook.md` without abandoning debugger-trace.

## Hard sequence W1

Default web live path when the user needs fresh page or endpoint evidence:

```text
capability snapshot (no dual target prewarm; record launch|attach|unavailable, curl impersonate max chrome, silent_backend)
  -> Auto Judge: intake + fingerprint-pressure + attach + silent_backend
  -> optional host/ENV open (Camoufox or managed profile) only when pressure is high or user-required
  -> fingerprint-baseline TARGET_ACTIVE:
       default means: chrome-devtools clean baseline + candidate business requests
       DP already required: js-reverse owns baseline + debugger-trace on one host; do not launch a second Chrome
       upgraded means: Camoufox/managed host clean baseline + candidate business requests
  -> sequential handoff (BASELINE_PARKED or RETAINED_EXCEPTION)
  -> debugger-trace TARGET_ACTIVE (branch, not linear tail):
       attach available:
         js-reverse first (initiator, mutation point, scripts, WS)
         + silent-value-capture immediately on upgrade triggers
       attach missing:
         debugger_attach_gap
         + silent-value-capture if silent_backend available
         else export artifacts and offline continue
  -> optional passive wire-store correlation
  -> offline rebuild (no browser MCP / no Camoufox runtime / no silent-value-capture backend runtime)
  -> fixed-input proof + repeated live HTTP replay
  -> delivery gate for declared shape
```

Do not place baseline-host actions and debugger-trace target actions (`js-reverse` or silent-value engine capture) in the same parallel tool batch.

## Triage table

| Situation | Intake / route bias | Baseline host / ACTIVE | Passive / ENV |
|---|---|---|---|
| HAR, request text, cookie/token sample, or reqable history; explain or draft replay | `artifact-only` + `evidence-reuse` | none | reqable / files |
| JS/WASM file restore or fixed vectors | `artifact-only` + static-ast / pure-python-rebuild | none | fixtures |
| Bare URL or unknown site; low fingerprint pressure | `live-target` + `chromium-recon` | `chrome-devtools` first; if DP is already required, `js-reverse` alone | optional reqable later |
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
- If a required web live first-pass role cannot be satisfied by any available means, report the blocker before claiming the page/runtime is understood. An exact endpoint may still earn only the endpoint-scoped transport-only delivery claim defined in `references/startup-triage-playbook.md`; missing tools alone never activate it.
- Missing Camoufox does not block low-pressure live work that can use `chrome-devtools`.
- Missing debug attach after a Camoufox-only baseline is a `debugger_attach_gap`, not silent paired success. It does not block `silent-value-capture` when a backend is available.
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
- If no debuggable endpoint is obtained, keep the clean baseline artifacts and record `debugger_attach_gap` or ENV blocker. Continue debugger-trace via `silent-value-capture` when a backend is available; otherwise continue offline. Do not invent initiator proof.
- MCP `select_page` or attach timeout is the same attach gap: harvest the script URL over Python HTTP and continue offline instead of retrying the hung call.
- Navigating the last Chrome tab to `about:blank` does not unlock a shared user-data directory. If `close_page` cannot drop the last page, keep Chrome as `TARGET_ACTIVE`, record `debugger_attach_gap`, and continue debugger-trace with page-world or `initScript` capture plus a local runtime; do not relaunch `js-reverse` against the same profile.
- Camoufox may satisfy `fingerprint-baseline` on high-pressure targets even when later debugger attach is unavailable. Do not claim debugger-trace completion from baseline alone; complete it with `js-reverse` when attach exists, or with correlated `silent-value-capture` cards when a backend is available, else leave debugger-trace incomplete.
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
- launch a second Chrome because the user asked to open DP
- force dual browser first-pass on pure HAR/artifact jobs, or on out-of-scope APK/app/mini-program primary tasks
- default Camoufox on low-risk or artifact-only work
- treat Camoufox/ENV start or passive capture as collector delivery
- treat Camoufox as a replacement for `js-reverse`
- claim debugger-trace success from baseline alone when attach is missing and no correlated silent-value cards exist
- invent initiator, mutation, or live acceptance after a missing MCP surface
- copy a newer live Chrome major onto a lower curl impersonate and restart risk-control reverse
- bulk-add unproven extra routes when risk-control is unknown
