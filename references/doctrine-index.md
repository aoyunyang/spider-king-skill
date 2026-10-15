# Doctrine Index

Use this file when the target is still broad, the failure mode feels familiar, or you need family-level rules before loading more specific playbooks.

These are transfer rules, not site notes.

## Contents

- [Doctrine 1: Trust the wire, not the page text](#doctrine-1-trust-the-wire-not-the-page-text)
- [Doctrine 2: The dynamic parameter is not always a signature](#doctrine-2-the-dynamic-parameter-is-not-always-a-signature)
- [Doctrine 3: Fixed-input validation beats naming](#doctrine-3-fixed-input-validation-beats-naming)
- [Doctrine 4: Narrow exceptions stay narrow](#doctrine-4-narrow-exceptions-stay-narrow)
- [Doctrine 5: Automation is not an acceptable crutch](#doctrine-5-automation-is-not-an-acceptable-crutch)
- [Doctrine 6: Environment mismatch is evidence](#doctrine-6-environment-mismatch-is-evidence)
- [Doctrine 7: Delivery gates outrank convenience](#doctrine-7-delivery-gates-outrank-convenience)
- [Doctrine 8: Public does not mean unsigned](#doctrine-8-public-does-not-mean-unsigned)
- [Doctrine 9: Stateful streams are protocol, not browser magic](#doctrine-9-stateful-streams-are-protocol-not-browser-magic)
- [Doctrine 10: Observer effect is real](#doctrine-10-observer-effect-is-real)
- [Doctrine 11: Cookie provenance beats cookie superstition](#doctrine-11-cookie-provenance-beats-cookie-superstition)
- [Doctrine 12: Packet framing and crypto are separate contracts](#doctrine-12-packet-framing-and-crypto-are-separate-contracts)
- [Doctrine 13: Pagination is a protocol surface](#doctrine-13-pagination-is-a-protocol-surface)
- [Doctrine 14: Raw source can beat parsed DOM](#doctrine-14-raw-source-can-beat-parsed-dom)
- [Doctrine 14A: Server-looking field names do not prove server issuance](#doctrine-14a-server-looking-field-names-do-not-prove-server-issuance)
- [Doctrine 14B: Minted session is not admitted session](#doctrine-14b-minted-session-is-not-admitted-session)
- [Doctrine 14C: Enumeration and hydration are separate contracts](#doctrine-14c-enumeration-and-hydration-are-separate-contracts)
- [Doctrine 15: Embedded runtimes are scalpels, not a second browser](#doctrine-15-embedded-runtimes-are-scalpels-not-a-second-browser)
- [Doctrine 16: Probe chains reveal the missing surface](#doctrine-16-probe-chains-reveal-the-missing-surface)
- [Doctrine 17: Transport admission is a separate contract](#doctrine-17-transport-admission-is-a-separate-contract)
- [Doctrine 18: Harvest challenge artifacts at the nearest stable boundary](#doctrine-18-harvest-challenge-artifacts-at-the-nearest-stable-boundary)
- [Doctrine 19: Server-issued state beats local invention](#doctrine-19-server-issued-state-beats-local-invention)
- [Doctrine 20: Split verifier targets by failure surface](#doctrine-20-split-verifier-targets-by-failure-surface)
- [Doctrine 21: Weak enforcement is evidence, not absolution](#doctrine-21-weak-enforcement-is-evidence-not-absolution)
- [Doctrine 22: Escalate one rung at a time](#doctrine-22-escalate-one-rung-at-a-time)
- [Doctrine 23: Small facts age better than big summaries](#doctrine-23-small-facts-age-better-than-big-summaries)
- [Doctrine 24: Counterexamples constrain better than slogans](#doctrine-24-counterexamples-constrain-better-than-slogans)
- [Doctrine 25: Positive-sample hygiene beats track tuning](#doctrine-25-positive-sample-hygiene-beats-track-tuning)
- [Doctrine 26: Environment risk is its own failure surface](#doctrine-26-environment-risk-is-its-own-failure-surface)
- [Doctrine 27: Two surfaces to confirm, one to suspect](#doctrine-27-two-surfaces-to-confirm-one-to-suspect)
- [Doctrine 28: Ablate one owned layer at a time](#doctrine-28-ablate-one-owned-layer-at-a-time)
- [Doctrine 29: Name one failure surface before broad patches](#doctrine-29-name-one-failure-surface-before-broad-patches)
- [Doctrine 30: One baseline pure end to end](#doctrine-30-one-baseline-pure-end-to-end)
- [Doctrine 31: Class before family folklore](#doctrine-31-class-before-family-folklore)
- [Doctrine 32: First divergent transform stage](#doctrine-32-first-divergent-transform-stage)
- [Doctrine 33: Exit before opcode](#doctrine-33-exit-before-opcode)
- [Doctrine 34: Class gates observation tools](#doctrine-34-class-gates-observation-tools)
- [Doctrine 35: Device-trust sidecars are session-fresh gates](#doctrine-35-device-trust-sidecars-are-session-fresh-gates)
- [Doctrine 36: Morph and state-chain before track folklore](#doctrine-36-morph-and-state-chain-before-track-folklore)
- [Doctrine 37: Event latch is not host-scalar parity](#doctrine-37-event-latch-is-not-host-scalar-parity)
- [Doctrine 38: Gateway accept is not business pass](#doctrine-38-gateway-accept-is-not-business-pass)
- [Doctrine 39: Ownership before rewrite](#doctrine-39-ownership-before-rewrite)
- [Doctrine 40: Same-world consistency before slot rewrite](#doctrine-40-same-world-consistency-before-slot-rewrite)
- [Doctrine 41: Protocol profile is not viewport spoof](#doctrine-41-protocol-profile-is-not-viewport-spoof)
- [Doctrine 42: Issued challenge artifacts must be consumed](#doctrine-42-issued-challenge-artifacts-must-be-consumed)
- [Related references added for dual writers and local challenge executors](#related-references-added-for-dual-writers-and-local-challenge-executors)

## Doctrine 1: Trust the wire, not the page text

- Real request paths beat page hints.
- Real headers beat visible business code.
- Real cookies beat guessed token stories.
- Real response shape beats archived notes.
- A `200 OK` document, loading placeholder, or rendered shell does not prove the business payload lives in the HTML.
- HTTP 403 JSON forbidden on this API is not session death when sibling APIs on the same session still return 200.
- The same 403 is transport admission when those admitted bytes 403 on stdlib and return business 200 on installed curl impersonate; do not restart signer reverse first.

## Doctrine 2: The dynamic parameter is not always a signature

The real moving part may be:

- a cookie
- a page-specific header
- a transport envelope
- a server-returned JS bootstrap
- a dynamic font
- a WebAssembly export
- a transport wrapper rewrite
- a response-side decoder
- an account-bound session contract

Do not assume every hard target is solved by hunting a `sign` function.

## Doctrine 3: Fixed-input validation beats naming

If a page helper is called `md5` or `btoa`, prove it on fixed inputs before trusting the name.

Minimum standard for suspicious helpers:

1. pick a fixed input such as `"abc"` or a captured timestamp
2. record browser output
3. record local output
4. compare intermediate values, not just final output

Node eval of a harvested digest file is a different environment, not a second browser sample.
A hasher-internal eval of recovered R is a side-effect bomb, not a second sample; stub it. hashlib ascii and digit-byte dual miss on a frozen timestamp keeps the bundled helper.
A statement-split named RSA, JSBN, or JSEncrypt helper is still PKCS#1 until padding and concat miss. Freeze the pad string before gold-token policy: random type 2 makes inequality expected, a proved constant PS makes equality a valid oracle, and textbook raw is a different writer.

## Doctrine 4: Narrow exceptions stay narrow

If only one page needs a special `User-Agent`, or only one request needs a rotated cookie, encode that exception explicitly.
Do not poison the entire collector with a fake "browser-only" conclusion.

## Doctrine 5: Automation is not an acceptable crutch

When stuck, do more protocol work:

- diff requests
- extract inline scripts
- run bootstrap JS locally
- port helper logic
- instantiate WASM locally
- decode fonts locally
- decode CSS-in-HTML sprites locally: hide-class, in-flow offset, image-byte identity

Do not fall back to browser automation as delivery.

## Doctrine 6: Environment mismatch is evidence

When local output and live output disagree, treat the mismatch as evidence:

- compare fixed inputs
- compare side assets
- compare patched helpers
- compare environment branches
- compare Node eval of a harvested digest against the browser branch rather than treating Node as the oracle
- Node eval of recovered R is not an environment sample; stub eval and timers because `require` exists there

Do not hand-wave the mismatch away as "probably browser-only".

## Doctrine 7: Delivery gates outrank convenience

If the only known path still depends on live page context, the task is not done.

- a browser profile is not a protocol artifact
- a hidden refresh click is not a collector
- an unexplained decoder is not acceptable handoff

Keep reversing until the moving parts are local, explicit, and testable.

## Doctrine 8: Public does not mean unsigned

Anonymous pages still have protocol contracts.

- a public list may still require entry-route cookies
- a public route may still require both page-seeded state and request-scoped signer material on the anonymous chain
- a bootstrap endpoint may still return the key, config, or envelope seed
- list visibility does not prove detail or submit visibility
- if a clean anonymous path exists, prove it before contaminating the baseline with logged-in cookies or account state

Treat anonymous access, envelope construction, and permission boundaries as separate questions.

## Doctrine 9: Stateful streams are protocol, not browser magic

If the target only becomes readable after login, pairing, or a warm-up WebSocket exchange, the session transcript is part of the protocol.

- pairing or login bootstrap is not UI fluff
- handshake outputs are protocol artifacts
- heartbeats, ack frames, counters, and reconnect rules are part of the collector

Do not collapse a stateful stream problem into a fake single-request sign story.

## Doctrine 10: Observer effect is real

Some targets get harder after you touch them.

- verifier-gated or behavior-sensitive flows may change once hooks, breakpoints, or monkey patches are installed
- capture one clean baseline request and response before invasive instrumentation
- prefer initiator stacks, request diffs, and narrow boundary hooks before broad global hooks
- if hooking changes the failure mode, treat that as evidence that your tooling is perturbing the target
- wrapping the product cookie setter on a mint host can poison the artifact even when the wrapper is observe-only
- when page-world observation stays observer-toxic, upgrade debugger-trace means with `references/silent-value-capture-playbook.md` instead of widening hooks
- a dead `!==` around one `Function("debugger")` does not make attach safe

Do not confuse hook-induced breakage with proof that the site is "browser-only".

## Doctrine 11: Cookie provenance beats cookie superstition

When a cookie gates replay, prove where it came from:

- `Set-Cookie` on a protocol response
- `document.cookie` from page code
- server-returned challenge or bootstrap JS
- redirect wrappers, iframes, workers, or SDK side effects
- a derived header or token that only looks like a cookie problem

Do not hardcode a rotating business cookie before proving its writer and refresh path.

## Doctrine 12: Packet framing and crypto are separate contracts

When a target uses encoded URL params, encoded form bodies, encrypted responses, or environment-bound cookies from the same page family, do not collapse everything into "the AES" or "the sign".

- separate outer packet framing from inner crypto: version byte, field prefix, checksum, custom alphabet, length rules, and state-derived slices may be just as binding as the cipher
- if the signer consumes a `fullUrl` or canonical request string, parameter order, empty fields, and URL encoding are part of the protocol contract
- prove whether URL, body, response, and cookie are four unrelated formats or one shared envelope family with small field-specific variants
- prove whether later requests need current session state bytes, storage state, or challenge output in addition to business plaintext
- if the decrypted response does not start at byte zero, treat prefix stripping and payload anchoring as part of the protocol, not parser cleanup noise
- if a key looks indirect, wrapped, or masked, recover the key-normalization step before blaming the AES mode or padding
- a named AES/GCM/WASM export can avalanche and still use packed keys, a non-textbook frame, XOR/end, or an inner-field PRNG; the primitive name is not the wire

Do not call crypto solved until framing, state dependency, and payload extraction are also locally reproducible.

## Doctrine 13: Pagination is a protocol surface

Pagination is not just UI chrome.
It can be part of the protocol contract.

- later pages may switch endpoint families even when page 1 looks static
- one working filename pattern does not prove the whole list uses that pattern
- a visible pager can hide a route cutoff where static pages become `/ui`, Ajax, or another endpoint family
- the collector should prefer live next-page targets over guessed page arithmetic once a route pivot is suspected

Do not call pagination solved until later pages are replayed through the same collector logic.

## Doctrine 14: Raw source can beat parsed DOM

When replay-critical route data lives inside inline handlers or legacy attributes, parsed DOM values may not be canonical.

- unescaped `&`, broken entities, legacy templates, or repair logic can mutate query strings or parameter names
- browser getters, HTML parsers, and beautifiers may normalize away the bytes that actually matter for replay
- when inline attributes carry the next route, freeze the raw tag snippet and compare it against parsed values before trusting either

Do not assume a DOM-decoded attribute is safe to replay just because it looks readable.

## Doctrine 14A: Server-looking field names do not prove server issuance

Names such as `__RequestVerificationToken`, `pageId`, request id, nonce, trace id, session cookie, or fingerprint cookie can be misleading.

- prove who writes the field: page code, wrapper code, bootstrap response, or server
- test tolerance with multiple fresh locally generated values under one known-good session
- session-looking or fingerprint-looking cookie names do not prove `Set-Cookie`; some are locally minted from bootstrap config, fingerprint vectors, or structured UUID variants
- if a locally minted field survives fresh conforming values, preserve the exact structure: inserted prefixes, fixed-width segments, compact JSON order, digest chaining, and key normalization steps
- cross-runtime parity on fixed inputs beats approximate randomness matching
- downgrade the field from hard gate to local filler if replay stays stable across fresh conforming values

Do not spend hours reversing decorative randomness just because the field name sounds important.

## Doctrine 14B: Minted session is not admitted session

A fresh cookie from a public warm-up, current-user, or bootstrap route may prove only that the transport and anonymous shell are alive.

- separate session minting from business admission
- if captured business cookies replay but freshly minted anonymous cookies do not, treat that as evidence that the request contract is solved and the missing piece is session bootstrap or permission state
- do not keep blaming the signer when the failure mode is a route-specific permission denial

Do not confuse "I have a new session" with "this session is authorized for the business method I care about."

## Doctrine 14C: Enumeration and hydration are separate contracts

List, detail, download, and export routes often share one envelope family but differ in identifiers, permission boundaries, and cost.

- solve one route, then probe sibling routes for shared wrapper and decoder reuse
- persist stable ids from the cheap enumeration stage
- persist normalized outputs and raw decoded payloads so later full-text or rule-based backfill does not require rerunning the entire crawl

Do not weld expensive detail hydration into the only path through the collector when a staged design is cheaper and safer.

## Doctrine 15: Embedded runtimes are scalpels, not a second browser

Use an embedded browser-like runtime such as `iv8` only for the narrow part that still needs host semantics.

- first decode and handwrite simple formulas in Python when fixed-input proof is cheap
- route to an embedded runtime only when JS depends on browser-visible host semantics such as `navigator`, `screen`, `location`, DOM lifecycle, timers, `document.cookie`, XHR wrappers, or reflection on native surfaces
- keep the runtime local and narrow: recover one token, cookie, URL suffix, wrapped body, or decoded payload, then hand control back to Python
- if the target still needs full rendering, gestures, canvas noise, or live browser state on every request, the runtime is still an analysis instrument, not proof that delivery is solved

Do not let a local runtime quietly become browser automation with fewer tabs.

## Doctrine 16: Probe chains reveal the missing surface

Modern targets often inspect the environment before any signer runs.

- watch which API is read, enumerated, stringified, or reflected before patching random globals
- treat `Object.keys`, `Reflect.ownKeys`, descriptor reads, `Function.prototype.toString`, `JSON.stringify`, and `document.all` as first-class evidence surfaces
- if a temporary patch is necessary, make its reflected shape match expectations as closely as possible
- use probe evidence to choose between fixing identity semantics, enumeration order, timing, cookie state, or a missing native-looking boundary

Do not collapse silent environment-probe branches into vague "JS obfuscation".

## Doctrine 17: Transport admission is a separate contract

Some targets block the clean baseline before signer, cookie, or decode logic is even visible.

- TLS fingerprint, ALPN, HTTP version, UA family, and route choice can decide whether the application contract is reachable at all
- copied HTTP headers do not clear a gate that is decided by ClientHello or HTTP/2 profile before normal request semantics exist
- JA3 or JA4 are summary indicators; compare the underlying ClientHello, ALPN, and H2 behavior before cargo-culting one hash
- when one browser family randomizes extension order or GREASE, preserve the family behavior or raw field profile instead of freezing one unstable summary value
- if stdlib clients die at H2 reset, timeout, or early disconnect while an impersonated transport passes, solve admission first and keep the exception narrow
- one landing route may be challenged while a sibling auth or data route remains usable; verify route-local policy before reversing the wrong fight
- prefer the closest transport family or narrow adapter before hand-patching a distant default stack one field at a time

Do not blame signer or cookie logic for traffic that never cleared transport admission.

## Doctrine 18: Harvest challenge artifacts at the nearest stable boundary

Do not over-solve a hostile runtime when one explicit artifact is enough.

- if a bootstrap runtime exposes a stable getter after synchronous init, call it before patching every later timer or DOM gap
- if the script self-submits via XHR or fetch, intercept the outgoing body and headers locally instead of emulating every opcode
- if a public multi-arity WASM/JS export already returns wire-shaped I/O, harvest that oracle before rebuilding inner AES/GCM
- preserve scheduler semantics: use execution paths that keep timers, microtasks, and request hooks alive
- patch the smallest faithful boundary and let structural errors propagate; a catch-all that hides recursion or state corruption is sabotage

Do not treat full challenge execution as the goal when one explicit artifact is enough for Python replay.

- prefer navigation or redirect URL harvest before cookie-by-cookie reverse when the runtime already rewrites the business URL
- treat business JSON routes that return challenge HTML as challenge bootstrap, not as a dead endpoint
- if one field has both a short research writer and a long wire-success writer, deliver only the live-accepted class

## Doctrine 19: Server-issued state beats local invention

Before rebuilding anything locally, inventory what the server already hands you.

- list session ids, work factors, asset URLs, answer schema, movement bounds, wrappers, and expiry windows separately from locally computed values
- preserve the scope and lifetime of each issued artifact: page-scoped, request-scoped, route-scoped, or session-scoped
- page-scoped challenge submit tokens must come from the current document; a previous page's token can return HTTP `200` with an empty body and is not a grant
- check/submit can accept the answer while a sibling complete flag stays false until the challenge document is GETed on the same jar; answer-accept is not complete
- do not waste time re-deriving locally what the server is already willing to issue unless refresh logic or binding rules force you to

Do not reverse-engineer a server-issued artifact when the real problem is how to carry, refresh, or bind it correctly.

## Doctrine 20: Split verifier targets by failure surface

When a verifier mixes requests, hashes, images, and behavior, force the problem into surfaces:

- protocol surface: endpoint chain, wrappers, session state, payload shape
- compute surface: hashes, PoW, encoding, packing, canonicalization
- perception surface: image preprocessing, transparency, coordinate mapping, match confidence
- behavior surface: trajectories, timing, gesture sidecars, telemetry blobs
- freeze the full ordered verifier transcript, including warm-up and telemetry routes, before treating the final verify request as the whole contract
- use one-variable block, omit, and restore controls to prove whether a sidecar changes final semantic acceptance
- model complete profile baselines and sparse deltas as one shared state contract rather than independently valid packets
- preserve actual wall-clock ordering when the transcript claims elapsed interaction time
- compare active asset hashes, helper boundaries, and fixed vectors before treating a dynamic path as a new algorithm
- attach an independent proof to each surface: raw responses, fixed-input tests, visual QA, and replay proof

Do not let a perception or behavior failure masquerade as a signer bug.

## Doctrine 21: Weak enforcement is evidence, not absolution

If an empty, stubbed, or simplified field passes once, record the tolerance carefully.

- capture the exact route, environment, and response when the relaxed field is accepted
- keep the field in the protocol model unless repeated evidence proves it is irrelevant for the route family you care about
- assume stricter production routes may enforce the field even if a public or demo route did not
- dummy collect accepted beside required POW or visual oracles is route-tolerance, not proof that collect never matters

Do not delete a field from the protocol story just because one relaxed path accepted it.

## Doctrine 22: Escalate one rung at a time

When the current proof fails, move up one layer only after you can say:

- what still works
- what exact blind spot remains
- why the heavier layer is the smallest layer that answers that blind spot

Do not jump from "Python parity is incomplete" straight to broad host emulation, and do not jump from "local runtime loads" straight to pagination or scale.

## Doctrine 23: Small facts age better than big summaries

When a target family or upgrade path looks reusable, preserve 5 to 15 minimal verifiable facts:

- route pivots
- field slots
- artifact shapes
- decode order
- session-chain rules
- acceptance checkpoints

Prefer re-checkable structural facts over copied cookies, secrets, or long narratives.

## Doctrine 24: Counterexamples constrain better than slogans

When the same bad move keeps recurring, promote it into a reusable anti-pattern:

- name the tempting shortcut
- explain why it creates false progress
- state the smallest honest next move
- end with one direct self-check

Use `references/anti-patterns-playbook.md` for those counterexamples.

## Doctrine 25: Positive-sample hygiene beats track tuning

When a verifier rejects behavior-sensitive proofs:

- treat clean success samples as higher authority than automation-contaminated failures
- prefer ordinary browser capture or non-instrumented listening over hooked automation profiles for positive oracles
- do not promote a failed automation hand-slide into proof that the trajectory family is wrong
- separate sample grades: clean success, contaminated failure, partial transcript
- read `references/positive-sample-hygiene-playbook.md`

Do not spend the next hour mutating tracks while the only negatives came from a polluted environment.

## Doctrine 26: Environment risk is its own failure surface

Split verifier failure surfaces explicitly:

- protocol and shared-state consistency
- compute or packing helpers
- perception or answer extraction
- behavior traces
- telemetry sidecars
- session freshness
- transport admission
- environment risk: exit reputation, automation marks, consecutive rejects, profile age

A structurally valid transcript can still fail after the environment score collapses. Change the environment surface on purpose; do not hide that work inside track search.

## Doctrine 27: Two surfaces to confirm, one to suspect

Before hardening a gate-family label, widening runtime, or handing work to a specialist:

- require two independent evidence surfaces
- one status code, cookie name, token name, old note, or plausible helper output is only a hypothesis
- missing specialist means generic Spider fallback, not a invented family shortcut

Read `references/evidence-corroboration-gate.md`.

## Doctrine 28: Ablate one owned layer at a time

When a clean success sample exists and the local path fails:

- freeze one positive oracle
- prove the local channel with the untouched success body when replay is legal
- replace exactly one ownership layer per experiment
- stop at first failure and open only that layer
- reverse-minimal control before durable implementation changes

Read `references/positive-sample-hygiene-playbook.md` then `references/positive-sample-ablation-playbook.md`.

## Doctrine 29: Name one failure surface before broad patches

Pick a primary surface before rewriting algorithms:

- `egress-environment` → `transport-admission` → `session-chain` → `request-contract` → `signer-confidence` / `verifier-sidecar` → `business-oracle`
- soft challenge shells, length heuristics, and single `200`s are not collector completion
- exit-only recovery is `egress-gated`, not proof of algorithm regression

Read `references/failure-surface-taxonomy.md`.

## Doctrine 30: One baseline pure end to end

Do not splice UA/Client-Hints, cookies/storage, fingerprint surfaces, and transport/exit from different captures into one replay chain.

- foreign fingerprint caches are contrast only; re-sample host-local values on the execution host
- stage-field bundles map to Phase 0-5; do not invent a second phase numbering system
- patch by `first_divergence` minimal units inside the current rung

Read `references/env-diff-playbook.md`, `references/workflow-overview.md`, and `references/reproducible-evidence-playbook.md`.

## Doctrine 31: Class before family folklore

Name `signature-bound`, `behavior-interceptor`, or `pure-obfuscation` from wire/runtime evidence before hardening vendor or SDK labels. Class selects method bias only.

- a URL or timeline substring is not family proof
- the same vendor can expose a mintable non-final bootstrap face and a hard interstitial face; do not merge them

Read `references/anti-bot-class-playbook.md`.

## Doctrine 32: First divergent transform stage

When local and browser signer outputs disagree, walk the seven-stage parity chain and stop at the first mismatch. Empty-body HTTP `200` is silent reject, not success.

Read `references/signer-parity-chain-playbook.md` and `references/failure-surface-taxonomy.md`.

## Doctrine 33: Exit before opcode

Name the final wire artifact and its visible exit before opening VM centers. Reverse-trace from that exit through producers; do not tour dispatch loops first.

Read `references/jsvmp-analysis-playbook.md`.

When the outer shell is only an emulator for a nested standard ISA or fixed memory image, dump the initialized memory, run a standard simulator from the proved entry, and drop the outer shell. Do not tour the emulator source first.

Public codec functions are exits too. `encodeURIComponent`, `unescape`, `Utf8.parse`, and hex nibble `join` can be the last visible preimage boundary. Hook those before opening VM centers. `$fast_unpack` / magic `WAFJ` that returns JavaScript source is an unpacker exit; read that source before touring unpacker opcodes.

## Doctrine 34: Class gates observation tools

`signature-bound`, `behavior-interceptor`, and `pure-obfuscation` constrain which hooks and preloads are legal. Proxy-all or pre-inject storms that poison a signature-bound sample are method errors.

Read `references/anti-bot-class-playbook.md` and `references/hook-techniques.md`.


## Doctrine 35: Device-trust sidecars are session-fresh gates

When a verifier consumes a fingerprint/device companion bound to mid/session:

- packer and track ownership do not prove companion trust
- official apply-path wiring beats "local Init untrusted" slogans
- local JS runtime (L2) may run the vendor SDK; do not call that pure-Python field port (L3)
- same-session immediate verify beats cross-session gold rebind
- label rejects as device-trust, stale-session, track-bind, rate-lock, or packer-crypto before broad patches

Read `references/device-trust-sidecar-playbook.md` and `references/local-sdk-env-patch-playbook.md`.


## Doctrine 36: Morph and state-chain before track folklore

When a multi-surface verifier returns a stable semantic reject despite mint-shaped tokens:

- positive samples prove existence, not mandatory morph
- envelope/codec success is not gate success
- ablate morph -> state-chain -> companions -> token-writer before track entropy
- same-family solved skeletons are process templates to migrate, not excuses to re-animate behavior walls first
- stability is an N-run hard-gate rate; L2 local JS helpers must not be sold as pure-Python field ports

Read `references/verifier-morph-and-state-chain-playbook.md`, `references/positive-sample-ablation-playbook.md`, and anti-patterns 37-44.

- false-progress blacklist: common-prefix/length-to-gold, mint-variant count, quieter helper logs
- mandatory kill-switches K1-K8 and day-card before another reverse day
- wall taxonomy: envelope/morph/state-chain/companion/writer/track/egress

## Doctrine 37: Event latch is not host-scalar parity

Some bootstrap scripts mint only after a collector pass registers `load` or `DOMContentLoaded`.

- evaluating into an already-complete document means native events will not fire again
- wait for a public collector-ready object, then synthesize the event
- matching UA, arch, or eval-length does not prove mint ran
- mutating collected fields is not the mint path

Read `references/server-js-cookie-bootstrap-playbook.md` and `references/local-challenge-executor-playbook.md`.

## Doctrine 38: Gateway accept is not business pass

Split precursor accept, verifier gateway accept, server grant presence, and business-oracle pass.

- verify/report `200` or envelope success can still leave the business route challenged
- server grants are parsed from the grant response, not invented
- consumed challenge ids are invalid ablation oracles

Read `references/verifier-replay-playbook.md` and `references/failure-surface-taxonomy.md`.

## Doctrine 39: Ownership before rewrite

Label decisive fields `python-owned`, `host-owned`, or `server-owned` before porting.

- host-owned materials need real script entries first
- same field names at different request sites are different slots by default
- script versions are round facts, not skill constants
- one slot may still contain layered sub-ownership (pure compute plus lifecycle state)

Read `references/parameter-ownership-playbook.md`.

## Doctrine 40: Same-world consistency before slot rewrite

Multi-slot verifier chains fail when each field looks locally valid but the fields describe different worlds.

Before rewriting any slot algorithm, prove one same-world gate for the round:

- one `roundKey` / challenge primary key threads precursors, materials, verify, and grant
- identity cookies, device/UMID-like tokens, and jar snapshots agree across Python session and every host helper
- one event or behavior sequence feeds every consumer that claims to observe it
- any signer that consumes a canonical URL or request string uses the exact bytes later sent
- stop assemble and send when any gate fails; do not debug trajectory or packing first
- one protocol profile feeds every helper; viewport spoofing is not profile proof

A field that matches length and alphabet is not same-world proof. Read `references/parameter-ownership-playbook.md` and `references/verifier-replay-playbook.md`.



## Doctrine 41: Protocol profile is not viewport spoof

Device-toolbar, responsive preview, or a changed UA string is not a protocol profile.

A protocol profile freezes the surfaces helpers actually read together:

- scene / client class
- UA and Client-Hints
- platform, touch capability, and event semantics
- screen geometry and challenge widget geometry
- any fingerprint surfaces the scripts read in-round

All host helpers in the round must read one profile. Viewport cosplay with desktop semantics is a method error. Read `references/parameter-ownership-playbook.md` and `references/env-diff-playbook.md`.

## Doctrine 42: Issued challenge artifacts must be consumed

When a verifier issues an image, token, or puzzle before later pages:

- unused issuance can count as a session miss even if the next submitted answer is correct
- submitted-wrong is often retryable on a newly issued round; skip-to-refresh is not
- the same `rate`/`score` field can be cumulative on accept and closeness on reject
- verifier accept below the session floor is not a business grant
- search the full canvas and a piece-sized four-edge rectangle before blaming the scorer

Read `references/challenge-state-envelope-playbook.md` and `references/verifier-replay-playbook.md`.

## Related references added for dual writers and local challenge executors

- `references/dual-writer-param-playbook.md`
- `references/local-challenge-executor-playbook.md`

