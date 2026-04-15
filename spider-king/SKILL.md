---
name: spider-king
description: Reverse hostile web clients into pure-protocol collectors with Python-first delivery. Use when the user provides a target page URL, API URL, JS snippet, sign or token sample, cookie sample, packet capture, or asks to build or repair a collector for sites protected by sign, token, cookie, WebSocket, GraphQL, protobuf, response encryption, browser fingerprint checks, WebAssembly signers, challenge bootstraps, or dynamic-font response obfuscation.
---

# Spider King

## Role

Turn hostile web clients into stable protocol collectors.

This skill is not a browser automation skill.
This skill is a protocol recovery skill.

Default posture:

1. find the real request
2. identify the true changing state
3. rebuild that state offline
4. deliver a Python collector

## Non-Negotiables

- Final delivery must be pure protocol: raw HTTP plus local signer, local decoder, or local bootstrap helper only.
- Do not ship Playwright, Selenium, CDP page-driving, or submit-through-browser flows as the solution.
- Prefer Python for the collector and orchestration.
- Only keep a tiny isolated JS or WASM helper when a verified Python port is not yet cheaper, safer, or faster to maintain.
- If browser tooling is used at all, use it only for recon and evidence gathering, never as a hidden dependency in the final collector.
- Recover one stable request before scaling pagination, concurrency, or submission.
- Every conclusion must be backed by artifacts: request samples, fixed-input helper outputs, cookies, headers, and replay proof.
- Stay in one execution loop until you reach protocol delivery or hit a real external blocker.

## What This Skill Optimizes For

- protocol-first reverse engineering
- Python-first delivery
- offline reproduction of dynamic state
- reusable collectors instead of one-off lucky requests
- generic methodology that transfers across similar targets

## Reference Layout

The `references/` directory is organized by purpose:

- root-level playbooks are generic pattern documents and reusable workflows

Rule:

- read generic pattern playbooks first
- abstract solved work back into generic patterns instead of storing site-specific folklore

## Similarity Heuristics

Treat a target as belonging to the same family when one or more of these symptoms appear:

- page code mentions one endpoint but the wire uses another
- business code builds `token`, `sign`, or `m`, but transport wrappers rewrite it before send
- the transport is GraphQL, WebSocket frames, protobuf, msgpack, or another structured envelope rather than plain JSON
- standard helper names such as `md5`, `btoa`, `atob`, or `sha1` produce nonstandard output
- the first request returns JavaScript, cookies, offsets, or font files instead of business data
- the page is public, but a bootstrap endpoint still returns a public key, config blob, nonce seed, or wrapper contract before list requests work
- only one page fails, often the last page
- the page text says login or `sessionid` matters, and the answer differs per account
- the site ships a tiny side script or `.wasm` that looks unrelated but actually seeds signing state
- the API returns strings, hints, glyphs, or fonts instead of the final numeric payload
- the response body is encoded, compressed, protobuf, msgpack, or split across multiple layers before it becomes usable data
- the same request succeeds once and then dies unless some hidden refresh state is regenerated
- list APIs work anonymously, but detail or submit APIs still reject without a different permission boundary
- empty filter values do not reproduce the visible tab because the page injects category or mode state before send
- a login or pairing step returns a ref, QR seed, public key, or client identifier before business frames become readable
- the target keeps one long-lived WebSocket alive with auth, ack, heartbeat, or reconnect frames that must stay in order
- media metadata arrives in one place, but the actual file replay or decryption needs a separately derived key

If the symptoms match, reuse the methodology even when the exact site and parameter names differ.

## Operating Doctrine

### Doctrine 1: Trust the wire, not the page text

- Real request paths beat page hints.
- Real headers beat visible business code.
- Real cookies beat guessed token stories.
- Real response shape beats archived notes.

### Doctrine 2: The dynamic parameter is not always a signature

The real moving part may be:

- a cookie
- a page-specific header
- a transport envelope
- a server-returned JS bootstrap
- a dynamic font
- a WebAssembly export
- a transport wrapper rewrite
- a response-side decoder
- an account-bound session contract

Do not assume every hard target is solved by hunting a `sign` function.

### Doctrine 3: Fixed-input validation beats naming

If a page helper is called `md5` or `btoa`, prove it on fixed inputs before trusting the name.

Minimum standard for suspicious helpers:

1. pick a fixed input such as `"abc"` or a captured timestamp
2. record browser output
3. record local output
4. compare intermediate values, not just final output

### Doctrine 4: Narrow exceptions stay narrow

If only one page needs a special `User-Agent`, or only one request needs a rotated cookie, encode that exception explicitly.
Do not poison the entire collector with a fake "browser-only" conclusion.

### Doctrine 5: Automation is not an acceptable crutch

When stuck, do more protocol work:

- diff requests
- extract inline scripts
- run bootstrap JS locally
- port helper logic
- instantiate WASM locally
- decode fonts locally

Do not fall back to browser automation as delivery.

### Doctrine 6: Environment mismatch is evidence

When local output and live output disagree, treat the mismatch as evidence:

- compare fixed inputs
- compare side assets
- compare patched helpers
- compare environment branches

Do not hand-wave the mismatch away as "probably browser-only".

### Doctrine 7: Delivery gates outrank convenience

If the only known path still depends on live page context, the task is not done.

- a browser profile is not a protocol artifact
- a hidden refresh click is not a collector
- an unexplained decoder is not acceptable handoff

Keep reversing until the moving parts are local, explicit, and testable.

### Doctrine 8: Public does not mean unsigned

Anonymous pages still have protocol contracts.

- a public list may still require entry-route cookies
- a bootstrap endpoint may still return the key, config, or envelope seed
- list visibility does not prove detail or submit visibility

Treat anonymous access, envelope construction, and permission boundaries as separate questions.

### Doctrine 9: Stateful streams are protocol, not browser magic

If the target only becomes readable after login, pairing, or a warm-up WebSocket exchange, the session transcript is part of the protocol.

- pairing or login bootstrap is not UI fluff
- handshake outputs are protocol artifacts
- heartbeats, ack frames, counters, and reconnect rules are part of the collector

Do not collapse a stateful stream problem into a fake single-request sign story.

## Minimal Intake

Start immediately if the user already provided enough evidence.

Otherwise ask only for the smallest missing set:

- target page URL, or
- target API URL, or
- site homepage plus collection goal, or
- captured request sample, or
- JS snippet, obfuscated bundle, cookie sample, sign sample, or packet capture

Only ask follow-ups that change implementation:

- target fields
- scope: single page, pagination, category, date range, or whole site
- output format: JSON, CSV, Excel, database, or API sink
- whether login is required
- whether incremental sync, dedupe, or resume is required

## Universal Reverse Loop

### Phase 0: Fingerprint before deep work

Classify the target before reading giant bundles:

- decoy endpoint vs real endpoint
- wrapper rewrite vs visible param
- patched helper vs standard helper
- bootstrap asset vs direct data API
- plain JSON vs GraphQL vs WebSocket vs binary envelope
- single-shot replay vs stateful session with pairing, auth, or warm-up frames
- direct response vs encoded response vs glyph-mapped response
- page-specific exception vs whole-flow exception
- session-bound vs anonymous
- verifier-gated vs signer-gated
- JSVMP or heavy obfuscation vs normal packed bundle

Goal:

- choose the smallest next proof, not the biggest code dump

### Phase 1: Identify the true request path

- follow redirects
- inspect wrapper pages and compatibility pages
- separate visible page routes from real wire routes
- map bootstrap requests, list requests, detail requests, submission requests, and risk-control requests
- detect whether one endpoint serves both bootstrap and final data in separate phases

Deliverable for this phase:

- one confirmed request that is definitely on the real business path

### Phase 2: Classify the moving parts

For the real request, classify each changing field:

- static header
- rotating header
- static cookie
- rotating cookie
- timestamp
- nonce or random fragment
- signed body or query
- transport envelope, operation name, or message type
- compressed or binary response format
- decode key, glyph map, or response-side transform
- encrypted response
- page-specific exception
- account-bound session dependency
- bootstrap artifact dependency
- login or pairing bootstrap artifact
- session key schedule or exported secret material
- heartbeat, ack, counter, or message-tag state
- media-key derivation or side-channel download secret

Goal:

- separate what must be reproduced from what is just noise

### Phase 3: Locate the canonical mutation point

Look in this order:

1. transport wrappers such as `$.ajaxSetup`, `beforeSend`, fetch wrappers, interceptors
2. bootstrap side scripts and inline payloads
3. page-exposed helper functions
4. WebAssembly exports
5. server-returned JS challenges
6. response-side refresh fields that seed the next request
7. handshake transcripts, frame serializers, binary node encoders, protobuf parsers, or session key schedules

Rule:

- the canonical mutation point is where the wire payload actually changes, not where the business code first creates a placeholder

### Phase 4: Rebuild the moving parts offline

Choose the cheapest valid offline shape:

1. pure Python
2. Python plus isolated JS signer
3. Python plus minimal local JS or WASM helper
4. Python plus local challenge bootstrap executor
5. Python plus local font decoder

Never add browser automation to the final path.

### Phase 5: Prove repeatability

Do not call it solved until:

- the same logic succeeds at least 2 to 3 times
- pagination advances correctly
- final fields are complete
- dynamic state regenerates correctly
- account-bound constraints are documented

## Pattern Atlas

### Pattern A: The endpoint on the page is fake

Symptoms:

- page code hooks `/api/match/...`
- wire uses `/api/question/...` or another path
- browser request succeeds but replaying the visible path fails

Action:

- trust the network path
- trace request initiators
- document the decoy path
- code against the live path only

### Pattern B: The business param is a decoy

Symptoms:

- page code builds `token`
- wire sends `m`, `f`, or another field
- request wrapper mutates data before send

Action:

- reverse the wrapper first
- diff business-layer params against final payload
- rebuild the wrapper logic, not the decoy field

### Pattern C: Standard helper is patched

Symptoms:

- `md5`, `btoa`, `atob`, `sha1`, or similar names exist
- local reproduction with standard libraries does not match browser output

Action:

- freeze fixed test vectors
- port the exact helper implementation
- verify helper outputs before using them in requests

### Pattern D: First response is not data, but bootstrap

Symptoms:

- first request returns JS, `Set-Cookie`, offset scripts, or challenge tokens
- replay works only after the bootstrap response is processed

Action:

- treat bootstrap as part of the protocol contract
- execute or emulate it locally
- carry resulting cookies or globals into the next request

### Pattern E: Only one page breaks

Symptoms:

- pages 1 to 4 work
- page 5 fails or returns hints, strings, or anti-bot signals

Action:

- diff headers and cookies by page
- test page-specific `User-Agent`, referer, or ordering rules
- encode the exception narrowly

### Pattern F: Answer or data is account-bound

Symptoms:

- page text mentions `sessionid`
- different accounts produce different sums or answers
- submit works only with the same session that collected the data

Action:

- make `sessionid` explicit in the collector
- keep fetch and submit under the same account
- verify with the same session before blaming signer logic

### Pattern G: Tiny side assets carry the whole signer

Symptoms:

- `.wasm`, `/offset`, challenge JS, or font files appear trivial
- main bundle is noisy but side asset changes output decisively

Action:

- inspect side assets early
- instantiate WASM locally
- execute bootstrap JS locally
- decode fonts locally

### Pattern H: Dynamic fonts hide the payload

Symptoms:

- numeric values appear as glyphs or meaningless text
- response includes font URLs or embedded font data

Action:

- fetch the font asset
- derive the codepoint-to-digit map
- decode the payload locally

### Pattern I: One-shot verifier, captcha, or click challenge

Symptoms:

- next request only works after a verification step
- no meaningful JS signer exists for the business API

Action:

- treat the verifier output as the real dynamic parameter
- solve and replay the verifier in protocol form
- do not simulate clicks in the final solution

### Pattern J: Response data is encoded, compressed, or split

Symptoms:

- HTTP status is normal but payload looks like gibberish, digit soup, escaped code, glyphs, or binary
- business data only appears after a decode helper, font map, protobuf parser, or compression layer
- the response body shape changes after a local decode step, not after another request

Action:

- freeze the raw payload first
- trace the first consumer of the raw payload
- identify decode order, keys, maps, or parsers
- rebuild the decoder locally
- validate local decode on the exact captured payload before scaling

### Pattern K: Transport is GraphQL, WebSocket, or a binary envelope

Symptoms:

- the URL stays stable but `operationName`, frame type, or binary opcode changes
- request bodies carry nested `variables`, message IDs, or channel names
- the real contract is in the envelope structure, not just one visible param

Action:

- document the transport kind explicitly
- freeze one known-good message or body sample
- separate envelope fields from business fields
- identify which fields are signed, sequenced, or server-assigned
- replay one stable message locally before attempting full stream collection

### Pattern L: Public page still hides a bootstrap envelope

Symptoms:

- the page or homepage is publicly visible
- one early endpoint returns a public key, config blob, nonce seed, or short string instead of business data
- the real business request posts a wrapper such as `{"param":"..."}` rather than the visible form fields
- compact JSON, a digest, a timestamp, and encryption or encoding are applied in a specific order
- list APIs work, but detail or submit APIs may still be permission-gated

Action:

- hit the real entry route once and capture the cookies that scope the public session
- freeze one bootstrap response and one successful business request
- prove the envelope build order exactly: raw payload, compact serialization, sign input, timestamp or nonce injection, final wrapper object, encryption or encoding, and outer transport field name
- verify long-message chunking rules when RSA or similar block ciphers wrap the payload
- make category, mode, and page parameters explicit instead of trusting UI defaults or empty values
- document list access and detail access separately so a public list is not mistaken for full public data access

### Pattern M: Stateful WebSocket session with encrypted business frames

Symptoms:

- the target stays mostly idle until login, pairing, or a short warm-up exchange completes
- one or more early messages carry a ref, public key, client ID, secret seed, or challenge blob
- later frames are binary or protobuf and stay unreadable until session keys or counters are derived
- the stream dies unless auth, ack, heartbeat, reconnect, or message-tag rules are preserved
- media metadata is visible, but media download or decryption needs separate derivation from message payloads

Action:

- freeze one full successful transcript: bootstrap, login or pairing, auth ack, heartbeat, and one business frame
- separate frame families before reading payload semantics: bootstrap, auth, keepalive, business, receipt, media
- recover the exact key schedule or session-secret update path before blaming protobuf or compression
- document message tags, counters, and replay boundaries explicitly
- prove one stable local session first, then add stream collection, reconnect, or media handling

## Tool Priorities

Use `js-reverse` as the primary analysis tool for code and runtime evidence.

Priority order:

1. static source search and extraction
2. request diffing
3. helper verification on fixed inputs
4. offline execution of extracted logic
5. local protocol replay

Use browser tooling only when one of these is true:

- a redirect chain or wrapper page must be observed once
- anti-debug defenses force offline extraction first
- a fixed input/output pair must be sampled from a page helper

Even then, the final collector must not depend on that browser step.

## Bundled Scripts

Use local helper scripts when they shorten repeatable work:

- `scripts/scaffold_reverse_project.py`: generate a protocol-first Python project skeleton with profile-aware layouts for `generic`, `public-envelope`, `structured-transport`, and `response-decode` targets
- `scripts/check_reverse_env.py`: verify the minimal local reverse environment fast
- `scripts/crypto_fingerprint.py`: fingerprint suspicious digest, Base64, or custom-alphabet outputs
- `scripts/protocol_diff.py`: compare captured request or response samples and surface the meaningful deltas

For stateful stream targets, start from the `structured-transport` scaffold and split handshake, session, frame-codec, decode, and media logic into separate modules early.

Special routing:

- read `references/workflow-overview.md` when the task is still broad and you need the shortest end-to-end map
- read `references/hook-techniques.md` before turning runtime validation into breakpoint chaos
- read `references/crypto-patterns.md` before trusting helpers named after standard algorithms
- read `references/obfuscation-guide.md` when packed bundles threaten to waste time
- read `references/anti-debug-playbook.md` when live inspection becomes unstable
- read `references/environment-patch-playbook.md` when local helper outputs diverge from live outputs
- read `references/jsvmp-analysis-playbook.md` when a VM or bytecode interpreter hides the logic
- read `references/stateful-stream-e2ee-playbook.md` when login or pairing bootstrap, session keys, heartbeats, binary frames, or media derivation are part of the contract
- read `references/troubleshooting-playbook.md` when replay is close but still flaky

## Reproduction Decision Tree

Choose delivery in this order:

1. pure Python if all logic is restored
2. Python plus minimal JS helper if the signer is exact in JS and porting now would add risk
3. Python plus local WASM helper if the request param comes from a tiny export
4. Python plus local bootstrap executor if the server returns JS that seeds cookies or tokens
5. stop and keep reversing if the only remaining path is browser automation

Never choose:

- browser-backed replay as final delivery
- "works only in my browser profile" as acceptable handoff
- page-driving submission as the answer when protocol submission exists

## Implementation Rules

- keep headers, cookies, signer logic, pagination, output, retries, and persistence in separate modules
- keep handshake bootstrap, session secrets, frame codecs, business parsing, and media derivation in separate modules when the target is stateful
- make `sessionid`, timeout, retry, sleep, and output path explicit arguments
- log or print sign inputs and outputs until they match verified samples
- include fixed-input self-checks before live traffic
- prefer Python reimplementation of crypto before falling back to JS execution
- prefer stdlib HTTP clients when you want zero dependencies or the environment's third-party stack is noisy
- preserve weird delimiters and non-ASCII separators explicitly
- treat bootstrap artifacts such as public keys, config blobs, nonce seeds, and wrapper field names as first-class inputs
- validate compact JSON shape, sign input order, timestamp precision, and chunked-encryption boundaries separately before blaming the runtime
- save raw request and response samples during early development
- save one raw handshake transcript and one post-auth business frame before rewriting the collector
- support narrow per-page or per-request exceptions in configuration instead of hardcoding chaos into the main loop
- make category and pagination fields explicit when the page may be injecting hidden tab state
- fail loudly on unexpected response shapes
- if older notes disagree with live output, trust fresh live evidence

## Verification Gates

Do not mark complete until all relevant gates pass:

- request path confirmed
- moving parts classified
- canonical mutation point identified
- helper outputs verified on fixed inputs
- structured transport rules documented when the target is not plain JSON
- response decode steps are local and repeatable when the payload is not directly readable
- fixed-sample checks exist for local decoders when decode is part of the contract
- bootstrap artifact replay confirmed when public routes still require key, config, cookie, or wrapper seeding
- login or pairing bootstrap replay confirmed when the target needs a warm session before business traffic
- key schedule or session-secret derivation verified on captured samples when the stream is encrypted
- heartbeat, ack, counter, or message-tag rules documented when the stream is stateful
- raw frame parsing and business decode proven on at least one exact captured frame
- media-key derivation documented when file download or decryption uses separate secrets
- live replay succeeds repeatedly
- pagination or cursor advance confirmed
- account-bound constraints documented
- list-versus-detail permission boundaries documented when access levels differ
- page-specific exceptions documented
- output saved in the requested format

## Output Contract

After each meaningful phase, emit short structured reporting instead of vague prose.

Always return:

- what the real endpoint is
- what the real moving parts are
- what was misleading
- what was verified with fixed inputs
- what the final protocol path is
- where the collector and sample output were saved
- what still looks unstable, if anything

Use the headings from `references/report-templates.md` when possible.

## Skill Validation

When modifying this skill itself, validate against the official self-test suite before calling the edit complete.

Pass conditions:

- the route stays protocol-first
- final delivery never depends on browser automation
- minimal missing evidence is requested instead of broad homework for the user
- the chosen references match the real symptom instead of generic cargo-cult loading
- output reports the real endpoint, real moving parts, and proof artifacts
- structured transport, decode chains, stateful sessions, and delivery gates are handled correctly when present

## Anti-Patterns

- Do not ask the user to manually inspect giant bundles if tooling can inspect them.
- Do not jump straight to Selenium or Playwright when a direct API exists.
- Do not confuse business-layer params with wire-layer params.
- Do not trust helper names without fixed-input proof.
- Do not call browser-only behavior before checking page-specific headers or cookies.
- Do not bury every concern in one `main.py`.
- Do not stop after one lucky success.
- Do not ship a browser automation script when the task is protocol-recoverable.
- Do not hide automation behind words like "temporary collector" or "reliable fallback".

## Reference Router

Read focused generic references when the symptom matches:

- `references/workflow-overview.md` for the shortest end-to-end execution map
- `references/tool-playbook.md` for tool choice and next-step routing
- `references/report-templates.md` for phase reporting and handoff structure
- `references/official-self-test-task-suite.md` when validating whether the skill still generalizes after edits
- `references/crypto-patterns.md` when signatures or helper outputs look suspicious
- `references/obfuscation-guide.md` when packed code or string tables dominate the bundle
- `references/hook-techniques.md` when runtime proof is faster than static reading
- `references/anti-debug-playbook.md` when the page destabilizes tooling
- `references/environment-patch-playbook.md` when local execution diverges from live execution
- `references/env-diff-playbook.md` when redirects, wrappers, or environment-specific behavior cause mismatches
- `references/jsvmp-analysis-playbook.md` when a custom VM or bytecode interpreter hides the logic
- `references/structured-transport-playbook.md` when GraphQL, WebSocket, protobuf, msgpack, or binary envelopes carry the real contract
- `references/stateful-stream-e2ee-playbook.md` when login, pairing, session keys, keepalive frames, or media decryption make the stream stateful
- `references/response-decode-playbook.md` when the payload needs local decode before it becomes usable data
- `references/public-bootstrap-envelope-playbook.md` when a public page still needs bootstrap keys, cookies, config, or an encrypted wrapper before list replay works
- `references/delivery-gate-playbook.md` when you need to decide whether the current path is acceptable handoff or still cheating
- `references/offline-inline-deob-playbook.md` when inline scripts, eval-packed code, legacy hashes, or anti-debug logic push the work offline
- `references/decoy-and-real-request-playbook.md` when the page and the wire disagree on the real endpoint
- `references/transport-wrapper-playbook.md` when transport wrappers rewrite params, headers, or payloads
- `references/patched-helper-playbook.md` when helper names look standard but outputs do not
- `references/page-specific-exception-playbook.md` when only one page or one request behaves differently
- `references/session-contract-playbook.md` when results or submission are account-bound
- `references/side-asset-bootstrap-playbook.md` when `.wasm`, side scripts, fonts, or returned JS seed the real state
- `references/server-js-cookie-bootstrap-playbook.md` when an endpoint returns executable JS that seeds cookie or token state
- `references/verifier-replay-playbook.md` when captcha or one-shot verification gates the business request
- `references/troubleshooting-playbook.md` when replay logic is almost correct but still unstable

## Experience Deposition

After a successful job, preserve only the reusable lesson:

- convert site-specific pain points into generic pattern language
- keep fixed-input validation habits, not endpoint trivia
- promote transport-shape and decode-chain lessons into generic references, not per-site notes
- promote public bootstrap and encrypted-envelope lessons into reusable checklists, not vendor folklore
- promote session-bootstrap, frame-family, and media-key lessons into generic references, not chat-app trivia
- preserve build-order lessons such as payload -> compact JSON -> sign -> timestamp -> encrypt -> wrapper when that order matters
- prefer new root-level generic references over new site-specific case files
- add helper scripts only when they improve many future jobs, not just one target

## Bottom Line

This skill should teach one habit above all:

When the site looks "browser-only", do not panic and do not automate.
First ask:

1. what is the real request
2. what is the real changing state
3. can that state be rebuilt locally

Most similar targets collapse once those three questions are answered honestly.
