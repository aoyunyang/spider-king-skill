# iv8 Runtime Cheatsheet

Use this reference after `references/embedded-browser-runtime-playbook.md` has already established that a local embedded host is the right delivery shape and `iv8` is the chosen runtime.

## Contents

- What this file is for
- Minimal setup
- Isolate and thread affinity
- Choose the right load path
- Script bytes and charset
- Time control
- Keep network local
- Patch the smallest faithful surface
- Probe before you patch
- Fast decision cues
- Evidence to keep
- Common traps

## What this file is for

Use `iv8` as a narrow local host when JavaScript still needs browser-visible semantics and the final collector can still live in Python.

Best-fit uses:

- bootstrap scripts that need host state before one concrete artifact appears
- probe chains where `navigator`, `document.cookie`, timers, or request hooks change the output
- local egress capture where `netLog` reveals the decisive URL, body, headers, or outbound `Cookie`
- narrow host-surface gaps such as `canvas`, WebGL, layout, or `Function.prototype.toString`

Use it only when the result can be handed back to Python.

Use `iv8` for browser-visible semantics such as:

- `navigator`, `screen`, `location`, `document.cookie`
- DOM lifecycle or parser order
- timers, microtasks, or request hooks
- wrapper observation through local XHR or fetch state
- native-looking surfaces such as `canvas`, WebGL, layout, or `Function.prototype.toString`

Do not let `iv8` become the HTTP client, browser profile, or hidden final collector.
Python still owns live HTTP, retries, parsing, persistence, and scaling.
If you cannot name the single artifact you expect to recover, you probably do not need `iv8` yet.

## Minimal setup

Start with the smallest environment that proves the branch you care about:

- `location`
- `navigator.userAgent`
- timezone when time or locale checks matter

Do not cargo-cult hundreds of fingerprint fields before the probe chain proves they matter.

If high-entropy host inputs are required, capture them on the execution host.
Canvas, WebGL, computed style, system colors, screen metrics, device memory,
hardware concurrency, fonts, audio, and similar profile fields are provenance
artifacts, not portable constants. A cache from another machine or browser
profile may be useful as a comparison fixture, but it is not a valid runtime
input unless the final collector is explicitly classified as snapshot-driven
and the capture scope is reported.

Useful `iv8` primitives from the tutorial:

- `JSContext(environment=..., config=..., time_mode=...)`
- `__iv8__.page.load(snapshot)`
- `document.documentElement.innerHTML = ...`
- `__iv8__.eventLoop.sleep/advance/drain`
- `ctx.add_resource(...)`
- `__iv8__.netLog.entries`
- `__iv8__.wrapNative(fn, name)`
- `with_devtools(..., watch_apis=[...])`

## Isolate and thread affinity

Keep `JSContext` and `page.load` on the thread that created the isolate.
A `ThreadPoolExecutor` worker can silently native-crash after the first few successes even when the same mint path is stable on the creating thread.
Python may still own HTTP, retries, and pagination on other threads; do not move the isolate itself onto a worker.

## Choose the right load path

Use `page.load(snapshot)` when:

- inline or external scripts must execute
- lifecycle events matter
- request hooks or parser order matter
- the HTML response, headers, and resource map are part of the bootstrap contract

Use plain DOM insertion such as `innerHTML` when:

- you only need structure or constants from HTML
- script execution is unnecessary
- you want the cheapest possible host surface

Rule:

- if the artifact depends on lifecycle or self-issued requests, prefer `page.load`
- if parsing alone is enough, do not pay the lifecycle cost

`page.load` snapshot key is `baseURL`. A string `url` field is not a substitute and can yield `location.href = http://undefined/`. Pass the document URL as `baseURL`, then map linked scripts in `resources` to the same absolute URLs the parser will request.

## Script bytes and charset

Decode each linked classic script the way the browser would, per asset, not once for the whole page.

Order:

1. HTTP `Content-Type` charset, when present
2. otherwise the `<script charset>` attribute
3. otherwise the document encoding

A bootstrap can mix these. One file may be `iso-8859-1` because the script attribute says so and the HTTP type has no charset; a sibling can be UTF-8 because `Content-Type` carries `charset=utf-8` and that wins over the tag.

Do not latin1-decode a chrome-devtools or other text-saved network body that is already UTF-8 of the browser's decoded source. That inflates string tables: scripts still parse and may even write a short decoy cookie, while the request hook never installs.

If unpacker internals remain on the bootstrap object after load, encoding or a missing DOM node is still wrong. Hook install means the native transport method was replaced, not that `executedScripts > 0`.

## Time control

`time_mode` is fixed at `JSContext` construction and cannot be switched later.

`logical` is for fast timer settle:

- `Date.now()` advances 1ms per call
- `eventLoop.sleep(ms)` is instant
- use it after the signer runtime already exists

`system` is for unpackers, PoW, and anti-debug timing:

- JS-period `Date.now()` / `performance.now()` follow real CPU elapsed time
- a CPU-heavy packer that treats a large `now` delta as debugger-pause will halt (`typeof unpacked === "undefined"`) or spin under `logical`
- `eventLoop.sleep(ms)` waits real milliseconds; pay that cost when unpack and timer settle share one context

Preferred flow:

1. pick the clock from the first time-sensitive gate, not from convenience
2. load the page or script
3. advance only the time you can justify
4. harvest the artifact or egress boundary as soon as it becomes stable

Useful moves:

- `sleep(ms)` to flush queued work (logical=instant, system=wall)
- `drain()` when time should not advance further
- `advance(total, step)` when frame-sized progression matters
- a short `sleep`/`drain` is enough when mint already exists; do not wait a seconds-long anti-debug `setInterval`
- stub exact `Function` bodies such as `debugger;`, `while (true) {}`, and `while(!![])` as no-ops; never `includes("debugger")`

## Keep network local

Community `iv8` should be treated as local bootstrap only.

Preferred replay shape:

1. JavaScript bootstrap runs locally in `iv8`
2. inspect `__iv8__.netLog.entries` for the decisive URL, body, headers, outbound `Cookie`, or other wrapper-mutated request fields
3. Python sends the real network request
4. `ctx.add_resource(...)` injects the captured response only when the local runtime must continue
5. extract the final artifact back to Python

If the egress `Cookie` header differs from `document.cookie` or a client-managed jar, trust the egress record for replay and treat the stored state as only one input to that wire result.

Do not let `iv8` quietly own live business HTTP.

## Patch the smallest faithful surface

Reach for these in order:

1. environment fields such as `location`, `navigator`, timezone
2. narrow property adapters with `Object.defineProperty`
3. native-looking shims with `__iv8__.wrapNative(...)`
4. targeted probes or wrappers on the exact host surface

Common examples from the tutorial that generalize well:

- `MessageChannel`
- `SharedArrayBuffer`
- `navigator.connection`
- `PerformanceObserver.supportedEntryTypes`
- specific `document.createElement` branches

Before replacing `btoa` in an embedded host, test the Latin1 vector `btoa("\x00\xffAz") === "AP9Beg=="`; code units above `0xff` must be rejected rather than UTF-8 encoded. Keep the host implementation when it passes. Patch only after a fixed positive or rejection vector proves a mismatch.

Rule:

- patch the exact missing surface
- keep the shape native-looking when reflection matters
- if one instance hook is bypassed, move to the shared boundary instead of adding more one-off stubs
- stub the actual transport callsite; an XHR send recorder is not a library-ajax wrapper
- fire the continuation the next request reads (`success` and `complete` when the pager waits on complete)
- freeze the observed clock writer the signer reads; a `Date.now` pin is not an ajax-success inject

## Probe before you patch

High-value ways to discover the missing surface:

- `with_devtools(..., watch_apis=[...])` for focused API access proof
- `Proxy` wrappers around `window`, `navigator`, `document`, or a narrow host object
- local wrappers on `canvas`, WebGL, layout, or descriptor reads

Treat these as evidence surfaces, not default instrumentation:

- `Object.keys`
- `Reflect.ownKeys`
- descriptor reads
- `Function.prototype.toString`
- `document.cookie`
- `canvas.toDataURL`
- `getComputedStyle`

If cookie, storage, script tags, or resource maps barely change the output, suspect native-surface gaps before replaying more bootstrap.

## Fast decision cues

Use `page.load` when local output changes after lifecycle or resource execution.

Use the same session, effective origin, and relevant discovery headers when reacquiring linked bootstrap assets or runner scripts.

Use `innerHTML` when the needed value is already in the DOM and scripts add no value.

Use `wrapNative` when reflection or `[native code]` checks matter.

Use `netLog.entries` when the runtime already emits the real wrapped request.

Use `add_resource` when the runtime needs a local response to continue but Python should still own the real HTTP.

Use `watch_apis` or `Proxy` when you still do not know which host surface is decisive.

Use `iv8` only until one decisive artifact is stable enough for Python replay.

## Evidence to keep

Record these artifacts:

- the exact HTML or bootstrap response used
- the resource map you supplied
- the minimal environment overrides
- timer mode and explicit event-loop advances
- the decisive host probes you observed
- the extracted cookie, token, URL, or body
- fixed-input checks proving local output matches the live sample

## Common traps

- overfilling environment fingerprints before proving the missing branch
- reusing another host's canvas, WebGL, system color, font, or device-profile cache as live runtime input
- using `page.load` when static DOM parsing would do
- reacquiring linked bootstrap assets under a fresh client or guessed origin instead of the same session chain that discovered them
- replaying full async bootstrap when injected issued state already unblocks the runtime
- reusing one signed suffix, header, token, or `Cookie` sample across page, keyword, referer, timestamp, or body changes without replay proof
- keeping a broad `iv8` harness after one getter, cookie, or egress boundary is enough
- mistaking a host-fidelity gap for a bad signer when the local blob is much shorter or structurally cleaner than the live one
- letting `iv8` become a stealth browser replacement instead of a narrow host runtime
- treating `iv8` as the final HTTP executor instead of a local bootstrap bridge
- wrapping `Math.random` with `wrapNative` before a packer unpacks; a native-looking constant PRNG can hang the packer
- pinning `Math.random` with a plain assignment so unpack *halts*, then calling the recovered signer; some packers stop without building the signer runtime and need native PRNG plus timeout/retry instead
- freezing `Date.now` to a constant while an unpacker waits on elapsed time
- after unpack, freeze the observed writer the signer reads to a server-issued clock only for signing: ajax success, a callback, or a rewritten `Date.now` only if that getter is the writer. Do not freeze a quieter `Date.now` sibling by default, do not keep that freeze during unpack, and do not treat a frozen clock as decoy if the same value is also sent
- keeping default `time_mode="logical"` for a CPU-heavy packer unpack; `Date.now()` +1ms per call can look like a debugger pause and halt or hang unpack. Use `system` for that gate, and accept real `sleep` if the same context must later install a timer export
- JSON.stringify / `console.log` of a recovered trap object before reading `typeof`, `Array.isArray`, and `length`
- concluding an export is absent after construct plus a short probe; some hosts install `window` functions on a timer that only appears after `eventLoop.sleep`
- writing `srcdoc` / `document.write` into an iframe and assuming inline scripts ran; some embedded hosts leave `scripts=0` / `bodyLen=0`. A cached `about:blank` iframe may also not be the later `about:srcdoc` detection frame
- intercepting `eval(packer)` to save the unpacked string, then evaluating that string in a fresh world; packer side effects can live in the original context, so the harvested function exists but crashes on call
- treating `window.call` as a token export when it is only a pager or click dispatcher
- missing a required `meta[name].content` or unnamed `<meta content>` blob and blaming the signer. A stripped "scripts-only" host can throw `Cannot read properties of undefined (reading 'content')`, leave a short decoy cookie, and keep native `XMLHttpRequest.prototype.open`
- treating `XMLHttpRequest.prototype.open.length` as the install oracle after the function name already changed
- decoding every bootstrap script as latin1, or as UTF-8, because one tag said `charset=iso-8859-1`
- latin1-decoding a UTF-8-saved network body and calling the helper broken when the hook stays native
- using `page.load({ url })` instead of `baseURL`
- wrapping both XHR and ajax "to be safe"; stacked wraps hide which continuation minted the field
- running `JSContext` / `page.load` on a `ThreadPoolExecutor` worker thread
- treating a mint-shaped cookie from an incomplete Node `document`/`cookie` host as live; native-looking `document`/`screen`/`createElement` can change the artifact
- waiting a seconds-long anti-debug interval after mint already exists
