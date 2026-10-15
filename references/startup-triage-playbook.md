# Startup Triage Playbook

Use this reference at the start of every fresh intake or when a prior gate becomes stale.

The goal is to decide what kind of fight this is before you load giant bundles or poison the page with broad hooks.

## Contents

- [Startup gate](#startup-gate)
- [Capability-aware evidence roles](#capability-aware-evidence-roles)
- [Escalation ladder before full browser dependence](#escalation-ladder-before-full-browser-dependence)
- [Anti-bot class](#anti-bot-class)
- [Family triage](#family-triage)
- [Observer-effect rule](#observer-effect-rule)
- [Continuation sibling scan](#continuation-sibling-scan)

## Startup gate

Complete these four checks first:

1. intake mode
   - choose `live-target` when a current page or endpoint needs fresh wire and runtime evidence
   - choose `artifact-only` when the input is a saved request, packet capture, source file, JS or WASM sample, token, cookie, or response without a live target requirement
   - choose `continuation` when the same target, session assumptions, tool registry, and delivery goal remain current
   - when a user-delivered same-family skeleton is present, record it during intake and prefer process migration over zero-base behavior reverse
   - do not claim live acceptance, current endpoint behavior, or runtime provenance from artifact-only evidence
2. environment and tool sanity
   - run `scripts/check_reverse_env.py --project-root <project>` when local execution is available; fingerprint only explicitly selected public helper lockfiles with repeatable `--helper-lockfile <path>` arguments
   - treat project `.venv` coherence as advisory by default; add `--require-project-venv` only when the user or bound project makes that environment a hard gate
   - for web `live-target`, confirm whether both `chrome-devtools` and `js-reverse` are usable through schemas, tool lists, or non-target health surfaces; this capability check must not open the target in both tools
   - record a capability snapshot: required browser families, optional passive wire-store / wire-visibility / ENV families when relevant, optional `silent_backend=available|absent`, required methods present, optional methods present, selected fallbacks, configured browser mode (`launch`/`attach`/`unavailable`), debuggable endpoint known or not, and blockers
   - for web `live-target`, do not place both browser tool families in one parallel tool batch
   - for web `live-target`, grant initial `TARGET_ACTIVE` by Auto Judge: default `chrome-devtools` when DP/initiator work is not required; if DP/initiator work is already required, grant `js-reverse` as the single owner for both `fingerprint-baseline` and `debugger-trace` and do not launch a second Chrome. Record `launch` vs `attach` and never pretend launch is attach. Defer a different family's first target action until the handoff gate in `references/tool-playbook.md` is complete; when `js-reverse` already owns the host, attach/select that same page instead of opening `chrome-devtools`
   - if the primary target is APK, native app, or mini-program, declare out of scope for this pure-web skill; do not invent web paired-browser first-pass as ceremony
   - for `artifact-only`, inspect local runtimes and supplied files first; browsers are not a ceremonial requirement
   - for `continuation`, reuse the prior capability snapshot unless the registry, browser mode, or target context changed
   - note whether a local embedded runtime such as `iv8` is available when host-bound bootstrap is suspected
   - report blockers early instead of pretending the missing tool does not matter
3. family triage
   - choose the first family that explains the failure mode best
   - before loading a family-specific scaffold or playbook, corroborate the family across at least two evidence surfaces such as response shape, cookie behavior, runtime markers, script traits, or wire behavior
   - if only one weak hint exists, keep the classification provisional and continue evidence gathering
   - if the family changes after new evidence, restate it explicitly
4. delivery intent
   - state the smallest acceptable final shape
   - reject browser-backed replay, profile-bound state, and automation-driven submission up front

## Capability-aware evidence roles

Choose an evidence role from the capability snapshot, not from a vendor label. Roles describe the proof needed next; they are not permanent routes, browser products, or permission to keep multiple target browsers active.

| Evidence role | Use it for | Minimum proof | Capability-aware limit or fallback |
|---|---|---|---|
| `fingerprint-baseline` | A clean flow where risk, visible interaction, renderer state, or observer effect may change the sample | untouched request and response, redirects, page state, configured browser/host mode, and session inventory | assign this role to stock Chromium via `chrome-devtools` by default; if DP/initiator work is already required, `js-reverse` may own this role on the same host; Camoufox/managed host only when fingerprint pressure is high; if no compatible host is proved, record the role gap and keep the ordinary clean Chrome baseline honest |
| `debugger-trace` | Initiator, source, call-frame, argument, return-value, canonical-mutation, or silent-value boundary evidence | correlate one wire request with its caller/mutation boundary, and/or a `fixed_input_ready` silent-value card | use `js-reverse` when attach exists; use `silent-value-capture` on upgrade triggers or when attach is missing but a backend is available; gaps alone do not complete the role |
| `cdp-bridge` | Network, Runtime, or Debugger evidence inside an already active target-compatible environment | record how the endpoint was obtained, which protocol domains are available, and how events correlate to the baseline | optional and conditional on an explicitly exposed, authorized connection; never guess a port, profile, launch method, or MCP helper |

Supporting passive surfaces such as reqable, HAR, or PCAP may supply wire-store or wire-visibility evidence beside these roles. They never become a fourth concurrent browser owner and never replace the required baseline then debugger first-pass roles on a fresh web `live-target`. Debugger-trace means include `js-reverse` and first-class `silent-value-capture` (`references/silent-value-capture-playbook.md`). Read `references/mcp-routing-playbook.md` when auto-judging among artifact-only, Camoufox/managed host, chrome-devtools, js-reverse, and silent-value-capture.

### Transport-only direct-endpoint exception

This is a narrow delivery exception, not page/runtime understanding and not a
way to skip available browser evidence. It may accept `compact-replay` or
`collector` for one exact direct endpoint when baseline or debugger means are
unavailable and every condition below is proved:

1. the exact business endpoint, method, parameters, response schema, and
   bounded collection scope are known without relying on a page-context fetch
2. a same-route, same-input, same-session admission matrix changes only the
   transport surface; the known-failing profile is retained as a negative
   control and the admitted profile reaches parseable downstream business data
3. no target JavaScript signer, page bootstrap, wrapper mutation, challenge
   state, response decoder, renderer state, interaction, or browser-generated
   request field participates in the accepted request
4. any session credential is ordinary carried account state; no page-minted
   state is assumed, and session compatibility is reported only for sessions
   actually replayed
5. page, cursor, route, header, or identity exceptions are kept local and
   repeated successfully; any claim that an exception is necessary or causal
   requires an independent one-variable ablation, otherwise necessity remains
   explicitly unproven
6. the final Python path exposes the negotiated protocol, fails closed on
   fallback, proves every promised bound, and passes at least two fresh live
   replays with the real business oracle
7. `fingerprint_baseline_gap` and/or `debugger_trace_gap` remain explicit in
   the capability snapshot and final report; the claim is endpoint-scoped
   collector acceptance, never that the page/runtime is understood

Exit this exception immediately if any signer, bootstrap, decode, wrapper,
browser-state, challenge, or interaction surface appears. Resume the normal
sequential roles or lower the declared shape. HTTP/2, a named ALPN, a UA, or a
particular client library is never a universal exception trigger by itself.

For every fresh web `live-target` outside the strict transport-only direct-endpoint exception, these roles supplement rather than replace the required first passes: collect the judged `fingerprint-baseline`, complete a `sequential handoff`, then collect `debugger-trace` evidence when attach is available. A typical role flow is:

```text
baseline host (`chrome-devtools` default; `js-reverse` owns both roles when DP is already required; Camoufox/managed host on high fingerprint pressure)
  -> optional `cdp-bridge` while the same owner remains TARGET_ACTIVE
  -> evidence checkpoint
  -> if the baseline owner is already `js-reverse`, continue debugger-trace on that host; do not launch `chrome-devtools`
  -> else BASELINE_PARKED or RETAINED_EXCEPTION, then debugger-trace means branch:
       attach available -> `js-reverse` first, plus `silent-value-capture` on upgrade triggers
       attach missing -> `debugger_attach_gap` + `silent-value-capture` if `silent_backend` available
```

At most one browser tool family or silent-value engine-capture backend remains `TARGET_ACTIVE`. Treat `cdp-bridge` as an evidence technique under the current owner, not a third concurrent owner. After a role returns its proof or named blocker, hand evidence to the role that can answer the next missing question; do not stay on one route merely because it was selected first. Apply the lifecycle gate in `references/tool-playbook.md` on every switch, including a return to an earlier role.

## Escalation ladder before full browser dependence

Use the smallest faithful layer that explains the evidence:

1. simple decode or standard algorithm: handwrite in Python first
2. host-bound JavaScript without true interaction: route to `references/embedded-browser-runtime-playbook.md`
3. full interaction or rendering dependence: observe in browser, but keep the delivery gate strict and do not confuse observation with the final collector

For the full rung-by-rung rule, proof requirements, and "do not jump layers" contract, read `references/escalation-ladder-playbook.md`.

## Anti-bot class

Before family folklore, classify how the server binds truth using `references/anti-bot-class-playbook.md`:

- `signature-bound` — host/challenge state participates in the answer
- `behavior-interceptor` — wrappers mutate business requests
- `pure-obfuscation` — hard to read, host-free once recovered

Record the class as provisional until two evidence surfaces agree. Class choice selects method bias only; it does not replace family triage or the delivery gate.

## Family triage

Choose one primary family for the application contract.
Add the secondary tag `transport-gated` when TLS, ALPN, UA, HTTP version, or route-local admission blocks the clean baseline before application semantics are visible.

### `signer-gated`

Symptoms:

- one or more request fields change every time
- the server rejects stale `sign`, `m`, `token`, header, or wrapper output
- the request initiator points into wrapper or helper logic

First move:

- capture one good request
- trace the initiator
- locate the canonical mutation point
- if the field collapses to a standard digest, compact JSON, or obvious packet format, handwrite it in Python before touching any runtime
- if the code reads host objects, lifecycle state, timers, or XHR wrappers, route to `references/embedded-browser-runtime-playbook.md`

Primary references:

- `references/transport-wrapper-playbook.md`
- `references/patched-helper-playbook.md`
- `references/crypto-patterns.md`
- `references/embedded-browser-runtime-playbook.md` when host semantics matter

### `transport-gated` (secondary tag)

Symptoms:

- standard HTTP clients fail at H2 reset, TLS EOF, handshake timeout, or early disconnect before meaningful application data appears
- the same route behaves differently across UA families, HTTP versions, or client stacks
- impersonated transport or mobile or app UA passes while default desktop or stdlib traffic fails
- a sibling auth, identity, or business route bypasses a challenged landing route

First move:

- freeze a small admission matrix across route, client stack, UA family, and HTTP version
- find one narrow profile that admits the baseline cleanly
- test route-local bypasses before loading giant bundles
- continue normal family triage only after application semantics become visible

Primary references:

- `references/transport-pre-gate-playbook.md`
- `references/env-diff-playbook.md`

### `verifier-gated`

Symptoms:

- the business request only works after a verifier, challenge, or warm-up step
- the page starts failing once hooks or breakpoints are installed
- there is no meaningful business signer, but a token, cookie, or coordinates appear after a separate request

First move:

- capture a clean untouched baseline before invasive instrumentation
- diff requests and verifier outputs first
- only then add the narrowest hook that proves the boundary
- if challenge HTML plus scripts appear to seed the cookie, URL suffix, or verifier token, route to `references/embedded-browser-runtime-playbook.md`
- if a bootstrap runtime exposes a getter after init or self-issues the decisive request, route to `references/challenge-artifact-harvest-playbook.md`

Primary references:

- `references/verifier-replay-playbook.md`
- `references/troubleshooting-playbook.md`
- `references/cookie-provenance-playbook.md` when cookies mutate during the verifier
- `references/embedded-browser-runtime-playbook.md` when offline bootstrap may recover the verifier state
- `references/challenge-artifact-harvest-playbook.md` when the verifier answer can be harvested locally from a runtime boundary

### `decode-gated`

Symptoms:

- the request succeeds, but the payload stays unreadable
- the body needs glyph mapping, decompression, protobuf, Base64, or layered decode
- fonts, side assets, or tiny helper functions decide whether the response becomes usable

First move:

- freeze the raw payload first
- locate the first consumer of the unreadable data
- rebuild the decode chain locally before scaling collection

Primary references:

- `references/response-decode-playbook.md`
- `references/side-asset-bootstrap-playbook.md`
- `references/structured-transport-playbook.md` when the payload sits inside a binary envelope

### `session-gated`

Symptoms:

- login, pairing, subscribe, heartbeat, or reconnect order decides success
- auth appears once, but later frames fail unless counters, tags, or keys stay in order
- media download or decryption needs secrets derived from prior traffic

First move:

- freeze one full successful transcript
- separate handshake, keepalive, and business frames before reading payload semantics
- rebuild one stable local session before adding scale

Primary references:

- `references/stateful-stream-e2ee-playbook.md`
- `references/structured-transport-playbook.md`
- `references/session-contract-playbook.md`

## Observer-effect rule

If hooks, breakpoints, or monkey patches make the target behave differently, assume your tooling may be changing the sample.

In that case:

1. revert to the cleanest possible capture
2. save one untouched request and response pair
3. move hooks outward toward the transport boundary
4. prefer initiator stacks and request diffs over broad global monkey patches

Do not call the target "browser-only" until you have ruled out your own instrumentation.


## Continuation sibling scan

On `continuation` intake, before restarting a long reverse:

- search the workspace for existing collectors, challenge helpers, or notes for the same host or endpoint family
- reuse a proven pure-protocol path when the target and environment are unchanged
- only reopen browser or deep reverse surfaces that new evidence actually invalidates
- if the user delivered a same-family solved pure-protocol skeleton, classify it as `template` and migrate host/path/state-chain before re-deriving behavior walls (`references/case-reuse-playbook.md`, `references/verifier-morph-and-state-chain-playbook.md`)
- on multi-day verifier continuations with mint-shaped tokens and stable rejects, require the day-card and kill-switches K1-K8 before more token/track reverse (`references/verifier-morph-and-state-chain-playbook.md`)
- do not reopen already-delivered non-gate business collectors unless the current hard gate or consumer oracle actually regressed

