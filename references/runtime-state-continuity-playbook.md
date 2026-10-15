# Runtime-State Continuity Playbook

Use this playbook when a local JS, VM, WASM, or SDK helper is called more than
once during one browser-shaped workflow. The helper's process, VM/context,
module graph, closures, caches, and mutable globals may be protocol state.

## Contents

- [Invariant](#invariant)
- [When to open this path](#when-to-open-this-path)
- [Minimal continuity matrix](#minimal-continuity-matrix)
- [State inventory](#state-inventory)
- [Decision rule](#decision-rule)
- [Acceptance and negative control](#acceptance-and-negative-control)
- [Packaging boundary](#packaging-boundary)
- [Applicability boundary](#applicability-boundary)
- [Evidence and handoff](#evidence-and-handoff)

## Invariant

Runtime lifetime is a possible protocol field. Replaying explicit cookies,
counters, bootstrap values, or function arguments does not prove that hidden
runtime state has been restored. A fresh local process is valid only when the
browser also creates a fresh execution world between those calls, or when a
fixed-input proof shows that runtime identity is irrelevant.

## When to open this path

Open this path before widening the environment or shrinking the helper when
one or more of these symptoms appear:

- the first call passes but a later page, retry, or step fails;
- a helper smoke test passes, but a continuous transcript does not;
- a new process per call fails while a browser page stays alive;
- resetting an explicit counter or replaying cookies does not remove the gap;
- output shape is plausible but the first downstream consumer rejects it.

Do not infer hidden runtime state from a single failure. Keep the browser
baseline and the instrumented/helper runs separate, then compare one bounded
continuity experiment.

## Minimal continuity matrix

Run the smallest matrix with URL, bootstrap, time, profile, and business input
held constant where the target permits it:

1. **Persistent world**: load once, call repeatedly in one process/context.
2. **Fresh world**: load or spawn a new process/context for every call.
3. **Explicit-state ablation**: keep the persistent world but reset only the
   visible counter, cookie, or argument that was suspected to carry state.

Record exact outputs or downstream responses, not only lengths or alphabets.
The first meaningful difference is the state transition to investigate.

## State inventory

Classify the suspected state before porting it:

- explicit inputs: URL, page, body, timestamp, nonce, counter, or arguments;
- server/session state: bootstrap tuple, cookie, storage, round, or refresh;
- runtime identity: process, VM/context, worker, module instance, or realm;
- hidden mutable state: closure variables, globals, caches, queues, memoized
  keys, PRNG state, lazy initialization, or call-order markers;
- host lifecycle: load order, event loop, timers, response callbacks, or
  cleanup behavior.

Do not collapse these classes into one copied final token. Record the writer,
scope, lifetime, refresh path, and wire consumer for each class.

## Decision rule

If each business call downloads a new bootstrap script, default to a fresh world
per call. A leftover locally-minted cookie on the next script GET is
explicit-state contamination, not proof that the helper must stay persistent.
If the persistent-world path passes and the fresh-world path fails or produces
a different accepted transcript, treat runtime continuity as a live hypothesis
and keep the helper alive across the same bounded sequence. If the persistent
world self-invalidates after the first encrypt (empty later tokens, sliced
bytecode, or one-shot init), do not keep that burned instance as a pager;
isolate or port the encrypt and let Python own pagination. If all three paths
agree under a complete fixed-input capsule, runtime identity is not yet a
necessary state and may be released. If the persistent path also fails for a
reason other than self-invalidation, return to the first divergent bootstrap,
transport, or environment boundary instead of adding arbitrary browser APIs.

## Acceptance and negative control

The positive oracle must be the first decisive downstream behavior: accepted
business schema/data, a proved state transition, or the requested artifact.
Helper load, non-empty output, shape similarity, and HTTP 200 are not enough.

The negative control should intentionally break continuity in the suspected
way and fail for the expected protocol reason. A delay-only or counter-only
change is not a continuity proof unless the relevant state writer is traced.

## Packaging boundary

Python owns live HTTP, orchestration, parsing, retries, persistence, and
output. A long-lived local JS/WASM helper is allowed only for the narrow
stateful boundary that was proved. Document initialization, per-run lifetime,
call count, reset semantics, timeout, cleanup, and runtime version. Never ship
browser automation, capture backends, page driving, or a browser profile as the
continuity mechanism.

## Applicability boundary

Rotating per-call bootstrap scripts default to fresh world per call unless the
matrix proves otherwise. Stop using this playbook when the browser demonstrably
creates a fresh world for each call, the server issues a fresh state that fully
explains the change, or a complete fixed-input capsule proves runtime identity
irrelevant. If the
same-context helper disagrees with the browser, runtime continuity is not a
solution by itself; return to wire, lifecycle, or host-surface evidence.

## Evidence and handoff

Save a task-local, secret-free record containing the matrix, first divergence,
positive and negative oracle, helper lifetime, runtime version, fixture hash,
and the exact boundary where the rule stops. Promote this invariant only after
two independent jobs, a deterministic fixture, both oracles, and clean-checkout
validation pass the experience-card gate.
