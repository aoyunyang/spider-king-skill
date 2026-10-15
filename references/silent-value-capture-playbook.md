# Silent Value Capture Playbook

Use this file when ordinary page-world hooks, breakpoints, or attach-based debugging cannot produce reusable boundary values without unacceptable observer effect.

Silent value capture is a **debugger-trace upgrade means**, not a baseline host and not a delivery runtime.

## Contents

- [Mission](#mission)
- [Position in the skill](#position-in-the-skill)
- [Trigger and skip conditions](#trigger-and-skip-conditions)
- [Success gate](#success-gate)
- [Backend selection](#backend-selection)
- [Recipes](#recipes)
- [Evidence layout](#evidence-layout)
- [Evidence card schema](#evidence-card-schema)
- [Correlation rules](#correlation-rules)
- [Promotion into rebuild](#promotion-into-rebuild)
- [Forbidden](#forbidden)
- [Capability gaps](#capability-gaps)

## Mission

Capture reusable values at the narrowest stable boundary with the lowest practical observer risk:

- function or wrapper arguments and returns
- VM public entry and exit values
- WASM export boundary values
- cookie, storage, or eval writers when they mint protocol state
- silent transport-side frames or packets only when they close a protocol gap

The goal is fixed-input material and wire correlation, not a large raw dump.

## Position in the skill

| Surface | Role of silent value capture |
|---|---|
| `fingerprint-baseline` | never replaces it |
| `debugger-trace` | first-class means: default remains `js-reverse` when attach exists; silent-value-capture is an equal-role alternative/upgrade, not a decorative tail |
| `compact-replay` / `collector` | never owns the final run path |

Contractual live order remains role-ordered, with **branched means**:

```text
fingerprint-baseline
  -> sequential handoff (park or retain baseline)
  -> debugger-trace
       attach available:
         js-reverse first
         + silent-value-capture immediately on upgrade triggers
       attach missing:
         record debugger_attach_gap
         + silent-value-capture if backend available
         else offline continue
  -> offline rebuild + browser-free delivery
```

### Combat priority

1. Acquire one correlated boundary value as early as practical (usually recipe A, B, or C).
2. Stop capture once rebuild material is enough; do not open whole-program traces for ceremony.
3. Deepen to opcode/instruction windows only after public boundary I/O is proved insufficient.
4. Prefer immediate layer change over widening toxic page-world hooks.

### Role-completion rule

`debugger-trace` is satisfied when any holds:

- correlated initiator/mutation proof from attach-based debugging, or
- one or more silent-value cards with `fixed_input_ready=true` and wire/state correlation, or
- both

`debugger_attach_gap` alone does **not** fail debugger-trace if silent-value cards already satisfy the role. Baseline evidence is still required for live understanding.

### Ownership

Keep target-serial ownership. At most one browser MCP family or silent-value engine-capture backend may be `TARGET_ACTIVE`. Before engine capture, baseline must be `BASELINE_PARKED` or `RETAINED_EXCEPTION`. Do not open silent-value-capture in the same parallel batch as another target-active browser family. Non-MCP backends are recorded in the capability snapshot as `silent_backend=available|absent` and must not be labeled as `chrome-devtools` or `js-reverse`.

## Trigger and skip conditions

### Upgrade or select when any is true

Enable immediately; do not burn a widening page-world hook cycle first.

- invasive page-world hooks change verifier behavior, timing, identity, or request admission
- attach is missing, unstable, or systematically misses the decisive boundary
- fixed-input work needs authentic argument and return vectors that source reading cannot provide
- JSVM or heavily obfuscated logic exposes a public boundary but resists stable breakpoints
- page self-checks make proxy, hook, or console-world probes untrusted
- a silent transport or storage writer is the only remaining uncorrelated mutation surface
- attach is absent but an operator-local silent backend is available (still record `debugger_attach_gap`)

### Skip when any is true

- clean wire evidence plus source already proves the mutation boundary
- a narrow breakpoint or observe-only hook already yields correlated fixed inputs
- the task is pure offline restore from known samples
- the only available capture path would become the delivery runtime

## Success gate

A silent-value capture is complete only when all are true:

1. one declared recipe was used; scope may live in `capture_plan.json` or on the evidence card, not necessarily both
2. at least one evidence card has `fixed_input_ready=true`, or an explicit negative proof that the chosen boundary is not value-bearing
3. positive value cards correlate to a real request, state write, or export boundary; negative proofs may omit business-field correlation when they only disprove that boundary
4. clean versus capture behavior was checked when observer risk was not already proved low
5. raw secrets remain task-local and redacted in shared notes

A pile of uncorrelated logs is not success.

## Backend selection

Choose the smallest available backend that can fill the evidence card:

1. `js-reverse` call-frame or breakpoint evaluation when attach exists and observer risk is acceptable
2. narrow behavior-preserving page-world hook only when still low or medium risk
3. optional local low-observer engine or host instrumentation when installed and mapped by operator overlay
4. offline local replay of a harvested script or helper when live capture is unnecessary

No-attach rule: if attach is missing and backend (3) or (4) can fill the card, continue. Do not treat `debugger_attach_gap` as automatic abandonment of debugger-trace.

Backend labels are descriptive only. Shared skill doctrine must not require any proprietary product, binary, or private environment-variable table.

If no backend can satisfy the recipe, record `silent_value_capture_gap` and continue with offline analysis, a lower delivery shape, or a named blocker.

## Recipes

Use one recipe per capture window. Narrow before widening.

| ID | Recipe | Capture target | Minimum success |
|---|---|---|---|
| A | `sign-boundary` | named signer, encryptor, token builder | one fixed args-to-return vector correlated to the request field |
| B | `script-scope` | unknown helpers inside one script URL family | decisive writes from that script correlated to the request |
| C | `vm-public-io` | custom VM or bytecode interpreter entry | public entry inputs and exit outputs before opcode recovery |
| D | `challenge-heavy` | anti-probe or challenge-heavy flows | narrow-scope values with explicit clean-vs-capture comparison |
| E | `transport-silent` | WebSocket, hidden transport, or packet-side mutation | frame or packet fields correlated to business state |
| F | `wasm-boundary` | WASM export or import boundary | export-level vectors sufficient for local helper work |
| G | `dynamic-compile-material` | `eval` / `new Function` compile body after param substitution | one compile-body snapshot (len/sha256/preview) correlated to the later wire field |

Recipe policy:

- prefer public boundaries over opcode or handler surgery
- prefer one helper output over whole-program tracing
- open PC windows, full stack dumps, or instruction traces only after public I/O is proved insufficient
- recipe G captures the compile body after substitution, not the later call; never wrap global `Function.prototype.apply` / `call` to get it

## Evidence layout

Under the task cache, create only what is needed:

```text
<project>/js_reverse_cache/tasks/<task-id>/
  silent_value/
    capture_plan.json
    sign_boundary.jsonl
    vm_public_io.jsonl
    wasm_boundary.jsonl
    dynamic_compile.jsonl
    state_writes.jsonl
    wire_correlations.jsonl
    source_index.json
```

`runtime-evidence.jsonl` may still receive short operational notes. Structured reusable values belong in `silent_value/`.

`source_index.json` may reference operator-local raw captures by path, size, and hash. Do not copy proprietary manuals, private switch tables, or secret-bearing raw dumps into the skill tree.

## Evidence card schema

Use schema name `spider-king.silent_value/v1`.

### `capture_plan.json`

Minimal required fields only: `why`, `recipe`, `success_gate`. Other fields are optional speed aids, not ceremony.

```json
{
  "schema": "spider-king.silent_value/v1",
  "kind": "capture_plan",
  "why": "invasive page hook changes verifier timing",
  "recipe": "A",
  "success_gate": "fixed_input_ready && wire correlation",
  "scope": {
    "url_contains": ["/api/"],
    "script_url_contains": [],
    "func_names": ["sign"],
    "pc_window": null
  },
  "stop_condition": "one stable business-request boundary",
  "observer_risk_budget": "low"
}
```

### Value card fields

```json
{
  "schema": "spider-king.silent_value/v1",
  "kind": "sign_boundary",
  "captured_at": "2026-08-06T12:00:00+08:00",
  "backend": "js-reverse | page-hook | engine-instrumentation | offline-replay | other",
  "backend_note": "optional local label only",
  "observer_risk": "low | medium | high",
  "scope": {
    "url_contains": [],
    "script_url_contains": [],
    "func_names": [],
    "pc_window": null
  },
  "boundary": {
    "name": "sign",
    "script_url": "",
    "args": [],
    "return": null,
    "side_writes": []
  },
  "correlation": {
    "request_id": "",
    "method": "",
    "url": "",
    "field_path": ""
  },
  "fixed_input_ready": false,
  "redaction": "prefer len/sha256/preview; keep raw values task-local"
}
```

Allowed `kind` values:

- `sign_boundary`
- `vm_public_io`
- `wasm_boundary`
- `state_write`
- `transport_event`
- `dynamic_compile`
- `negative_proof`

For sensitive values prefer:

- type
- length
- sha256 or task-local HMAC token
- short structural preview

Do not place live cookies, tokens, passwords, or full private responses into shared chat or version control.

## Correlation rules

Every positive value card should bind to at least one of:

- HTTP or WebSocket request id and field path
- cookie or storage key writer path
- WASM export name and call site
- explicit state transition used by the business request

If correlation is impossible, mark the card as incomplete or convert it to `negative_proof` for that boundary.

## Promotion into rebuild

Promote capture results into pure-Python rebuild only when:

1. the boundary is stable across repeated captures or one frozen vector is enough for the declared shape
2. fixed-input parity can be attempted without the capture backend
3. Python owns live HTTP for `compact-replay` and `collector`
4. any remaining JS or WASM helper is tiny, local, and free of live page driving

After promotion, the capture backend is analysis history, not runtime dependency.

## Forbidden

- skipping `fingerprint-baseline` because a silent-value backend exists
- declaring live understanding without `fingerprint-baseline` evidence (silent-value may satisfy debugger-trace, never baseline)
- requiring dual-backend cross-proof as ceremony when one correlated card already unlocks rebuild
- placing engine instrumentation, managed browser profiles, or page driving into `compact-replay` or `collector`
- treating unrestricted whole-program traces as completion
- hardcoding rotating capture outputs before writer, scope, and refresh path are proved
- writing proprietary backend manuals or private absolute tool paths into the shared skill package

## Capability gaps

Use exact gap names:

| Gap | Meaning | Stop? |
|---|---|---|
| `debugger_attach_gap` | CDP/`js-reverse` attach unavailable | No, if silent backend or offline path remains |
| `silent_value_capture_gap` | needed card cannot be filled by any backend | Continue offline or lower delivery shape |
| `silent_value_correlation_gap` | values exist but are not bound to request/state | Keep hunting correlation; do not discard the boundary |
| `silent_value_observer_gap` | every available capture path changes target behavior | Narrow scope, change backend, or lower claim |

A gap is a reason to continue with the next honest path. It is not permission to invent browser-backed delivery.
