# Hook Techniques

Use this file when runtime proof is faster than static reading.

## Contents

- [Class-gated observation](#class-gated-observation)
- [Highest-value hook targets](#highest-value-hook-targets)
- [Hook goals](#hook-goals)
- [Word-packing feed-cut](#word-packing-feed-cut)
- [Dynamic compile snapshots](#dynamic-compile-snapshots)
- [Hook timing and recovery matrix](#hook-timing-and-recovery-matrix)
- [First-screen and challenge timing](#first-screen-and-challenge-timing)
- [Evidence interpretation](#evidence-interpretation)
- [Logging shape](#logging-shape)
- [Hooking order](#hooking-order)
- [Behavior safety](#behavior-safety)
- [Common traps](#common-traps)
- [Paste-ready profile](#paste-ready-profile)

## Class-gated observation

Before installing hooks, read `references/anti-bot-class-playbook.md` observation allow/deny:

- `signature-bound`: clean baseline first; prefer egress, initiator, transparent, or source-level observation; do not open with proxy-all host hooks or pre-document hook storms
- `behavior-interceptor`: first-screen pre-document hooks are valid when challenge writers finish before a late install
- `pure-obfuscation`: hooks are optional; fixed vectors may be enough

Always prove **XHR and fetch** (and other sibling transports) before claiming a quiet boundary. See dual-channel rules in `references/jsvmp-analysis-playbook.md`.

## Highest-value hook targets

- `fetch`
- `XMLHttpRequest.prototype.open`
- `XMLHttpRequest.prototype.send`
- library ajax (`$.ajax` / `jQuery.ajax`) and its `success` / `complete` callbacks
- `encodeURIComponent` / `unescape`
- hex nibble join (`Array.join` of `0-f` chars); plaintext `Array.join` on long fragments
- `eval` / `new Function` compile body after param substitution (constructor Proxy, not global `apply`/`call`)
- transport wrapper functions
- bootstrap helpers
- signer helpers
- public writer function arguments before concat is guessed
- storage reads and writes when session state is changing
- word-packing primitives: fixed-width `slice`, `charCodeAt`, `fromCharCode`, `TextEncoder` / `TextDecoder` (local executor first; see below)

## Hook goals

- capture pre-sign strings
- capture final payloads after wrapper mutation
- capture response-side refresh fields
- capture cookies or globals that change between requests
- capture pre-cipher plaintext at the word-packing boundary
- capture the pre-cipher object at the payload assembler, not only at `JSON.stringify`
- capture preimage at public codec exits (`encodeURIComponent`, `Utf8.parse`, hex nibble join, plaintext `Array.join`) before VM centers
- capture `eval` / `Function` compile bodies after substitution as key material, not as a later call trace
- capture public writer arguments before guessing concat from route names or leftover sibling fields

## Word-packing feed-cut

Use this when a VM or signer must turn a long plaintext into words before the cipher, and vendor export names rotate.

This is **not** the verifier/device-trust `packer` in `references/doctrine-index.md`. That word means challenge payload or track packaging. This section is only the plaintext-to-word boundary.

Do not wrap `String.prototype` on a live `signature-bound` page as a first move. Global `slice` / `charCodeAt` hooks can poison native-looking surfaces and signer inputs. Prefer:

1. public export or transport egress
2. the same observe-only hook inside a local challenge executor or harvested-script host
3. live-page word-packing hooks only after class proof says `behavior-interceptor` or `pure-obfuscation`, or after a clean baseline shows the prototype wrap is not observer-toxic

Highest-signal word-packing boundaries:

- `String.prototype.slice` where `end - start` is a fixed width (commonly 4 or 8) and `this.length` is large
- tight `charCodeAt` loops over those slices
- `fromCharCode` rebuilds after the cipher
- `TextEncoder.encode` / `TextDecoder.decode` on the same long string

Method:

1. keep the hook observe-only and return the native result
2. on the first long source string, log `this` once and remember it
3. ignore later slices of the same string
4. correlate that plaintext to the later wire field with `references/jsvmp-analysis-playbook.md` reverse-trace
5. do not install word-packing hooks as a substitute for XHR/fetch proof

These names outlive vendor helper names. They remain helper-level hooks: install after wire and wrapper hooks unless first-screen timing requires preload, and still obey the class gate above.

## Dynamic compile snapshots

Use this when dictionaries, alphabets, or recovered helpers appear only after `eval` / `new Function` substitutes parameters into a compile body.

The snapshot of that body is key material. The later invocation is just execution. Do not treat a call-stack dump as a substitute for the substituted source. On `signature-bound` pages this is still not a first hook: keep wire/egress proof first, and treat a constructor Proxy as observer-toxic until a clean baseline says otherwise.

Method:

1. Proxy the `Function` constructor (and wrap `eval` if that is the compile path) in an observe-only way: capture `arguments[arguments.length - 1]` / the eval string after substitution, hash it, then construct with the original
2. restore the constructor immediately after the capture window
3. correlate the snapshot to the later wire field (`references/silent-value-capture-playbook.md` recipe G)
4. never wrap global `Function.prototype.apply` or `Function.prototype.call` to chase VM dispatch; those wraps are observer-toxic and hang mixers
5. `Array.join` of long fragments can dump plaintext before the compile step; keep that hook observe-only and dedupe the same source string

## Hook timing and recovery matrix

Treat preload as a capability, not a promised method name. Preserve a clean baseline before any controlled reload or invasive hook.

| Observed state | Smallest next move | Claim boundary and recovery |
|---|---|---|
| `preload available` and the page is not initialized | install the narrow observe-only hook through the schema-confirmed before-document capability, then navigate once | record injection order and prove that original arguments, `this`, return values, and promises are preserved |
| `preload unavailable` | use the earliest stable breakpoint, a controlled refresh with a post-bundle stable boundary, or an offline local runtime | do not claim constructors, bootstrap writes, or early requests were observed; record the missing capability in the snapshot |
| `page already initialized` | treat a late hook as evidence for subsequent events only; save current state before deciding whether refresh is replayable | if refresh would destroy unique state, use `RETAINED_EXCEPTION` and switch to source, breakpoint, or egress evidence instead |
| `hook miss` | verify install time, target frame, execution world, replacement order, and whether a prototype, constructor wrapper, ingress, or egress is more authoritative | a miss clears only that boundary during that window; do not delete the hypothesis yet |
| `page-owned world` miss from console or an isolated world | repeat the narrow proof in the page-owned world when the installed capability exposes it | if it does not, use source, call-frame, or wire-egress evidence and record the world gap |
| `sibling transport` remains possible | inspect XHR, fetch, wrappers, beacon, WebSocket, worker, service-worker, and message relays one channel at a time | correlate every hit to method, URL, field, caller, and request id; silence on one channel is not whole-transport proof |
| tool disconnect, restart, or registry change | stop target actions, persist the evidence already obtained, and perform a `capability snapshot` refresh | record the last confirmed lifecycle state plus control loss; never infer `PARKED`, `CLOSED`, or restored `TARGET_ACTIVE` ownership, then resume through `sequential handoff` |

Change one timing, world, or transport variable at a time. If the hook changes target behavior, restore the clean baseline and treat the failure as observer-effect evidence before escalating.

When page-world hooks remain observer-toxic, miss systematically, or cannot yield correlated fixed inputs, escalate evidence means to `silent-value-capture` under `references/silent-value-capture-playbook.md` instead of widening hooks. That upgrade is still debugger-trace work, not a license to automate delivery.

## First-screen and challenge timing

Challenge and bootstrap scripts often finish before a late hook is installed.

Rules:

1. if the decisive cookie, token, or wrapper install happens on first document load, prefer schema-confirmed before-document / init-script injection, then navigate once
2. a normal navigate-then-hook sequence is invalid for first-screen proof; record `first_screen_hook_gap` instead of claiming the writer is absent
3. when preload is unavailable, use the earliest controlled refresh that preserves session intent, or switch to offline local execution of harvested scripts
4. install observe-only transport hooks before challenge JS when the class is `signature-bound` or the status chain shows early `412`/`403` challenge hops (`references/anti-bot-class-playbook.md`)
5. after install, prove runtime activity with one correlated event; install acknowledgement alone is insufficient (`references/jsvmp-analysis-playbook.md` instrumentation health gate)

## Evidence interpretation

- a silent hook only disproves that exact boundary
- a quiet `document.cookie` hook does not clear `Set-Cookie`, returned JS, redirect wrappers, workers, or other writers
- a quiet storage setter hook does not clear direct property assignment or sibling state writers
- a quiet `fetch` hook does not clear XHR, wrapper, worker, or message-based transport
- if a console or isolated-world probe misses a page-owned helper, repeat the proof in the page-owned world before abandoning the lead
- an XHR `open` substring filter on a route token such as `"match"` misses relative paths; filter on the resolved URL

## Logging shape

- bind captures to target, event, method, URL, field, and a short caller hint when possible
- one request-bound log line is worth more than a dump of naked values
- cap high-frequency traces; reverse-trace from a known exit value instead of reading forward dumps (`references/jsvmp-analysis-playbook.md`)

## Hooking order

1. wire-level hooks
2. wrapper-level hooks
3. helper-level hooks
4. local-variable breakpoints only if hooks still leave ambiguity

Rule:

- if instance-level hooks get replaced or skipped, move upward to the shared boundary that every call must cross such as the prototype, constructor wrapper, or transport egress
- word-packing primitives belong with helper-level hooks; they do not replace wire or wrapper proof, and they are not live `signature-bound` first hooks

## Behavior safety

- default hooks to observe only
- forward original args, preserve `this`, and return the original result or promise
- if a hook changes behavior, treat the new failure mode as possible observer effect until proven otherwise
- wrapping `Number.prototype.toString` or `TextEncoder.encode` is observer-toxic on some mixers even when the wrap is observe-only and FTS looks native
- wrapping global `Function.prototype.apply` or `.call` is observer-toxic; snapshot compile bodies at the constructor/`eval` boundary instead
- `TextEncoder.encode.length === 0` is a contract; restoring a wrapped function with `.length === 1` is a detectable mutation
- do not `Proxy` `Uint8Array`, `matchMedia` returns, `form.elements`, or freshly created `img`/`div` nodes to log gets; `ArrayBuffer.isView` and `Object.getOwnPropertySymbols` diverge from Chrome
- if the write setter is itself the product path, prefer local-executor jar intercept or egress observation over live setter hooks

## Common traps

- hooking business-layer functions while missing the transport wrapper
- hooking one convenient object instance when the runtime keeps rebinding or cloning the real caller
- pausing too early with breakpoints and drowning in noise
- capturing only final hashes without the input string that produced them
- widening page-world hooks after observer effect is already proved instead of changing capture layer
- pre-inject or proxy observation on `signature-bound` flows that poisons the sample
- proving silence on XHR only while fetch (or a worker) carries the real mutation
- hooking a vendor export name that rotates while the fixed-width slice boundary stays stable
- wrapping `String.prototype` on a live `signature-bound` page before proving the wrap is not observer-toxic
- wrapping `document.cookie` on a success host that mints through that setter; even an observe-only wrapper can poison the product cookie
- logging every slice without deduping the long source string
- installing a late global `JSON.stringify` hook and treating a miss as proof that no plaintext object exists
- wrapping XHR while the signer exits through library ajax, or firing `success` without `complete`
- stacking `encodeURIComponent`, `unescape`, `Utf8.parse`, and hex-join wraps on one page; capture one public exit instead
- wrapping `Number.prototype.toString` or `TextEncoder.encode` because an earlier FTS-only wrap looked oracle-safe
- wrapping global `Function.prototype.apply`/`call`, or treating an `eval`/`Function` compile snapshot as a later call trace
- wrapping XHR or `toString` on a signature-bound VM because the list request stayed silent under `navigator.webdriver`
- `Proxy` on TypedArray, live collections, or `createElement` results to log gets
- guessing concat from route names or leftover sibling fields before hooking the public writer arguments
- filtering `XMLHttpRequest.open` on a path substring and missing relative business URLs

## Paste-ready profile

For a known observation boundary that only needs a Console/Snippets script, use `references/profiles/browser-hook-snippets/index.md` instead of expanding into full protocol discovery.
