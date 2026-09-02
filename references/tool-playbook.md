# Tool playbook

Use this file as the fast map from reverse-engineering task to tool choice.

## Contents

- [Preferred order](#preferred-order)
- [Evidence surfaces do different jobs](#evidence-surfaces-do-different-jobs)
- [Capability-aware evidence route matrix](#capability-aware-evidence-route-matrix)
- [Recon and network capture](#recon-and-network-capture)
- [Capability snapshot](#capability-snapshot)
- [Passive wire stores](#passive-wire-stores)
- [Environment providers](#environment-providers)
- [Browser lifecycle and handoff](#browser-lifecycle-and-handoff)
- [Static JS analysis](#static-js-analysis)
- [Dynamic validation](#dynamic-validation)
- [Session and environment handling](#session-and-environment-handling)
- [Embedded runtime routing](#embedded-runtime-routing)
- [Failure routing](#failure-routing)
- [Focused profile tools](#focused-profile-tools)
- [Local helper scripts](#local-helper-scripts)

## Preferred order

1. Capture one clean baseline request.
2. Find the real request.
3. Trace the initiator.
4. Diff the moving fields.
5. Add the narrowest runtime proof that still preserves the sample.
6. Reproduce one stable request.
7. Scale collection only after the first request is repeatable.

Prefer clean baselines, initiator stacks, and narrow proofs over broad hooks. Prefer focused source reads over loading giant bundles into context.

## Evidence surfaces do different jobs

Do not let one proof surface pretend to clear another:

- initiator stacks and source reads prove where mutation logic lives
- wire capture or request egress proves what actually crossed the boundary
- environment traces prove DOM, BOM, descriptor, timer, and native-surface truth
- downstream business replay proves whether the recovered path is actually accepted

Treat these as complementary surfaces, not interchangeable ones. A value seen in locals, a quiet hook, or a convincing environment patch does not outrank the live wire or downstream business result.

## Capability-aware evidence route matrix

Treat the role definitions, evidence requirements, and fallback limits in `references/startup-triage-playbook.md` as canonical. This table only maps those roles to installed capability families; never bind them to a vendor, profile id, assumed port, or unconfirmed method.

| Evidence role | Useful confirmed capabilities | Transition signal |
|---|---|---|
| `fingerprint-baseline` | a target-compatible configured browser mode, wire capture, redirects, page snapshots, and session inspection | clean baseline saved and observer-effect risk bounded |
| `debugger-trace` | request initiators, source search/export, breakpoints, call frames, argument/return inspection, or a narrow behavior-preserving hook | wire request correlated to the smallest mutation boundary or a named capability gap |
| `cdp-bridge` | an explicitly exposed connection with the required Network, Runtime, or Debugger domains | correlated bridge evidence saved under the current owner, or the bridge declared unavailable |

Roles may hand evidence to one another; they are not choose-once routes. For a fresh web `live-target`, the contractual order remains `fingerprint-baseline` followed by `debugger-trace` after the handoff gate. Default baseline means are `chrome-devtools`; Camoufox/managed host may take baseline when Auto Judge finds high fingerprint pressure. `debugger-trace` commonly uses later `js-reverse`, and optional `cdp-bridge` work stays under the current `TARGET_ACTIVE` owner. None of these role labels excuses missing baseline or debugger evidence when that role is required and available means exist. That ordered pair is the required first-pass evidence surface for fresh web live targets. In default means language, keep the chrome baseline followed by `js-reverse` after the handoff gate when debugger attach exists; host upgrades change means only, never the role order or browser-free delivery rule.

## Recon and network capture

### `js-reverse`

- `new_page` / `navigate_page`: open the target and follow the real landing URL
- `list_network_requests`: list XHR, Fetch, document, script, and preflight traffic
- `list_network_requests(reqid=...)`: inspect the chosen request in full
- `get_request_initiator`: jump from request back to the caller stack
- `get_websocket_messages(analyze=true)`: group streaming traffic by message family
- `get_websocket_messages(frameIndex=...)`: inspect one exact frame in full
- `evaluate_script`: inspect `document.cookie`, `localStorage`, `sessionStorage`, or page globals when state matters

### `chrome-devtools`

- `navigate_page` / `new_page`: open the page when UI flow evidence matters
- `take_snapshot`: inspect page structure fast
- `wait_for`: wait on target text while triggering filters, search, or pagination
- `list_network_requests` and `get_network_request`: second source of truth when UI flow matters
- `take_screenshot`: capture evidence for hidden panels, captcha gates, or lazy regions

Use browser DevTools when DOM state matters. Use `js-reverse` when JavaScript runtime, request initiators, or hooks matter.

## Capability snapshot

Before a `live-target` pass, inspect the active tool registry and record:

- required methods that are available
- optional methods that are available
- selected fallback for every missing optional method
- configured browser mode (`launch`, `attach`, or `unavailable`) and whether it can be changed without restarting or reconfiguring the server
- optional non-browser families when mounted: passive wire-store, wire-visibility, environment provider
- blockers that prevent one evidence surface from being collected
- profile-directory conflict or other mutual-exclusion limits between browser families
- whether a debuggable attach endpoint is already known

Treat these as the core method families, not as a promise that every installation has every helper:

- Chrome baseline: `navigate_page` or `new_page`, `list_network_requests`, `get_network_request`, `take_snapshot`, and `take_screenshot`
- js-reverse runtime: `navigate_page` or `new_page`, `list_network_requests`, `get_request_initiator`, `list_scripts`, `search_in_sources`, `get_script_source`, `save_script_source`, `set_breakpoint_on_text`, `break_on_xhr`, `get_paused_info`, `evaluate_script`, `step`, `pause_or_resume`, and `remove_breakpoint`
- optional cleanup or preload support: `close_page` and `navigate_page(initScript=...)`

If a named optional method is missing, use the documented fallback and report the capability gap. Do not block the entire reverse when the same evidence can be obtained through supported methods.

Refresh the capability snapshot after a tool-server restart or reconnect, registry or schema change, browser-mode or target-context change, control-channel disconnect, or a method result that contradicts the recorded snapshot. Stop target actions during refresh. Preserve already saved evidence, record the last explicitly confirmed lifecycle state plus the control loss, and do not infer `PARKED`, `CLOSED`, or restored ownership from reconnection alone. Re-enter through the same ownership and `sequential handoff` gates.


## Passive wire stores

Use installed passive traffic stores such as Reqable, imported HAR, or task-local `network.jsonl` as complementary wire evidence.

- Search and freeze ordered HTTP or WebSocket history after a browser pass when the store is available.
- Prefer artifact-led `evidence-reuse` when the user already provided complete captures and does not require live acceptance.
- Correlate passive captures with browser egress; when they disagree, trust live wire egress.
- Never treat a passive store as `TARGET_ACTIVE` ownership or as a browser-backed collector runtime.

For symptom routing across MCP families, read `references/mcp-routing-playbook.md`.

## Environment providers

Use Camoufox, AdsPower, or other managed hosts only as environment / baseline-host providers. Auto Judge decides when they are required; do not start them by default.

- Open or select a target-compatible host/profile first when fingerprint pressure or multi-profile isolation is required.
- On high fingerprint pressure, Camoufox/managed host may own the clean `fingerprint-baseline` pass.
- Obtain an explicit debuggable endpoint or browser URL before debugger analysis.
- Attach `chrome-devtools` or `js-reverse` to that endpoint; do not launch a second anonymous browser for the same job while the managed host is the intended surface.
- Host/profile start alone is not baseline proof for debugger understanding and does not replace sequential first-pass roles.
- If attach is impossible after a clean host baseline, export artifacts and continue offline with an explicit attach gap.

Portable attach defaults and placeholders live in `references/local-mcp-environment.md`; keep operator-private absolute paths and secrets in an outside-skill local overlay.
## Browser lifecycle and handoff

### Ownership invariant

- At most one browser tool family may be `TARGET_ACTIVE` at a time.
- Never place `chrome-devtools` and `js-reverse` target actions in the same parallel tool batch.
- A schema, tool-list, or non-target health check may confirm availability without taking target ownership. Capability checks must not prewarm both target browsers.
- A parked MCP server or browser process may remain alive. Process presence is not the same as target-active ownership.

Use these lifecycle states:

```text
IDLE
  -> CHROME_ACTIVE
  -> CHROME_PARKED or RETAINED_EXCEPTION
  -> JS_REVERSE_ACTIVE
  -> JS_REVERSE_PARKED or MCP_PROCESS_ENDED
```

Use `CLOSED` only when the installed tool explicitly confirms browser or MCP-process termination. Never infer closure from a blank page, a missing tab, an idle tool call, or the end of one analysis phase.

### Sequential handoff gate

Before switching tool families:

1. save the clean request and response pair, redirect chain, target URL, relevant page state, network identifiers, screenshots or snapshots, and every artifact needed by the next phase
2. record whether the current session, verifier round, in-memory secret, manual interaction, or challenge state is replayable
3. remove or disable invasive instrumentation when supported, and resume a paused runtime before parking it
4. quiesce target activity as far as the installed tool allows
5. record the resulting lifecycle state and only then grant `TARGET_ACTIVE` ownership to the next family

Evidence roles can switch at this checkpoint. The role selected first does not own the investigation to completion; transfer the saved baseline, request identifiers, source coordinates, and state inventory to whichever role answers the next unresolved question.

For `chrome-devtools`:

- close every extra page that the installed tool permits
- if the final page cannot be closed, navigate it to `about:blank` and mark Chrome `CHROME_PARKED`, not closed
- do not use `taskkill`, process-wide termination, or profile deletion to simulate lifecycle support

For `js-reverse`:

- remove breakpoints and resume execution when those controls are available
- navigate selectable pages away from the target when the installed tool permits it
- if no page-close or browser-close operation exists, mark the family `JS_REVERSE_PARKED`; end with `MCP_PROCESS_ENDED` only when process termination is actually observed

### Retained-state exception

Use `RETAINED_EXCEPTION` when cleanup would destroy the only live session chain, one-time verifier round, in-memory key, manual verification result, or another artifact that is not yet reproducible.

- preserve the state and record why it cannot be rebuilt yet
- do not invoke the retained tool family while another family owns `TARGET_ACTIVE`
- record autonomous background traffic or mutation if the retained page cannot be fully quiesced
- do not compare retained-state traffic with a clean baseline as though they were equivalent
- if the next phase requires the same session chain, postpone the switch until the chain can be transferred or replayed faithfully
- clear the exception as soon as replayability is proven

### Browser-mode routing

- Obey the installed tool's configured mode. Do not claim runtime headless, headful, isolated-profile, or CloakBrowser switching unless the tool schema or server lifecycle actually exposes it.
- If a headless-capable configuration exists, compare it against the clean Chrome baseline before trusting it for target evidence.
- Fall back to a headful or stealth-capable configured mode when manual verification, visible interaction, headless detection, window state, Canvas, WebGL, font, layout, or renderer behavior is part of the protocol evidence.
- Record the mode, the reason for changing it, and whether the change altered network or runtime behavior.
- Treat a headless/headful mismatch as evidence. Do not hide it behind a global default.

## Static JS analysis

- `list_scripts`: enumerate candidate bundles
- `search_in_sources`: search keywords across all loaded sources
- `get_script_source`: inspect the exact function neighborhood
- `save_script_source`: dump a full bundle locally when a file is too large to inspect in slices

Fallback recipes when you wanted a missing helper:

- no `find_in_script`: use `search_in_sources`, then `get_script_source`
- no automatic code summary: read the initiator stack first, then the smallest source slice around the mutation point
- no automatic crypto detector: search helper names, compare fixed inputs, and route to `references/crypto-patterns.md`
- no automatic deobfuscator: use `search_in_sources`, `save_script_source`, and `references/obfuscation-guide.md`

Operational notes for saved sources:

- if a file is one giant line, beautify or pretty-print a working copy before relying on line numbers
- if `evaluate_script` or a similar tool writes through a JSON-serializing `filePath`, run `json.loads` on the saved text before treating it as raw JavaScript
- prefer `save_script_source` or a direct `fetch` of the asset URL, then continue offline when live inspection is noisy
- when string-table recovery is needed, route to `references/obfuscation-guide.md` and `references/offline-inline-deob-playbook.md` instead of inventing an automatic deobfuscator tool


Keyword packs:

- request path: `"/api/"`, `"graphql"`, `"fetch("`, `"axios"`, `"XMLHttpRequest"`
- signer: `"sign"`, `"token"`, `"nonce"`, `"timestamp"`, `"trace"`, `"x-sign"`, `"beforeSend"`, `"ajaxSetup"`, `"requestId"`
- crypto: `"md5"`, `"sha"`, `"sm3"`, `"hmac"`, `"aes"`, `"rsa"`, `"crypto.subtle"`, `"native code"`
- environment: `"navigator"`, `"canvas"`, `"webgl"`, `"performance"`, `"webdriver"`
- probe chain: `"Object.keys"`, `"Reflect.ownKeys"`, `"getOwnPropertyDescriptor"`, `"toString"`, `"document.all"`, `"JSON.stringify"`

## Dynamic validation

Start with a clean baseline. Then use initiator stacks and request diffs. Add runtime proofs only after you know why you are instrumenting.

### Baseline-first proof flow

1. capture one clean request and response pair
2. use `get_request_initiator` to jump from the request to the caller stack
3. use `search_in_sources` and `get_script_source` to inspect the smallest relevant code region
4. use `set_breakpoint_on_text`, `get_paused_info`, `evaluate_script(frameIndex=...)`, and `step(direction='over'|'into'|'out')` when a named helper is stable enough to trace without poisoning the target
5. use `break_on_xhr` when you need to stop at the exact request boundary
6. when a justified before-load observation is required, use Chrome `navigate_page(initScript=...)` during the Chrome phase only when the capability snapshot confirms it; otherwise use the earliest stable breakpoint, a controlled refresh after preserving the baseline, or an offline local runtime instead of inventing an unsupported tool call
7. when hooking, log target, event, method, URL, field, caller, decisive method arguments, or returned child-object shapes so captured values stay attributable to one request boundary
8. if a hook stays quiet, treat that as evidence only about that exact boundary and rule out sibling writers or alternate transport channels before concluding the field is absent
9. if the target is verifier-gated or behavior-sensitive, remove invasive instrumentation and recapture a clean baseline the moment behavior changes

Use the compact preload, initialized-page, hook-miss, page-owned-world, sibling-transport, and disconnect recovery matrix in `references/hook-techniques.md` before widening instrumentation.

### Breakpoint tools

- `set_breakpoint_on_text`: best when the bundle is minified
- `get_paused_info`: inspect locals and scope
- `evaluate_script(frameIndex=...)`: print the exact pre-sign string, key, iv, or payload in the paused call frame
- `pause_or_resume`: resume execution after inspection
- `step(direction='over'|'into'|'out')`: only after you already know why you are pausing

## Session and environment handling

- `evaluate_script`: inspect `document.cookie`, storage values, bootstrap globals, or runtime helper outputs
- `evaluate_script(mainWorld=true)`: inspect page-owned globals such as webpack caches, SDK objects, or exposed bootstrap helpers
- if a console or isolated-world probe misses a page-owned wrapper, constructor, or global, repeat the proof in the page-owned world before discarding that path
- `navigate_page(initScript=...)`: patch or observe a narrow pre-load boundary during the Chrome phase when the installed Chrome tool exposes it
- `save_script_source`: preserve suspicious bundles for offline diffing when environment mismatch remains unclear

## Embedded runtime routing

- If the target needs `navigator`, `screen`, `location`, DOM lifecycle, timers, `document.cookie`, or XHR wrapper semantics without true interaction, route to `references/embedded-browser-runtime-playbook.md`.
- If the runtime exposes a synchronous getter after init or self-issues the decisive XHR or fetch payload, route to `references/challenge-artifact-harvest-playbook.md` before brute-force DOM patching.
- Use a local embedded runtime such as `iv8` to run offline page bootstrap, advance logical time, observe API probe chains, or inspect local net-log style mutations.
- If `iv8` is the chosen runtime, then read `references/iv8-runtime-cheatsheet.md` for concrete recipes on `page.load` versus DOM insertion, logical time control, resource injection, `netLog`, and `wrapNative`.
- Extract explicit artifacts back to Python: cookie string, final URL, wrapped body, token, or decoded payload.
- Do not let the runtime own live HTTP or turn into a stealth browser dependency when a narrower local helper would do.

## Failure routing

- H2 reset, TLS EOF, handshake timeout, or browser-pass and stdlib-fail before app semantics: suspect transport admission and route to `references/transport-pre-gate-playbook.md`
- `403`, `412`, `429`: compare headers, cookies, sign freshness, and request pacing
- business error with normal `200`: compare payload assembly order and timestamp precision
- decrypt failure after a successful `200`: verify whether the runtime key/iv is transformed through a helper such as digit-pair-to-char before AES is applied
- empty data: verify pagination, filters, referer, login state, and cursor evolution
- occasional success: inspect one-time tokens, session refresh, or concurrent request coupling
- first request works but immediate replay fails: compare cookie mutation, in-memory timestamp slots, and whether a page refresh function must run before every request
- response gibberish: search for decrypt path, compression, protobuf, or msgpack
- local runtime timers fail after init but one getter or outgoing request boundary is visible: route to `references/challenge-artifact-harvest-playbook.md` before patching more DOM
- hooked page fails but clean page works: suspect observer effect, remove invasive hooks, and recapture the baseline before deeper tracing

- MCP family needed by the current role is not mounted in the active session: record `missing_mcp`, use only available surfaces, and stop short of claims that require the missing surface
- managed profile started but no debuggable endpoint is available: keep ENV blocked and do not invent attach-mode evidence
- passive wire-store is empty or offline: fall back to browser network capture or user-supplied HAR rather than assuming traffic exists
- packet capture suggests transport failure before application semantics: route to `references/transport-pre-gate-playbook.md`; do not treat coarse PCAP success as signer recovery
- one browser family fails to start because the other already holds the user-data directory: keep a single `TARGET_ACTIVE` family for wire evidence, mark the blocked family in the capability snapshot, and continue static recovery offline with saved sources plus local Node or Python
- saved JS from an evaluate-style file export looks quoted or escaped end to end: decode the JSON string before analysis
- a named national or textbook digest still mismatches fixed samples: route to `references/crypto-patterns.md` and diff IV, constants, packing, and compress masks instead of trusting the algorithm name



## Focused profile tools

When the goal is already narrow, prefer the internal profiles before reopening full target discovery:

- paste-ready observation only: `references/profiles/browser-hook-snippets/index.md` and its `scripts/*.js`
- known entry needs Node/VM host surfaces: `references/profiles/env-patch/index.md` and `references/profiles/env-patch/scripts/env-diagnose.js`
- fixed-trace pure Python rebuild: `references/pure-python-rebuild-playbook.md`

These routes complement `chrome-devtools` and `js-reverse`. They do not replace wire evidence for unknown multi-layer collectors.

## Local helper scripts

Use the bundled local scripts when they are faster than re-deriving the same mechanics:

- `scripts/check_reverse_env.py`: confirm the local reverse stack quickly
- `scripts/crypto_fingerprint.py`: classify suspicious digest or alphabet outputs
- `scripts/protocol_diff.py`: compare captured requests or responses and surface the meaningful deltas
- `scripts/scaffold_reverse_project.py`: start a clean Python-first collector layout
