# Environment Patch Playbook

Use this file when extracted logic runs in a local runtime but outputs still differ from the page.

## Contents

- [Common mismatch sources](#common-mismatch-sources)
- [Working method](#working-method)
- [Sniper versus net patching](#sniper-versus-net-patching)
- [Webpack require sniper](#webpack-require-sniper)
- [Timer queue contract](#timer-queue-contract)
- [Heat versus causal input](#heat-versus-causal-input)
- [Severity tiers](#severity-tiers)
- [UA branch and no-touch rules](#ua-branch-and-no-touch-rules)
- [Verification rule](#verification-rule)
- [Boundary-selection rule](#boundary-selection-rule)
- [Common traps](#common-traps)
- [Delivery rule](#delivery-rule)
- [Executable profile](#executable-profile)

## Common mismatch sources

- missing globals
- different user agent branches
- DOM-derived constants
- text encoding assumptions
- `Date.now()` or randomness precision
- scheduler, timer, or microtask differences; a `setTimeout` that runs the callback before returning turns retry/polling into a sync hang
- webpack UI `$mount` / layout sinks when the encrypt export is reachable through `require`
- document-complete evaluation of scripts that only mint on a later `load` or `DOMContentLoaded` listener
- host-scalar parity without completing that event latch
- load-order mistakes between env surfaces, polyfills, hooks, init, and trigger
- helper functions patched by side scripts
- instance-level hooks bypassed by prototype rewrites, rebinding, or wrapper replacement
- async bootstrap state that is only consumed later from cookie, storage, or one cached object
- unimplemented native surfaces such as `canvas`, WebGL, layout metrics, or style computation that quietly collapse fingerprint or verifier payloads
- host-object contract mismatches such as descriptors, prototype chains, constructor identity, enumeration, or native-looking function surfaces
- returned child-object shape mismatches where the method exists but its produced object diverges from the browser contract
- lifecycle-semantic gaps such as live collections, indexed slots, attach or detach behavior, or objects that should exist only while attached
- JS engine or host-version drift that changes builtin availability, native function own-property lists, or constructor surfaces
- structurally shortened outputs caused by null-returning host APIs rather than wrong business logic
- host-call heat that never survives ablation of the returned object
- a page-world JavaScript replica that matches inside Chrome but not in the local DOM host
- `Proxy` leaks on live collections or freshly created elements
- `Function.prototype.toString` camouflage applied to the wrong `Function` object
- named function expressions used as integrity preimages; installing them on `window` changes `typeof window[name]` and poisons toString-based decoder offsets

## Working method

1. classify the gap first: missing surface, load-order contract, or host-object contract mismatch
2. compare helper outputs on the same fixed inputs
3. compare structural metrics such as length, repeated blocks, and field presence before chasing semantics
4. identify the first diverging intermediate value
5. if cookie, storage, script, or resource injection barely changes the output, inspect which host APIs are actually probed
6. log decisive method arguments and returned child-object shapes, not only property gets, when those calls gate later branches
7. stabilize the environment in layers:
   - base DOM, BOM, and obvious scalar values
   - descriptors, prototype chains, constructor identity, enumeration, and returned-object shapes
   - higher-entropy fingerprint surfaces such as `canvas`, WebGL, audio, fonts, layout, or style only after evidence proves they matter
8. if the right names exist but probes branch on descriptors, `ownKeys`, `instanceof`, constructor checks, or native-looking functions, patch the contract before adding more globals
9. if probes depend on live collections, indexed slot persistence, or attach or detach transitions, patch the lifecycle contract at the prototype boundary instead of returning static placeholders
10. if one local engine version matches host contracts materially better than another, pin that version before rewriting more business logic
11. if hooks vanish, the artifact stays empty, or a script registers `load` / `DOMContentLoaded` only after collector-ready, prove load-order and fire the delayed event after the public object exists; do not mutate collected fields as a substitute
12. patch only the smallest missing environment surface or authoritative boundary that downstream code cannot bypass
13. if the runtime later only reads a server-issued cookie, storage value, token, or cached blob, test whether injecting a verified sample removes the async bootstrap from the hot path
14. allow structural failures to propagate; suppress only the exact recoverable error class you can justify
15. keep the patch local to the helper runtime, not a whole browser dependency
16. if a decoder or integrity offset hashes `Function#toString` plus a function name, preserve named-function-expression identity: do not install that name on `window` unless the live page-world actually does

## Webpack require sniper

Heavy UI SDKs (Vue `$mount`, transitions, layout readers) are a sinkhole in a headless host. If encrypt/sign lives in a webpack module, expose require and skip rendering.

- patch the webpack bootstrap so `globalThis.__wpRequire = R` before `R(0)` / the entry call
- call `__wpRequire(moduleId)` to take `{encrypt, sign, ...}` and feed frozen args
- do not start by completing `$mount` / `initEvents` / `getWidth`
- patch UI crash points only after proving the export is unreachable
- see `references/profiles/env-patch/references/webpack.md`

## Timer queue contract

On hosts without a native event loop, `setTimeout` must enqueue a macro-task. Never invoke the callback inside the `setTimeout` function body.

- drive the queue with `__drainTimers__(limit)`
- `setInterval` returns `0` and does not simulate periodic work when no native interval exists (prevents an infinite queue)
- if top-level load hangs, suspect a sync `setTimeout` before adding more DOM stubs
- `fromCharCode` heat (million vs 0) tells you whether a VM entered; timer-drain and init come before more canvas cosmetics (`references/jsvmp-analysis-playbook.md`)

Host-fidelity scoring is L0-L4 in `references/env-diff-playbook.md`. Canvas/navigator JS shims cannot be probe-counted as L0.

## Sniper versus net patching

Prefer sniper patches over net-wide DOM forgery.

- **Sniper**: patch only host surfaces the target actually read or called during a successful run (property heat, method heat, silent-value cards, or correlated traces)
- **Net**: full browser-vs-local diff of hundreds of attributes; use only when heat data is unavailable

Why sniper first:

1. most mismatched attributes are never consulted by the signer
2. net patches create false confidence and UA-branch poison
3. heat-guided lists stay small enough to verify one surface at a time

If only net diffs exist, rank candidates by whether changing them moves the fixed-output artifact, then delete non-causal patches.

## Heat versus causal input

A host call in a heat log is not mixer input.

Ablate the returned object before freezing a computed-name list because the call fired. `getComputedStyle(form)` can run while `length`, indexed slots, `getPropertyValue`, and a long computed-name table still fail causal ablation (sign unchanged). Snapshot-equal for-in order is not causal either.

Chrome page-world replica success is not local-DOM-host success:

- a JavaScript `MediaQueryList` replica (class extends `EventTarget`, `length` 0, getter names `get media` / `get matches`, `window.MediaQueryList` enumerable false) can be enough **inside Chrome**
- if the local host still diverges, sniper the next heat surface; do not keep stacking MQL cosmetics
- native `Function.prototype.toString` camouflage must target `window.Function.prototype.toString` and WebIDL internals (`esValue` / `implSymbol` / `globalObject`). In jsdom `beforeParse`, `window.Function !== Function`; wrapping Node `Function.prototype` never reaches the page VM. A getter `.name` of `get media` is not the FTS string
- host constructors built in Node and assigned onto `window` fail `instanceof window.Object`; define FakeXHR / MQL-class objects via `window.eval`
- do not `defineProperty` live jsdom CSS index slots to fake Chrome longhand order

Do not `Proxy` these live returns to log gets:

- `matchMedia` results
- `form.elements` / `HTMLFormControlsCollection`
- `createElement('img'|'div')`

A jsdom `Proxy` get can leak `Symbol(impl)` / `Symbol(SameObject caches)`. Chrome `Object.getOwnPropertySymbols(img)` is `[]`. A `Proxy` on `Uint8Array` makes `ArrayBuffer.isView` false.

Custom-attribute mixer probes belong on a freshly created element: `setAttribute(<custom>, <custom>)`, then `Attr.name` / `Attr.value` / `NamedNodeMap.getNamedItem`, not `getAttribute`. Reordering `NamedNodeMap.prototype` for-in to Chrome order can snapshot-match and still miss the mixer.

`element.style` for-in / own-key counts can wildly mismatch and still fail ablation. Matching indexed longhands (`[0]`, `length`, `cssText`) is not proof the for-in list enters the mixer.

`performance.memory` often has empty own keys, prototype getters, `constructor.name === "Object"`, and `@@toStringTag` MemoryInfo. Heap numbers are not automatically mixer inputs.

A hidden named form can be a signed-path latch. Unsigned ajax of business fields only is a fallback. `document.forms.<name>.elements` is `HTMLFormControlsCollection`; Chrome for-in is `namedItem,length,item`.

## Severity tiers

When multiple host gaps exist, repair in this order and re-check fixed output after each tier:

### Fatal (often blocks acceptance)

- native-looking function surfaces (`Function.prototype.toString` / descriptor story) that leak the local runtime
- `navigator.webdriver` or automation marks that the baseline browser does not show. CDP launch Chrome can itself expose `navigator.webdriver === true`; a JSVMP may skip the business XHR. If `Navigator.prototype.webdriver` is configurable, delete it in an authorized initScript and recapture before calling that fingerprint pressure or opening Camoufox
- empty plugin/mime trees when the baseline exposes a real structure
- focus/visibility lies that the baseline reports as active documents
- zero layout metrics (`offset*`, `getBoundingClientRect`) when the target reads non-zero geometry

### High (often enters fingerprint or branch selection)

- wrong `Object.prototype.toString` / `Symbol.toStringTag` labels
- missing `window.chrome` or UA-branched surfaces that the **same baseline UA** exposes
- missing `performance.timing` / navigation semantics used by the helper
- constructor/prototype identity breaks on objects the helper instantiates

### Medium (existence checks)

- long tails of missing APIs (`Notification`, `Worker`, WebRTC, audio contexts, etc.)
- only patch these after fatal/high tiers stop moving the artifact, and only if heat or ablation shows a read

Never promote a medium API stub above a proved fatal native-surface gap.

## UA branch and no-touch rules

- keep one pure baseline UA / Client-Hints / platform story end to end (`references/env-diff-playbook.md`)
- do not attach Chrome-only surfaces onto a Firefox-shaped UA, or mobile-only surfaces onto a desktop baseline, unless the live baseline proves those surfaces exist there
- native-looking `Function.prototype.toString` / descriptor camouflage must be applied once at a stable layer; repeated rewraps create detectable stacks
- reject foreign-machine fingerprint blobs as live inputs; re-sample host-local values on the execution host
- if patch volume keeps growing without fixed-output movement, stop and re-check anti-bot class and public boundary

## Verification rule

Loading success is only a milestone.
A helper that no longer throws can still emit an empty, downgraded, or structurally wrong artifact.

Before live replay:

1. rerun the decisive artifact in the same patched environment, hook placement, and load order you plan to ship
2. compare fixed-input browser and local outputs by structure first: length, prefix, segment count, field presence, encoding, or emitted headers and body
3. for hook-driven runtimes, treat order as part of the contract:
   - environment surfaces or fake transport primitive
   - target bundle
   - capture hook or observation boundary
   - init or config
   - trigger
4. if a target polyfill or wrapper replaces your early hook, move the hook after that replacement or upward to a stable boundary every call must cross
5. verify detection-sensitive surfaces **inside the host global the target code sees** (same runtime context as the helper), not only from the outer Python/Node driver
6. if signer bytes still disagree after host patches, switch to `references/signer-parity-chain-playbook.md` before adding more surfaces

## Boundary-selection rule

Patch the nearest stable boundary, not the prettiest one.

Prefer these boundaries over one-off instance patching when the target keeps rebinding helpers:

- prototype methods such as `XMLHttpRequest.prototype.open` or `.send`
- prototype-level DOM lifecycle hooks such as `appendChild` or `removeChild` when attachment state drives later probes
- constructor-time wrappers
- transport-wrapper ingress before mutation
- request egress after mutation but before live HTTP

If the runtime can replace one instance method and skip your patch, that patch surface is too low.

## Common traps

- implementing `setTimeout` as a synchronous callback, or mounting webpack UI instead of exposing `__wpRequire`
- counting canvas/navigator JS-shim probes as host-fidelity L0
- stripping unnamed `<meta content>` or other DOM bootstrap nodes from a "scripts-only" host and treating the later `.content` TypeError as a signer bug
- decoding mixed bootstrap scripts with one charset; HTTP `Content-Type` charset wins over `<script charset>` per asset
- patching one object instance when the runtime clones, rebinds, or replaces the method upstream
- fixing every undefined while ignoring load order between env surfaces, polyfills, hooks, init, and trigger
- replaying an entire async bootstrap when the signer only reads an already-issued cookie, storage slot, or token
- copying cookie, storage, script, or resource snapshots when the runtime actually branches on `canvas`, WebGL, layout, style, or native descriptors
- logging property gets only, while the decisive divergence sits in method arguments or returned child-object structure
- adding more globals when the real divergence is descriptor, prototype, constructor, or native-surface shape
- jumping straight to `canvas`, WebGL, audio, or font patching before base names, descriptors, and returned-object contracts are stable
- escalating `canvas`, WebGL, or audio after impersonate plus the current cookie-mint helper already returns business 200
- opening Camoufox because CDP `navigator.webdriver` is true, or wrapping XHR/`toString` to force a silent JSVMP, instead of deleting the configurable prototype property
- feeding foreign-machine fingerprint caches (canvas, WebGL, system colors, device metrics) into the live baseline; re-sample host-local values on the execution host and treat foreign caches as contrast only
- pretending a missing native surface is complete by pasting someone else's captured fingerprint blob without a capability gap note
- filling a host object with static values when the runtime checks live collection length, indexed slot persistence, or attach or detach lifecycle
- patching the entire DOM when only one global value was needed
- treating a much shorter verifier sidecar as an answer-quality problem instead of environment evidence
- matching UA, arch, or eval-length and concluding mint ran when the load latch never fired
- debugging under one JS engine version and shipping under another without rerunning fixed-input parity checks
- calling the job done because the helper loads without throwing
- swallowing every runtime error and hiding recursion, stack overflow, or corrupted VM state
- blaming crypto before checking environment-sensitive branches
- Never auto-stub real builtins (Function, Object, Array, Promise, Symbol) via capitalised-name Proxy factories; this breaks Function.prototype.call.bind and poisons fingerprint SDKs
- treating a host-call heat list as mixer input, or stacking a Chrome-only replica into jsdom after that replica already matched in page world
- wrapping Node `Function.prototype.toString` and believing a STYLE/FTS dump, or `defineProperty` on live jsdom CSS index slots
- binding a named function expression onto `window` to "complete" the host. A named function expression is not a `window` property. Integrity or string-table offsets that hash `fn.toString()` plus the function name can require `typeof window[name] === "undefined"`; assigning the function onto `window` changes the offset and collapses decoder `charAt` starts. Leave the name off `window` unless live page-world evidence shows it is actually installed
- `Proxy` on `matchMedia` returns, `form.elements`, freshly created `img`/`div`, or `Uint8Array` to log gets
- missing crypto page globals expected by vendor SDKs (AES/Hmac helpers) are a bootstrap gap, not a reason to load full captcha UI shells
- after a fingerprint SDK emits successfully, stop expanding host stubs unless a new branch is proved; further rejects may be session freshness
- for vendor fingerprint SDKs used as device-trust sidecars, follow `references/local-sdk-env-patch-playbook.md` before inventing more DOM patches

## Delivery rule

Prefer tiny local patches and explicit state injection over browser-backed execution.
Pin the shipped local engine version when helper parity depends on native-surface shape.

## Executable profile

When the entry, invocation contract, and fixed expected output are already known, prefer the executable diagnosis loop in `references/profiles/env-patch/index.md` over inventing ad-hoc `window` stubs. Keep pure protocol work in the Spider core loop; use the profile only for host-surface gaps.
