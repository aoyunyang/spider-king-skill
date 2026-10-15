# Symptom Heuristics

Use this file when the target is fresh, the symptom is still broad, or you need a quick family match before picking a more specific playbook.

## Contents

- [Failure surface first](#failure-surface-first)
- [Quick scenario router](#quick-scenario-router)
- [JSON API returns full challenge HTML](#json-api-returns-full-challenge-html)
- [Same param is sometimes short and sometimes long](#same-param-is-sometimes-short-and-sometimes-long)
- [Impersonation changes which wall you hit](#impersonation-changes-which-wall-you-hit)
- [Same-vendor bootstrap face is not the hard WAF face](#same-vendor-bootstrap-face-is-not-the-hard-waf-face)
- [Challenge submit token from another page returns 200 empty](#challenge-submit-token-from-another-page-returns-200-empty)
- [CSS-stacked digit images are a local decode, not a signer](#css-stacked-digit-images-are-a-local-decode-not-a-signer)
- [Check API success with finish false](#check-api-success-with-finish-false)
- [Named MD5 403 while sibling APIs 200](#named-md5-403-while-sibling-apis-200)
- [Stdlib 403 of a live-admitted token](#stdlib-403-of-a-live-admitted-token)
- [HTML placeholder zeros with no list XHR](#html-placeholder-zeros-with-no-list-xhr)
- [Dummy HTTP sibling does not retire a WebSocket list](#dummy-http-sibling-does-not-retire-a-websocket-list)
- [Chrome-devtools HTTP log is not a WebSocket inventory](#chrome-devtools-http-log-is-not-a-websocket-inventory)
- [First short WebSocket text is not the list](#first-short-websocket-text-is-not-the-list)
- [Named AES short vector is 8 bytes](#named-aes-short-vector-is-8-bytes)
- [JSVMP silent under CDP webdriver](#jsvmp-silent-under-cdp-webdriver)
- [UTF-8 network dump of protobuf](#utf-8-network-dump-of-protobuf)
- [Empty ajax beforeSend is not a signer](#empty-ajax-beforesend-is-not-a-signer)
- [JSON number strings carry CR or LF](#json-number-strings-carry-cr-or-lf)
- [Bootstrap JS evals cleanly but never writes the cookie](#bootstrap-js-evals-cleanly-but-never-writes-the-cookie)
- [Mint-shaped token but stable verifier reject code](#mint-shaped-token-but-stable-verifier-reject-code)
- [Positive desktop gold still fails local protocol rebuild](#positive-desktop-gold-still-fails-local-protocol-rebuild)
- [Common-prefix to human gold rises but gate never flips](#common-prefix-to-human-gold-rises-but-gate-never-flips)
- [Multi-day token reverse without morph ablation row](#multi-day-token-reverse-without-morph-ablation-row)

Treat a target as belonging to a familiar family when one or more of these symptoms appear:

- page code mentions one endpoint but the wire uses another
- business code builds `token`, `sign`, or `m`, but transport wrappers rewrite it before send
- the page renders a loading shell or SSR frame with `200 OK`, but the hydration blob is empty and the real business data arrives only on a later API
- the response says `ok`, `success`, or `error=false`, but the business payload is missing or a subcode still signals rejection
- the transport is GraphQL, WebSocket frames, protobuf, msgpack, or another structured envelope rather than plain JSON
- standard helper names such as `md5`, `btoa`, `atob`, or `sha1` produce nonstandard output
- the first request returns JavaScript, cookies, offsets, or font files instead of business data
- the top page URL stays fixed and shows no obvious form, but the real auth or business flow actually lives inside an iframe or embedded frame
- the page is public, but a bootstrap endpoint still returns a public key, config blob, nonce seed, or wrapper contract before list requests work
- the page works in a fresh anonymous profile, but replay becomes flaky once logged-in cookies or unrelated account state leak into the session
- a hidden field with a server-looking name such as verification token, request id, or page id is appended by page code and any fresh format-conforming value seems accepted
- a browser-captured blob matches the expected shape, but replay only succeeds after moving it to a different transport slot such as a custom header, cookie echo, or wrapper field
- one minimal in-page or host-runtime request automatically acquires extra signer params, cookies, or headers that are missing from the same request shape when sent directly from Python
- a prehandle or bootstrap call returns session ids, work factors, asset URLs, answer schema, movement bounds, or other challenge config that the client mostly relays rather than derives
- verifier `get/load/prehandle` returns one-round token, image URLs, callback ids, or random keys, and final verify fails whenever any of them are reused from another round
- entry HTML plus challenge JS must run first to seed environment-bound cookie, storage state, or preflight token before business replay stabilizes
- local helper output stays much shorter, simpler, or more repetitive than browser output even after seeding cookie, storage, script, or resource state
- a callback or SDK init reports success, yet the decisive token field stays empty until a later network response or state write lands
- one page bootstrap writes a page-scoped cookie or storage value, while a later request computes a separate request-scoped header, param, or token
- JSONP, callback wrappers, or other non-JSON framing must be stripped before the payload becomes usable
- the code branches on environment probes such as `Object.keys(window)`, `Reflect.ownKeys`, `getOwnPropertyDescriptor`, `Function.prototype.toString`, `JSON.stringify`, or `document.all`
- the runtime touches `canvas`, WebGL, `getComputedStyle`, layout metrics, or similar native surfaces before the decisive field appears
- page HTML plus offline-loaded scripts can seed cookies, signed URL suffixes, or XHR wrapper state without full rendering or gestures
- changing only the UA major version, parser timing, or timer mode changes bootstrap order, cookie output, or token output
- standard clients die at H2 reset, TLS EOF, handshake timeout, or early disconnect, while impersonated transport, HTTP/1.1, or a mobile or app UA passes
- a bootstrap runtime exposes one synchronous getter or object method after init even though later timers or DOM probes still throw
- a challenge or bootstrap script self-issues XHR or fetch with the real wrapped body, binary payload, or decisive headers
- a top-level SDK init dies inside axios, fetch, adapter glue, or telemetry setup, yet a smaller inner export or serializer still returns the exact blob family you need
- only one page fails, often the last page
- early pages replay through one route family, but later pages pivot to a different pagination endpoint, static path, or `/ui` route even though the visible pager looks uniform
- inline `onclick`, `tagname`, template strings, or hidden pager metadata carry replay-critical URLs or params, and DOM-parsed values no longer match the raw source because of entity decoding, broken escaping, or legacy markup
- the page text says login or `sessionid` matters, and the answer differs per account
- the site ships a tiny side script or `.wasm` that looks unrelated but actually seeds signing state
- visual assets arrive as sprite sheets, RGBA cutouts, padded masks, or answer geometry whose preprocessing changes solver confidence more than signer code changes
- the business body fields decode cheaply with a fixed XOR, hex, or base64 variant while the real pain remains a separate environment-bound signer on the outer request
- one prompt image, text hint, or challenge string defines click order while a different background image defines hit geometry, and final verify packages both into encrypted coordinates
- the API returns strings, hints, glyphs, or fonts instead of the final numeric payload
- list JSON cells are stacked digit images with extra classes and `left` offsets, and the request body is only a page index
- a check or submit API returns answer-accept success while a sibling `finish` / `done` / `complete` flag stays false
- the response body is encoded, compressed, protobuf, msgpack, or split across multiple layers before it becomes usable data
- URL query, body field, response body, and cookie appear to share one packet family: version marker, checksum, custom alphabet, state-derived prefix, or the same inner cipher
- GET replay only fails when query ordering, empty-field preservation, or URL encoding diverges from the frontend-built sign input
- the same request succeeds once and then dies unless some hidden refresh state is regenerated
- a track blob, collect field, verifier sidecar, or similar behavior payload is formally present but only loosely enforced on one public or demo route
- list APIs work anonymously, but detail or submit APIs still reject without a different permission boundary
- a human-facing detail page loads fine, but the real full text still arrives through the same parse or wrapper endpoint with a different method, cfg, or identifier
- bootstrap or current-user endpoints mint a fresh session cookie successfully, yet the first real business route still returns a permission denial
- login or bootstrap returns a grant token, redirect handle, or async follow-up URLs, but the target backend still redirects to login until extra post-auth session exchanges run
- relative action paths only work when resolved against the effective entry origin, while hardcoded sibling hosts yield CSRF or credential-looking failures
- one authenticated session can switch the active tenant, shop, org, or workspace by mutating one context field while leaving the main session cookie unchanged
- sending the body as a library-native form dict or JSON fails, while replaying the exact frontend-style urlencoded bytes succeeds
- OCR or template matching finds a correct gap or click location on a restored or padded image, yet verify still fails until that position is mapped into the display or submission coordinate space
- list output contains stable ids that can feed a second-stage detail collector more cheaply than rerunning the search
- empty filter values do not reproduce the visible tab because the page injects category or mode state before send
- a trigger only starts an async side channel, and the usable code, token, approval link, or artifact arrives later through mail, SMS, webhook, queue, or delayed callback
- the same previously understood request starts returning password-like, field-like, or user-facing validation errors only after tight pacing or repeated attempts
- a login or pairing step returns a ref, QR seed, public key, or client identifier before business frames become readable
- the target keeps one long-lived WebSocket alive with auth, ack, heartbeat, or reconnect frames that must stay in order
- media metadata arrives in one place, but the actual file replay or decryption needs a separately derived key
- a challenged landing route fails, but a sibling auth, identity, or business route bypasses the same gate cleanly

- the page text says login or `sessionid` participates in signing, but the business list route already returns full data with no session cookie
- a helper is named `sm3`, `md5`, or `sha*`, standard libraries miss the fixed sample, environment checks select IV/Tj/packing/compress, and Node eval of the harvested file is a different digest
- ascii hashlib and digit-byte hashlib both miss a frozen timestamp, and a hasher-internal eval/setInterval reconstructs a function from charcodes
- HTTP 403 JSON forbidden on this API while sibling APIs on the same session return 200; ablate stdlib versus impersonate on the same admitted bytes before calling it digest or WAF
- schema-valid JSON numeric strings fail `int()` because of CR/LF
- MCP `select_page` or attach times out while the script URL is still downloadable over HTTP
- a huge chart/painter/SVG webpack bundle dwarfs the tiny module that owns the list URL
- an obfuscator-style string table rewrite changes nothing until member-map objects are expanded and hex keys are normalized
- Python digest parity fails only on some pages because `ROTL(x, 0)` or another uint32 edge case is wrong
- login cookies exist and the home page opens, but list or export data belongs to another tenant, shop, supplier, or data range
- a context switch returns HTTP 200 or success, yet a final identity reread still shows the previous scope
- operators choose a display name, while activation requires a live authorization code or resource value with exactly one match
- concurrent workers share one session and keep switching shops or suppliers, then read each other's data
- RSA or password-login errors look like bad credentials until ciphertext encoding length or alphabet is checked
- short-lived login handoff tickets were saved as durable cookies and later fail replay
- an export or report create returns HTTP 200, but history gains no new task id
- polling immediately finds a successful task whose time range or fields belong to an older run
- regenerate or retry works, while first-create still fails or creates nothing
- downloaded file opens, yet column count is lower than the requested custom field set
- a mailbox or SMS code is accepted only when taken after a fresh send baseline, and code length differs by scene
- risk or signature errors disappear only after method, content-type, or body placement is aligned with the signer input
If the symptoms match, reuse the methodology even when the exact site and parameter names differ.

## Failure surface first

When the failing layer is unclear, classify with `references/failure-surface-taxonomy.md` before applying the symptom recipes below. For local-versus-success disagreements, use `references/positive-sample-ablation-playbook.md` after sample hygiene. For multi-stage bootstrap gaps, use the multi-stage settle rule in `references/workflow-overview.md`.

## Quick scenario router

| Symptom cluster | First open |
|---|---|
| status/redirect loops, challenge seeds cookie/URL | `references/anti-bot-class-playbook.md`, `references/challenge-state-envelope-playbook.md` |
| same-vendor bootstrap face vs hard interstitial | `references/anti-bot-class-playbook.md`, `references/server-js-cookie-bootstrap-playbook.md` |
| challenge submit 200 with empty or still-challenge body | `references/challenge-state-envelope-playbook.md`, `references/failure-surface-taxonomy.md` |
| verify/gateway accept but business still punished/challenged | `references/verifier-replay-playbook.md` (layered acceptance), `references/parameter-ownership-playbook.md` |
| many dynamic fields, unclear what to rewrite vs execute vs only parse | `references/parameter-ownership-playbook.md` |
| helper evals but no cookie until a later load event | `references/server-js-cookie-bootstrap-playbook.md`, `references/local-challenge-executor-playbook.md` |
| XHR/fetch wrapper appends sign | `references/jsvmp-analysis-playbook.md` (entry taxonomy + feed-cut) |
| local sign bytes != browser | `references/signer-parity-chain-playbook.md` |
| helper loads, artifact short/empty | `references/environment-patch-playbook.md` (severity tiers + sniper) |
| first-screen writers missed | `references/hook-techniques.md` |
| HTTP 200 empty business body | `references/failure-surface-taxonomy.md` (silent reject) |
| TLS/H2 dies before app data | `references/transport-pre-gate-playbook.md` |
| WS/binary/graphql envelope | `references/structured-transport-playbook.md` |
| fonts hide payload | `references/pattern-atlas.md` Pattern H |
| case hit but rebuild fails | `references/case-reuse-playbook.md` (constraint internalization) |
| named MD5 403, sibling APIs 200 | `references/crypto-patterns.md`, `references/anti-patterns-playbook.md`, `references/transport-pre-gate-playbook.md` |
| stdlib 403 of live-admitted token, impersonate 200 | `references/transport-pre-gate-playbook.md` |
| empty ajax `beforeSend` IIFE, captured body equals visible fields | `references/transport-wrapper-playbook.md`, `references/transport-pre-gate-playbook.md` |
| HTML zeros, no list XHR | `references/decoy-and-real-request-playbook.md`, `references/anti-debug-playbook.md` |
| HTML zeros plus HTTP 200 dummy filler, WebSocket unproven | `references/decoy-and-real-request-playbook.md`, `references/structured-transport-playbook.md` |
| named AES.encrypt, short vector is 8-byte CT | `references/crypto-patterns.md`, `references/patched-helper-playbook.md` |
| JSVMP silent, CDP webdriver true | `references/environment-patch-playbook.md`, `references/anti-debug-playbook.md` |
| protobuf body saved as UTF-8 / `U+FFFD` | `references/structured-transport-playbook.md`, `references/tool-playbook.md` |
| JSVMP plus protobuf `serializeBinary` or wasm `encode` | `references/jsvmp-analysis-playbook.md` |
| JSON numbers fail `int()` or sums drift | `references/response-decode-playbook.md` |
| MCP select/attach timeout | `references/anti-debug-playbook.md` |

## JSON API returns full challenge HTML

If a business data route responds with HTML challenge chrome, linked challenge scripts, or inline bootstrap blobs:

- do not stop at "endpoint blocked"
- treat it as challenge-state bootstrap on the business route
- harvest redirect URL or cookies on the same session chain
- route to `references/challenge-artifact-harvest-playbook.md` and `references/local-challenge-executor-playbook.md`

## Same param is sometimes short and sometimes long

If one field name shows disjoint length bands across research and live success samples:

- assume dual writers until proven otherwise
- compare success wire shape before packaging a generator
- route to `references/dual-writer-param-playbook.md`

## Impersonation changes which wall you hit

If plain clients get one verifier wall and impersonated clients get JS challenge HTML or a cleaner route:

- fix transport admission before deep algorithm work
- keep the admitted profile on the whole challenge and replay chain
- route to `references/transport-pre-gate-playbook.md` when transport fails first

## Same-vendor bootstrap face is not the hard WAF face

If one client sees a non-final status plus probe or bootstrap JS that can mint a cookie, and another sees a hard status plus a different probe asset and WAF interstitial text:

- do not treat them as one wall
- do not rename the target from a URL or timeline substring such as `jsl`
- corroborate family with cookie-name cluster plus status, body, or header evidence
- route to `references/anti-bot-class-playbook.md` and `references/server-js-cookie-bootstrap-playbook.md`

## CSS-stacked digit images are a local decode, not a signer

If list JSON is schema-valid, each cell is stacked images or spans with extra classes and `left` offsets, and the request body is only a page index or id:

- tag `decode-gated`; do not hunt a missing sign field
- derive the hide class from companion fields on a fixed vector, drop those nodes, then place remaining glyphs by in-flow visual x
- identify glyphs by image-byte hash, not CSS class names
- do not OCR the sprites in the collector
- route to `references/response-decode-playbook.md`

## Check API success with finish false

If check or submit returns answer-accept success (`status_code=1`, `message=success`, or equivalent) while `finish` / `done` / `complete` stays false:

- split answer-accept from complete
- warm GET the challenge document on the same jar, then POST check again
- cookie-only POST of the answer is not collector success
- if the document GET rotates a token, follow the page-bound submit-token rule instead
- route to `references/challenge-state-envelope-playbook.md`

## Named MD5 403 while sibling APIs 200

If a named MD5 of a timestamp returns HTTP 403 JSON forbidden, but sibling APIs on the same session return 200:

- treat it as not session death
- replay the same admitted token or cookie bytes on stdlib versus installed curl impersonate
- impersonate business 200 is transport admission; only then, if impersonate still 403s, freeze the timestamp vs the bundled digest
- hashlib ascii and digit-byte dual miss keeps the helper
- stub hasher-internal eval/setInterval; never execute recovered R
- route to `references/transport-pre-gate-playbook.md`, `references/crypto-patterns.md`, and anti-patterns 63/64/68

## HTML placeholder zeros with no list XHR

If the rendered table or list is filled with zeros or placeholders and the network log has no list XHR or fetch:

- do not scrape or sum the DOM numbers
- treat it as missing observation or activation, not an empty payload
- check `navigator.webdriver` and interceptor registration before schema reverse
- route to `references/decoy-and-real-request-playbook.md` and anti-pattern 71

## Dummy HTTP sibling does not retire a WebSocket list

If HTML zeros coexist with HTTP 200 on a similarly named REST path, and that body is a constant filler:

- do not sum the dummy HTTP body or the DOM zeros
- freeze one live WebSocket or text business frame before treating the list as solved
- dummy HTTP filler is intercept, not grant
- route to `references/decoy-and-real-request-playbook.md`, `references/structured-transport-playbook.md`, and anti-pattern 76

## Chrome-devtools HTTP log is not a WebSocket inventory

If chrome-devtools `list_network_requests` shows only document/css/js, HTML started as zeros, and the DOM later fills with numbers:

- do not conclude there is no list API
- that tool's network list is HTTP resources, not WebSocket frames
- hook `WebSocket` constructor/send/message or use `js-reverse` `get_websocket_messages`
- route to `references/tool-playbook.md`, `references/decoy-and-real-request-playbook.md`, and anti-pattern 78

## First short WebSocket text is not the list

If a WebSocket send is followed by a short constant text frame and then JSON:

- do not JSON.parse or sum the short frame
- skip non-object text and keep reading until the business JSON object
- one recv landing on the prefix is not reuse failure
- route to `references/structured-transport-playbook.md` and anti-pattern 79

## Named AES short vector is 8 bytes

If a helper is named `AES.encrypt` with a 16-byte key, and a short plaintext such as `"hello"` yields 8-byte ciphertext:

- do not port AES-128 because the live token is 16-aligned
- first textbook try is 2-key 3DES-EDE, not AES
- if Node diverges, compare navigator/location catch-path key order to the browser branch
- route to `references/crypto-patterns.md`, `references/patched-helper-playbook.md`, and anti-pattern 77

## JSVMP silent under CDP webdriver

If a JSVMP loads under Chrome CDP, `navigator.webdriver === true`, and the business XHR never fires:

- if `Navigator.prototype.webdriver` is configurable, delete it in an authorized initScript and recapture
- do not wrap XHR or `toString` on a signature-bound VM
- do not open Camoufox for a webdriver boolean
- record `launch` vs `attach`
- route to `references/anti-debug-playbook.md`, `references/environment-patch-playbook.md`, and anti-pattern 72

## UTF-8 network dump of protobuf

If a saved MCP or DevTools body contains `U+FFFD`, or a protobuf decoder fails on a text-saved request:

- recapture ArrayBuffer or hex at `serializeBinary` or XHR send
- do not restart opcode work because the dump is unreadable
- regenerate fresh clock-bucket fields through the public encoder; a second int32 may be client-chosen if the token remains `encode(t1,t2)`
- route to `references/structured-transport-playbook.md` and anti-patterns 73/74

## Stdlib 403 of a live-admitted token

If an in-page or clean-browser fetch already returned business 200 with a token, but the stdlib client gets HTTP 403 JSON forbidden with those same bytes, while sibling routes still return 200 on stdlib:

- freeze the admitted bytes
- replay them on installed curl impersonate
- impersonate business 200 means transport admission, not a bad helper
- do not escalate canvas, audio, or WebGL as the remaining HTTP gate
- lock replay identity to the impersonate chrome major
- route to `references/transport-pre-gate-playbook.md` and anti-patterns 66/68/69

## Empty ajax beforeSend is not a signer

If ajax or fetch exposes a `beforeSend`, middleware, or wrapper hook, the hook body is empty or a no-op IIFE, and the captured body matches the visible business fields:

- do not hunt a missing token or start JSVMP reverse
- freeze the wire body and diff it against the visible fields
- if they match, skip signer reverse and ablate stdlib versus impersonate on those bytes
- route to `references/transport-wrapper-playbook.md`, `references/transport-pre-gate-playbook.md`, and anti-pattern 75

## JSON number strings carry CR or LF

If schema-valid JSON numeric strings fail `int()` or the sum is unstable:

- strip CR/LF before parse; do not invent a cipher
- do not drop rows because a CR made two strings look different
- route to `references/response-decode-playbook.md`

## Challenge submit token from another page returns 200 empty

If verify or submit with a previous document's page id, seq, or callback token returns HTTP `200` but an empty body or remaining challenge chrome:

- the token is bound to the document that displayed the challenge
- harvest the live token from the current HTML on the same session chain
- HTTP `200` plus empty business body is not a grant
- route to `references/challenge-state-envelope-playbook.md`

## Bootstrap JS evals cleanly but never writes the cookie

If a returned challenge script finishes without throwing and host scalars look right, but no cookie or storage write appears:

- check whether the script registers `load` or `DOMContentLoaded` only after collector-ready
- if `readyState` is already `complete`, native events will not fire again
- wait for the public collector-ready object, then synthesize the event
- do not mutate collected fields as a substitute for mint
- route to `references/server-js-cookie-bootstrap-playbook.md`

## Mint-shaped token but stable verifier reject code

If the behavior/device token has the expected family (prefix/length) and submit returns a stable structured reject code:

- do not first add track micro-entropy
- label possible `morph-mismatch`, `state-chain-incomplete`, or `companion-sign-mismatch`
- ablate morph -> state-chain -> companions -> token-writer
- route to `references/verifier-morph-and-state-chain-playbook.md` and `references/failure-surface-taxonomy.md`

## Positive desktop gold still fails local protocol rebuild

If a human desktop success sample exists but local rebuild stays rejected:

- treat the sample as existence proof, not mandatory morph
- compare scene/device class and bootstrap transcript before replaying tracks
- if a same-family solved skeleton exists, migrate host/path/state-chain first (`references/case-reuse-playbook.md`)
- require N-run gate metrics before calling the path stable

## Common-prefix to human gold rises but gate never flips

If offline binary/token similarity to a human success sample keeps improving while live reject codes stay stable:

- treat similarity as a false-progress metric
- stop mint-variant expansion and env sprawl
- name primary wall (`morph-wall` / `state-chain-wall` / `companion-wall`)
- run kill-switches in `references/verifier-morph-and-state-chain-playbook.md`

## Multi-day token reverse without morph ablation row

If more than one working day was spent on fireye/track/env without an alternate morph end-to-end row:

- stop and fill the day-card
- force K1/K6 actions before more reverse
- route to anti-patterns 41/42/44
