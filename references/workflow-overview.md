# Workflow Overview

Use this file as the shortest end-to-end map for a pure-web reverse job. APK, native app, and mini-program primary reverse are out of scope for Spider King.

## Startup gate

Before deep work:

- declare `live-target`, `artifact-only`, or `continuation`
- check local tool sanity
- for web `live-target`, record the capability snapshot, confirm both browser tool families without opening the target in both, then assign initial `TARGET_ACTIVE` ownership to `chrome-devtools`; APK/app/mini-program primary tasks are out of scope and must not invent this paired first-pass
- for `artifact-only`, start from the supplied files or captures and mark live acceptance as unproven
- for `continuation`, reuse the current gate and reopen only the evidence surfaces invalidated by the new input
- classify the target as `signer-gated`, `verifier-gated`, `decode-gated`, or `session-gated`
- state the smallest acceptable browser-free delivery shape
- distinguish "browser-free now" from "runtime-free goal" when an embedded host is being considered
- if the next move would widen the runtime, patch surface, or transport profile, read `references/escalation-ladder-playbook.md` first
- before implementing an ambiguous or authority-widening `compact-replay` or `collector`, record the conditional implementation brief from `references/provider-work-order.md`; do not impose it on bounded `evidence`, `local-proof`, or explicit no-write analysis

## Browser handoff checkpoints

- capture the clean Chrome baseline first
- before activating `js-reverse`, save the baseline evidence and apply the handoff gate in `references/tool-playbook.md`
- mark the prior family `PARKED`; use `RETAINED_EXCEPTION` instead when cleanup would destroy the only unreplayable session or verifier state
- when returning to Chrome, park `js-reverse` first and reacquire or restore the Chrome evidence state explicitly
- use `CLOSED` only after the installed tool confirms termination

## Phase 0: Fingerprint the target

Before touching code, classify the target:

- decoy endpoint vs real endpoint
- wrapper rewrite vs visible param
- patched helper vs standard helper
- signer-gated vs verifier-gated vs decode-gated vs session-gated
- session-bound vs anonymous
- bootstrap asset vs direct data API
- one-page exception vs whole-flow exception
- clean-baseline-first vs trace-first vs decode-first vs transcript-first
- JSVMP or heavy obfuscation vs normal packed bundle

## Phase 1: Prove the real request

- capture the request that returns useful data
- record its initiator
- record exact query, body, headers, cookies, and response shape
- store fresh captures in a task-local cache separate from stable helper code or user-maintained fixtures

## Phase 2: Isolate the moving state

Treat each moving part separately:

- timestamp
- random fragment
- rotating cookie
- response-side refresh tuple or challenge subcode payload
- transport wrapper field
- page-specific header
- session contract
- bootstrap output
- cookie provenance

## Phase 3: Rebuild offline

Choose the cheapest valid path:

1. pure Python
2. Python plus tiny JS helper
3. Python plus tiny WASM helper
4. Python plus local bootstrap executor

For verifier-gated or challenge-bootstrap targets, do not widen host patching or runtime-removal work until one fresh single-page live replay succeeds on one session chain.
When the same business route first returns a machine challenge and then succeeds after local refresh, keep that fail -> refresh -> success loop on the same session chain and prove it before searching for alternate endpoints.
Climb one rung at a time and record why the lighter rung failed before escalating.
Use `references/escalation-ladder-playbook.md` when the next move is debatable.

When captured target code, HTML, or runtime blobs are volatile, generate temporary local runners from the fresh cache instead of overwriting stable scaffolding by default.

## Phase 4: Verify repeatability

- helper outputs match fixed test vectors
- local helper load success, fewer exceptions, or browser-shaped artifacts are not counted as success unless the real request replays repeatedly
- verifier-gated targets keep working after you remove broad hooks
- page 1 replays at least twice
- single-page live replay is proven before pagination scaling or runtime shrink work
- pagination or cursor works
- known exceptions are encoded narrowly
- bootstrap-heavy targets keep one session chain intact unless cross-session reuse is explicitly proven

## Phase 5: Deliver

- protocol-only collector
- one compact protocol handoff from `references/report-templates.md` as the canonical rerun and audit summary; do not duplicate the same facts across extra project documents
- saved samples
- redacted reports plus a local-only secret store when raw credentials, tokens, or cookie values must be retained
- `analysis/proof_manifest.json` with capability snapshot, artifact hashes, session scope, helper versions, fixed vectors, and live replay counts
- clear notes about headers, cookies, and instability
- when the family is likely to recur, preserve 5 to 15 minimal verifiable facts
- use `references/minimal-verifiable-facts-playbook.md` to keep those facts structural and re-checkable
