# Pattern Atlas

Use this file when the target already resembles a recurring pattern and you want the shortest proven first move.

## Contents

- [Pattern A: The endpoint on the page is fake](#pattern-a-the-endpoint-on-the-page-is-fake)
- [Pattern B: The business param is a decoy](#pattern-b-the-business-param-is-a-decoy)
- [Pattern C: Standard helper is patched](#pattern-c-standard-helper-is-patched)
- [Pattern D: First response is not data, but bootstrap](#pattern-d-first-response-is-not-data-but-bootstrap)
- [Pattern E: Only one page breaks](#pattern-e-only-one-page-breaks)
- [Pattern F: Answer or data is account-bound](#pattern-f-answer-or-data-is-account-bound)
- [Pattern G: Tiny side assets carry the whole signer](#pattern-g-tiny-side-assets-carry-the-whole-signer)
- [Pattern H: Dynamic fonts hide the payload](#pattern-h-dynamic-fonts-hide-the-payload)
- [Pattern H2: CSS-in-HTML sprites hide the numbers](#pattern-h2-css-in-html-sprites-hide-the-numbers)
- [Pattern I: One-shot verifier, captcha, or click challenge](#pattern-i-one-shot-verifier-captcha-or-click-challenge)
- [Pattern I2: Cloud verifier multi-stage transcript](#pattern-i2-cloud-verifier-multi-stage-transcript)
- [Pattern I3: Issued challenge must be consumed](#pattern-i3-issued-challenge-must-be-consumed)
- [Pattern J: Response data is encoded, compressed, or split](#pattern-j-response-data-is-encoded-compressed-or-split)
- [Pattern K: Transport is GraphQL, WebSocket, or a binary envelope](#pattern-k-transport-is-graphql-websocket-or-a-binary-envelope)
- [Pattern L: Public page still hides a bootstrap envelope](#pattern-l-public-page-still-hides-a-bootstrap-envelope)
- [Pattern M: Stateful WebSocket session with encrypted business frames](#pattern-m-stateful-websocket-session-with-encrypted-business-frames)
- [Pattern N: Challenge-generated state gates a shared envelope family](#pattern-n-challenge-generated-state-gates-a-shared-envelope-family)
- [Pattern O: Pagination route pivots mid-sequence](#pattern-o-pagination-route-pivots-mid-sequence)
- [Pattern P: Parsed attributes lie about replay-critical routes](#pattern-p-parsed-attributes-lie-about-replay-critical-routes)
- [Pattern Q: Transport pre-gate blocks the clean baseline](#pattern-q-transport-pre-gate-blocks-the-clean-baseline)
- [Pattern R: Challenge runtime already knows the answer](#pattern-r-challenge-runtime-already-knows-the-answer)
- [Pattern S: Business response is a refresh contract](#pattern-s-business-response-is-a-refresh-contract)
- [Pattern T: Login and business context are separate states](#pattern-t-login-and-business-context-are-separate-states)
- [Pattern U: Activation looks successful but the data-range is stale](#pattern-u-activation-looks-successful-but-the-data-range-is-stale)
- [Pattern V: Display labels are not protocol ids](#pattern-v-display-labels-are-not-protocol-ids)
- [Pattern W: Create returns success but no new export task](#pattern-w-create-returns-success-but-no-new-export-task)
- [Pattern X: Polling reuses a historical successful task](#pattern-x-polling-reuses-a-historical-successful-task)
- [Pattern Y: First-create and regenerate are different contracts](#pattern-y-first-create-and-regenerate-are-different-contracts)
- [Pattern Z: Challenge rewrites the business URL](#pattern-z-challenge-rewrites-the-business-url)
- [Pattern AA: SDK loads but signs only registered request paths](#pattern-aa-sdk-loads-but-signs-only-registered-request-paths)

## Pattern A: The endpoint on the page is fake

Symptoms:

- page code hooks `/api/match/...`
- wire uses `/api/question/...` or another path
- browser request succeeds but replaying the visible path fails

Action:

- trust the network path
- trace request initiators
- document the decoy path
- code against the live path only

## Pattern B: The business param is a decoy

Symptoms:

- page code builds `token`
- wire sends `m`, `f`, or another field
- request wrapper mutates data before send
- a swallowed `call()` return or field `m` is assigned but never sent

Action:

- reverse the wrapper first
- diff business-layer params against final payload
- rebuild the wrapper logic, not the decoy field

## Pattern C: Standard helper is patched

Symptoms:

- `md5`, `btoa`, `atob`, `sha1`, or similar names exist
- local reproduction with standard libraries does not match browser output
- ascii hashlib and digit-byte hashlib both miss a frozen timestamp
- a hasher calls `eval` or `setInterval(eval)` on a recovered function string

Action:

- freeze fixed test vectors
- port the exact helper implementation
- port the browser branch; do not eval the harvested file in Node as the oracle
- named JSEncrypt/JSBN/RSA under statement-split is still standard padding; freeze the pad string before gold-token policy; random PKCS#1 inequality is not a custom port
- keep the bundled helper after hashlib dual miss; stub hasher-internal eval/timers; never execute recovered R
- a nearby charcode array is not T constants until a frozen vector needs those values
- verify helper outputs before using them in requests

## Pattern D: First response is not data, but bootstrap

Symptoms:

- first request returns JS, `Set-Cookie`, offset scripts, or challenge tokens
- first request returns non-final HTML such as `412` plus inline bootstrap state and one or more linked challenge assets
- replay works only after the bootstrap response is processed
- the same document URL returns the real HTML only on a later pass after challenge state is rebuilt

Action:

- treat bootstrap as part of the protocol contract
- test whether the challenged document route itself is the real business path
- execute or emulate it locally
- carry resulting cookies or globals into the next request
- validate replay with semantic anchors, not status alone

## Pattern E: Only one page breaks

Symptoms:

- pages 1 to 4 work
- page 5 fails or returns hints, strings, or anti-bot signals

Action:

- diff headers and cookies by page
- test page-specific `User-Agent`, referer, or ordering rules
- encode the exception narrowly
- prove necessity with a one-variable negative control
- reject HTTP 200 plus a hint or string array unless the typed business payload appears
- do not copy the last-page profile onto sibling pages
- packing collisions are not interchangeable pages; keep the live clock refresh

## Pattern F: Answer or data is account-bound

Symptoms:

- page text mentions `sessionid`
- different accounts produce different sums or answers
- submit works only with the same session that collected the data
- or the opposite trap: page text claims session participates in signing, yet the list route already returns full data anonymously

Action:

- prove the claim from wire behavior before hardcoding session material into the signer
- make required session inputs explicit only for the chains that need them
- keep fetch and submit under the same account when the answer is account-bound
- split anonymous collection from login-only submit when the wire shows that split
- verify with the same session before blaming signer logic

## Pattern G: Tiny side assets carry the whole signer

Symptoms:

- `.wasm`, `/offset`, challenge JS, or font files appear trivial
- main bundle is noisy but side asset changes output decisively

Action:

- inspect side assets early
- instantiate WASM locally
- execute bootstrap JS locally
- decode fonts locally

## Pattern H: Dynamic fonts hide the payload

Symptoms:

- numeric values appear as glyphs or meaningless text
- response includes font URLs or embedded font data

Action:

- fetch the font asset
- derive the codepoint-to-digit map
- decode the payload locally

## Pattern H2: CSS-in-HTML sprites hide the numbers

Symptoms:

- list JSON is readable, but each cell is stacked images or spans with extra classes and `left` offsets
- the request body is only a page index or id; no sign field appears on the wire
- companion fields such as `key` and `value` sit next to the HTML

Action:

- tag `decode-gated`; do not invent a signer
- derive the hide class from companion fields on a fixed vector, then drop those nodes
- place remaining glyphs by `inFlowWidth * visibleIndex + leftOffset`
- identify glyphs by image-byte or pixel hash, not CSS class names
- route to `references/response-decode-playbook.md`

## Pattern I: One-shot verifier, captcha, or click challenge

Symptoms:

- next request only works after a verification step
- no meaningful JS signer exists for the business API

Action:

- treat the verifier output as the real dynamic parameter
- solve and replay the verifier in protocol form
- do not simulate clicks in the final solution

## Pattern I2: Cloud verifier multi-stage transcript

Symptoms:

- final verify is only one step in a longer ordered chain
- device, warm-up, log, or telemetry hosts fire before acceptance
- complete profile baseline and later sparse or delta packets must agree
- HTTP 200 or sidecar upload success still ends in risk-like rejection
- business URL accepts only after a same-round grant is attached

Action:

- freeze init -> sidecars -> verify -> first downstream consumer as one transcript
- build a one-variable ablation matrix before answer or track tuning
- enforce shared baseline and sparse delta consistency
- separate structure, sidecar, timeline, answer, and environment risk surfaces
- package dual-runtime helpers only as local compute, with Python owning HTTP
- split verifier gateway accept, server grant, and business oracle; gateway-only success is stage success
- read `references/verifier-replay-playbook.md`, `references/parameter-ownership-playbook.md`, `references/verifier-error-localization-playbook.md`, and `references/positive-sample-hygiene-playbook.md`

## Pattern I3: Issued challenge must be consumed

Symptoms:

- GET/init of a slider or puzzle image, then a later page 403s even after a correct verify
- accept body shows simple fractions (`50%`, `66.67%`, `83.33%`) after skipped images
- reject body shows messy closeness percentages on a submitted-wrong answer
- gap search never looks past an arbitrary x cap and latches onto a tall dark column

Action:

- consume every issued round or abandon the session
- split unused-issue (session miss) from submitted-wrong (often retryable)
- treat accept-rate as a cumulative floor and reject-rate as closeness until proved otherwise
- search `0 .. width - piece_width` and score a piece-sized four-edge rectangle
- read `references/challenge-state-envelope-playbook.md` and `references/verifier-replay-playbook.md`

## Pattern J: Response data is encoded, compressed, or split

Symptoms:

- HTTP status is normal but payload looks like gibberish, digit soup, escaped code, glyphs, or binary
- business data only appears after a decode helper, font map, protobuf parser, or compression layer
- the response body shape changes after a local decode step, not after another request
- schema-valid JSON numeric strings fail `int()` because of CR/LF

Action:

- freeze the raw payload first
- trace the first consumer of the raw payload
- identify decode order, keys, maps, or parsers
- rebuild the decoder locally
- strip CR/LF from numeric strings before `int` or sum; do not invent a cipher
- validate local decode on the exact captured payload before scaling

## Pattern K: Transport is GraphQL, WebSocket, or a binary envelope

Symptoms:

- the URL stays stable but `operationName`, frame type, or binary opcode changes
- request bodies carry nested `variables`, message IDs, or channel names
- the real contract is in the envelope structure, not just one visible param

Action:

- document the transport kind explicitly
- freeze one known-good message or body sample as hex or ArrayBuffer, not a UTF-8 MCP dump
- separate envelope fields from business fields
- identify which fields are signed, sequenced, or server-assigned
- regenerate clock-bucket protobuf fields through the public encoder; a second int32 may be client-chosen if the token remains `encode(t1,t2)`
- replay one stable message locally before attempting full stream collection

## Pattern L: Public page still hides a bootstrap envelope

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

## Pattern M: Stateful WebSocket session with encrypted business frames

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

## Pattern N: Challenge-generated state gates a shared envelope family

Symptoms:

- entry HTML and challenge JS must run first before business replay stabilizes
- a derived cookie, storage item, or preflight token binds session, page challenge, and environment model
- the business route depends on several coordinated fields at once, such as cookie, URL query, header token, and encoded body
- URL query, body, response, and sometimes cookie look like variants of one packet family rather than unrelated formats
- packet framing includes field prefixes, version markers, checksum bytes, custom alphabets, dynamic prefixes, or state-derived slices in addition to the inner cipher
- a preflight token request returns the same encoded family and seeds a later header or request field

Action:

- freeze one fresh two-stage trace: entry HTML, challenge JS, derived cookie or storage state, preflight token request and response, and one business request and response
- separate the problem into proofs: environment model, state transition, packet framing, key normalization, inner cipher, and business plaintext
- map the shared envelope family once across URL, body, response, and cookie, then record which fields are exact siblings and which are field-specific variants
- prove whether business plaintext alone is sufficient or whether current state bytes are also required to build later fields
- keep validation checkpoints explicit: cookie shape or length, token shape or length, checksum success, decoded prefix length, and expected JSON anchor or schema fields
- deliver the final collector as an explicit staged pipeline such as `entry -> local challenge/bootstrap -> token preflight -> business request -> local response decode`

## Pattern O: Pagination route pivots mid-sequence

Symptoms:

- early pages replay through one clean URL family, but later page numbers 404 or return the wrong content
- the visible pager looks uniform, but late-page links point to a different endpoint family such as `/ui`, Ajax, or a hidden template route
- guessing page numbers from the first-page URL works briefly and then collapses
- the real next page is stored in inline handlers, hidden templates, or pager metadata rather than a plain `href`

Action:

- treat pagination as part of the protocol contract, not filename arithmetic
- capture the cutoff page where the route family changes
- extract next-page targets from the live pager or raw source rather than extrapolating one URL pattern
- keep the collector logic route-aware so early and late pages can coexist without browser fallback

## Pattern P: Parsed attributes lie about replay-critical routes

Symptoms:

- inline handlers or metadata attributes carry query strings, `&`, entity-like text, or custom delimiters
- the parsed DOM value no longer matches the source bytes
- replay built from `onclick`, `tagname`, or similar DOM attributes fails, while the raw HTML snippet points to the correct route
- prettifying or reparsing the page changes the route or parameter names

Action:

- preserve the raw tag snippet before parsing or beautifying it
- compare raw source, DOM-decoded value, and wire behavior on the same page
- extract replay-critical route data from raw HTML when entity decoding or repair logic mutates it
- normalize entity handling explicitly instead of trusting parser defaults

## Pattern Q: Transport pre-gate blocks the clean baseline

Symptoms:

- standard HTTP clients die at H2 reset, TLS EOF, handshake timeout, or early disconnect before meaningful application data appears
- the same route behaves differently across UA families, ALPN, or HTTP versions
- mobile or app UA, impersonated TLS, or HTTP/1.1 passes while default desktop or stdlib traffic fails
- a sibling auth, identity, or business route bypasses a challenged landing route
- stdlib returns HTTP 403 JSON forbidden with a live-admitted token, while impersonate returns business 200 on those same bytes

Action:

- separate transport admission from signer, cookie, or payload logic
- map a narrow matrix of route, client stack, UA family, and HTTP version before loading giant bundles
- keep any passing transport profile scoped only to the blocked route family that needs it
- continue application-layer reversing only after one clean admitted baseline exists
- do not restart signer or canvas reverse when impersonate plus the current helper already returns business 200

## Pattern R: Challenge runtime already knows the answer

Symptoms:

- a bootstrap or challenge script exposes a getter after init, or self-issues XHR or fetch with the decisive wrapped payload
- later timer callbacks throw, but a usable artifact already exists before full DOM parity
- blocking `vm` execution deadlocks while DOM or script execution preserves timers or request hooks
- full VM understanding is expensive, but one outgoing payload, cookie, or header set is enough to continue

Action:

- classify the artifact path first: exposed getter, intercepted egress, or alternate-route bypass
- preserve scheduler semantics and intercept the nearest stable boundary
- stub only the minimal success response the runtime expects after local interception
- if runtime egress already exposes the authoritative outbound `Cookie` header, harvest that exact header before over-reversing individual cookie writers
- hand the harvested artifact back to Python for the real HTTP replay, and retry with fresh bootstrap when challenge bundles are version-randomized

## Pattern S: Business response is a refresh contract

Symptoms:

- the business endpoint returns HTTP 200 or an application subcode plus fields such as seed, timestamp, name, nonce, or refresh offsets
- retrying the same URL family works after those response fields are merged with one locally derived token, cookie, or header
- the local cookie jar looks close, but the exact outbound `Cookie` header or header bundle still decides success
- the helper depends more on original site JS plus narrow host patches than on business payload semantics

Action:

- treat the response payload as refresh state, not a generic failure
- freeze one fail -> refresh -> success triplet on one session chain
- retry the same business route before hunting alternate endpoints
- update server-issued seed fields and locally derived replay fields as one bundle
- compare request-egress artifacts, especially the full outbound `Cookie` header, against the stored jar
- keep any local runtime narrow, pinned, and self-contained

## Pattern T: Login and business context are separate states

Symptoms:

- account login works
- home page opens
- data still belongs to the wrong tenant, shop, supplier, or org

Action:

- split account authentication from business-context activation
- validate every required identity layer before export or scrape
- read `references/multi-context-session-playbook.md`

## Pattern U: Activation looks successful but the data-range is stale

Symptoms:

- switch or update-session returns 200 or success
- tenant or role looks right
- scoped data still reflects a previous or empty range

Action:

- compare the full activation payload, including type and value fields
- reread identity from an authoritative final surface
- treat silent incomplete activation as failure

## Pattern V: Display labels are not protocol ids

Symptoms:

- operators select a human-readable name
- wire requests need codes, resource ids, or authorization values
- wrong or ambiguous name resolution creates a wrong-context session

Action:

- use labels only to locate rows in a live authorization response
- submit protocol ids, not display text
- require exactly one match; stop on zero or many

## Pattern W: Create returns success but no new export task

Symptoms:

- create or submit returns HTTP 200
- history shows no new task id
- later code still "finds" a successful row

Action:

- snapshot task ids before create
- require a new id or explicit create-returned id
- re-diff method, body placement, content-type, and signer coverage
- read `references/async-export-job-playbook.md`

## Pattern X: Polling reuses a historical successful task

Symptoms:

- export finishes too fast
- time range or fields belong to an older run
- pre-create history already contained the chosen task id

Action:

- never take history row zero as this run
- prefer create-returned id, else only post-create new ids
- require filter and field-set match

## Pattern Y: First-create and regenerate are different contracts

Symptoms:

- regenerate or retry works with one method or body shape
- first create still fails or creates nothing
- signer was built from the wrong sample

Action:

- capture first-create separately from regenerate
- keep method, query, body, and signer inputs on the same proven sample
- leave first-create unproven rather than promoting regenerate folklore

## Pattern Z: Challenge rewrites the business URL

Symptoms:

- business JSON API first returns challenge HTML instead of data
- successful retry uses the same route plus a long verifier query param
- short offline tokens for the same param name fail live
- helper or runtime navigates to a rewritten URL before business JSON appears

Action:

- freeze fail -> challenge assets -> success on one session chain
- harvest redirect or navigation URL before deep encrypt reverse
- use a local challenge executor when needed
- prove whether app signer headers are still required after rewrite
- read `references/challenge-artifact-harvest-playbook.md`, `references/local-challenge-executor-playbook.md`, and `references/dual-writer-param-playbook.md`

## Pattern AA: SDK loads but signs only registered request paths

Symptoms:

- the SDK parses and loads without error, but the captured request is unchanged
- HTML placeholder zeros appear and no list XHR fired while `navigator.webdriver` is true
- a public signer works while XHR or fetch remains silent, or only one transport signs
- output appears only for some paths, methods, headers, or body shapes
- the sign has the expected length and alphabet but fails a browser fixed vector

Action:

- treat load and interceptor activation as separate gates
- if CDP `navigator.webdriver` is true, delete the configurable prototype property in initScript before Camoufox or opcode work
- recover `init`/`setup`, path whitelist, feature switches, load order, and the exact business-shaped trigger before adding environment APIs
- test one registered path and one unregistered path as positive and negative controls
- inspect public signer, XHR, fetch, URL/header/body, and response/warm-up channels independently
- trust the final wire-shaped URL, headers, and body over an internal return value
- read `references/profiles/env-patch/references/jsvmp-interceptor-contract.md`, `references/profiles/env-patch/references/no-touch-and-profile-coherence.md`, and `references/profiles/env-patch/references/verification-and-replay.md`
