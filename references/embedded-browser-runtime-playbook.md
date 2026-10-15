# Embedded Browser Runtime Playbook

Use this playbook when host-bound JavaScript needs browser-visible semantics, but the target does not truly require a full browser for every request.

Examples of suitable runtimes include local embedded hosts such as `iv8`.
In some cases a pinned local JS engine plus a patched VM context is enough before a fuller host such as `iv8`.

If `iv8` becomes the chosen host, then read `references/iv8-runtime-cheatsheet.md` for concrete load-path, timer, resource-injection, and native-surface recipes.

## Contents

- [iv8 selection rule](#iv8-selection-rule)
- [iv8 exit rule](#iv8-exit-rule)
- [Browser-free versus runtime-free](#browser-free-versus-runtime-free)
- [Route here when](#route-here-when)
- [Do not route here first when](#do-not-route-here-first-when)
- [Decision ladder](#decision-ladder)
- [High-value runtime moves](#high-value-runtime-moves)
- [Evidence to record](#evidence-to-record)
- [Common traps](#common-traps)
- [Delivery rule](#delivery-rule)

## iv8 selection rule

Use `iv8` only when all of these are true:

- a trivial Python rewrite or tiny JS helper is not enough on fixed inputs
- the remaining mismatch depends on host-visible semantics such as `navigator`, `document.cookie`, timers, parser order, or native-surface probes
- the runtime can hand a concrete artifact back to Python for real HTTP replay

If any one of those is false, stay in Python or a tiny local helper.

## iv8 exit rule

Stop the runtime as soon as one decisive artifact is recovered:

- cookie string
- token
- signed URL
- navigation target or redirect URL
- wrapped body
- decoded payload
- stable getter

If the flow still needs real rendering, gestures, or ongoing page state after that point, `iv8` is not the final path.

## Browser-free versus runtime-free

A Python collector that still calls an embedded host is browser-free, but not automatically runtime-free.

That intermediate shape is acceptable only when:

- the runtime is local and narrow
- Python still owns the real HTTP
- the handoff states that an embedded host still remains

If the task explicitly asks to remove the runtime as well, keep shrinking after the first live replay proof instead of packaging the browser-free intermediate state as final completion.

## Route here when

- the decoded field is not a simple Python rewrite and the code reads `navigator`, `screen`, `location`, `document.cookie`, timers, or DOM lifecycle state
- the target probes `Object.keys`, `Reflect.ownKeys`, descriptors, `Function.prototype.toString`, `JSON.stringify`, or `document.all` before the business signer runs
- page HTML plus inline or linked scripts are enough to seed a cookie, signed URL suffix, wrapped XHR body, or later token
- a challenged document page plus one linked challenge script can locally recover the replayable `Cookie` header or token without needing a full browser
- the request logic depends on parser order, lifecycle events, or timer scheduling
- you need local observation of XHR or fetch mutation without launching a real browser
- the host bridge is synchronous, but the runtime may still accept injected cookie, storage, or token state instead of replaying the full async bootstrap path on every call
- local output remains much shorter, simpler, or more repetitive than live output even after cookie, storage, script, or resource seeding

## Do not route here first when

- the field collapses to Base64, hex, JSON, SHA, HMAC, AES, or another standard chain you can handwrite and verify in Python
- the flow still needs real rendering, gestures, challenge images, canvas entropy, WebGL behavior, or live browser state on each request
- the runtime would become a hidden replacement for all HTTP instead of a narrow bootstrap or helper stage

## Decision ladder

This ladder explains the runtime-specific middle rungs.
For the generic "do not jump layers" rule across the whole skill, also read `references/escalation-ladder-playbook.md`.

1. Decode first.
   Prove whether the problem is still just a standard algorithm or compact packet format.

2. Handwrite in Python when the proof is cheap.
   If fixed-input checks already match, stop there.

3. Escalate to an embedded runtime only for host semantics.
   Use it when the JavaScript truly needs DOM, timer, cookie, XHR, or native-surface behavior, and the result can still be harvested into a browser-free Python replay.

4. Keep the runtime local.
   Recover explicit artifacts such as:
   - cookie string
   - outbound `Cookie` header
   - final signed URL
   - wrapped body
   - token
   - decoded payload
   Stop once the artifact is stable enough to replay in Python.

5. Hand control back to Python.
   Python should still own live HTTP, retries, parsing, persistence, and scaling.

## High-value runtime moves

- Before escalating to a heavier host such as `iv8`, test whether a pinned local JS engine plus a patched VM context and the original site bundle already yield the decisive artifact.
- Use `page.load`-style offline bootstrap when lifecycle events, inline scripts, or XHR hooks matter.
- Use plain DOM insertion only when you need parsing without script execution.
- Prefer DOM or script insertion over blocking `vm` evaluation when timers, microtasks, or self-issued XHR or fetch calls must fire.
- Before escalating to a heavier host, test whether a thin DOM runtime plus a few native-looking patches is enough for parser order, `document.cookie`, and one linked challenge script.
- Pin the local engine version when native function surfaces, builtin availability, or host-object enumeration differ across versions; record which version ships and which version was used only for diagnostics.
- Freeze the UA major version when parser budget or event ordering changes behavior.
- Use logical time to advance timers and queued work without waiting on wall clock time.
- If entry HTML references linked bootstrap assets or runner scripts, fetch them under the same session, effective origin, and relevant headers that discovered them; detached downloads can fork the bootstrap chain.
- If the business route itself returns a machine challenge payload, parse the tuple in Python and call the local runtime only for the derived refresh artifact before retrying the same request family.
- If a bootstrap runtime exposes a stable getter after synchronous init, harvest that artifact before trying to finish every later timer callback.
- If a thin DOM or embedded runtime emits the final navigation target or same-route redirect URL before full page parity, treat that URL as a first-class artifact and hand replay back to Python immediately.
- If the runtime records intended network requests locally without sending them, drive it as observe planned request -> send exact HTTP in Python -> inject response -> advance the queue, rather than rebuilding the whole scheduler first.
- If the chosen host bridge is synchronous, test whether the runtime only consumes already-issued state from `document.cookie`, storage, or one cached object. If so, inject a verified sample and defer full refresh-path reversal until replay evidence says it is necessary.
- When a local runtime self-issues the decisive request, intercept body and headers locally and return the minimal fake success response needed to keep the runtime moving.
- If a callback reports success but the decisive field is still empty, follow the response or state write that actually fills the value instead of preserving fragile callback choreography.
- Watch API probes before broad patching so you know whether the missing surface is identity, enumeration, timing, cookie state, or a native-looking function boundary.
- If cookie, storage, scripts, or resource maps barely move the artifact, stop replaying more bootstrap and trace which native surfaces are actually probed.
- Treat `canvas`, WebGL, `getComputedStyle`, layout metrics, and native descriptor identity as first-class host surfaces; bridge them with narrow local adapters or stubs before escalating to broader emulation.
- Read local net-log style artifacts when the runtime can show the final URL, body, headers, outbound `Cookie`, or other wrapper-mutated request fields after bootstrap.
- If `document.cookie` or the session jar looks correct yet replay still fails, prefer the outbound `Cookie` header seen at request egress over stored-state guesses.

## Evidence to record

- exact HTML or bootstrap response used
- seed cookie inputs and the final harvested outbound `Cookie` header when cookie replay is the decisive artifact
- offline resource map or script bundle map
- environment overrides and omitted defaults
- structural metrics such as artifact length, field presence, repeated blocks, or entropy changes before and after each patch
- local engine version
- UA major version
- timer mode and every explicit event-loop advance
- final artifact extracted from the runtime
- whether the decisive artifact was a cookie delta, a redirect URL, or both
- fixed-input checks that prove the runtime output matches the live sample

## Common traps

- using an embedded runtime before trying the trivial Python rewrite
- using one JS engine version for diagnostics and another for the shipped helper without rerunning fixed-input parity checks
- feeding the wrong UA version and then blaming crypto for an ordering mismatch
- using full page bootstrap when plain DOM parsing would do
- assuming iframe `srcdoc` or `document.write` executes inline scripts; prove `contentDocument.scripts.length` and `contentWindow.location` (`about:blank` vs `about:srcdoc`) before treating the inner VM as running
- downloading linked bootstrap assets out of band with a different session, origin, or header profile than the entry chain
- treating a business-response challenge tuple as proof you found the wrong endpoint when the same route may simply need local refresh and retry
- treating failure under Node, jsdom, or a thin shim as proof the VM cannot run in a closer local engine or embedded host
- insisting on full async bootstrap replay when the runtime only needs one already-issued cookie, storage value, or token to proceed
- assuming you need full deobfuscation or a heavier host before testing whether a thin DOM runtime already yields the decisive cookie header for same-URL replay
- discarding a recovered redirect or navigation target because later runtime notices still appear after the decisive artifact has already been emitted
- reconstructing callback timing after the authoritative value is already visible in a local response or state write
- leaving the one fresh success chain to keep patching the host before the smallest live replay path is proven
- replaying cookies, storage, scripts, and resource maps forever when the real gap is a null or fake native surface such as `canvas`, WebGL, or layout APIs
- letting the runtime issue real business HTTP when only local mutation evidence was needed
- patching dozens of globals before checking which API probe actually branched
- mistaking a much shorter verifier sidecar for a bad answer instead of a host-fidelity gap
- treating reduced exceptions, successful load, or a plausible cookie or token shape as success before the real request replays
- trusting `document.cookie` or a client jar without comparing the outbound `Cookie` header that actually crossed the request boundary
- keeping a broad helper alive after you have already identified the one field that must be recovered
- calling a browser-free path "done" while an embedded runtime still regenerates the decisive artifact and runtime removal was part of the goal
- keeping `iv8` alive after one artifact is enough to hand control back to Python

## Delivery rule

An embedded runtime is acceptable only as a local bootstrap or helper stage.

The final collector should read like:

`Python request -> local runtime bootstrap or signer recovery -> explicit artifact extraction -> Python replay`

Not:

`Python orchestrates a hidden browser replacement`
