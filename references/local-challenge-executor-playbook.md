# Local Challenge Executor Playbook

Use this playbook when challenge HTML or challenge JS must run locally to emit a replayable artifact, and the final collector must stay browser-free.

## Contents

- [Route here when](#route-here-when)
- [Core idea](#core-idea)
- [Material classes](#material-classes)
- [Visual-oracle geometry](#visual-oracle-geometry)
- [Contract](#contract)
- [Minimal host requirements](#minimal-host-requirements)
- [Document lifecycle contract](#document-lifecycle-contract)
- [Stateful signer driver](#stateful-signer-driver)
- [Lifecycle marker progression](#lifecycle-marker-progression)
- [Fast execution path](#fast-execution-path)
- [Local bridge containment](#local-bridge-containment)
- [Artifact priority](#artifact-priority)
- [Post-artifact noise](#post-artifact-noise)
- [Coupling with other gates](#coupling-with-other-gates)
- [Delivery shape](#delivery-shape)
- [Version-randomized helper boundary](#version-randomized-helper-boundary)
- [Formal backend choice](#formal-backend-choice)
- [Common traps](#common-traps)
- [Minimal handoff notes](#minimal-handoff-notes)

## Route here when

- a business JSON API returns `text/html` challenge chrome instead of data
- a document route returns non-final HTML plus linked challenge scripts
- success depends on a rewritten URL, derived cookie header, or storage-seeded module produced by challenge execution
- full offline crypto rebuild is slower than executing the challenge blob in a minimal host
- anti-debug or missing DOM APIs make browser harvest noisy, but a stubbed local executor still emits the artifact

## Core idea

Before building a host bootstrap, classify signer entry (`export-fn`, intercept channel, `dual-channel`, `init-gated`) with `references/jsvmp-analysis-playbook.md`. An executor that never registers the interceptor is not an algorithm failure.

Label outputs as `host-owned` versus Python packaging versus `server-owned` grants using `references/parameter-ownership-playbook.md`. Run real script entries before guessing ciphertext algorithms from length or alphabet.

Python owns live HTTP.
The helper only restores the missing challenge artifact.

Success is not "the script finished cleanly".
Success is a **Python-replayable** `redirectUrl`, composed `Cookie` header, or equivalent wire artifact.

## Material classes

Classify every leftover field before choosing Python, helper, or patch. Map the class onto the generation labels in `references/delivery-gate-playbook.md` before calling the port pure:

| Class | Signal | Delivery move | Generation label |
|---|---|---|---|
| `algorithm-portable` | mix, framing, or prefix-plus-nonce POW ignore host APIs | rewrite in Python | `algorithmic` when no captured profile remains |
| `session-extracted` | key, token, or schedule lives in the current bytecode or an info-export | run the current blob in the helper; do not hardcode | `snapshot-driven` |
| `host-patched` | field reads canvas, UA, DOM, or other browser surfaces | sniper-patch the observed reads | still `snapshot-driven` until those reads are explicit inputs |
| `separate-oracle` | visual answer, click/trajectory, or human puzzle | keep it out of the signer; treat as its own oracle | not signer generation; do not fold into the three labels |

A collector that still extracts per-session key words is browser-free and `snapshot-driven`, not fully algorithmic.

Cheap prefix-plus-nonce hash puzzles are `algorithm-portable`. Visual oracles are not protocol state; do not merge them into the signer just because they share a challenge page.

## Visual-oracle geometry

When a box `[x1, y1, x2, y2]` is the visual answer, the drag origin is box `x1` (left edge), not the center `(x1+x2)/2`. Center origin shifts right by half the gap width and overshoots.

OCR or a captcha-platform call is a **diagnostic** for that oracle. It is never collector runtime, never a delivery dependency, and never a reason to keep page-driving. A compact-replay may submit a placeholder click to prove the envelope; that is not an auto-solver.

A structurally valid envelope with a semantic reject means the signer or packer passed and the separate oracle did not. Do not call that a protocol failure. A compact-replay that submits a default or placeholder click to prove envelope and encryption is protocol replay, not an auto-solver. Leave the visual answer unsolved until the platform semantic bit flips to accepted.

A same-round captured plaintext replay through the local encryptor isolates the shell from the oracle. If that replay is accepted and a regenerated visual answer is rejected, do not reopen the cipher.

## Contract

### Helper input

```json
{
  "url": "https://example.invalid/api/business?...",
  "html": "<!doctype html>...",
  "externalScriptUrl": "https://example.invalid/challenge.js",
  "externalScriptText": "/* challenge source */",
  "seedCookies": "a=1; b=2",
  "timeoutMs": 5000
}
```

### Helper output

```json
{
  "redirectUrl": "https://example.invalid/api/business?...&decode=...",
  "cookieString": "a=1; c=3",
  "navigationAttempts": ["..."],
  "errors": ["optional noise"],
  "xhrRequests": [],
  "fetchCalls": [],
  "resourceRequests": []
}
```

At least one of `redirectUrl` or a replayable `cookieString` must be present.

## Minimal host requirements

Implement the smallest host that preserves challenge progress:

1. **Document URL** equals the challenged business or document URL.
2. **Script injection** serves the captured challenge script for the expected URL; other subresources may 404 unless proven required.
3. **Cookie jar** seeded from the first-hop response on the same session chain.
4. **Location capture** on navigate / assign / replace / href setter. If the candidate artifact is that navigation URL, install the capture on the host navigation primitive **before** the DOM library loads. A stock host that throws `navigation to another Document` / not implemented will drop the URL; serialize the target, then swallow the unimplemented cross-document throw. Once a replayable redirect URL or cookie already exists, later unimplemented-navigation notices are post-artifact noise.
5. **Canvas / WebGL stubs** when fingerprint probes exist.
6. **XHR and fetch stubs** that record calls and return empty success unless a real local response is required.
7. **Timer compression** so long `setTimeout` chains still finish inside `timeoutMs`.
8. **Anti-debug tolerance**: ignore or neutralize `debugger` loops when they only delay artifact emission.
9. **Document lifecycle contract**: preserve `readyState`. If the script registers `load` or `DOMContentLoaded` after document-complete, delay the synthetic event until a public collector-ready signal exists.

Do not pin the skill to one host brand.
`jsdom`, `happy-dom`, `iv8`, or another minimal host is acceptable when it preserves the needed semantics.

## Document lifecycle contract

A local executor is not finished when the script file has been injected.

If Python or the helper evaluates challenge JS into an already-complete document:

1. record `readyState` at eval time
2. record when `addEventListener('load'|'DOMContentLoaded')` is installed
3. wait for collector-ready (exposed object key fields present)
4. only then fire the matching synthetic event
5. treat cookie and storage writes after that event as the artifact, not `eval` returning

Immediate fire after eval usually misses the listener. Mutating collected fields after the fact is not the mint path.

Host-scalar parity does not replace this latch. Report the delivery honestly: browser-free is allowed; a host that still runs official scripts is not runtime-free.


## Stateful signer driver

Some challenge scripts are not a one-shot `sign(input)` function. They accumulate transport observations and interaction events inside one JS context, then sign a final canonical request string.

Expose a narrow driver to Python using these semantic phases (names may differ):

| Phase | Python owns | Host helper does |
|---|---|---|
| `init` | roundKey, UA, seed cookies, document URL | load current scripts once into one retained context |
| `observe` | real HTTP order and URLs already discovered | let the script see the same XHR/fetch/script intent order without owning egress |
| `interact` | one shared event/behavior sequence for the round | deliver the same sequence to every consumer that listens |
| `sign` | final canonical URL/body bytes that will be sent | call the script entry on those exact bytes |

Rules:

- keep one helper process/context from `init` through `sign` for the round
- after each phase, read host cookie/storage deltas and write them back into the Python jar when the live chain does so
- never let the helper send the business verify request
- if canonical bytes change after `sign`, resign or fail; do not patch the signature string

This pairs with the same-world gate in `references/parameter-ownership-playbook.md`.

## Lifecycle marker progression

Some materials are rewritten across page phases by marker-ordered calls rather than computed once.

When evidence shows progressive rewrite:

1. capture the marker order from the clean transcript
2. before each marker, sync the cookie/DOM/config snapshot that marker could read
3. record before/after values to prove the material actually changed
4. do not collapse the chain into the final marker only
5. keep pure-compute sublayers (for example PoW base) separate from marker rewrite sublayers

If integrity checks reject function wrapping, prefer entry breakpoints or offline executor hooks that preserve return paths.

## Fast execution path

1. Python GETs the business or document URL with the admitted transport profile.
2. If the body is challenge HTML, freeze HTML, linked script URL, script body, and seed cookies on one session chain.
3. Run the local helper with the contract above.
4. Prefer artifacts in this order:
   - rewritten navigation / redirect URL with decisive query params
   - full outbound `Cookie` header or cookie string
   - storage module only if it is later proven necessary for regeneration
5. Python merges cookies, applies any original-URL echo field required by replay evidence, and performs the real HTTP replay.
6. Validate business anchors (JSON schema keys, list length, HTML markers), not merely HTTP 200.

## Local bridge containment

Treat challenge or collector-like JavaScript as untrusted code. If a local host
needs to observe XHR or fetch intent, Python must still own every real HTTP
request and the bridge must be narrowly contained.

Enforce these controls:

- build an allowlist from exact URLs already discovered by Python on the same session chain
- require HTTPS and the expected origin unless live evidence proves another route is part of the contract
- restrict methods to the observed contract
- disable redirects, or reject any unexpected redirect before following it
- strip collector-controlled `Cookie`, `Authorization`, `Proxy-Authorization`, `Host`, `Connection`, and forwarding headers
- make the Python session jar the only cookie authority
- cap request count, body size, response size, and per-request timeout
- reject `file:`, `data:`, localhost, loopback, link-local, private-network, and arbitrary hostnames
- log blocked requests with structural metadata, not raw secrets

Do not resolve or forward a helper-selected hostname merely because it is
same-origin-looking. The exact URL discovered from the live page, the effective
origin, and the Python session chain are the authority.

## Artifact priority

1. navigation / redirect URL
2. composed Cookie header / cookie string
3. single named cookie
4. localStorage / sessionStorage module
5. full encrypt-chain reverse

Stop escalating once Python can replay.

## Post-artifact noise

These are not automatic failures after a valid artifact exists:

- `navigation to another Document` / not implemented, **once** a replayable redirect URL or cookie was already captured
- missing analytics endpoints
- later timer exceptions
- partial fingerprint API gaps that did not block artifact emission

If the candidate artifact is the navigation URL and it was never captured, the unimplemented throw is mint failure, not noise. Patch capture first; do not widen DOM parity to silence the throw.

## Coupling with other gates

- If the same param also has a short offline signer path, use `references/dual-writer-param-playbook.md` before choosing the product writer.
- If transport impersonation changes whether you receive JS challenge HTML versus another wall, fix transport admission first.
- If app-layer HMAC/sign is independent, prove whether challenge replay needs it at all.

## Delivery shape

```text
bare business request
  -> challenge HTML + script (same session)
  -> local challenge executor
  -> Python replay(redirectUrl or Cookie)
  -> pagination / concurrency
```

Report browser-free status as:

- browser-free collector with local challenge executor
- not fully runtime-free if a JS host remains, including `jsdom` or another host running official scripts
- not fully algorithmic if leftover fields are `session-extracted` or `host-patched`
- not an auto-solver if the visual or click oracle is still a placeholder or unsolved

## Version-randomized helper boundary

When challenge scripts or dynamic VM assets change path every round:

1. hash the active asset
2. compare the public helper or VM call boundary, not only the URL
3. rerun fixed vectors from a clean success sample
4. if the boundary is stable, a tiny local opcode or wrapper scan helper may remain acceptable
5. rebuild a new helper version only when framing, vectors, or outputs diverge

The stable boundary is arity and I/O shape, not the URL. A randomized WASM or JS path is not a new algorithm while arity and I/O still match. Opcode-sequence templates and stable-magic anchors may survive path churn; keep that helper tiny.

Python still owns live HTTP, session order, waits, and acceptance. The helper must not become a browser. WASM/WAT remains evidence, not collector runtime.



## Formal backend choice

If multiple executor hosts can run the challenge scripts, choose the formal one with `references/opaque-runtime-profile-playbook.md` bakeoff rules:

- one protocol profile across candidates
- lifecycle and event parity before output comparison
- fresh server acceptance over local ciphertext equality
- Python still owns real HTTP

## Common traps

- promoting an executor host because ciphertext matched another host without server acceptance
- treating a stateful signer as a one-shot sign after a fresh context
- calling only the final lifecycle marker and ignoring earlier rewrites
- letting the helper own real HTTP while Python only pastes the final headers
- using Playwright or CDP page-driving as the product path
- treating a randomized WASM URL as a new algorithm when arity and I/O still match
- letting the local helper choose arbitrary network destinations or own live HTTP
- requiring zero helper errors instead of a replayable artifact
- redownloading challenge scripts on a detached client after first-hop cookies already bound the chain
- rebuilding the whole encryptor after redirect URL already carries the decisive param
- forgetting original-URL echo fields on replay when evidence shows them
- calling a helper-extracted per-session key a pure Python constant
- using visual-box center as drag origin instead of `x1`
- shipping OCR or a captcha-platform client inside the collector runtime
- folding a visual answer or trajectory oracle into the signer
- treating a legal envelope plus semantic reject as proof that the signer is still wrong
- labeling a placeholder-answer compact-replay as an auto-solver
- reopening AES, RSA, or PoW after a same-round captured-plaintext replay already passed
- binding manual coordinates to a newly issued challenge image
- issuing a new challenge image in the helper and skipping verify because the visual oracle looked weak
- firing `load` or `DOMContentLoaded` immediately after injecting a script into an already-complete document
- treating host-scalar parity as mint proof
- mutating collected objects instead of completing the collector-then-event contract
- calling a host that still runs official scripts runtime-free
- treating unimplemented cross-document navigation as helper failure after a redirect URL was already captured
- treating unimplemented cross-document navigation as post-artifact noise when the candidate artifact is that URL and capture was never installed before the host loaded

## Minimal handoff notes

Report:

- challenged route and content type
- helper host family
- which artifact won (`redirectUrl` / cookie / both)
- whether original-URL echo was required
- transport profile used for admission
- live regeneration proof on a fresh timestamp or page
- material class for each leftover field (`algorithm-portable` / `session-extracted` / `host-patched` / `separate-oracle`)
- whether document-complete eval required a delayed load latch
- browser-free versus runtime-free
