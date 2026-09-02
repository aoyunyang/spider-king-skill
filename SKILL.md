---
name: spider-king
description: "Pure-web protocol reverse skill: turn hostile browser clients into browser-free Python collectors. Auto-judge intake and tool path from signals: artifact-only first when samples suffice; for a fresh web live-target, collect sequential fingerprint-baseline then debugger-trace evidence (default chrome-devtools then js-reverse; upgrade baseline host to Camoufox/managed profile only on fingerprint pressure); for continuation, reuse the current gate when target and environment are unchanged. Route only mounted web-relevant MCP families. Out of primary scope: APK, native app, and mini-program reverse as the main path. Use for hostile web sign, token, cookie, WebSocket, GraphQL, protobuf, response-decode, browser-fingerprint, WebAssembly, challenge-bootstrap, dynamic-font, or protocol-collector flows."
---

# Spider King

## Mission

Turn hostile web clients into stable protocol collectors.

This is a pure-web protocol-recovery skill, not a browser-automation skill and not an APK/mini-program reverse skill. Use browser tooling only to gather web evidence. Deliver raw HTTP plus narrow local sign, bootstrap, decode, or transport helpers. If the primary target is APK, native app, or mini-program, state out-of-scope instead of inventing a web dual-browser first-pass.

## Non-Negotiables

- Before any tool choice on a fresh task, run the Auto Judge Card in this file and `references/mcp-routing-playbook.md`: decide intake, whether a browser is needed, which baseline host to use, and whether `js-reverse` is required. Do not open tools first and rationalize later.
- Start every fresh web target classified as `live-target` with sequential evidence for both roles before claiming that live web target is understood: `fingerprint-baseline` then `debugger-trace`. Default means are `chrome-devtools` then `js-reverse`. When fingerprint pressure is proved, the baseline host may be Camoufox or another managed profile; debugger-trace still prefers `js-reverse` only after a real handoff and only when a debug attach surface exists. This skill's primary scope is web clients only; APK, native app, and mini-program primary tasks are out of scope and must not invent paired-browser proof as ceremony. If a required role or its available means is missing for a web live-target, report the blocker before claiming the live target is understood.
- Keep browser evidence collection target-serial: at most one tool family may be `TARGET_ACTIVE`, and never place both families in the same parallel tool batch. Apply the handoff gate in `references/tool-playbook.md`; preserve unique unreplayable state with `RETAINED_EXCEPTION` instead of destroying it for cleanup.
- For `compact-replay` and `collector`, deliver a browser-free Python run path. Never use browser automation, Playwright, Selenium, CDP page-driving, page-context fetch, browser profiles, or manual browser state as the final replay path or fallback.
- Prefer pure Python for HTTP, orchestration, parsing, retries, persistence, and output.
- Keep JS or WASM only as a tiny local helper when a verified Python port would currently be riskier. Helpers must not depend on live `window`, `document`, browser storage, page driving, or manual clicks.
- A local bootstrap executor may emulate required host semantics, but Python must own live HTTP. State clearly whether delivery is browser-free only or fully runtime-free.
- Recover one stable business request before pagination, concurrency, submission, or runtime shrinking.
- Back every conclusion with the evidence its declared shape requires. Require repeated live replay only when claiming current live acceptance. Keep raw sensitive values local; redact credentials, tokens, personal data, and cookie values from chat, reports, and version control.
- Never hardcode rotating state before proving its writer, slot, scope, expiry, and refresh path.
- Preserve one session chain for bootstrap-heavy flows until cross-session reuse is proven.
- Stop only when the declared shape passes its capability-specific gate or a real external blocker is proved. Do not label `evidence` or `local-proof` as a collector, and do not disguise incomplete automation as a temporary collector.
- `compact-replay` and `collector` delivery include a PyCharm right-click runnable Python entrypoint, normally project-root `main.py` or `collector/main.py`, with no required terminal arguments. `evidence` and `local-proof` do not require an entrypoint unless the requested artifact is executable code.
- Route only MCP families confirmed available in the current agent tool registry or schema. Source trees on disk are not availability.
- Passive wire stores such as Reqable or HAR may coexist with a browser `TARGET_ACTIVE` owner, but they do not replace web live first-pass evidence and must not become the final run path.
- `compact-replay` and `collector` must remain free of MCP browser runtime, page driving, and profile-bound operation.

For failure-shaped counterexamples, read `references/anti-patterns-playbook.md`. Before packaging a result, apply only the matching capability gate from `references/delivery-gate-playbook.md`.

## Lightweight Dispatch

Use these labels internally to keep the first move small. Do not force a rigid machine header in normal user replies.

| Shape | Deliverable |
|---|---|
| `evidence` | real request, initiator, state source, mutation point, or precise blocker |
| `local-proof` | fixed vectors, decoded sample, restored source, or callable helper without live egress |
| `compact-replay` | one bounded right-click runnable replay for a proved request |
| `collector` | repeatable browser-free Python collector with bounds |

Default to the smallest shape that answers the user. User-provided HAR, packet capture, request text, JS/WASM, cookie/token sample, fixed vector, or existing project artifact starts as `evidence` or `local-proof`; do not open a browser just to satisfy live-target ceremony. A bare URL by itself does not authorize browser navigation, live replay, writes, account/session use, dependency installation, or broad collection.

Route names describe the current capability owner, not the gate family: `evidence-reuse`, `chromium-recon`, `browser-hook`, `static-ast`, `env-patch`, `iv8-local-runtime`, `verifier`, `transport`, `pure-python-rebuild`, or `python-collector`. Run one route until it returns evidence or a named blocker. If two routes look plausible, pick the smaller offline route first and record what proof would justify escalation.

Before any route writes files, sends live egress, executes target-supplied code, uses account/session state, installs dependencies, or changes runtime state, apply the compact contract in `references/provider-work-order.md`.

## Fast Routes and Ownership

Use a focused route when the goal is already narrow. Do not restart full unknown-target discovery for these cases.

| Current goal | Route |
|---|---|
| Paste-ready browser observation Hook at a known boundary | `references/profiles/browser-hook-snippets/index.md` |
| Structured Babel AST restoration of a supplied JS file | `references/profiles/static-ast/index.md` |
| Known entry + invocation + fixed browser output in Node/VM | `references/profiles/env-patch/index.md` |
| Fixed-trace pure-Python signer/decoder rebuild or regression | `references/pure-python-rebuild-playbook.md` |
| Unknown or multi-layer end-to-end collector | Continue Startup Gate + Universal Reverse Loop below |
| Entry/call-chain location only | Dedicated reverse skill when available; else `chrome-devtools` / `js-reverse` initiator evidence |
| Explicit Python + iv8 runtime | iv8 skill when available; if unavailable, report the unmet constraint and use env-patch/local helper only after the user accepts that substitution |
| Confirmed CAPTCHA/TDC or family-owned protocol | Matching specialist skill when available; Spider stays secondary runtime help only |
| Already-captured HAR, Reqable history, or request text to explain or draft replay | `evidence-reuse`; read `references/mcp-routing-playbook.md` before opening browsers |
| Fingerprint or managed profile required before evidence | Auto-judge high fingerprint pressure -> Camoufox/managed host baseline, then attach/`js-reverse` handoff when debug endpoint exists |
| Enough HAR/request/JS/cookie sample and no fresh live proof needed | `artifact-only` / `evidence-reuse`; do not open Camoufox, Chrome, or `js-reverse` for ceremony |

Focused profile rules:

- Browser-hook, static-ast, and env-patch routes may skip the full unknown-target Startup Gate ceremony only for `artifact-only` or already-proved known-boundary work, but still require reversible changes and secret-safe logs. Structure-only static AST detection may begin from the supplied file alone; require fixed samples before behavioral claims or dynamic escalation. If the route needs fresh interaction with a current target, classify it as `live-target` and apply the paired sequential browser rule above.
- If a profile uncovers missing bootstrap, session, transport, decode, or pagination state, exit the profile and return to the Universal Reverse Loop.
- Process artifacts go under the executing project `js_reverse_cache/tasks/<task-id>/` (`task.json`, `network.jsonl`, `runtime-evidence.jsonl`, `handoff.json`, `fixtures/`, `report.md`). Delivery proof remains `analysis/proof_manifest.json` and related analysis files. Never write task secrets into this skill directory. Apply `references/project-artifact-contract.md` before the first save or promotion.

## Auto Route Card

Use this before tool choice. It does not relax any delivery gate.
Full signal tables and host-upgrade rules live in `references/mcp-routing-playbook.md` and `references/startup-triage-playbook.md`.

### Auto Judge Card (signal-driven)

Judge in this order and record the branch before the first target action:

1. **Intake**: enough offline samples and no live acceptance need -> `artifact-only`; bare URL or fresh page/session proof -> web `live-target`; same target/env/goal -> `continuation`; APK/app/mini-program primary -> out of scope.
2. **Browser needed?**: pure offline explain/restore/fixed-vector work -> no browser; need current request/page/wire proof -> baseline host; known-boundary debugger only -> `js-reverse` after attach owner is confirmed.
3. **Baseline host**: default `chrome-devtools`; upgrade to Camoufox/managed host only on fingerprint pressure or clean-baseline failure; never default Camoufox for ordinary low-risk work.
4. **Debugger**: after a candidate business request exists and attach is available, sequential handoff to `js-reverse`; if attach is missing, export artifacts, record `debugger_attach_gap`, and continue offline.
5. **Stop browser early**: once the real request, mutation point, and rebuild path are proved, leave browser MCP and finish in pure Python.

### Default live sequence

```text
capability snapshot
  -> Auto Judge
  -> fingerprint-baseline (chrome-devtools default; Camoufox/managed host only on pressure)
  -> sequential handoff
  -> js-reverse when attach exists
  -> offline rebuild + delivery gate
```


## Startup Gate

Complete and report this gate before deep analysis. Expanded checklists stay in `references/startup-triage-playbook.md`.

### 0. Intake mode

Declare one mode before tool use:

- `live-target`: current web page/endpoint needs fresh browser and wire evidence; use sequential role order
- `artifact-only`: only saved requests/source/tokens/samples; mark live acceptance unproven
- `continuation`: same target/env/goal; reuse the current gate and reopen only changed surfaces

### 1. Environment and tools

Snapshot installed MCP families, attach/debug availability, and optional passive wire stores. Route only confirmed tools. Missing optional families are gaps, not ceremony.

### 2. Family triage

Tag the smallest dominant gate family (`signer-gated`, `transport-gated`, `verifier-gated`, `decode-gated`, `session-gated`) from current evidence, then open only that path.

### 3. Delivery intent

State the declared shape (`evidence`, `local-proof`, `compact-replay`, `collector`) and stop at that gate. Do not brand incomplete automation as a temporary collector.


## Minimal Intake

Start immediately when the user provides a target page or API URL, site and collection goal, captured request, JS or WASM sample, cookie or token sample, or packet capture. Choose the intake mode before deciding whether browser evidence is required.

Ask only for missing information that changes implementation: target fields, collection scope, output format, login requirement, and whether dedupe, resume, or incremental sync is required.

For read-only evidence or local-proof requests, ask only for the missing sample, vector, trigger action, or source path. Delay project-root, retention, live replay, and request-budget questions until the next action would write, execute target code, or contact the target.

Before implementing a `compact-replay` or `collector`, use the conditional implementation brief in `references/provider-work-order.md` when multiple implementation forms remain viable or the next step would widen the currently resolved runtime, dependency, writable-scope, or live-authority boundary. Do not turn that brief into a mandatory approval ceremony for `evidence`, `local-proof`, or an implementation choice the user already made.

## Universal Reverse Loop

Use `references/workflow-overview.md` as the short execution map and `references/tool-playbook.md` for tool selection.

### Phase 0: Fingerprint

- Capture a clean baseline before broad hooks when observer effect is possible.
- Distinguish decoy from real endpoint, transport gate from application gate, visible param from wrapper rewrite, bootstrap asset from data API, and single request from stateful transcript.
- Identify plain JSON, GraphQL, WebSocket, protobuf, binary envelope, encrypted response, glyph mapping, JSVMP, or host-bound runtime early.
- Choose the smallest next proof, not the largest bundle dump.

### Phase 1: Prove the real request

- Follow redirects and wrapper or compatibility pages.
- Map entry, bootstrap, list, detail, submission, verifier, warm-up, telemetry, download, risk-control, and async export or report job routes separately.
- Capture exact URL, method, query, body bytes, headers, outbound Cookie header, response shape, and initiator.
- Treat pagination pivots and challenged document replays as part of the protocol contract.

Deliver one confirmed request on the real business path.

### Phase 2: Isolate moving state

Classify every changing part: timestamp, nonce, signed query or body, rotating header or cookie, wrapper field, operation name, cursor, bootstrap artifact, decode key, glyph map, session secret, profile baseline, sparse delta, counter, heartbeat, elapsed-time dependency, media key, page exception, account state, or host semantic.
When the surface is an export or signed open platform style API, also bucket fields into business, static app, server-issued, and per-request dynamic classes before designing regeneration.

Prove cookie provenance and distinguish server-issued artifacts from locally minted filler. Treat page text about session participation as a hypothesis only until wire behavior confirms it. When login is only the first gate, validate tenant, role, and data-range with a final identity reread before export; see `references/multi-context-session-playbook.md`. Keep stored jar state separate from the authoritative outbound Cookie header when they diverge.

### Phase 3: Locate the canonical mutation point

Trace in this order:

1. transport wrappers, interceptors, `beforeSend`, fetch, Ajax, XHR, worker, or message boundaries
2. bootstrap scripts and inline payloads
3. exposed helpers and returned child objects
4. WASM exports or inner serializer, packer, signer, or decoder primitives
5. server-returned challenges and response-side refresh fields
6. frame serializers, protobuf parsers, handshake transcripts, and key schedules

The canonical mutation point is where the wire-shaped payload actually changes, not where business code creates a placeholder.

When a named digest is present, prove it on fixed inputs before trusting a standard library. Prefer environment-selected digest constants and the browser branch over UI or function names; route to `references/crypto-patterns.md`.

### Phase 4: Rebuild offline

- Climb one rung at a time: fixed-input parity, narrow boundary observation, pure local reproduction, narrow host bootstrap, then evidence-backed host-surface patching.
- Before escalating, record the last proved artifact, exact blind spot, why the next rung is smallest, and how browser-free delivery remains intact.
- Read `references/escalation-ladder-playbook.md` before widening runtime, patch surface, or transport profile.
- When transport evidence proves that the closest maintained backend cannot express the admitted browser profile, read `references/native-transport-profile-playbook.md` before building a route-local native adapter.
- When an opaque staged artifact still depends on captured runtime inputs, read `references/opaque-runtime-profile-playbook.md`; preserve one atomic run, port stage by stage, and distinguish algorithmic generation from snapshot-driven generation or pool replay.
- Preserve exact serialization, field slot, framing, JSONP callback, delimiter, compression, cipher, and decode order.
- When porting JS digests to Python, validate uint32 truncation, `ROTL` edge cases, and per-byte packing masks on a frozen preimage before live replay.
- For string-table-heavy bundles, begin with the non-executing `references/profiles/static-ast/index.md` detector and conservative rewrite, then recover the decoder offline with a two-pass rewrite before deep beautify work; see `references/obfuscation-guide.md` and `references/offline-inline-deob-playbook.md`.
- Regenerate request-shaped artifacts inside the request loop when page, keyword, body, referer, timestamp, or session state can change them.

### Phase 5: Prove repeatability and scale

- Verify helpers and decoders against fixed-input or fixed-payload vectors.
- Prove one fresh single-page replay on one session chain before scaling or shrinking runtimes.
- Require repeated live replay at least two to three times; helper load success or plausible token shape is not acceptance.
- For verifier-gated flows, prove required sidecars, shared-state consistency, actual request timing, final verifier semantics, and the first downstream consumer on one complete round. Keep the hard order above; record an ablation matrix and a local error-semantic map before scaling retries.
- For verifier-gated flows, prove positive-sample hygiene: clean success samples outrank contaminated automation failures. Environment risk (exit IP, automation marks, consecutive failures) is a separate failure surface from track quality.
- Prove the next page or cursor, route pivots, refresh behavior, field completeness, and relevant permission boundaries.
- For async exports, prove create with a pre-create task-id snapshot plus condition match, isolate the polled task, and block persistence when downloaded columns are thinner than requested fields; see `references/async-export-job-playbook.md`.
- Save raw samples early and fail loudly on unexpected response shapes.

## Implementation Contract

- Split client, settings, bootstrap, headers and cookies, sign, envelope, decode, extraction, retries, storage, and tests by concern.
- Bind one task project before writing and keep dynamic evidence under `js_reverse_cache/tasks/<task-id>/`; do not use OS temp, Desktop drop folders, the skill directory, or hidden browser profiles as primary storage.
- Keep stable scaffolding separate from volatile captures and generated runtime blobs.
- Catalog server-issued and locally computed state separately.
- Keep bootstrap-heavy acquisition and replay on one session chain until reuse is proven.
- Treat wire egress as authoritative when it differs from intermediate getters, callbacks, or cookie jars.
- Test transport admission separately when traffic dies before application semantics.
- Keep deterministic proof mode separate from live-generation mode.
- Keep every final helper self-contained and free of runtime-backed predecessor imports.
- Reuse existing solved helpers only through `references/case-reuse-playbook.md`: match by exact scope or multiple independent signals, run fixed vectors first, and never promote copied secrets or historical notes as current proof.

Use `scripts/scaffold_reverse_project.py` for a Python-first project, `scripts/protocol_diff.py` for request or response deltas, `scripts/transport_profile_diff.py` for structured TLS and H2 profile deltas, `scripts/transform_trace_diff.py` for staged runtime parity, and `scripts/crypto_fingerprint.py` for preliminary encoding or digest hints.

For reusable evidence, read `references/reproducible-evidence-playbook.md`; use `scripts/evidence_normalizer.py` to create a redacted ordered package, `scripts/transcript_diff.py` to locate the first chain divergence, and `scripts/practice_lab.py` to exercise positive and negative protocol controls offline.

The skill-owned loopback practice lab is deterministic fixture evaluation, not a fresh live target. Probe it with direct HTTP only; do not activate the paired browser Startup Gate for this self-test.

## Verification and Reporting

Do not mark complete until every gate relevant to the declared shape passes:

- Startup Gate is current.
- For live claims, the real endpoint, canonical mutation point, and moving state are proven.
- For a fresh web `live-target`, both first-pass tool evidence surfaces are recorded; `artifact-only` web work states those surfaces as unproven, and non-web primary targets are out of scope instead of inventing web browser proof.
- Clean-baseline and observer effect risk are handled when relevant.
- Fixed-input helper or decoder checks pass.
- Non-empty signs, plausible token length, helper load success, one HTTP `200`, a current cookie jar, or an expired browser export are not acceptance by themselves.
- Cookie provenance, slot placement, session chain integrity, transport, envelope, decode, stream, pagination, and permission rules are documented when applicable.
- For `compact-replay` and `collector`, repeated live replay succeeds unless the accepted result is an explicitly bounded offline replay with live acceptance marked unproven.
- Any final replay or collector runs without browser automation or browser profiles.
- Output is saved in the requested format.
- Sensitive artifacts are redacted outside a task-local secret store. A persisted normalized evidence package uses the evidence-specific manifest schema in `references/project-artifact-contract.md`; runnable replay or collector manifests additionally record capability, session scope, helper, and replay evidence without copying secrets. A no-write conversational evidence result does not require a manifest file.

After each meaningful phase, use the concise phase-delta format from `references/report-templates.md`; use the full templates only for major decisions and final delivery. For `compact-replay` and `collector`, finish with its compact protocol handoff summary rather than creating redundant project documents. Always report family choice, what each available evidence surface proved, real endpoint, moving parts, misleading signals, fixed-input proof, final protocol path, collector/helper split, saved paths, browser-free status, and remaining instability. Add cookie, observer effect, sibling route, envelope-family, decode, session, pagination, or minimal-verifiable-fact details only when relevant.

When a reusable family emerges, preserve 5 to 15 structural facts using `references/minimal-verifiable-facts-playbook.md`. Keep a one-job lesson task-local; after two independent reproductions, use `references/experience-card-schema.md` to promote only the invariant, fixture, positive/negative oracles, and applicability boundary.

## Reference Router

Load only references that match current evidence, but keep every route directly discoverable here.

### Core workflow and maintenance

- focused Hook / env-patch / pure-Python routes: see Fast Routes and Ownership
- `references/profiles/browser-hook-snippets/index.md`
- `references/profiles/static-ast/index.md`
- `references/profiles/env-patch/index.md`
- `references/pure-python-rebuild-playbook.md`
- `references/startup-triage-playbook.md`
- `references/workflow-overview.md`
- `references/tool-playbook.md`
- MCP family choice and signal-driven auto-judge: read `references/mcp-routing-playbook.md` when deciding among artifact-only, Camoufox/managed host, chrome-devtools, js-reverse, passive wire stores, wire visibility, or environment providers
- local attach ports or debug profile path issues: `references/local-mcp-environment.md`
- `references/escalation-ladder-playbook.md`
- `references/delivery-gate-playbook.md`
- `references/anti-patterns-playbook.md`
- `references/report-templates.md`
- `references/doctrine-index.md`
- `references/symptom-heuristics.md`
- `references/pattern-atlas.md`
- `references/minimal-verifiable-facts-playbook.md`
- `references/reproducible-evidence-playbook.md`
- `references/provider-work-order.md`
- `references/specialist-handoff-contract.md`
- `references/project-artifact-contract.md`
- `references/case-reuse-playbook.md`
- `references/experience-card-schema.md`

### Request path, signers, and obfuscation

- modified standard digests, uint32 ports, fixed-sample crypto: `references/crypto-patterns.md`
- string-table or obfuscator-style recovery: `references/obfuscation-guide.md`, `references/offline-inline-deob-playbook.md`
- `references/decoy-and-real-request-playbook.md`
- `references/transport-wrapper-playbook.md`
- `references/patched-helper-playbook.md`
- `references/jsvmp-analysis-playbook.md`
- `references/opaque-runtime-profile-playbook.md`

### Cookies, bootstrap state, and sessions

- multi-layer business identity after login: `references/multi-context-session-playbook.md`
- `references/cookie-provenance-playbook.md`
- `references/session-contract-playbook.md`
- `references/public-bootstrap-envelope-playbook.md`
- `references/challenge-state-envelope-playbook.md`
- dual writers for one param name: `references/dual-writer-param-playbook.md`
- local challenge HTML/JS executor contract: `references/local-challenge-executor-playbook.md`
- `references/server-js-cookie-bootstrap-playbook.md`
- `references/side-asset-bootstrap-playbook.md`

### Host-bound runtime and observation

- `references/environment-patch-playbook.md`
- `references/embedded-browser-runtime-playbook.md`
- `references/iv8-runtime-cheatsheet.md`
- `references/challenge-artifact-harvest-playbook.md`
- prefer redirect URL harvest before encrypt rebuild; see also `references/local-challenge-executor-playbook.md`
- `references/hook-techniques.md`
- `references/anti-debug-playbook.md`
- `references/env-diff-playbook.md`

### Transport, decode, and structured protocols

- async export, report download, task isolation: `references/async-export-job-playbook.md`
- `references/transport-pre-gate-playbook.md`
- `references/native-transport-profile-playbook.md`
- `references/response-decode-playbook.md`
- `references/structured-transport-playbook.md`
- `references/stateful-stream-e2ee-playbook.md`

### Verifiers, pagination, exceptions, and recovery

- `references/verifier-replay-playbook.md`
- `references/verifier-error-localization-playbook.md`
- `references/positive-sample-hygiene-playbook.md`
- `references/pagination-route-pivot-playbook.md`
- `references/page-specific-exception-playbook.md`
- `references/troubleshooting-playbook.md`

### Skill validation

- `references/skill-maintenance.md`
- `references/official-self-test-task-suite.md`
- behavioral forward-test execution and independent review: `references/forward-testing-playbook.md`

## Maintaining This Skill

Before editing, read `references/skill-maintenance.md`. Validate against `references/official-self-test-task-suite.md` and run `scripts/validate_skill.py` when present. The default validation is static; run `scripts/validate_skill.py --run-trusted-self-tests` only against the trusted current skill root. Use `scripts/validate_skill.py --export-tests <path-outside-skill>` when a machine-readable JSON suite is needed; keep the Markdown suite as the single source of truth. Static PASS is not behavioral proof. For a behavioral non-regression claim, follow `references/forward-testing-playbook.md` and validate an external fresh-runner, independent-reviewer report with `scripts/forward_test_report.py`; keep the report and response artifacts outside this skill tree.

Put reusable detail in its most specific reference. Keep this entry as the protocol-first execution path and direct router. Preserve generic facts and fixed vectors, never live secrets, copied cookies, account tokens, or site-specific folklore.

## Bottom Line

When a site looks browser-only, ask:

1. What is the real request?
2. What is the real changing state?
3. Can that state be rebuilt locally?

Most targets collapse once those questions are answered with wire evidence and repeatable replay.
