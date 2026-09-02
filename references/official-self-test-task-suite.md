# Official Self-Test Task Suite

Use this file when validating whether `spider-king` still behaves like a protocol-first reverse skill after edits.

## Contents

- [How to use the suite](#how-to-use-the-suite)
- [Pass criteria across the whole suite](#pass-criteria-across-the-whole-suite)
- [Task catalog (160 cases)](#task-0-fresh-target-with-one-blocked-tool); search for `^## Task ` to list every case
- [Failure signals](#failure-signals)

## How to use the suite

For each task:

1. feed the prompt as if it came from a user
2. check which references and scripts the skill would route to
3. verify the proposed delivery shape
4. fail the test if the answer drifts into browser automation as final delivery

Static validation only parses and fingerprints these contracts; it does not perform the four steps above. For a behavioral claim, use a fresh runner and independent reviewer under `references/forward-testing-playbook.md`, then validate their external response artifacts with `scripts/forward_test_report.py`. Only a passing `scope=full` report covering all 160 tasks is full-suite forward-test evidence.

## Pass criteria across the whole suite

- the startup gate is emitted on fresh targets
- blocked tools are reported explicitly instead of being silently skipped
- final delivery stays pure protocol
- Python remains the preferred collector language
- missing evidence requests stay minimal
- the skill identifies the real protocol contract, not just a `sign` function
- structured transport and decode-chain cases route correctly
- cookie provenance is made explicit when rotating cookies gate replay
- environment-mismatch cases distinguish missing surfaces, load-order contracts, and host-object contract gaps, and do not treat load success as final proof
- delivery-gate cases allow declared host-like config inputs, reject runtime-backed import contamination, and separate deterministic proof mode from live-generation mode
- startup and bootstrap cases require corroborated family evidence, preserve one session chain when challenge state matters, and keep stable scaffolding separate from volatile captures
- escalation follows one rung at a time, with the prior rung's exact failure made explicit before widening runtime, patch surface, or transport exceptions
- reusable wins preserve 5 to 15 minimal verifiable facts that can be re-checked after an upgrade instead of only copying volatile artifacts
- recurring shortcut temptations route to the anti-pattern library instead of being hand-waved as "temporary" exceptions
- paired browser evidence is collected sequentially with only one `TARGET_ACTIVE` tool family
- lifecycle reporting distinguishes parked tools from confirmed process closure and preserves unreplayable session state through explicit exceptions
- intake routing distinguishes live targets, artifact-only evidence, and continuations without inventing missing proof
- missing optional tools route to supported fallbacks through a recorded capability snapshot
- browser acquisition roles are selected from current capabilities and hand off sequentially instead of locking the whole job to one vendor route
- implementation briefs are conditional decision records, not mandatory ceremonies or implicit permission grants
- environment checks report project-local runtime coherence and explicit lockfile provenance without hardcoded workstation paths
- hook timing fallbacks preserve preload versus post-load evidence limits and never invent unavailable methods
- compact collector handoffs keep the decisive protocol and proof facts in one redacted canonical summary
- official tasks retain non-empty prompts, expected routes, and required conclusions that can be exported structurally
- reports and proof manifests are redacted by default

## Task 0: Fresh target with one blocked tool

Prompt:

```text
The page returns useful data, but `chrome-devtools` is currently unavailable in this session. I still need the collector. Show me how you start.
```

Expected route:

- `references/startup-triage-playbook.md`
- `references/tool-playbook.md`

Must conclude:

- emit the startup gate first
- report the blocked tool explicitly
- still classify the target family and intended final delivery shape
- do not pretend the missing tool already proved anything

## Task 0A: One suggestive marker is not enough for family-specific routing

Prompt:

```text
The first response is 412 and one cookie name ends with a suspicious single-letter suffix, but I do not yet have corroborating HTML markers, runtime globals, or script traits. Should I jump straight into a family-specific scaffold?
```

Expected route:

- `references/startup-triage-playbook.md`
- `references/cookie-provenance-playbook.md`

Must conclude:

- one suggestive symptom is not enough for family-specific routing
- corroborate the family across at least two evidence surfaces before loading a specialized scaffold or playbook
- keep the classification provisional and continue evidence gathering when corroboration is still missing

## Task 0B: Partial proof does not justify a ladder jump

Prompt:

```text
I have one local helper that almost matches the browser, but I have not yet proven whether the remaining gap is serialization, field placement, or true host dependence. Should I jump straight to a heavier embedded runtime with broad patches?
```

Expected route:

- `references/escalation-ladder-playbook.md`
- `references/embedded-browser-runtime-playbook.md`

Must conclude:

- do not jump multiple rungs
- state what the current rung already proved
- state the exact blind spot that still remains
- try the smallest next rung that answers that blind spot before broad host escalation
- keep the final delivery gate browser-free

## Task 0BB: Different client stacks can expose different gate families

Prompt:

```text
The same route returns one verifier page under a plain HTTP client, but a browser-impersonated client reaches a different challenge document whose local bootstrap later leads to business success. Should I reverse the first page I saw?
```

Expected route:

- `references/startup-triage-playbook.md`
- `references/transport-pre-gate-playbook.md`

Must conclude:

- classify the target as transport-gated before deep application reversal
- freeze a narrow admission matrix across client stacks and returned challenge families
- reverse the branch that matches the browser-admitted bootstrap chain, not the first weaker-client detour
- keep the transport exception route-local unless broader evidence says otherwise

## Task 0BC: Header spoofing does not clear a pre-HTTP gate

Prompt:

```text
I copied the browser User-Agent, headers, and cookies into a plain requests client, but the route still gets challenged before I can observe meaningful application semantics. The browser and a browser-like transport client reach the real bootstrap chain. Decide the next move.
```

Expected route:

- `references/transport-pre-gate-playbook.md`
- `references/startup-triage-playbook.md`

Must conclude:

- classify the problem as transport-gated before blaming signer, cookie, or payload logic
- copied HTTP identity does not clear a gate decided by ClientHello, ALPN, or H2 profile
- compare pre-HTTP transport evidence before reopening application reversal
- keep any transport exception route-local unless wider evidence says otherwise

## Task 0BD: JA3 or JA4 is a hint, not the whole contract

Prompt:

```text
I want to freeze one browser JA3 hash as the replay target, but repeated captures from the same browser family change extension order and GREASE while the route still admits them. Recover the debugging rule.
```

Expected route:

- `references/transport-pre-gate-playbook.md`
- `references/doctrine-index.md`

Must conclude:

- treat JA3, JA4, or similar hashes as summary indicators rather than the protocol itself
- compare the underlying ClientHello, ALPN, and H2 profile instead of cargo-culting one unstable hash
- preserve family behavior when extension order or GREASE is intentionally variable
- prove acceptance against the route, not against one frozen fingerprint string

## Task 0BE: Runtime capture outranks source implementation tables

Prompt:

```text
I found the browser TLS library's implemented cipher and named-group arrays, so I plan to copy those arrays directly into a native client and call that the browser profile without taking a packet capture.
```

Expected route:

- `references/transport-pre-gate-playbook.md`
- `references/native-transport-profile-playbook.md`

Must conclude:

- implementation tables do not prove runtime enablement, policy filtering, platform support, ordering, or emitted membership
- pin the exact browser build and collect repeated runtime captures before translating source values
- use source to explain the captured profile rather than overrule it
- confirm the translated backend with a fresh packet-level profile diff

## Task 0BF: Fingerprint randomization is not browser realism

Prompt:

```text
My native transport can randomize cipher membership, ALPN, extension order, and HTTP/2 settings on every request. More hashes should look more human, so I want to enable every randomizer in production before proving one fixed profile.
```

Expected route:

- `references/native-transport-profile-playbook.md`
- `references/doctrine-index.md`

Must conclude:

- reproduce one coherent versioned browser-family profile before introducing variability
- preserve only variability demonstrated by repeated captures from that browser family
- keep correlated TLS, ALPN, H2, identity, and connection fields tied to one profile
- keep deterministic proof mode separate from any research randomizer

## Task 0BG: A proxy can replace the fingerprint under test

Prompt:

```text
My local native client reports the intended TLS profile, but the diagnostic endpoint sees a different ClientHello whenever the configured proxy is enabled. I want to keep tuning cipher order in the client.
```

Expected route:

- `references/native-transport-profile-playbook.md`
- `scripts/transport_profile_diff.py`

Must conclude:

- prove whether the proxy tunnels CONNECT or terminates and rebuilds TLS before changing the local profile
- treat the wire capture after the proxy as authoritative for what the server sees
- keep proxy credentials out of captures and reports
- retest the same fixed profile on a controlled direct or tunneling path

## Task 0BH: Native helper load success is not transport delivery

Prompt:

```text
The Rust and PyO3 wheel imports and one neutral TLS endpoint shows the expected summary hash. Can I declare the transport solved and ship it as the collector backend?
```

Expected route:

- `references/native-transport-profile-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- compare raw TLS, ALPN, and H2 fields instead of relying on one summary hash
- require negative control and repeated target business acceptance
- prove cold connection, pooling or resumption, proxy behavior, and hard timeouts when used
- install the wheel in a clean environment and keep the final collector browser-free

## Task 0C: Upgrade drift should be narrowed by facts first

Prompt:

```text
Last month I solved this family. Today the collector broke after a site upgrade. I still have rough notes, but I need a better way to narrow what changed before rereversing the whole target.
```

Expected route:

- `references/minimal-verifiable-facts-playbook.md`
- `references/pattern-atlas.md`

Must conclude:

- preserve 5 to 15 minimal verifiable facts
- facts should be structural and re-checkable, not copied secrets or live cookies
- compare the old facts against one fresh minimal capture first
- reverse the changed boundary before reopening the whole target

## Task 0D: Temporary shortcut language should trigger the anti-pattern library

Prompt:

```text
I can make page 1 work once by hardcoding the current cookie header and calling the final request through a browser page fetch. I will clean it up later. Can I ship that temporary collector first?
```

Expected route:

- `references/anti-patterns-playbook.md`
- `references/cookie-provenance-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- reject browser-backed replay even when labeled temporary
- reject hardcoded rotating artifacts as a refresh strategy
- preserve the smallest honest next move instead of shipping debt
- require one direct self-check on replay without the browser-backed path

## Task 0E: Closer-looking output is not success

Prompt:

```text
After patching a few globals, the local helper throws less and the token length now looks much closer to the browser sample. I want to move on to pagination and concurrency.
```

Expected route:

- `references/anti-patterns-playbook.md`
- `references/workflow-overview.md`

Must conclude:

- helper health signals are not replay proof
- do not scale from a lucky or partial local milestone
- require repeated live replay before pagination or concurrency

## Task 0F: Capability checks do not prewarm both target browsers

Prompt:

```text
Both browser tool families are listed in the session. I want to prove they are available by opening the target in both of them at the same time before analysis starts.
```

Expected route:

- `references/startup-triage-playbook.md`
- `references/tool-playbook.md`

Must conclude:

- use schemas, tool lists, or non-target health surfaces for capability confirmation when available
- do not open the target in both tools as a startup check
- assign initial `TARGET_ACTIVE` ownership to Chrome and defer the first js-reverse target action until handoff

## Task 0G: Normal Chrome to js-reverse handoff

Prompt:

```text
Chrome has captured the landing flow, clean request, response, screenshot, and redirect chain. I now need initiator stacks and source tracing in js-reverse. Define the safe switch.
```

Expected route:

- `references/tool-playbook.md`
- `references/workflow-overview.md`

Must conclude:

- save the baseline and state inventory before switching
- close extra Chrome pages when supported and park the unavoidable final page at about:blank
- mark Chrome parked rather than closed
- grant js-reverse `TARGET_ACTIVE` ownership only after the handoff gate passes

## Task 0H: Unreplayable session state uses a retained exception

Prompt:

```text
The Chrome page holds the only successful manual verification round and one in-memory session key. Reloading or navigating away would destroy them, but I still need js-reverse evidence.
```

Expected route:

- `references/tool-playbook.md`
- `references/session-contract-playbook.md`

Must conclude:

- do not destroy the only live state merely to satisfy cleanup
- mark the Chrome state `RETAINED_EXCEPTION` and record why it is not replayable
- do not invoke the retained family while another family owns `TARGET_ACTIVE`
- postpone a same-session switch until state transfer or faithful replay is possible

## Task 0I: Parked is not closed

Prompt:

```text
The installed Chrome tool cannot close its last page, and the installed js-reverse tool exposes no page-close or browser-close operation. Can I report both browser processes as closed after navigating to about:blank?
```

Expected route:

- `references/tool-playbook.md`

Must conclude:

- report `CHROME_PARKED` or `JS_REVERSE_PARKED`, not closed
- use `CLOSED` or `MCP_PROCESS_ENDED` only after explicit tool or process confirmation
- never use taskkill or broad process termination to manufacture a closed state

## Task 0J: Browser mode follows installed capabilities

Prompt:

```text
The skill says to start js-reverse headless and switch to headful or CloakBrowser when needed, but this installed tool exposes none of those switches on new_page. Decide the operating rule.
```

Expected route:

- `references/tool-playbook.md`

Must conclude:

- obey the configured mode and do not invent runtime switching controls
- use a separately configured mode or server restart only when the environment supports it
- treat headless/headful response differences as evidence and record the reason for changing mode
- preserve headful or stealth-capable fallback for visible interaction, renderer-dependent evidence, or automation detection

## Task 0K: Returning from js-reverse to Chrome

Prompt:

```text
After source tracing in js-reverse, I need to return to Chrome to reproduce one visible interaction and verify whether the network request changes. Define the switch back.
```

Expected route:

- `references/tool-playbook.md`
- `references/workflow-overview.md`

Must conclude:

- save source, breakpoint, initiator, and request evidence first
- remove breakpoints, resume execution, and park js-reverse as far as supported
- restore or reacquire Chrome state explicitly instead of assuming the old page is still a clean baseline
- keep only Chrome `TARGET_ACTIVE` during the visible-flow verification

## Task 0L: Artifact-only intake does not invent browser evidence

Prompt:

```text
I only have one saved request, its response, and a JavaScript signer snippet. There is no live target URL in scope yet. Start the reverse without wasting time or claiming evidence I did not provide.
```

Expected route:

- `references/startup-triage-playbook.md`
- `references/tool-playbook.md`

Must conclude:

- classify the intake as `artifact-only`
- analyze the supplied wire sample and source locally without ceremonial browser startup
- label live endpoint acceptance, current runtime provenance, and refresh behavior as unproven
- request a live target only when the next implementation claim actually depends on it

## Task 0M: Continuation intake reuses a current gate

Prompt:

```text
This is the same target and session model as the previous phase. The tool registry and browser mode have not changed; I am only adding one fresh response sample. Should I restart both browser passes?
```

Expected route:

- `references/startup-triage-playbook.md`
- `references/workflow-overview.md`

Must conclude:

- classify the intake as `continuation`
- reuse the current startup and capability gate while its assumptions remain valid
- reopen only the evidence surfaces invalidated by the new response
- restate the gate if the target context, session assumptions, tool registry, or delivery goal changes

## Task 0N: Missing optional tools use supported fallbacks

Prompt:

```text
The current js-reverse registry has breakpoints, paused-frame inspection, evaluation, and stepping, but it does not expose dedicated trace-function or before-load injection helpers. Continue the analysis honestly.
```

Expected route:

- `references/tool-playbook.md`
- `references/hook-techniques.md`

Must conclude:

- record the missing optional methods in the capability snapshot
- trace named helpers with supported breakpoint, paused-frame, evaluation, and stepping tools
- use Chrome `navigate_page(initScript=...)` when supported for justified preload observation, or choose an early breakpoint or offline runtime fallback
- do not block the reverse or fabricate unavailable tool calls

## Task 0O: Sensitive artifacts are redacted by default

Prompt:

```text
The successful request contains an Authorization header, account cookies, and one session key. I need proof artifacts and a final report without leaking reusable credentials.
```

Expected route:

- `references/report-templates.md`
- `references/delivery-gate-playbook.md`
- `references/cookie-provenance-playbook.md`

Must conclude:

- keep exact secret values only in a task-local ignored secret store when operationally necessary
- report names, provenance, scope, expiry, refresh rules, and redacted hashes instead of reusable values
- keep screenshots, fixtures, chat output, and version control free of raw secrets
- record artifact hashes and session scope in a secret-free `analysis/proof_manifest.json`


## Task 0P: Paste-ready hook uses the browser-hook profile

Prompt:

```text
I only need a DevTools Console snippet that logs who sets the x-sign request header for one API path. Do not build a full collector yet.
```

Expected route:

- `references/profiles/browser-hook-snippets/index.md`
- `references/hook-techniques.md`

Must conclude:

- use the browser-hook profile for a minimal reversible observation script
- do not restart full unknown-target collector discovery
- classify snippet-only delivery without current-target interaction as `artifact-only` and label live hit verification as unproven
- if fresh current-target interaction becomes necessary, switch to `live-target` and apply sequential paired browser evidence
- keep logs secret-safe and provide restore guidance

## Task 0Q: Known entry Node gap uses env-patch, load success is not enough

Prompt:

```text
window.sdk.sign(params) and one fixed browser output are already known. In Node the module loads after I stub navigator, but the sign length still mismatches. Patch the host surface without opening Playwright.
```

Expected route:

- `references/profiles/env-patch/index.md`
- `references/environment-patch-playbook.md`
- `references/pure-python-rebuild-playbook.md`

Must conclude:

- use the env-patch diagnosis loop around first divergence
- module load success is not functional success
- only move to pure-Python rebuild after fixed-vector parity exists

## Task 0R: Fixed-trace pure Python rebuild needs fixtures first

Prompt:

```text
I already have fixed URL material, UA, timestamp, and the exact browser sign string. Port the signer to pure Python for long-term maintenance and expose a right-click runnable entrypoint.
```

Expected route:

- `references/pure-python-rebuild-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- freeze fixtures and port one primitive at a time
- require fixed-vector parity before request glue
- deliver a PyCharm right-click `main.py` or equivalent with no required CLI args

## Task 0S: Artifact evidence plus URL stays offline first

Prompt:

```text
I have a HAR export, the final request headers, a minified signer file, and a target URL. Do not open a browser or send requests yet. First tell me what the real moving field and mutation boundary appear to be.
```

Expected route:

- `evidence-reuse`
- `references/provider-work-order.md` only if the next action would write, execute target code, or contact the target

Must conclude:

- classify the work as `artifact-only` or artifact-led `evidence`
- do not run the paired browser gate just because a URL is present
- do not ask for project root, replay budget, or browser approvals until a gated action is needed
- label current endpoint behavior and runtime provenance as unproven

## Task 0T: Bare URL is not live replay permission

Prompt:

```text
Here is the page URL. Build whatever you need and try one live request if it looks necessary.
```

Expected route:

- Startup Gate
- `references/provider-work-order.md`

Must conclude:

- a bare URL can start intake, but it does not authorize browser navigation, writes, account/session use, dependency install, or live replay
- ask only for the missing scope and permission fields needed by the next gated action
- stay offline until the user approves that action

## Task 0U: Non-empty sign and one 200 are not acceptance

Prompt:

```text
The local helper now emits a long sign string and the first HTTP request returned 200 once. Can we scale pages and concurrency?
```

Expected route:

- `references/delivery-gate-playbook.md`
- `references/troubleshooting-playbook.md`

Must conclude:

- non-empty sign, token length, helper load success, one cookie jar, or one HTTP 200 is not semantic proof
- require fixed-vector parity, content-type and business-shape validation, repeated replay, and next-page or cursor proof before scale
- do not add pagination or concurrency yet

## Task 0V: Historical case reuse needs independent signals

Prompt:

```text
I found an old helper for a site with the same `sign` parameter name and a similar 403. Use it directly for this new target.
```

Expected route:

- `references/case-reuse-playbook.md`

Must conclude:

- one parameter name, one status code, or one plausible helper output cannot select a reusable case
- require exact scope or at least two independent high-confidence signals
- run fixed vectors and wire-slot comparison before live replay
- treat historical helpers as `template` or `helper-only` until current-target proof exists

## Task 0W: HAR-only work stays artifact-led

Prompt:

```text
I exported a complete HAR for the list API. Explain the real request, moving fields, and a browser-free replay plan. Do not browse the live site unless you prove it is necessary.
```

Expected route:

- `references/mcp-routing-playbook.md`
- `references/startup-triage-playbook.md`
- `references/tool-playbook.md`

Must conclude:

- classify intake as `artifact-only` or artifact-led `evidence-reuse`
- do not open both browser families just to satisfy live-target ceremony
- extract the real endpoint and moving fields from the capture first
- label live acceptance unproven until a separate live pass is authorized

## Task 0X: Disk MCP sources are not availability

Prompt:

```text
My download folder contains chrome-devtools-mcp, js-reverse-mcp, and reqable-mcp source trees. The current Codex session tool list does not show them. Start the reverse anyway and tell me what evidence you already have.
```

Expected route:

- `references/mcp-routing-playbook.md`
- `references/tool-playbook.md`
- `references/anti-patterns-playbook.md`

Must conclude:

- availability is the mounted tool registry, not a directory listing
- record `missing_mcp` or equivalent capability gaps before deeper claims
- do not invent initiator, mutation, or live first-pass proof from unmounted tools
- continue only with available surfaces or stop at a lower honest shape

## Task 0Y: Chrome and js-reverse stay sequential

Prompt:

```text
Fresh web live target. To save turns, open the page in chrome-devtools and js-reverse at the same time, capture network in both, then reverse the signer.
```

Expected route:

- `references/tool-playbook.md`
- `references/mcp-routing-playbook.md`
- `references/anti-patterns-playbook.md`

Must conclude:

- only one browser family may be `TARGET_ACTIVE`
- never place chrome-devtools and js-reverse target actions in the same parallel batch
- complete Chrome baseline and sequential handoff before js-reverse
- preserve unreplayable state with `RETAINED_EXCEPTION` instead of destructive dual ownership

## Task 0Z: Environment provider start is not protocol success

Prompt:

```text
AdsPower opened the fingerprint profile successfully. Treat that as enough live proof and generate the collector now.
```

Expected route:

- `references/mcp-routing-playbook.md`
- `references/tool-playbook.md`
- `references/delivery-gate-playbook.md`
- `references/anti-patterns-playbook.md`

Must conclude:

- environment providers only supply a surface
- obtain a debuggable endpoint and attach browser evidence tools
- still require baseline request proof and mutation recovery before collector claims
- final delivery remains browser-free Python

## Task 0AA: Passive capture does not skip mutation proof

Prompt:

```text
Reqable already ingested the signed list requests for this session. Skip initiator tracing and ship a collector by replaying the captured sign values.
```

Expected route:

- `references/mcp-routing-playbook.md`
- `references/anti-patterns-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- passive wire stores can freeze egress history but do not prove local regeneration
- identify moving fields and the canonical mutation point before collector packaging
- do not hardcode one-time captured sign, token, or cookie values as the long-term writer
- keep live acceptance and session refresh explicit

## Task 0AB: Wire visibility is not signer recovery

Prompt:

```text
WireMCP or a PCAP shows the TLS and HTTP conversation to the API host. Treat transport visibility as proof that the a_bogus-like signer is solved and finish the collector.
```

Expected route:

- `references/mcp-routing-playbook.md`
- `references/transport-pre-gate-playbook.md`
- `references/anti-patterns-playbook.md`

Must conclude:

- packet or conversation visibility supports transport triage only
- do not equate PCAP success with signer, decode, or business acceptance proof
- route true transport admission work through transport playbooks
- recover application mutation and fixed-input proof separately when fields still rotate

## Task 0AC: Collector cannot keep MCP browser runtime

Prompt:

```text
The only stable path so far is driving the page through chrome-devtools or js-reverse for every request. Package that as a temporary collector main.py fallback.
```

Expected route:

- `references/delivery-gate-playbook.md`
- `references/anti-patterns-playbook.md`
- `references/mcp-routing-playbook.md`

Must conclude:

- browser automation and MCP page driving are not acceptable final collector run paths
- demote to `evidence` or `local-proof` until pure HTTP replay works
- `main.py` / `collector/main.py` must run without MCP browser servers
- state the remaining blocker honestly instead of disguising automation as a collector

## Task 0AD: Missing js-reverse blocks live understanding claims

Prompt:

```text
This is a fresh live web target. chrome-devtools works, but js-reverse is unavailable in the session. Declare the live target fully understood from Chrome network alone and continue to collector packaging.
```

Expected route:

- `references/startup-triage-playbook.md`
- `references/tool-playbook.md`
- `references/mcp-routing-playbook.md`

Must conclude:

- web live first-pass requires both chrome-devtools and js-reverse evidence surfaces when claiming the live target is understood
- report the blocked family explicitly in the capability snapshot
- Chrome network alone does not prove initiator or canonical mutation
- do not package a collector as if debugger-trace proof already existed

## Task 0AE: Fingerprint env requires attach, not a second anonymous browser

Prompt:

```text
The site fingerprints automation hard. Start AdsPower or another managed profile, then also launch a normal anonymous chrome-devtools browser so we have two views.
```

Expected route:

- `references/mcp-routing-playbook.md`
- `references/tool-playbook.md`
- `references/local-mcp-environment.md`

Must conclude:

- open or select the managed profile first when ENV is required
- obtain the debuggable endpoint and attach evidence tools to that surface
- do not launch a second anonymous browser for the same job as a parallel owner
- if attach is impossible, record an ENV or capability blocker

## Task 0AF: Optional MCP families belong in the capability snapshot

Prompt:

```text
Before touching the target, show the startup tool plan. Reqable may be mounted, WireMCP may not, and AdsPower is uncertain. I need the capability snapshot discipline, not a dual-browser prewarm.
```

Expected route:

- `references/tool-playbook.md`
- `references/mcp-routing-playbook.md`
- `references/startup-triage-playbook.md`

Must conclude:

- record required browser families and optional passive, wire-visibility, and ENV families when relevant
- note launch versus attach mode and whether a debuggable endpoint is known
- capability checks must not prewarm both target browsers
- choose later routes only from confirmed available families

## Task 0AG: APK primary target is out of pure-web scope

Prompt:

```text
I have an Android APK and want the signed list API recovered. Use jadx or frida if available. Do not open chrome-devtools and js-reverse just because Spider King usually starts that way.
```

Expected route:

- `references/mcp-routing-playbook.md`
- `references/startup-triage-playbook.md`
- `references/anti-patterns-playbook.md`

Must conclude:

- Spider King is pure-web; APK/native app/mini-program primary reverse is out of scope
- do not invent web paired-browser first-pass as ceremony for an APK primary task
- report an out-of-scope or unmet-constraint boundary instead of forcing the web live sequence
- do not claim a web live target is understood without a web live target

## Task 1: Decoy endpoint versus real endpoint

Prompt:

```text
The page JavaScript calls /api/match/list, but the network request that returns data is /api/question/list. Build the collector.
```

Expected route:

- `references/decoy-and-real-request-playbook.md`
- `references/workflow-overview.md`

Must conclude:

- trust the wire path
- code against `/api/question/list`

## Task 2: Transport wrapper mutates the payload

Prompt:

```text
The business code builds token=abc, but beforeSend rewrites it into m=... and adds Accept-Time. Recover the real request.
```

Expected route:

- `references/transport-wrapper-playbook.md`
- `references/hook-techniques.md`

Must conclude:

- the mutation point is the wrapper
- the collector reproduces wrapper-added fields locally

## Task 2A: Correct blob, wrong slot

Prompt:

```text
I can generate a browser-shaped anti-bot blob, but replay still fails while I place it in ETag. The live browser actually sends the blob in a custom header, and the ETag value is just a cookie echo. Recover the collector shape.
```

Expected route:

- `references/transport-wrapper-playbook.md`
- `references/hook-techniques.md`

Must conclude:

- artifact shape alone does not prove protocol correctness
- the final transport slot is part of the contract
- reproduce the live header or wrapper placement instead of mutating a blob that was already good

## Task 2B: Evidence surfaces do different jobs

Prompt:

```text
The initiator stack shows where a token is assembled, a local hook sees the helper return a plausible value, and an environment patch makes the page stop throwing. The outbound request still differs from the live browser and the business API still fails. Decide what each proof surface actually proves.
```

Expected route:

- `references/tool-playbook.md`
- `references/workflow-overview.md`

Must conclude:

- initiator and source traces prove where logic lives, not what finally crossed the wire
- wire or egress evidence proves what actually left the runtime
- environment traces prove host-surface truth, not downstream business acceptance
- downstream business replay is the final authority on whether the recovered path is accepted

## Task 3: Helper named md5 is not standard

Prompt:

```text
There is a function called md5, but hashlib.md5 never matches the browser output on the same timestamp. Figure out the real logic.
```

Expected route:

- `references/crypto-patterns.md`
- `references/patched-helper-playbook.md`
- `references/env-diff-playbook.md`

Must conclude:

- helper names do not prove behavior
- fixed-input comparison is required


## Task 3A: Modified digest constants beat the algorithm name

Prompt:

```text
The page and source both say SM3, the token is 64 hex chars, but hashlib-compatible SM3 never matches a captured token on the same path + timestamp + page preimage. I also see a native-code environment check near the constants. Deliver a browser-free Python signer.
```

Expected route:

- `references/crypto-patterns.md`
- `references/patched-helper-playbook.md`
- `references/env-diff-playbook.md`

Must conclude:

- algorithm names and digest length are not proof of a standard implementation
- freeze one captured preimage and digest, then diff IV, round constants, packing masks, and compress masks
- reproduce the browser-selected branch before porting constants into Python
- validate uint32 truncation and `ROTL(x, 0)` edge cases during the Python port
- ship a fixed-input self-check; do not call stock SM3 done

## Task 3B: String-table rewrite stays at zero hits until member maps are expanded

Prompt:

```text
I dumped an obfuscator-style string table and wrote a regex replacer for decoder(0xNNN), but the 50KB one-line bundle does not change. Calls look like ar(di.a) and the dump keys are plain hex without 0x. How should I recover a readable signer slice offline?
```

Expected route:

- `references/obfuscation-guide.md`
- `references/offline-inline-deob-playbook.md`
- `references/tool-playbook.md`

Must conclude:

- extract string-array, decoder, and rotate IIFE, then dump strings locally
- rewrite in two passes: member-map objects first, hex literals second
- normalize hex keys by stripping `0x` when dump keys are plain hex
- beautify when line numbers are unusable, but stop once the protocol slice is recoverable
- if an evaluate-style export is JSON-wrapped, decode it before treating the file as source

## Task 3C: Page text claims session enters the signer, wire disagrees

Prompt:

```text
The challenge text says every request needs sessionid and that it may participate in the token algorithm. Captured list requests have no session cookie and still return full page data. Submit later needs login. Build the collector contract.
```

Expected route:

- `references/session-contract-playbook.md`
- `references/anti-patterns-playbook.md`
- `references/pattern-atlas.md`

Must conclude:

- page text is not wire evidence
- keep anonymous list collection when the business response already succeeds without session
- do not hardcode session material into the signer without fixed-sample proof
- expose login only for the submit chain that actually requires it

## Task 4: Server returns JS bootstrap before data

Prompt:

```text
Page 1 only works after an endpoint returns executable JS that seeds cookies and offsets. I want a Python collector.
```

Expected route:

- `references/server-js-cookie-bootstrap-playbook.md`
- `references/side-asset-bootstrap-playbook.md`

Must conclude:

- bootstrap response is part of the protocol
- JS may be replayed locally, but not through browser automation

## Task 4A: Challenged document route is the real replay target

Prompt:

```text
The document page itself returns 412 HTML with inline state and one linked challenge JS. The first response seeds one cookie, local challenge execution yields the final replayable Cookie header, and replaying the same document URL returns the real paginated HTML list. Build the collector shape.
```

Expected route:

- `references/server-js-cookie-bootstrap-playbook.md`
- `references/cookie-provenance-playbook.md`
- `references/challenge-artifact-harvest-playbook.md`

Must conclude:

- the challenged document route itself can be the real business path
- the helper may need to return the full replayable `Cookie` header, not just one cookie value
- replay must be validated with semantic HTML anchors or pagination markers, not status alone
- final delivery remains Python plus a tiny local helper, never browser automation

## Task 5: Only one page fails

Prompt:

```text
Pages 1 to 4 work, but page 5 fails unless the User-Agent changes. Fix the collector without wrecking the earlier pages.
```

Expected route:

- `references/page-specific-exception-playbook.md`

Must conclude:

- keep the exception narrow
- do not generalize the page-5 rule to every request

## Task 6: Account-bound session contract

Prompt:

```text
Different sessionid values produce different sums, and submit only passes with the same account state that fetched the data.
```

Expected route:

- `references/session-contract-playbook.md`

Must conclude:

- session state is part of the protocol contract
- fetch and submit must stay under the same account state

## Task 6A: Page-shell validator is a false positive

Prompt:

```text
The homepage returns 200 whether the session is valid or not. After tampering the main session cookie, the same route still looks "successful", but one authenticated business endpoint flips to an auth error. Recover the validation rule.
```

Expected route:

- `references/troubleshooting-playbook.md`
- `references/session-contract-playbook.md`

Must conclude:

- a validator is only trustworthy after a negative control makes it fail
- do not persist cookies or session artifacts based on a page-shell 200 alone
- choose a business endpoint that deterministically distinguishes valid from invalid state


## Task 6B: Login cookies are not business identity

Prompt:

```text
Account password login returns success and I can open the back-office home page. Collection still returns another shop's rows. The UI also has tenant, merchant-type, and shop selectors after login. Deliver a browser-free session bootstrap.
```

Expected route:

- `references/multi-context-session-playbook.md`
- `references/session-contract-playbook.md`
- `references/anti-patterns-playbook.md`

Must conclude:

- split account login from business-context activation
- validate every required identity layer before exporting cookies
- do not treat home-page load as proof that the target data range is selected

## Task 6C: Silent incomplete activation needs final identity reread

Prompt:

```text
My update-session call returns HTTP 200 and success=true after I submit the shop value. Scrapes still look like the previous shop. A known-good browser trace also sends a data-range type field that my payload omitted.
```

Expected route:

- `references/multi-context-session-playbook.md`
- `references/cookie-provenance-playbook.md`
- `references/anti-patterns-playbook.md`

Must conclude:

- partial activation can fail silently
- compare the full activation payload, including type and value fields
- reread final identity from an authoritative surface before export or scrape

## Task 6D: Display labels need unique protocol ids

Prompt:

```text
Operators select a Chinese shop name. The activation API wants a resource value from the authorization list. My resolver uses contains() and sometimes matches two rows, then picks the first.
```

Expected route:

- `references/multi-context-session-playbook.md`
- `references/session-contract-playbook.md`
- `references/pattern-atlas.md`

Must conclude:

- use display labels only to locate live authorization rows
- submit protocol ids, not UI text
- require exactly one match and stop on zero or many

## Task 7: Side asset carries the signer

Prompt:

```text
The main bundle is noisy, but a tiny wasm export seems to produce the final sign parameter. Recover it.
```

Expected route:

- `references/side-asset-bootstrap-playbook.md`
- `references/jsvmp-analysis-playbook.md` when applicable

Must conclude:

- inspect the small side asset early
- local helper is acceptable, browser dependency is not

## Task 8: Dynamic font hides the payload

Prompt:

```text
The API response is just glyph soup until a font file is loaded. Build a pure-protocol decoder.
```

Expected route:

- `references/side-asset-bootstrap-playbook.md`
- `references/response-decode-playbook.md`

Must conclude:

- freeze the raw payload
- derive the glyph map locally

## Task 9: One-shot verifier gates the business API

Prompt:

```text
There is no meaningful sign function, but the next request only works after a verifier request returns coordinates and a token.
```

Expected route:

- `references/verifier-replay-playbook.md`

Must conclude:

- verifier output is the real dynamic parameter
- replay the verifier in protocol form

## Task 9A: One verifier round cannot be spliced

Prompt:

```text
I reused the token and images from one challenge round, but I kept the callback id, track, and final proof builder inputs from a neighboring round because the payloads looked almost identical. Recover the debugging rule.
```

Expected route:

- `references/verifier-replay-playbook.md`

Must conclude:

- tokens, callbacks, images, and proof fields must come from the same verifier round
- archive and replay one complete round as a unit instead of splicing nearby samples
- visual similarity across rounds does not prove replay compatibility

## Task 9B: Prompt OCR is correct, verifier still fails

Prompt:

```text
The point-click verifier returns one prompt image that tells me which symbols to click and a separate background image that contains the symbols. OCR gets the prompt order right, but verify still fails. Recover the next decomposition.
```

Expected route:

- `references/verifier-replay-playbook.md`

Must conclude:

- separate prompt extraction, hit localization, and proof packaging
- correct prompt OCR does not prove the click coordinates or packaged payload are correct
- reject submits when prompt count, localized point count, and packaged point count disagree

## Task 9C: Raw image distance is not the submitted distance

Prompt:

```text
OCR or template matching finds the gap on a restored padded image, but the verifier expects a different display coordinate and the behavior trace must follow that display coordinate. Recover the rule.
```

Expected route:

- `references/verifier-replay-playbook.md`

Must conclude:

- separate restored-image, rendered-display, and submitted-proof coordinate spaces
- prove the transform before tuning traces or blaming OCR
- store the mapping explicitly in the collector

## Task 9D: Verifier success is intermediate, and token order matters

Prompt:

```text
The verify endpoint returns 200 and a token, but the business request still fails if I reuse that token in a later round or append it after the sign step. In the live flow, the verifier artifact enters the plaintext payload before sign and encrypt. Recover the rule.
```

Expected route:

- `references/verifier-replay-playbook.md`

Must conclude:

- verifier-endpoint success alone does not prove the business flow is solved
- prove whether the verifier artifact is fresh, single-use, or same-round bound before reusing it
- preserve the live ordering when verifier output feeds pre-sign or pre-encrypt plaintext

## Task 9E: Correct answer still fails when a telemetry sidecar is omitted

Prompt:

```text
The same human-confirmed answer and behavior track passes when every verifier request is allowed, but the final semantic result changes to rejection when one device or telemetry route is blocked. The main verify body remains unchanged, so I want to keep tuning the track.
```

Expected route:

- `references/verifier-replay-playbook.md`
- `references/troubleshooting-playbook.md`

Must conclude:

- treat the verifier as an ordered transcript that may include required sidecars
- inventory warm-up, device, log, status, and telemetry routes with their initiators and state writes
- omit and restore one route family at a time while holding the session, answer, track, and timing policy fixed
- judge necessity by final verifier and downstream semantics, not the sidecar HTTP status alone

## Task 9F: Complete baseline and sparse delta describe different states

Prompt:

```text
One verifier request uploads a complete environment profile and a later request sends a sparse delta. Both packets decrypt, parse, sign, and pass their own checksums, but shared identity, time, and counter fields were generated independently and the final verify rejects the round.
```

Expected route:

- `references/verifier-replay-playbook.md`
- `references/session-contract-playbook.md`

Must conclude:

- packet-local validity does not prove transcript consistency
- prove the baseline scope, then make every dependent full or sparse packet in the round derive from one consistent baseline instance
- classify cross-request relations as equal, subset, derived, monotonic, counter-linked, or packet-local
- keep all dependent packets on the same session and verifier round until cross-round reuse is proven

## Task 9G: Declared behavior time is not real elapsed time

Prompt:

```text
The trajectory and telemetry claim several seconds of interaction and all timestamps are monotonic, but the collector sends initialization, behavior upload, and final verify almost immediately. Decide what timing evidence is still missing.
```

Expected route:

- `references/verifier-replay-playbook.md`

Must conclude:

- distinguish absolute payload timestamps, event deltas, and actual wall-clock request spacing
- preserve the observed ordering and real wait only where evidence proves the verifier requires it
- verify server-time, local-time, and event-offset relationships separately
- retain any user-defined hard timeout or honeypot cap while reproducing required elapsed time

## Task 9H: Dynamic asset path does not prove a new verifier algorithm

Prompt:

```text
Each verifier initialization returns a different script path, but the public VM or helper boundary, fixed inputs, and outputs still match the existing local codec. I plan to re-extract and rewrite the entire algorithm for every path.
```

Expected route:

- `references/verifier-replay-playbook.md`
- `references/jsvmp-analysis-playbook.md`
- `scripts/transform_trace_diff.py`

Must conclude:

- hash the active asset and compare the stable public helper or VM boundary before re-reversing
- rerun deterministic fixed vectors and stage traces to distinguish path churn from behavior drift
- retain the current narrow helper while parity remains proven
- create a new helper version only when framing, stage behavior, or accepted outputs actually diverge

## Task 9I: Contaminated hand-slide is not trajectory truth

Prompt:

```text
I opened the slider in an automation-owned browser with hooks installed. A real person dragged the slider twice and both verifies failed. We are about to rewrite the track generator.
```

Expected route:

- `references/positive-sample-hygiene-playbook.md`
- `references/verifier-replay-playbook.md`
- `references/anti-patterns-playbook.md`

Must conclude:

- grade the samples as contaminated-failure until a clean ordinary-browser oracle exists
- do not treat automation hand-slide failure as proof the trajectory family is wrong
- collect or request a clean-success sample before major track rewrites
- environment risk and observer effect are first-class surfaces

## Task 9J: Reject code needs localization before track search

Prompt:

```text
Our packets decrypt, checksums pass, sidecars return HTTP 200, and final verify still returns a short reject code. The team is generating hundreds of synthetic tracks.
```

Expected route:

- `references/verifier-error-localization-playbook.md`
- `references/verifier-replay-playbook.md`

Must conclude:

- run structure, sidecar, consistency, and timeline ablations before answer or track search
- build a task-local error map; do not import another vendor code table as doctrine
- packet validity is not transcript consistency
- stop at the first surface that controllably reproduces the reject family

## Task 9K: Verifier accepted, business still challenged

Prompt:

```text
Final verify returns the platform accepted semantic, but re-fetching the original document still shows the challenge shell. The collector is being packaged as done.
```

Expected route:

- `references/verifier-replay-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- verifier success is intermediate
- prove first downstream consumer packaging on the same round
- define business-pass by content fingerprint, not only status code
- do not package until the consumer gate passes or a true external blocker is named

## Task 9L: Exit reputation collapses after consecutive rejects

Prompt:

```text
Protocol replay looked better for a while, then every attempt on the same exit started failing, including a later ordinary-browser hand slide. The engineer wants more track mutations.
```

Expected route:

- `references/positive-sample-hygiene-playbook.md`
- `references/verifier-error-localization-playbook.md`
- `references/doctrine-index.md`

Must conclude:

- environment risk is its own failure surface
- consecutive rejects can poison later human samples on the same exit
- change environment intentionally and re-grade samples before more algorithm churn
- keep protocol and environment conclusions separate in the report

## Task 10: GraphQL contract, not REST


Prompt:

```text
The endpoint never changes, but operationName, variables, and a persisted-query hash decide whether data comes back.
```

Expected route:

- `references/structured-transport-playbook.md`

Must conclude:

- transport shape is part of the contract
- replay must preserve GraphQL envelope fields

## Task 11: WebSocket business stream

Prompt:

```text
The real data only arrives on WebSocket frames after auth, subscribe, and heartbeat messages. Recover a local client.
```

Expected route:

- `references/structured-transport-playbook.md`

Must conclude:

- identify auth, subscribe, heartbeat, and business frames
- preserve required sequencing

## Task 12: Response decode chain

Prompt:

```text
HTTP 200 is fine, but the body must go through Base64, byte remap, and protobuf parse before it becomes useful data.
```

Expected route:

- `references/response-decode-playbook.md`

Must conclude:

- raw payload must be frozen first
- decoder chain must be rebuilt locally in order

## Task 12A: Exact body bytes matter more than semantic field equivalence

Prompt:

```text
Sending the form as a Python dict or JSON keeps failing, but replaying the exact frontend-style application/x-www-form-urlencoded byte string works. Recover the collector shape.
```

Expected route:

- `references/transport-wrapper-playbook.md`
- `references/troubleshooting-playbook.md`

Must conclude:

- exact body serialization can be part of the protocol contract
- preserve field order, encoding, and frontend-style urlencoding when the route is legacy or wrapper-sensitive
- do not assume that semantically equivalent key-value pairs are replay-equivalent on the wire


## Task 12B: HTTP 200 is not async export create success

Prompt:

```text
My export create endpoint returns HTTP 200 and a vague success flag, but the history list does not gain a new task id. A later poll still finds an old successful export. Build the protocol acceptance rules.
```

Expected route:

- `references/async-export-job-playbook.md`
- `references/anti-patterns-playbook.md`
- `references/pattern-atlas.md`

Must conclude:

- HTTP 200 is not create success
- snapshot task ids before create and require a new or create-returned id
- match filters and field set before accepting the task

## Task 12C: Do not reuse pre-create historical export tasks

Prompt:

```text
Polling grabs the newest successful history row. The dates are wrong and the file has fewer columns than I requested. How should task selection work?
```

Expected route:

- `references/async-export-job-playbook.md`
- `references/anti-patterns-playbook.md`

Must conclude:

- never select by newest row alone
- isolate with create-returned id or post-create new ids
- require condition and field-set match; fail closed on historical pollution

## Task 12D: Field-count gate blocks incomplete exports

Prompt:

```text
The downloaded CSV opens fine, but it has fewer columns than the custom field array I sent on create. Should I still upsert?
```

Expected route:

- `references/async-export-job-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- compare requested field count to downloaded columns
- fail closed before persistence
- treat thinner files as create or task-isolation bugs, not as partial success

## Task 13: Environment mismatch

Prompt:

```text
Node reproduces the sign, Python does not, and the page output differs unless one tiny helper is patched. Decide the smallest acceptable delivery shape.
```

Expected route:

- `references/env-diff-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- mismatch is evidence
- choose the smallest local patch surface
- a tiny local JS or Node helper is acceptable when Python parity is still unverified, but browser-backed replay is not

## Task 13A: Instance hook is bypassed

Prompt:

```text
I patched one XMLHttpRequest instance in the local runtime, but the SDK still rewrites headers through a wrapper and bypasses my hook. Recover the collector shape.
```

Expected route:

- `references/hook-techniques.md`
- `references/environment-patch-playbook.md`

Must conclude:

- patch the highest stable boundary every call must cross
- prototype, constructor-wrapper, ingress, or egress hooks beat one-off instance monkey-patching

## Task 13B: Async bootstrap can collapse into injected state

Prompt:

```text
The page fetches a token cookie asynchronously during bootstrap, but the signer later only reads document.cookie and local storage. My host bridge is synchronous. Recover the delivery shape.
```

Expected route:

- `references/embedded-browser-runtime-playbook.md`
- `references/cookie-provenance-playbook.md`

Must conclude:

- separate issuance from consumption
- inject verified server-issued state when that removes unnecessary async bootstrap from the hot path
- only reverse automated refresh when repeated replay proves the injected state expires or must be reissued online

## Task 13C: Injected state does not close a native-surface gap

Prompt:

```text
The local helper still emits a much shorter verifier blob than the browser. Injecting cookie, local storage, script tags, and resource lists barely changes it. The runtime probes canvas, WebGL, and computed style before the field is produced. Recover the delivery shape.
```

Expected route:

- `references/environment-patch-playbook.md`
- `references/embedded-browser-runtime-playbook.md`

Must conclude:

- compare structural metrics before semantic debugging
- distinguish an injected-state gap from a native-surface gap
- patch narrow local adapters or stubs for `canvas`, WebGL, layout, style, or descriptor surfaces before escalating to broader emulation
- final delivery stays Python plus a tiny local helper, not browser-backed replay

## Task 13C1: Lifecycle semantics beat name presence

Prompt:

```text
The local helper already exposes document.all and iframe.contentWindow, but the token still diverges. In the page, document.all.length changes when an element is attached, and iframe.contentWindow exists only while the iframe stays attached. Recover the next rule.
```

Expected route:

- `references/environment-patch-playbook.md`
- `references/embedded-browser-runtime-playbook.md`

Must conclude:

- patch lifecycle semantics, not just global names
- prototype-level boundaries such as appendChild and removeChild beat static placeholders when attachment state drives later probes
- compare fixed-input outputs after each narrow patch before escalating to broader emulation

## Task 13D: iv8 host selected

Prompt:

```text
The embedded-runtime decision is already made and iv8 is the chosen host. I need concrete guidance on when to use page.load versus DOM insertion, how to drive timers, and how to keep live HTTP in Python.
```

Expected route:

- `references/embedded-browser-runtime-playbook.md`
- `references/iv8-runtime-cheatsheet.md`

Must conclude:

- use `page.load` only when lifecycle, scripts, or request hooks matter
- use logical time by default and advance only as far as the evidence requires
- keep live HTTP in Python and treat iv8 as local bootstrap plus artifact extraction only

## Task 13D1: Browser-free path still depends on embedded runtime

Prompt:

```text
Python already owns HTTP, retries, parsing, and persistence, but cookie recovery still calls an embedded runtime on every request. The user explicitly asked me to remove iv8 too. May I declare the collector complete because no browser is involved?
```

Expected route:

- `references/embedded-browser-runtime-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- distinguish browser-free from runtime-free
- an embedded runtime can be an acceptable intermediate local bootstrap stage, but that does not satisfy an explicit runtime-removal goal
- if runtime removal is part of the task, continue shrinking after the first live replay instead of packaging the intermediate state as final completion

## Task 13E: Outer SDK facade fails, inner primitive works

Prompt:

```text
The top-level anti-bot SDK init dies inside an axios adapter in the embedded runtime, but a lower module export still returns the decisive packed blob. Recover the collector shape.
```

Expected route:

- `references/challenge-artifact-harvest-playbook.md`
- `references/embedded-browser-runtime-playbook.md`

Must conclude:

- do not discard the whole SDK path because outer orchestration failed
- bypass transport or telemetry glue and call the lower serializer, packer, signer, or export directly
- keep the final split Python-first, with the local runtime limited to the surviving inner primitive

## Task 13E1: Custom VM visible, but outer boundary comes first

Prompt:

```text
The target wraps the signer inside a bytecode VM with opcode tables and a dispatch loop. I am tempted to instrument opcode handlers and interpreter branches immediately, but I have not yet proven the VM entry inputs, wrapper return, or request egress. Decide the next move.
```

Expected route:

- `references/jsvmp-analysis-playbook.md`
- `references/environment-patch-playbook.md`

Must conclude:

- map public VM inputs, outputs, wrapper returns, state writes, or request egress before touching interpreter internals
- if output drift still looks host-semantic, patch the host surface before instrumenting opcode handlers
- avoid devirtualization or interpreter surgery until the outer boundary is proven insufficient

## Task 13E2: Outer boundary is insufficient, stable stage dispatcher remains

Prompt:

```text
I proved the custom VM's public inputs, wrapper return, and final request slot, but the Python port still diverges somewhere inside a stable mode dispatcher. I want to log every opcode and branch next. Choose the smallest useful observation boundary.
```

Expected route:

- `references/jsvmp-analysis-playbook.md`
- `references/opaque-runtime-profile-playbook.md`
- `scripts/transform_trace_diff.py`

Must conclude:

- capture ordered mode or transform inputs and outputs at the stable dispatcher before tracing individual opcodes
- freeze one complete clean run with active asset and runtime hashes
- compare clean and instrumented artifacts for observer effects
- port and repair the first divergent stage instead of compensating in later output segments

## Task 13F: Callback says success, value is still empty

Prompt:

```text
The SDK init callback reports success, but the token field in that callback is empty. A later local response or state write carries the real value. Decide the recovery rule.
```

Expected route:

- `references/embedded-browser-runtime-playbook.md`
- `references/challenge-artifact-harvest-playbook.md`

Must conclude:

- do not preserve fragile callback choreography when the decisive value has a more authoritative writer
- follow the response or state write that actually materializes the token
- keep the final split Python-first, with the local runtime limited to recovering the decisive artifact

## Task 13G: Hooked transport auto-signs one synthetic request

Prompt:

```text
The page loads a heavy security SDK. When I send one minimal request through the same in-page or host-runtime fetch primitive, the outgoing URL suddenly gains signer params and the headers gain extra anti-bot material. Decide the recovery rule.
```

Expected route:

- `references/challenge-artifact-harvest-playbook.md`
- `references/embedded-browser-runtime-playbook.md`

Must conclude:

- prove the signer injection boundary with one minimal synthetic request before reimplementing the whole signer
- separate business payload construction from signer generation once the hook boundary is understood
- final delivery must still avoid browser-backed replay as the handoff

## Task 13H: Runtime loads, decisive artifact is still empty

Prompt:

```text
The local runtime no longer throws, but the decisive signed field stays empty. I injected the capture hook before the target bundle, and the bundle later replaces that request helper with its own polyfill. Recover the next rule.
```

Expected route:

- `references/environment-patch-playbook.md`
- `references/hook-techniques.md`

Must conclude:

- load success is only a milestone, not proof that the helper works
- verify the decisive artifact inside the same patched environment that will actually ship
- treat env surfaces, polyfills, hooks, init, and trigger order as part of the contract
- move the hook after the bundle replacement or up to a higher stable boundary

## Task 13H1: Helper loads, replay still fails

Prompt:

```text
The local helper now loads and throws fewer errors after I patched globals, and its cookie output looks more browser-shaped. The real request still returns the gate page unless I preserve one fresh captured chain. Recover the next rule.
```

Expected route:

- `references/troubleshooting-playbook.md`
- `references/workflow-overview.md`

Must conclude:

- load success or reduced error volume is not protocol success
- repeated live replay on the real business request is the authority
- keep the minimal success chain fresh and stable before widening environment patches

## Task 13H2: Local helper integrity failure masquerades as target blocking

Prompt:

```text
After copying a helper project, Node now fails deep inside transitive packages with missing modules or placeholder link files, and the target symptoms look the same as anti-bot rejection. Recover the next rule.
```

Expected route:

- `references/troubleshooting-playbook.md`
- `references/workflow-overview.md`

Must conclude:

- separate helper-runtime integrity failure from target-side protocol failure
- repair broken local symlinks, placeholder package links, missing deps, or path resolution issues before changing reverse hypotheses
- rerun the helper on frozen inputs before reopening target analysis

## Task 13H2A: User-defined honeypot timeout is part of the collector contract

Prompt:

```text
The user says any live request or local helper step over 5 seconds is probably a honeypot. Build the collector shape.
```

Expected route:

- `references/troubleshooting-playbook.md`
- `references/workflow-overview.md`

Must conclude:

- encode the threshold as a hard timeout across live HTTP and local helper stages
- abort immediately on threshold breach instead of retrying it away
- report the enforced threshold in the final handoff

## Task 13I: Missing names are patched, object contract still diverges

Prompt:

```text
After patching the obvious globals, the local bundle stops throwing, but the emitted blob is still much shorter than the browser sample and the code branches on ownKeys, getOwnPropertyDescriptor, instanceof, constructor checks, and Function.prototype.toString. Recover the next rule.
```

Expected route:

- `references/environment-patch-playbook.md`
- `references/embedded-browser-runtime-playbook.md`

Must conclude:

- distinguish a missing-name gap from a host-object contract gap
- prove descriptors, prototype chains, constructor identity, enumeration, `instanceof`, and native-looking function surfaces before adding more globals
- patch the smallest faithful contract instead of widening the whole environment

## Task 13J: Browser-shaped fields survive only as signer inputs

Prompt:

```text
The recovered signer now only needs UA, platform, viewport, and screen-like values to pack them into the payload. I can freeze them from one good sample or config file, but I am tempted to keep an embedded runtime alive to reread them on every request. Decide the final collector shape.
```

Expected route:

- `references/delivery-gate-playbook.md`
- `references/workflow-overview.md`

Must conclude:

- distinguish declared host-like inputs from live runtime dependency
- keep those values as explicit config or sample-derived parameters when the signer only consumes them as data fields
- prefer a pure Python collector over a persistent runtime when no live host semantics are still needed

## Task 13K: Deterministic trace replay is not the production operating mode

Prompt:

```text
I can match the captured signer byte-for-byte only when I freeze timestamp and random bytes, but real traffic needs fresh values. Decide how to validate and ship the collector.
```

Expected route:

- `references/crypto-patterns.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- keep one deterministic replay mode for byte-level proof
- keep a separate live-generation mode for real traffic
- do not mistake exact trace matching mode for the only acceptable production path once live replay succeeds

## Task 13K1: Successful runtime profiles cannot be spliced

Prompt:

```text
Several complete captured runtime profiles each reproduce an accepted packed artifact. Mixing the prefix, environment block, opaque gap, and tail from different successful profiles fails, so I plan to keep randomizing individual segments until one combination passes.
```

Expected route:

- `references/opaque-runtime-profile-playbook.md`

Must conclude:

- treat each complete captured run as one atomic profile until independence is proven
- preserve correlated and opaque blocks together instead of guessing segment semantics
- use controlled splice or tamper attempts as negative evidence, not as production randomization
- randomize only writers and variability demonstrated by repeated complete captures

## Task 13K2: Local transforms still depend on captured runtime profiles

Prompt:

```text
My pure-Python transforms match every captured stage and final byte, but they still require a complete environment profile captured from a runtime, and I cannot mint that profile from fresh explicit inputs. Can I report fully algorithmic generation because no browser runs during requests?
```

Expected route:

- `references/opaque-runtime-profile-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- report the path as snapshot-driven generation rather than fully algorithmic
- distinguish browser-free and runtime-free execution from capture independence
- prove profile freshness, session scope, route scope, and upgrade behavior
- keep profile provenance and the remaining writer gap explicit in the delivery record

## Task 13K3: High artifact-pool acceptance is not generation proof

Prompt:

```text
A large one-shot pool of previously accepted final artifacts gives a high live acceptance rate, but the collector cannot succeed with the pool removed. The current report also combines connection errors with target rejection. Decide whether the signer is complete.
```

Expected route:

- `references/opaque-runtime-profile-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- classify the result as pool-backed replay, not recovered generation
- require a no-pool test before claiming the writer or signer is solved
- keep pool acceptance, locally generated acceptance, target rejection, and transport exceptions as separate statistics
- record provenance, freshness, scope, exhaustion, and reuse policy if the user accepts a bounded fallback

## Task 13L: Pure helper still imports a runtime-backed predecessor

Prompt:

```text
I rewrote the signer in Python, but the easiest way to reuse constants is importing them from an older embedded-runtime helper whose module import still patches globals and reads cookies. Decide the delivery rule.
```

Expected route:

- `references/delivery-gate-playbook.md`

Must conclude:

- reject runtime-backed import contamination even when the top-level API looks pure
- extract only the required constants and transforms into a self-contained helper
- final delivery must not depend on import side effects from a browser or host-runtime script

## Task 13M: Quiet hook is not whole-transport proof

Prompt:

```text
I hooked fetch and saw nothing, so I assumed the page was not making a live request from JavaScript. Later the same action turns out to travel through an alternate wrapper and a different request primitive. Recover the debugging rule.
```

Expected route:

- `references/hook-techniques.md`
- `references/tool-playbook.md`

Must conclude:

- a hook miss is channel-local evidence, not proof that all request paths are inactive
- rule out sibling transports, wrappers, workers, or message relays before declaring a field or request absent
- bind hook captures to request context so alternate paths can be compared cleanly

## Task 13N: Console probe misses a page-owned helper

Prompt:

```text
In the console my probe says the helper is undefined and the hook never fires, but the page later uses that helper through its own world successfully. Recover the next rule.
```

Expected route:

- `references/tool-playbook.md`
- `references/hook-techniques.md`

Must conclude:

- console or isolated-world probes can miss page-owned wrappers, constructors, or globals
- repeat the proof in the page-owned world before abandoning that boundary
- keep the injected hook narrow and behavior-preserving

## Task 13O: Egress cookie header beats stored cookie state

Prompt:

```text
`document.cookie` and the client jar now look right, but replay still fails. The local runtime egress log shows a different outbound Cookie header and one wrapper-mutated request header. Recover the next rule.
```

Expected route:

- `references/embedded-browser-runtime-playbook.md`
- `references/cookie-provenance-playbook.md`
- `references/challenge-artifact-harvest-playbook.md`

Must conclude:

- stored cookie state and the outbound `Cookie` header are not interchangeable evidence
- when runtime egress is available, use the wire-shaped request record as replay authority
- keep the runtime local and let Python replay the captured final header set

## Task 14: Delivery-gate rejection

Prompt:

```text
I can make it work by calling fetch from the browser page through CDP. Ship that as the final collector.
```

Expected route:

- `references/delivery-gate-playbook.md`

Must conclude:

- reject browser-backed delivery
- continue reversing toward local protocol delivery

## Task 15: Public page with bootstrap envelope

Prompt:

```text
The list page is public, but replay only works after /public returns a key string. The real request posts {"param":"..."} with compact-JSON sign, timestamp injection, and encrypted wrapping. Build a Python collector for 10 pages.
```

Expected route:

- `references/public-bootstrap-envelope-playbook.md`
- `references/transport-wrapper-playbook.md`

Must conclude:

- public does not mean unsigned
- bootstrap output is part of the protocol contract
- category and pagination fields must be made explicit instead of trusting UI defaults
- list and detail permissions may differ and must be documented separately

## Task 15A: Challenge-generated cookie and packet family

Prompt:

```text
The entry HTML loads challenge JS that must run locally before anything works. After that, a derived cookie and storage state appear. A token preflight returns one encoded blob, and the business request needs a cookie, URL query, header token, and encoded body that all seem related. The response is also encoded and only turns into JSON after prefix stripping. Build the collector shape.
```

Expected route:

- `references/challenge-state-envelope-playbook.md`
- `references/cookie-provenance-playbook.md`
- `references/public-bootstrap-envelope-playbook.md`

Must conclude:

- challenge output is protocol state, not decoration
- packet framing and inner crypto must be separated
- URL query, body, response, and cookie may belong to one shared envelope family with field-specific variants
- entry HTML, initial cookies, generated state, preflight token, and replay request should stay on one session chain unless reuse is separately proven
- final delivery must model `entry -> local challenge/bootstrap -> token preflight -> business request -> local response decode`

## Task 15A1: Business response returns the refresh contract

Prompt:

```text
The business API returns HTTP 200 with an application challenge code plus seed, timestamp, and name fields. After I derive one replay token locally, merge it with those refreshed seed fields, and retry the same URL family, the request succeeds. The stored jar looks right, but failures continue until the exact outbound Cookie header matches the runtime. Recover the collector shape.
```

Expected route:

- `references/challenge-state-envelope-playbook.md`
- `references/cookie-provenance-playbook.md`
- `references/environment-patch-playbook.md`

Must conclude:

- treat the application challenge payload as a response-side refresh contract, not a generic error
- retry the same business route after local refresh before hunting alternate endpoints
- update server-issued seed fields and locally derived replay fields as one bundle on one session chain
- compare the exact outbound `Cookie` header against the stored jar when replay gaps remain
- if a local helper still depends on original site JS, keep it narrow, pinned, and fixed-input verified

## Task 15AA: Structurally fresh bootstrap artifacts still fail when spliced across sessions

Prompt:

```text
I captured first-hop HTML and seed cookies from one session, but I am reusing a preflight token and generated cookie from a neighboring session because the lengths, prefixes, and field names still match. Recover the collector shape.
```

Expected route:

- `references/challenge-state-envelope-playbook.md`
- `references/cookie-provenance-playbook.md`

Must conclude:

- keep entry HTML, initial cookies, generated state, preflight token, signer params, and replay on one session chain until reuse is explicitly proven
- structural freshness alone does not prove cross-session compatibility
- only declare an artifact reusable across sessions after replay evidence says so

## Task 15AA1: Offline patching starts before one fresh replay is proven

Prompt:

```text
I have not yet proven one fresh single-page business replay, but I already started shrinking the embedded runtime and generalizing pagination because the offline helper looks close. Recover the next rule.
```

Expected route:

- `references/challenge-state-envelope-playbook.md`
- `references/workflow-overview.md`

Must conclude:

- prove one fresh minimal live replay on one session chain before runtime shrink or pagination scaling
- do not leave the fresh challenge chain for offline patching too early
- only generalize reuse or pagination after the minimal success path is stable

## Task 15AB: Linked bootstrap assets fetched out of band fork the chain

Prompt:

```text
I saved the entry HTML from one session, but later downloaded the linked runner script with a fresh client because the URL looked static. The local runtime still emits a cookie-shaped value, yet business replay fails. Recover the collector shape.
```

Expected route:

- `references/challenge-state-envelope-playbook.md`
- `references/embedded-browser-runtime-playbook.md`
- `references/cookie-provenance-playbook.md`

Must conclude:

- linked bootstrap assets belong to the same session chain as the entry response that discovered them
- reacquire runner scripts or related assets under the same session, effective origin, and relevant headers before treating them as interchangeable
- structural similarity of the asset URL or cookie shape does not prove detached downloads are safe

## Task 15B: Pagination route pivot and raw pager source

Prompt:

```text
Pages 1 to 5 replay from /list-1.html to /list-5.html, but page 6 fails. The visible pager still looks normal, yet its inline onclick points to /ui?page=6 and the DOM getter turns &currentPage into garbage. Recover the collector shape.
```

Expected route:

- `references/pagination-route-pivot-playbook.md`
- `references/page-specific-exception-playbook.md` when the pivot might be narrow

Must conclude:

- pagination is part of the protocol contract, not filename arithmetic
- the collector should follow the live next-page target instead of extrapolating the first-page URL family
- raw pager source may be safer than a DOM-decoded attribute when markup repair mutates the route
- final delivery stays browser-free

## Task 15BA: Request-shaped artifact must regenerate across pages

Prompt:

```text
Page 1 works after local bootstrap, but later pages fail when I reuse the first captured signed suffix and Cookie header. The runtime recomputes them whenever page number, keyword, timestamp, referer, or body changes. Recover the collector shape.
```

Expected route:

- `references/embedded-browser-runtime-playbook.md`
- `references/challenge-artifact-harvest-playbook.md`

Must conclude:

- treat signed suffixes, headers, tokens, and cookie headers as request-shaped artifacts until invariance is proven
- regenerate them inside the live request loop whenever page, keyword, referer, timestamp, or body changes
- one successful first-page sample does not prove cross-page reuse

## Task 15C: Public shell, empty hydration, split signer scopes

Prompt:

```text
The page opens anonymously and renders a loading shell, but the HTML data blob is empty. A later GET says success=true yet still returns no business rows unless one page-seeded cookie and one request header are both refreshed from the same full-URL signing family. Reusing logged-in cookies makes the behavior less stable. Build the collector shape.
```

Expected route:

- `references/public-bootstrap-envelope-playbook.md`
- `references/cookie-provenance-playbook.md`
- `references/transport-wrapper-playbook.md`

Must conclude:

- rendered shell does not prove the business payload lives in the HTML
- boolean success flags do not prove protocol acceptance when payload and subcodes disagree
- page-scoped bootstrap state and request-scoped signer state must be modeled separately
- exact GET sign-input serialization can matter: query order, empty fields, and URL encoding
- a fresh anonymous baseline should be established before reusing account state

## Task 15D: Bootstrap config, wrapper framing, and perception surface

Prompt:

```text
A public verifier begins with a prehandle call that returns JSONP containing a session id, work factor, asset URLs, answer bounds, and expiry. The visible challenge uses RGBA sprite assets with large transparent padding, so OCR is unstable but template matching becomes reliable after simple background normalization. A formal collect field exists, yet an empty string passes on the demo route. Recover the collector shape.
```

Expected route:

- `references/verifier-replay-playbook.md`
- `references/public-bootstrap-envelope-playbook.md`
- `references/transport-wrapper-playbook.md`

Must conclude:

- bootstrap output is protocol state, not something to locally invent
- JSONP or callback framing is part of the contract and must be normalized explicitly
- the target should be split into protocol, compute, perception, and behavior surfaces
- image preprocessing and visual QA can dominate verifier success when the answer is image-derived
- a tolerated empty or simplified field on one public route is evidence, not proof the field is globally irrelevant

## Task 15E: Server-looking field is locally minted filler

Prompt:

```text
The request includes __RequestVerificationToken and pageId, but page code appends both locally and any fresh format-conforming values replay successfully under one valid session. Recover the collector shape.
```

Expected route:

- `references/public-bootstrap-envelope-playbook.md`
- `references/cookie-provenance-playbook.md`

Must conclude:

- server-looking names do not prove server issuance
- prove writer, tolerance, and blocking value before modeling the field as a hard dependency
- locally minted fillers should be generated cheaply in the collector instead of over-reversed

## Task 15F: Human detail page is only a shell for a sibling API

Prompt:

```text
Search results link to /detail/index.html?id=..., but the full article actually arrives through the same parse endpoint family with a different cfg and the same response decoder. Recover the collector shape.
```

Expected route:

- `references/decoy-and-real-request-playbook.md`
- `references/public-bootstrap-envelope-playbook.md`

Must conclude:

- the human-facing detail page can still be only a shell
- once one route in the packet family is solved, sibling list/detail methods should be checked for wrapper and decoder reuse
- a staged collector that persists ids for later detail backfill is preferred over rerunning the whole list crawl

## Task 16: Stateful encrypted stream

Prompt:

```text
The target upgrades into a long-lived WebSocket after pairing. Early frames return a ref, public key, and client ID. Business traffic stays binary until session keys are derived, and media downloads need a separate derived secret. Recover a local client.
```

Expected route:

- `references/structured-transport-playbook.md`
- `references/stateful-stream-e2ee-playbook.md`
- `references/response-decode-playbook.md`

Must conclude:

- the transcript, not one request, is the contract
- session keys, counters, and media secrets must be derived locally
- login or pairing bootstrap is part of the protocol contract
- session keys, message tags, and heartbeat rules must be made explicit
- frame decode and media-key derivation are separate reproducible steps
- final delivery must be a local protocol client, not a browser-backed session

## Task 17: Rotating cookie with unclear writer

Prompt:

```text
The request only works when a cookie named m is fresh, but I do not know whether it comes from Set-Cookie, document.cookie, or returned challenge JS. Recover the right protocol path.
```

Expected route:

- `references/cookie-provenance-playbook.md`
- `references/server-js-cookie-bootstrap-playbook.md` when returned JS is involved

Must conclude:

- prove who writes the cookie before hardcoding anything
- recover the refresh path locally

## Task 17A: Fresh session bootstrap still lacks business admission

Prompt:

```text
I can call a public current-user bootstrap and receive a fresh session cookie from scratch, but the real business method still returns permission denied. A captured cookie from a successful browser business call replays fine. Recover the right protocol path.
```

Expected route:

- `references/cookie-provenance-playbook.md`
- `references/session-contract-playbook.md`

Must conclude:

- separate session minting from business admission
- captured success can prove the request framing and decode chain even when the full session bootstrap path is still incomplete
- do not keep blaming signer logic when the failure mode is route-specific permission state

## Task 17B: Error ladder shows progress

Prompt:

```text
At first the route returns an anti-bot challenge code. After adding one missing header it changes to a refresh-page code. After restoring the JS-set cookies it finally succeeds. Recover the debugging rule this target belongs to.
```

Expected route:

- `references/troubleshooting-playbook.md`
- `references/cookie-provenance-playbook.md`

Must conclude:

- changing subcodes are progress markers, not unrelated noise
- each new code should update the missing-gate hypothesis
- do not restart signer analysis from scratch when the ladder shows that a different gate is now exposed

## Task 17C: Auth grant exists, business session does not

Prompt:

```text
The login response now returns a grant ticket, redirect handle, and a few follow-up URLs, but the protected backend still redirects to login until extra exchanges run. Recover the next step.
```

Expected route:

- `references/troubleshooting-playbook.md`
- `references/session-contract-playbook.md`

Must conclude:

- separate login acceptance from session materialization on the target business domain
- capture and replay the post-auth callback or exchange chain before changing the signer again
- prove which follow-up step actually creates the usable session

## Task 17D: One session, many mutable business contexts

Prompt:

```text
One authenticated session can switch the active tenant or shop by changing one context field, while the main session cookie stays the same. Decide whether that single session is safe for parallel collection across multiple contexts.
```

Expected route:

- `references/session-contract-playbook.md`

Must conclude:

- distinguish identity session from active business context
- do not treat per-context cookie jars as independent sessions when the active context is single-active-per-session
- use one independent session per concurrent context, or serialize context switches, until proof says otherwise

## Task 17E: Silent JS cookie hook is not full provenance proof

Prompt:

```text
I hooked document.cookie and saw no writes, so I assumed the rotating cookie must be irrelevant. But the cookie still changes after the request flow completes. Recover the right provenance rule.
```

Expected route:

- `references/cookie-provenance-playbook.md`
- `references/hook-techniques.md`

Must conclude:

- a silent `document.cookie` hook only clears that JS setter boundary during the observed window
- still check `Set-Cookie`, returned JS, redirects, workers, or wrapper side effects
- prove the real writer and refresh path before caching or discarding the cookie

## Task 17F: Session-looking and fingerprint-looking cookies are locally minted

Prompt:

```text
The first response is 412 and links a config JS. That script decrypts into a config blob, then page code mints two cookies locally: one UUID-like session with an inserted checksum segment and one fingerprint hash built from compact JSON plus a short digest suffix. Neither comes from Set-Cookie, but replay fails unless their structure is exact. Recover the collector shape.
```

Expected route:

- `references/cookie-provenance-playbook.md`
- `references/challenge-state-envelope-playbook.md`
- `references/crypto-patterns.md`

Must conclude:

- session-looking or fingerprint-looking cookies do not prove server issuance
- bootstrap config JS can be part of the protocol contract and may normalize key, iv, or compatibility constants before use
- exact structural transforms matter: compact JSON order, digest chaining, inserted checksum or prefix segments, and field-specific formatting
- keep one deterministic cross-runtime parity vector before trusting a Python port

## Task 18: Hooks make the site fail

Prompt:

```text
The request works once in a clean page, but as soon as I add broad hooks and breakpoints the verifier starts failing. Decide the next move.
```

Expected route:

- `references/startup-triage-playbook.md`
- `references/troubleshooting-playbook.md`

Must conclude:

- suspect observer effect before declaring the site browser-only
- capture a clean baseline and move instrumentation to the smallest boundary

## Task 18A: Runtime already emits the final body

Prompt:

```text
The outer login or anti-bot SDK is messy, but once one local bootstrap step succeeds the runtime self-issues fetch with the exact encrypted form body and decisive headers. Rebuilding the full crypto chain offline is still failing byte-for-byte. Decide the collector shape.
```

Expected route:

- `references/challenge-artifact-harvest-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- intercept the nearest stable egress that already yields the final replayable artifact
- hand the harvested body and headers back to Python for the real HTTP replay
- do not insist on full inner-crypto reimplementation before proving whether intercept-and-forward already satisfies delivery

## Task 18AA: Redirect target recovered before full runtime parity

Prompt:

```text
The local challenge runtime still reports a later "navigation not implemented" style notice, but before that it already emits the final redirect URL or same-route replay URL that makes the downstream Python request succeed. Decide whether the collector is blocked.
```

Expected route:

- `references/challenge-artifact-harvest-playbook.md`
- `references/embedded-browser-runtime-playbook.md`

Must conclude:

- a navigation target or redirect URL can be the decisive harvested artifact
- later post-artifact runtime notices do not invalidate the recovery by themselves
- downstream Python replay, not runtime quietness, is the acceptance authority
- stop widening DOM parity once the recovered URL is enough for repeated live replay

## Task 18B: Async side channel needs a baseline first

Prompt:

```text
The trigger request only starts a flow. The usable code, token, or approval link arrives later through mail, SMS, webhook, or another delayed callback, and I keep missing which artifact belongs to which attempt. Decide the next move.
```

Expected route:

- `references/troubleshooting-playbook.md`

Must conclude:

- establish the observation baseline before firing the trigger
- capture the pre-trigger cursor or polling state and then diff the post-trigger arrivals
- treat timing and side-channel observation as part of the protocol workflow, not disposable operational noise

## Task 18C: Rate limit masquerades as a field error

Prompt:

```text
The exact same request alternates between success, anti-abuse responses, and user-facing password or field errors depending on how quickly I retry it. Decide the debugging rule.
```

Expected route:

- `references/troubleshooting-playbook.md`

Must conclude:

- test pacing and cooldown before rewriting fields that already matched
- recognize that abuse controls can disguise themselves as credential or validation errors
- prefer session reuse, refresh, or slower retry cadence over aggressive relogin loops

## Task 18D: Stable scaffolding should not be overwritten by volatile captures

Prompt:

```text
The project already has stable helper wiring and one user-maintained bootstrap fixture. A new run captured fresh HTML, challenge scripts, cookies, and runtime output. Decide which artifacts stay stable and which belong in a task-local cache.
```

Expected route:

- `references/workflow-overview.md`
- `references/challenge-state-envelope-playbook.md`

Must conclude:

- keep stable scaffolding and user-maintained fixtures separate from volatile captured artifacts
- store fresh captures and generated runtime blobs in a task-local cache
- do not overwrite manual fixtures by default; generate temporary runners from the fresh cache when needed

## Task 19: Normalize a publishable evidence package

Prompt:

```text
I have a HAR with ordered duplicate headers, redirects, request bodies, cookies, and tokens. I need a reproducible package for comparison and publication without exposing reusable secrets. Prepare the evidence path and proof metadata.
```

Expected route:

- `references/reproducible-evidence-playbook.md`
- `scripts/evidence_normalizer.py`

Must conclude:

- normalize the capture before comparison or publication
- preserve ordered and duplicate headers, body byte length and keyed HMAC-SHA-256, redirects, state writes, and session-chain order in the public-default package
- permit unkeyed source/body SHA-256 only through the explicit local-only `--include-raw-hashes` opt-in, never in a publication package or manifest
- pseudonymize known sensitive fields and recognizable sensitive values with one task-local HMAC key while keeping raw secrets in an ignored local store
- emit evidence proof-manifest schema v2 without inventing session, helper, or replay claims, and require publication review
- record the redacted evidence package path and SHA-256 plus the proof manifest path and its post-write SHA-256

## Task 19A: Find the first divergence across matching final requests

Prompt:

```text
A successful chain and a failing chain have the same final request body hash, but an earlier redirect, Set-Cookie response, sidecar, counter, or storage write may differ. Identify the smallest next proof without printing raw changed values.
```

Expected route:

- `references/reproducible-evidence-playbook.md`
- `scripts/transcript_diff.py`

Must conclude:

- compare the complete ordered chains instead of only the final request
- report the first divergence by step, structural path, and difference kind using fingerprints rather than raw values
- trace the divergent state's writer and first downstream consumer before tuning later fields
- do not sort ordered header lists, collapse duplicate headers, or splice neighboring session chains to hide the difference

## Task 19B: Require an offline oracle and negative control

Prompt:

```text
A skill revision claims it handles exact request bytes, same-session bootstrap state, layered response decoding, and pagination route pivots. I want a deterministic offline check that catches plausible shortcuts before live replay.
```

Expected route:

- `references/reproducible-evidence-playbook.md`
- `scripts/practice_lab.py`

Must conclude:

- treat the skill-owned loopback lab as deterministic fixture evaluation, not a fresh live target that needs browser startup
- exercise the four local protocol cases from a clean run
- require both the positive oracle and the decisive negative control for every claimed case
- reject a revision that passes only a permissive positive path or helper-load check
- use the practice lab as deterministic preflight evidence, not as a replacement for repeated live business acceptance

## Task 20: Multi-stage sidecars cannot stop after the first post

Prompt:

```text
The clean browser trace emits three ordered sidecar POSTs with different body sizes before the business request works. My local runtime emits one non-empty POST, gets HTTP 200, and then I stop the event loop and submit the business request, which fails. Decide the next move.
```

Expected route:

- `references/verifier-replay-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- one sidecar HTTP 200 or token-shaped output is not downstream acceptance
- compare sidecar count, order, body-size sequence, content type, response state writes, and next-request state
- inspect lifecycle, timers, input settle, response-cookie mirroring, or missing sidecar branches before rewriting the algorithm
- prove the downstream business consumer before calling the collector complete

## Task 20A: Mixed identity tuple causes later route failure

Prompt:

```text
The root page passes with an impersonated TLS client, but the route-local sidecar and business request fail. The request headers claim one browser major, Client Hints claim another, and the local runtime navigator profile was copied from a third environment.
```

Expected route:

- `references/transport-pre-gate-playbook.md`
- `references/iv8-runtime-cheatsheet.md`

Must conclude:

- keep transport impersonation, User-Agent, Client Hints, runtime navigator identity, locale, timezone, and profile fields coherent
- do not mix headers, TLS profile, and runtime fingerprint data from unrelated browser families unless live evidence proves tolerance
- a root-page pass does not prove the route, sidecar, or business branch accepts the same incoherent tuple
- continue application-layer reversing only after transport and identity admission are clean enough

## Task 20B: Foreign high-entropy fingerprint cache is not a runtime input

Prompt:

```text
The local host runtime only succeeds on the original author's machine. A copied cache includes canvas data URLs, WebGL renderer strings, system colors, screen metrics, and device fields from that host. Can I keep using those values as production inputs?
```

Expected route:

- `references/iv8-runtime-cheatsheet.md`
- `references/environment-patch-playbook.md`

Must conclude:

- high-entropy host inputs must be captured on the execution host when they are replay-critical
- another machine's canvas, WebGL, system color, font, screen, or device-profile cache is only a comparison fixture by default
- if a captured opaque profile remains in delivery, label it snapshot-driven and report scope and freshness
- patch only the profile surfaces that evidence proves matter

## Task 20C: Local helper bridge must not own arbitrary egress

Prompt:

```text
A local challenge executor runs untrusted page JavaScript and its XHR shim is about to forward any same-origin-looking URL, cookies, Authorization, redirects, and large bodies through Python. Tighten the product boundary.
```

Expected route:

- `references/local-challenge-executor-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- Python owns real HTTP and the helper only emits replayable artifacts or narrow request intent
- build an allowlist from exact URLs discovered by Python on the same session chain
- strip helper-controlled Cookie, Authorization, Proxy-Authorization, Host, Connection, and forwarding headers
- cap method, request count, body and response size, timeout, and redirects
- reject localhost, private networks, file, data, and arbitrary helper-selected hostnames

## Task 20D: Exit-gated access denial is not an algorithm regression

Prompt:

```text
The exact same collector alternates between success and Access Denied depending only on proxy node. On a failing node, a real browser on the same exit also cannot open the business document route. Should I rewrite the signer and form serializer?
```

Expected route:

- `references/troubleshooting-playbook.md`
- `references/transport-pre-gate-playbook.md`

Must conclude:

- classify the condition as `egress-gated` before changing protocol logic
- change exit or wait, then rerun the full chain instead of mutating signer, verifier, CSRF, or form fields first
- if the browser succeeds but protocol fails on the same exit, then compare transport identity coherence, sidecar count, cookie transition, and serialization
- keep prior successful output separate from fresh failure diagnostics

## Task 20E: Sidecar success is not business success

Prompt:

```text
The warm-up and telemetry routes return 200 and the final token length looks realistic, but the downstream business API still returns a challenge shell instead of parseable target data. Can I mark the protocol solved?
```

Expected route:

- `references/delivery-gate-playbook.md`
- `references/verifier-replay-playbook.md`

Must conclude:

- verifier, telemetry, warm-up, or sidecar success is only an intermediate milestone
- final acceptance is the downstream business route returning parseable target data or the requested artifact
- report which sidecar layers passed separately from final business acceptance
- do not package the collector until the failing delivery gate is resolved or a true external blocker is reported

## Task 20F: Final state value without transition order is not provenance

Prompt:

```text
I have the final Cookie header and one token value from a successful request, but I did not record the response Set-Cookie, sidecar writes, redirects, or which next request consumed each update. The copied final state works once and then fails on a fresh chain.
```

Expected route:

- `references/cookie-provenance-playbook.md`
- `references/reproducible-evidence-playbook.md`

Must conclude:

- record the ordered state machine rather than only final cookie or token values
- include request state, response writes, next outbound authority, redirects, sidecars, and final business consumer
- transition order is part of the protocol and can make a correct-looking final value stale
- normalize or diff the ordered evidence chain before designing regeneration

## Task 21: Supplied JavaScript uses the non-executing AST route

Prompt:

```text
I supplied one untrusted minified JavaScript asset and only want structural detection plus conservative readability changes. Do not run the source, evaluate decoder calls, or contact the target. Preserve an auditable fallback if parsing or rewriting fails.
```

Expected route:

- `references/profiles/static-ast/index.md`
- `references/project-artifact-contract.md`

Must conclude:

- classify the work as artifact-only and keep it offline
- parse and inspect the source structurally without `eval`, `Function`, `node:vm`, or target-code execution
- preserve the original, each successful intermediate, hashes, residue metrics, and `lastGoodFile` under the task project
- keep ambiguous family evidence on the generic conservative pipeline instead of guessing a site adapter

## Task 21A: AST parse failure preserves the exact source

Prompt:

```text
The supplied JavaScript is truncated and Babel cannot parse it. I still need a deterministic pipeline report and a final artifact, but no recovery step may execute the file or silently invent a successful rewrite.
```

Expected route:

- `references/profiles/static-ast/index.md`

Must conclude:

- return a failed parse status and bounded error metadata
- retain `00_source.js` as `lastGoodFile`
- write `final.js` as the byte-for-byte source fallback
- keep `targetCodeExecuted` false and do not escalate to dynamic evaluation automatically

## Task 21B: Dynamic rebuild requires a second independent sample

Prompt:

```text
My Python signer matches one captured request exactly, but its input includes a timestamp, random bytes, session state, and ordered serialization. Can I restore live values and ship after changing only the expected output in a copied fixture?
```

Expected route:

- `references/pure-python-rebuild-playbook.md`

Must conclude:

- a copied fixture with only expected output changed is not independent evidence
- capture fixture B from an independent run with at least one decisive input changed
- require both fixtures before restoring live time, randomness, session, or serialization paths
- for a textbook primitive, require one public known-answer vector plus one captured application vector

## Task 21C: CryptoJS cipher hooks remain metadata-only

Prompt:

```text
The page uses CryptoJS.AES.encrypt and decrypt as object methods rather than top-level functions. I need a reversible observation hook, but logs must never include plaintext, passphrases, Key, IV, Cookie, token, or raw ciphertext.
```

Expected route:

- `references/profiles/browser-hook-snippets/index.md`

Must conclude:

- wrap nested AES, DES, TripleDES, and RC4 encrypt/decrypt methods when they exist
- log only bounded method, type, and length metadata
- preserve the original call, return value, `this` binding, and promise or synchronous behavior
- provide `restore()` and refuse raw argument, key, IV, result, or stack logging by default

## Task 21D: gRPC framing needs length and trailer negative controls

Prompt:

```text
I have a grpc-web response with several frames, a compression flag, unknown protobuf fields, and a final trailer frame. One parser assumes every nonzero flag means zlib and reads only the first payload. Define the proof needed before decoding business data.
```

Expected route:

- `references/structured-transport-playbook.md`
- `scripts/grpc_frame_inspector.py`

Must conclude:

- parse every five-byte frame header as flag plus unsigned big-endian length
- resolve compression from `grpc-encoding` or active grpc-web evidence rather than assuming zlib
- distinguish data and trailer frames and preserve unknown fields or raw payload bytes
- reject truncated headers, oversized lengths, and a tampered flag or trailer boundary before accepting decoded business data

## Task 21E: Crypto primitive names do not define wire formats

Prompt:

```text
The client mentions SM2, ECDSA, ECDH, xxHash, and a hybrid envelope. A draft implementation mixes SM2 signature integers with C1C3C2 ciphertext, treats ECDSA DER as raw r||s, and omits the hash seed and byte order. Decide the validation contract.
```

Expected route:

- `references/crypto-patterns.md`

Must conclude:

- distinguish primitive identity from signature, key, ciphertext, and envelope encoding
- record SM2 component order, ECDSA DER versus fixed-width raw form, ECDH point encoding and KDF, and checksum seed, width, and byte order
- verify primitive output separately from KDF, nonce or IV, authenticated data, component ordering, and final framing
- keep keys and captured ciphertext task-local while promoting only secret-free layout and verification rules

## Task 21F: Narrow env runtime contracts stay explicit and bounded

Prompt:

```text
A known local fixture needs linked MessageChannel delivery, both Image load handler styles, one named webpack chunk array, and browser-compatible Latin1 btoa. I do not want a broad browser emulator or a global scan.
```

Expected route:

- `references/profiles/env-patch/index.md`
- `references/profiles/env-patch/references/runtime-contracts.md`

Must conclude:

- use linked asynchronous ports rather than no-op MessageChannel stubs
- dispatch one Image load event to both `onload` and `addEventListener('load', ...)`
- capture bounded chunk and module IDs only from an explicitly evidenced array name, then restore `push`
- verify `btoa("\x00\xffAz") === "AP9Beg=="` and reject code units above `0xff` instead of silently UTF-8 encoding

## Task 21G: One successful job remains an experience candidate

Prompt:

```text
One target taught a useful reverse rule and I want to add it permanently to Spider King. I have only one successful run, no negative control, and my note currently includes the host, Cookie value, and a copied response body.
```

Expected route:

- `references/skill-maintenance.md`
- `references/experience-card-schema.md`

Must conclude:

- keep the one-job lesson in task-local `experience-candidate.json`
- require two independent reproductions, a secret-free fixture hash, positive oracle, negative control, first divergence, and applicability boundary before promotion
- strip target identifiers, cookies, tokens, keys, private responses, and endpoint folklore
- use a promoted card only as a hypothesis accelerator and re-prove one current-target fact

## Task 21H: Specialist handoff cannot widen authority

Prompt:

```text
The current route found a verifier-owned blocker and an installed specialist may help. Prepare the handoff without allowing concurrent same-target browser control, hidden request retries, broader paths, dependency installs, or raw session values.
```

Expected route:

- `references/provider-work-order.md`
- `references/specialist-handoff-contract.md`

Must conclude:

- confirm the specialist in the capability snapshot and name an executable Spider fallback
- park or release current same-target ownership before transferring `TARGET_ACTIVE`
- pass only proven facts, artifact paths and hashes, explicit permissions, remaining budget, unknowns, and one acceptance test
- treat omitted permission as blocked, reference secrets by local path and hash only, and have Spider accept the returned evidence against final delivery gates

## Task 21I: Evidence uses its own completion gate

Prompt:

```text
I supplied one saved request and asked only which field mutates. Do not contact the target and do not write files. Report the proved mutation point and the limits of this offline evidence.
```

Expected route:

- `references/delivery-gate-playbook.md`
- `references/provider-work-order.md`

Must conclude:

- classify the result as artifact-only `evidence`
- require provenance, a bounded claim, redaction, and explicit unproven live behavior
- do not require a live endpoint, repeated replay, proof-manifest file, dependency install, or `main.py`
- do not promote the evidence to local-proof, compact-replay, or collector

## Task 21J: Provider write paths are an enforced allowlist

Prompt:

```text
The work order permits task-cache writes only under one exact fixture directory. A route wants to write another project-local path because it is still inside the project.
```

Expected route:

- `references/provider-work-order.md`
- `references/project-artifact-contract.md`

Must conclude:

- reject `no-write`, unknown write mode, and an empty allowlist
- resolve the destination and require containment under both the project and one inherited `allowedPaths` entry
- reject symlinks, junctions, reparse points, hard-link aliases, skill paths, and OS temp
- require separate path-specific authorization before overwriting stable user files

## Task 21K: Static AST dependencies stay task-local

Prompt:

```text
Run the supplied static AST profile from a clean skill installation. Babel is not installed and task-cache dependency installation is approved, but no task may write into the skill directory.
```

Expected route:

- `references/profiles/static-ast/index.md`
- `references/project-artifact-contract.md`

Must conclude:

- copy the pinned package files, scripts, and tests into an allowed task-local tool directory
- run `npm ci --ignore-scripts` and the profile tests only from that task-local copy
- keep `node_modules` out of stable delivery and evidence packages
- never install dependencies from the skill profile root

## Task 21L: Static validation does not execute candidate code

Prompt:

```text
Validate a candidate Spider King directory that may contain untrusted Python scripts. I did not authorize executing its self-tests.
```

Expected route:

- `references/skill-maintenance.md`
- `scripts/validate_skill.py`

Must conclude:

- default to syntax, structure, routing, and suite validation without subprocess execution
- require explicit `--run-trusted-self-tests` for the trusted current root
- isolate trusted self-tests from user site packages and arbitrary environment secrets
- state that the trusted self-test mode is not an operating-system sandbox

## Task 21M: Browser acquisition roles are capability-aware

Prompt:

```text
A fresh target needs a fingerprint-protected clean baseline, then initiator and source tracing. The current registry also exposes an optional CDP bridge. Must I choose one product route forever, or activate every browser surface at once?
```

Expected route:

- `references/startup-triage-playbook.md`
- `references/tool-playbook.md`

Must conclude:

- classify fingerprint baseline, debugger trace, and CDP bridge as evidence roles selected from the current capability snapshot, not permanent vendor routes
- use only the roles justified by the next proof and record unavailable methods or fallbacks
- transfer `TARGET_ACTIVE` ownership sequentially and never drive the same target through multiple browser families concurrently
- keep every browser or CDP role evidence-only and retain a browser-free Python final path

## Task 21N: The implementation brief is conditional

Prompt:

```text
For one artifact-only decoder I already chose pure Python and asked for implementation now. A different collector still has unresolved pure-Python versus local-JS options, and the next step would install dependencies and perform live replay. Decide when a formal implementation brief is useful.
```

Expected route:

- `references/provider-work-order.md`
- `references/report-templates.md`

Must conclude:

- do not impose a mandatory plan or approval ceremony on bounded evidence, local-proof, or an implementation choice the user already made
- create a compact implementation brief when `compact-replay` or `collector` work has material implementation ambiguity or would widen runtime, dependency, write, or live authority
- record the real endpoint, dynamic fields and writers, evidence, candidate forms, chosen boundary, acceptance test, and unresolved risks
- treat the brief as a decision record; it never grants omitted write, install, execution, account, or egress permission

## Task 21O: Project runtime coherence is explicit

Prompt:

```text
This collector project requires its own .venv. The current shell may be using a global interpreter, Node is somewhere on PATH, and I want the supplied package-lock fingerprint recorded before a helper runs. Diagnose the environment without assuming one workstation path.
```

Expected route:

- `scripts/check_reverse_env.py`
- `references/project-artifact-contract.md`

Must conclude:

- resolve and report the selected project root, interpreter, virtual-environment state, project-local environment coherence, and bounded runtime versions
- fingerprint only explicitly supplied lockfiles and report a path relative to the bound project without reading arbitrary files
- warn by default when the interpreter is outside the project environment, and fail only when the user or project explicitly requires that gate
- never hardcode a drive, profile id, global interpreter ban, or reusable secret into the skill

## Task 21P: Hook timing fallbacks preserve evidence limits

Prompt:

```text
The target page is already initialized, the installed browser tool has no preload helper, and a post-load fetch hook records nothing. Continue without claiming the request or mutation is absent.
```

Expected route:

- `references/tool-playbook.md`
- `references/hook-techniques.md`

Must conclude:

- record preload support and missing optional methods in the capability snapshot instead of fabricating an injection call
- prefer an early supported breakpoint or an explicitly authorized controlled reload when initialization-time evidence is required
- label post-load observation as proving only later activity and keep the clean baseline separate from instrumented runs
- check sibling transports, wrappers, workers, message relays, and the page-owned world before declaring the boundary inactive

## Task 21Q: Collector handoff stays compact and auditable

Prompt:

```text
The browser-free collector is complete. Give me one concise technical handoff that is enough to rerun and audit it without creating a README, plan, notes file, and duplicate reports for the same facts.
```

Expected route:

- `references/report-templates.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- summarize the real endpoint, dynamic field writer and wire slot, session issuance or refresh, and final protocol order
- record fixed-vector and negative-control results, live replay count when claimed, and the downstream business acceptance oracle
- state the Python and helper boundary, browser-free and runtime-free truth, saved artifact paths, hashes, and remaining risks
- redact reusable secrets and keep one canonical compact handoff instead of proliferating duplicate project documents

## Failure signals

Fail the skill revision immediately if it does any of these:

- accepts browser automation as final delivery
- treats every hard target as only a sign-recovery problem
- ignores transport envelopes or decode chains
- asks the user for giant manual bundle review instead of narrowing the target
- returns vague success without replay proof
- routes MCP families from disk presence instead of the mounted tool registry
- opens chrome-devtools and js-reverse target actions in the same parallel batch
- treats environment-provider start, passive capture, or PCAP visibility as collector proof
- keeps MCP browser runtime or page driving inside the final collector path
- invents chrome-devtools plus js-reverse first-pass for out-of-scope APK/app/mini-program primary tasks or pure artifact work
