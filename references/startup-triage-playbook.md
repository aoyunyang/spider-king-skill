# Startup Triage Playbook

Use this reference at the start of every fresh intake or when a prior gate becomes stale.

The goal is to decide what kind of fight this is before you load giant bundles or poison the page with broad hooks.

## Contents

- [Startup gate](#startup-gate)
- [Capability-aware evidence roles](#capability-aware-evidence-roles)
- [Escalation ladder before full browser dependence](#escalation-ladder-before-full-browser-dependence)
- [Family triage](#family-triage)
- [Observer-effect rule](#observer-effect-rule)
- [Continuation sibling scan](#continuation-sibling-scan)

## Startup gate

Complete these four checks first:

1. intake mode
   - choose `live-target` when a current page or endpoint needs fresh wire and runtime evidence
   - choose `artifact-only` when the input is a saved request, packet capture, source file, JS or WASM sample, token, cookie, or response without a live target requirement
   - choose `continuation` when the same target, session assumptions, tool registry, and delivery goal remain current
   - do not claim live acceptance, current endpoint behavior, or runtime provenance from artifact-only evidence
2. environment and tool sanity
   - run `scripts/check_reverse_env.py --project-root <project>` when local execution is available; fingerprint only explicitly selected public helper lockfiles with repeatable `--helper-lockfile <path>` arguments
   - treat project `.venv` coherence as advisory by default; add `--require-project-venv` only when the user or bound project makes that environment a hard gate
   - for web `live-target`, confirm whether both `chrome-devtools` and `js-reverse` are usable through schemas, tool lists, or non-target health surfaces; this capability check must not open the target in both tools
   - record a capability snapshot: required browser families, optional passive wire-store / wire-visibility / ENV families when relevant, required methods present, optional methods present, selected fallbacks, configured browser mode (`launch`/`attach`/`unavailable`), debuggable endpoint known or not, and blockers
   - for web `live-target`, do not place both browser tool families in one parallel tool batch
   - for web `live-target`, grant initial `TARGET_ACTIVE` ownership to `chrome-devtools`; defer the first `js-reverse` target action until the Chrome handoff gate in `references/tool-playbook.md` is complete
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
| `fingerprint-baseline` | A clean flow where risk, visible interaction, renderer state, or observer effect may change the sample | untouched request and response, redirects, page state, configured browser/host mode, and session inventory | assign this role to stock Chromium via `chrome-devtools` by default, or to Camoufox/managed host when fingerprint pressure is high; if no compatible host is proved, record the role gap and keep the ordinary clean Chrome baseline honest |
| `debugger-trace` | Initiator, source, call-frame, argument, return-value, or canonical-mutation evidence | correlate one wire request with its caller and decisive mutation boundary | use only schema-confirmed debugger capabilities; fall back to saved source, the earliest stable breakpoint, a narrow behavior-preserving hook, or offline runtime proof |
| `cdp-bridge` | Network, Runtime, or Debugger evidence inside an already active target-compatible environment | record how the endpoint was obtained, which protocol domains are available, and how events correlate to the baseline | optional and conditional on an explicitly exposed, authorized connection; never guess a port, profile, launch method, or MCP helper |

Supporting passive surfaces such as reqable, HAR, or PCAP may supply wire-store or wire-visibility evidence beside these roles. They never become a fourth concurrent browser owner and never replace the required baseline then debugger first-pass roles on a fresh web `live-target`. Read `references/mcp-routing-playbook.md` when auto-judging among artifact-only, Camoufox/managed host, chrome-devtools, and js-reverse.

For every fresh web `live-target`, these roles supplement rather than replace the required first passes: collect the judged `fingerprint-baseline`, complete a `sequential handoff`, then collect `debugger-trace` evidence when attach is available. A typical role flow is:

```text
baseline host (`chrome-devtools` default, or Camoufox/managed host on high fingerprint pressure)
  -> optional `cdp-bridge` while the same owner remains TARGET_ACTIVE
  -> evidence checkpoint
  -> BASELINE_PARKED or RETAINED_EXCEPTION
  -> `js-reverse` `debugger-trace` when debug attach exists
```

At most one browser tool family remains `TARGET_ACTIVE`. Treat `cdp-bridge` as an evidence technique under the current owner, not a third concurrent owner. After a role returns its proof or named blocker, hand evidence to the role that can answer the next missing question; do not stay on one route merely because it was selected first. Apply the lifecycle gate in `references/tool-playbook.md` on every switch, including a return to an earlier role.

## Escalation ladder before full browser dependence

Use the smallest faithful layer that explains the evidence:

1. simple decode or standard algorithm: handwrite in Python first
2. host-bound JavaScript without true interaction: route to `references/embedded-browser-runtime-playbook.md`
3. full interaction or rendering dependence: observe in browser, but keep the delivery gate strict and do not confuse observation with the final collector

For the full rung-by-rung rule, proof requirements, and "do not jump layers" contract, read `references/escalation-ladder-playbook.md`.

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

