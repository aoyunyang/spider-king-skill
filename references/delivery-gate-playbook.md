# Delivery Gate Playbook

Use this reference to accept the declared result shape without silently grading a smaller result as a collector or a partial collector as complete.

## Contents

- [Core rule](#core-rule)
- [Acceptable runnable delivery shapes](#acceptable-runnable-delivery-shapes)
- [Generation truth labels](#generation-truth-labels)
- [Unacceptable delivery shapes](#unacceptable-delivery-shapes)
- [Common gate](#common-gate)
- [False completion signals](#false-completion-signals)
- [Smoke levels L1-L4](#smoke-levels-l1-l4)
- [Evidence gate](#evidence-gate)
- [Local-proof gate](#local-proof-gate)
- [Compact replay and collector gate](#compact-replay-and-collector-gate)
- [Challenge and dual-writer extras](#challenge-and-dual-writer-extras)
- [Graded degrade and stream split](#graded-degrade-and-stream-split)
- [Escalation rule](#escalation-rule)

## Core rule

Apply exactly one primary capability gate: `evidence`, `local-proof`, `compact-replay`, or `collector`.

If a runnable replay or collector still depends on live page context, it is not done. Evidence may describe browser observations, but it must not claim that those observations are a browser-free replay.

Explicit config inputs are acceptable.
Live page reads are not.

If browser-shaped values such as UA, platform, viewport, or screen metrics only survive as signer inputs, they may remain as declared config or sample-derived parameters in the final collector.
That does not justify keeping a browser, embedded runtime, or page-context call alive just to reread them on every run.

## Acceptable runnable delivery shapes

- pure Python HTTP collector
- Python plus isolated local JS helper
- Python plus local WASM helper
- Python plus local bootstrap executor
- Python plus local decoder for fonts, protobuf, msgpack, or compressed payloads

## Generation truth labels

Report opaque signer or profile-backed delivery with one of these labels:

- `algorithmic`: decisive transforms and fresh inputs are regenerated locally without captured final artifacts or captured runtime profiles
- `snapshot-driven`: transforms run locally, but one complete captured runtime profile still supplies opaque or environment inputs
- `pool-backed`: previously accepted final artifacts are selected from a pool

All three can be browser-free during execution, but they are not equivalent.
Snapshot-driven delivery must state capture freshness and scope. Pool-backed
replay is a diagnostic or explicitly accepted bounded fallback, not proof that
issuance or generation was recovered.

## Unacceptable delivery shapes

- browser automation as the collector
- silent-value-capture / engine-instrumentation runtime as the collector
- CDP or page-context `fetch` as the steady-state path
- manual cookie export as an operating requirement
- "works only with my browser profile" handoff
- hidden verifier clicks instead of protocol replay
- importing runtime-backed predecessor modules whose import side effects still patch globals, read cookies, or depend on browser or host state
- live browser or host-runtime reads whose only purpose is to refill payload fields already understood as explicit inputs
- calling snapshot-driven generation or prevalidated artifact-pool replay fully algorithmic

## Common gate

Every shape must pass all common checks:

- the shape and intake mode are stated
- each conclusion is bounded by named evidence or a precise blocker
- unobserved live behavior, endpoint currency, account scope, and runtime provenance are marked unproven
- reports and persisted artifacts contain no raw credentials, tokens, session secrets, cookie values, personal data, or unkeyed low-entropy secret fingerprints
- no task artifact is written outside approved project paths or into the skill directory
- runtime ownership, cleanup state, and residual risk are honest
- unfinished work names a primary failure surface from `references/failure-surface-taxonomy.md` instead of implying collector completion



## Smoke levels L1-L4

Borrow the verifier smoke ladder when challenge or host helpers are in play:

- L1 helper smoke is not delivery
- L2 verifier accept is not business pass
- L3 business oracle on a fresh round is the minimum runnable claim for challenge-gated routes
- L4 multi-round stability is required before calling a hard gate stable

See `references/verifier-replay-playbook.md`.

## False completion signals

- L1 helper smoke or L2 verifier accept packaged as collector completion

None of the following alone completes `compact-replay` or `collector`:

- intermediate challenge, interstitial, or shell document success
- cookie/token length or alphabet heuristics
- helper load success or non-empty plausible output
- mint-shaped tokens or stable structured verifier reject codes
- bootstrap/report telemetry HTTP 200 without verifier grant artifact
- verifier gateway accept without same-round business-oracle pass
- a server grant cookie/token copied from another round or invented locally
- pool/profile generation that only matches offline shape checks
- one HTTP `200` without repeated fresh acceptance
- one lucky gate accept without an N-run success rate on the hard gate metric
- success that appears only after changing exit node with no implementation change (`egress-gated`)
- manual browser state export still required on the run path
- product-foreign consumer oracles (for example a status code taken from another route family)

If the implementation is unchanged and only the exit flips the result, keep the algorithm hypothesis stable and label `egress-environment`.

## Evidence gate

Use this gate for a request specimen, initiator, state writer, mutation point, structural observation, or blocker:

- preserve provenance, ordering, method, route shape, field names, types, lengths, and keyed fingerprints needed for the claim
- distinguish wire, source, browser, environment, and downstream-acceptance evidence
- do not require live replay, a Python entrypoint, dependency installation, or a persisted manifest when the authorized result is no-write conversational evidence
- when an evidence package is persisted, store it under the approved task project and record a secret-free proof manifest
- do not promote evidence to `local-proof`, `compact-replay`, or `collector` without passing that higher gate

## Local-proof gate

Use this gate for a fixed vector, decoded sample, restored source, or callable offline helper:

- record exact non-secret inputs, output or checkpoint, and one negative boundary
- keep the proof offline unless separate live egress was authorized
- label runtime and dependency requirements explicitly
- require no live endpoint, repeated request, or right-click entrypoint unless the user requested executable packaging
- state current live acceptance and session compatibility as unproven

## Compact replay and collector gate

Apply these checks to both runnable shapes; pagination, resume, dedupe, persistence, and scaling checks apply only when promised by `collector`:

1. real endpoint confirmed
2. moving parts named explicitly
3. signer or decoder has fixed-sample proof
4. request succeeds repeatedly; report `repeatableLiveReplay` count when live replay is authorized
5. decode or parser path is local when applicable
6. required session state is explicit
7. no browser dependency remains in the final run path (includes engine instrumentation, silent-value backends, managed profiles, and page driving). Judgment test: would this keep working in a headless CI or container with no GUI browser installed for a long unattended run? If no, the shape fails.
8. host-like signer inputs are explicit config when they are only consumed as values
9. deterministic proof mode and live-generation mode are separated when randomness, timestamp jitter, or filler noise matter
10. opaque staged ports identify the first divergent stage and preserve complete profile provenance when applicable
11. delivery is labeled algorithmic, snapshot-driven, or pool-backed when captured profiles or artifacts are involved
12. pool-backed paths have an explicit exhaustion policy and a no-pool test
13. final helper code is self-contained and free of runtime-backed import side effects
14. when repeated helper calls are part of the protocol, runtime lifetime and continuity are explicit and persistent-world versus fresh-world behavior is tested when applicable
15. `analysis/proof_manifest.json` records intake mode, capability snapshot, keyed artifact fingerprints, session scope, helper versions, fixed vectors, replay counts, and any runtime-profile dependency without copying secrets
16. async export or report jobs prove create with task isolation, keep first-create boundaries honest, and enforce artifact format plus exact requested-field completeness before persistence
17. a PyCharm right-click runnable entrypoint exists (`main.py` or `collector/main.py`) with defaults that need no CLI args
18. investigation caches live under `js_reverse_cache/` while delivery proofs stay in project-root `analysis/`
19. verifier, warm-up, telemetry, or collector-like sidecars are not counted as final success until the downstream business route accepts and returns parseable target data or the requested artifact
20. any residual exit, IP, proxy, or transport reputation dependence is labeled explicitly as `egress-gated` or route-local transport risk instead of being described as implementation flakiness
21. a collector proves every promised bound, pagination, refresh, dedupe, resume, persistence, and output rule beyond the compact replay
22. when a check or submit JSON exposes both answer-accept and complete flags, both must pass; a cookie-only answer POST that leaves complete false is not collector success

For transport-gated collectors, also verify the transport admission contract
inside the final Python path. The collector should expose or record the
negotiated HTTP version (and ALPN when available), keep any connection-reuse
requirement explicit, and fail loudly if the client silently falls back to a
different protocol. A transport `200`, a challenge-shaped body, or a plausible
token is not a business oracle; acceptance requires the promised page/cursor
coverage, field types, and parseable downstream data.

When browser first-pass roles are incomplete, the only runnable transport
claim allowed is the exact `transport-only direct-endpoint exception` in
`references/startup-triage-playbook.md`. The manifest must retain each role
gap, prove every exception entry condition, and label acceptance as scoped to
the exact endpoint; it must not claim page/runtime understanding. Any signer,
bootstrap, wrapper, challenge, decode, renderer, or interaction dependency
fails this exception and restores the ordinary live-target role gate.

## Challenge and dual-writer extras

For verifier-gated deliveries, reports must state separately whether precursor, verifier gateway, server grant, and business oracle passed. "slide/verify 200" language alone is insufficient.

When a `compact-replay` or `collector` is challenge- or verifier-gated, also require:

- X1: wire-success token or param class is identified; rejected short or research-only writers are labeled misleading
- X2: live regeneration works on a fresh timestamp, page, or equivalent variable input
- X3: if a local challenge executor is used, it returns a Python-replayable artifact and is not Playwright or CDP page-driving
- X4: app-layer signer gates and challenge verifier gates are listed separately with necessity proof
- X5: original-URL echo fields are included when replay evidence requires them
- X6: sidecar ablation matrix exists and shows which stages are necessary
- X7: shared baseline and sparse or delta packets are consistency-checked on one round
- X8: final acceptance uses platform verifier semantics plus first downstream consumer pass
- X9: positive-sample hygiene grade is recorded for any human or browser oracle
- X10: task-local error semantic map exists when reject codes guided debugging
- X11: if a tiny JS or WASM helper remains, install steps and baseline artifact files are packaged without secrets

## Graded degrade and stream split

Optional dependencies (OCR diagnostics, extra transports, secondary oracles) must not hide our bugs as "platform down".

- `ImportError` / `NameError` / missing local module = our bug. Alarm on stderr (`!!!`); do not silent-fallback as if the vendor were down
- vendor timeout, HTTP 5xx, or a typed external error = fallback is allowed
- a leftover `except Exception` still alarms; it does not stay quiet
- print key request/response summaries to **stderr**
- keep **stdout** as machine JSON for the final summary so `>result.json` stays parseable

This is a collector-hygiene rule. It does not add OCR, captcha-platform, or browser automation to the delivery path.

## Escalation rule

If a gate for the declared shape fails, do not package the result under that shape. Continue until it passes or return a lower shape that independently passes its own gate and states the higher-shape blocker explicitly.
