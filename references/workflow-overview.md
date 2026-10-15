# Workflow Overview

Use this file as the shortest end-to-end map for a pure-web reverse job. APK, native app, and mini-program primary reverse are out of scope for Spider King.

Phase numbers here match the Universal Reverse Loop in `SKILL.md`. Cross-cutting rules are not extra phases.

## Contents

- [Startup gate](#startup-gate)
- [Browser handoff checkpoints](#browser-handoff-checkpoints)
- [Phase 0: Fingerprint the target](#phase-0-fingerprint-the-target)
- [Phase 1: Prove the real request](#phase-1-prove-the-real-request)
- [Phase 2: Isolate the moving state](#phase-2-isolate-the-moving-state)
- [Phase 3: Locate the canonical mutation point](#phase-3-locate-the-canonical-mutation-point)
- [Phase 4: Rebuild offline](#phase-4-rebuild-offline)
- [Phase 5: Deliver](#phase-5-deliver)
- [Multi-stage settle rule](#multi-stage-settle-rule)
- [Stage fields checklist](#stage-fields-checklist)
- [Phase map for stage fields](#phase-map-for-stage-fields)

## Startup gate

Before deep work:

- declare `live-target`, `artifact-only`, or `continuation`
- check local tool sanity
- for web `live-target`, record the capability snapshot including attach and optional `silent_backend` (`available` or `absent`); confirm available browser tool families without opening the target in both; assign initial `TARGET_ACTIVE` to `chrome-devtools` by default, or to `js-reverse` alone when DP/initiator work is already required (do not launch a second Chrome; never record `launch` as `attach`)
- if `silent_backend=absent`, do not probe capture backends; after attach/js-reverse gaps, continue offline rebuild or lower the delivery shape
- APK/app/mini-program primary tasks are out of scope and must not invent the paired first-pass
- for `artifact-only`, start from the supplied files or captures and mark live acceptance as unproven; do not open dual-role browser ceremony
- for `continuation`, reuse the current gate and reopen only the evidence surfaces invalidated by the new input
- classify the target as `signer-gated`, `verifier-gated`, `decode-gated`, or `session-gated`
- state the smallest acceptable browser-free delivery shape
- distinguish "browser-free now" from "runtime-free goal" when an embedded host is being considered
- if the next move would widen the runtime, patch surface, or transport profile, read `references/escalation-ladder-playbook.md` first
- before implementing an ambiguous or authority-widening `compact-replay` or `collector`, record the conditional implementation brief from `references/provider-work-order.md`; do not impose it on bounded `evidence`, `local-proof`, or explicit no-write analysis

## Browser handoff checkpoints

- capture a clean baseline first: `chrome-devtools` unless DP/initiator work is already required, in which case `js-reverse` owns both roles on one host
- before activating a different debugger-trace family or silent-value engine capture, save the baseline evidence and apply the handoff gate in `references/tool-playbook.md`; if `js-reverse` already owns baseline, attach/select the current page and do not open `chrome-devtools`
- debugger-trace means: default `js-reverse` when attach exists; use `silent-value-capture` immediately on upgrade triggers, or when attach is missing but a backend is available (`references/silent-value-capture-playbook.md`)
- mark the prior family `PARKED`; use `RETAINED_EXCEPTION` instead when cleanup would destroy the only unreplayable session or verifier state
- when returning to a Chrome-owned baseline that is not the current DP host, park `js-reverse` first and reacquire or restore that Chrome evidence state explicitly
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

Before closing this phase, answer the static analysis six questions in `references/minimal-verifiable-facts-playbook.md` (scope, dynamic factors, response side, runtime codegen, precursors, chain rewrite). If interceptors or VMs appear, also classify signer entry and apply exit-first analysis from `references/jsvmp-analysis-playbook.md`.

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

When business replay fails against a browser success packet, recover the request contract with `references/session-contract-playbook.md` before deepening signer work. Keep one baseline pure (`references/env-diff-playbook.md`).

## Phase 3: Locate the canonical mutation point

Trace in this order:

1. transport wrappers, interceptors, fetch/XHR/Ajax, worker, or message boundaries
2. bootstrap scripts and inline payloads
3. exposed helpers and returned child objects
4. WASM exports or inner serializer/packer/signer/decoder primitives
5. server-returned challenges and response-side refresh fields
6. frame serializers, protobuf parsers, handshake transcripts, and key schedules

The canonical mutation point is where the wire-shaped payload actually changes, not where business code creates a placeholder.

## Phase 4: Rebuild offline

Choose the cheapest valid path:

1. pure Python
2. Python plus tiny JS helper
3. Python plus tiny WASM helper
4. Python plus local bootstrap executor

Climb one rung at a time and record why the lighter rung failed before escalating.
Use `references/escalation-ladder-playbook.md` when the next move is debatable.
Inside a rung, patch only the `first_divergence` minimal unit (`references/reproducible-evidence-playbook.md`).
When stage counts differ from the browser path, apply the multi-stage settle rule below before algorithm rewrites.

For verifier-gated or challenge-bootstrap targets, do not widen host patching or runtime-removal work until one fresh single-page live replay succeeds on one session chain.
When the same business route first returns a machine challenge and then succeeds after local refresh, keep that fail -> refresh -> success loop on the same session chain and prove it before searching for alternate endpoints.
When captured target code, HTML, or runtime blobs are volatile, generate temporary local runners from the fresh cache instead of overwriting stable scaffolding by default.

## Phase 5: Deliver

This phase is `SKILL.md` Phase 5 (**Prove repeatability and scale**) plus delivery packaging. There is no separate phase number beyond Phase 5.

### Prove repeatability

- helper outputs match fixed test vectors
- local helper load success, fewer exceptions, or browser-shaped artifacts are not counted as success unless the real request replays repeatedly
- verifier-gated targets keep working after you remove broad hooks
- page 1 replays at least twice when live replay is authorized
- single-page live replay is proven before pagination scaling or runtime shrink work
- pagination or cursor works when promised
- known exceptions are encoded narrowly
- bootstrap-heavy targets keep one session chain intact unless cross-session reuse is explicitly proven
- unfinished work names a primary failure surface (`references/failure-surface-taxonomy.md`) instead of implying collector completion

### Delivery packaging

- protocol-only collector or compact replay with no browser automation on the final path
- one compact protocol handoff from `references/report-templates.md` as the canonical rerun and audit summary; do not duplicate the same facts across extra project documents
- saved samples, redacted reports, and `analysis/proof_manifest.json` when writes are authorized
- clear notes about headers, cookies, residual risk, and browser-free status
- when the family is likely to recur, preserve 5 to 15 minimal verifiable facts via `references/minimal-verifiable-facts-playbook.md`

## Multi-stage settle rule

Cross-cutting rule for Phase 2-5. Not a separate phase number.

When the browser path shows multiple ordered bootstrap or sensor-like posts and the local path emits fewer stages:

1. diff stage count, timing, body size/framing sequence, and cookie/header transitions first
2. prefer lifecycle fixes (timers, promises, input settle, event-loop drain) before rewriting algorithms
3. keep all stages on one fresh session chain before the business request
4. mark a missing stage "non-gating for the current route" only after repeated independent business successes; keep the branch and evidence because policy can rotate

## Stage fields checklist

Carry only fields the current stage proved. Do not invent later-stage certainty.

### Observe / Capture fields

- `target_url`, `target_method`, query/body shape
- `target_fields`
- `suspect_scripts`
- `entry_candidates` or confirmed `entry_function`
- `entry_script_url` and local source path when saved
- `sample_input` / `sample_output` or wire pair ids
- `env_reads` observed so far
- injection timing and observer-effect notes

### Rebuild / Patch fields

- `undefined_paths` or missing host surfaces
- `first_divergence`: path, expected, actual
- `loaded_modules` or init order when relevant
- baseline id and session identity
- trigger order that reaches the mutation point

### Consolidate / Port fields

- fixed fixture input/output hashes
- stable sign/cookie/token shape without raw secrets
- request contract and serialization rules
- refresh policy and per-request regeneration rules
- server validation result and residual risks

Missing stage fields means the stage is not complete enough to escalate ownership.

## Phase map for stage fields

Use one vocabulary when reporting:

| Field bundle | Universal Reverse Loop phases |
|---|---|
| Observe / Capture fields | Phase 0-2, and Phase 3 once the mutation point is found |
| Rebuild / Patch fields | Phase 3-4 |
| Consolidate / Port fields | Phase 5: Deliver (prove + package) and delivery gate |

Do not use Observe/Port labels as a second phase numbering system.
