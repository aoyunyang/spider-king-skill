# Server-JS Cookie Bootstrap Playbook

Use this reference when:

- an API first returns `202` or another non-final status with a JavaScript payload
- `JSON.data` contains executable JS instead of the expected data array
- the page succeeds only after a cookie such as `m` is created by running returned code
- the same endpoint must be called twice: once to get the challenge and once to get the data
- a page script exposes a refresh function that can be rerun to renew cookies or request parameters
- a JSON API returns HTTP `200` challenge HTML and later admits only after the same URL gains a query slot

## Contents

- [1. Recognize the pattern](#1-recognize-the-pattern)
- [2. What to capture](#2-what-to-capture)
- [3. Fastest stable strategy](#3-fastest-stable-strategy)
- [4. Minimal sandbox checklist](#4-minimal-sandbox-checklist)
- [4A. Event latch after document-complete](#4a-event-latch-after-document-complete)
- [4B. Rotating per-page JS and dual write slots](#4b-rotating-per-page-js-and-dual-write-slots)
- [5. Parsing the result](#5-parsing-the-result)
- [6. Delivery recommendation](#6-delivery-recommendation)
- [7. Verification checklist](#7-verification-checklist)

## 1. Recognize the pattern

Typical flow:

1. call the target endpoint without the derived cookie or token
2. receive a challenge response, often `202`
3. challenge payload contains executable JS
4. executing the payload sets `document.cookie`, storage, or a token variable
5. replay the same endpoint with the new state
6. receive the real data array

Do not treat the first response as an error if the site clearly uses it as a bootstrap step.

Variant:

1. page load downloads obfuscated bootstrap JS from a separate script endpoint
2. inline page code exposes a function such as `_$KS()`
3. rerunning that function refreshes cookies or request params
4. an extra in-memory timestamp such as `$_zw[23]` must also be updated
5. replay succeeds only after both pieces are refreshed

Variant:

1. the first request to a document route returns non-final HTML such as `412`
2. that HTML carries inline bootstrap state plus one or more linked challenge scripts
3. the first response also seeds one or more cookies, but those are only bootstrap inputs
4. local execution of the challenge yields the replayable cookie or full outbound `Cookie` header
5. replaying the same document URL from Python returns the real HTML page

## 2. What to capture

Record all of these:

1. first request URL, method, query, headers, and cookies
2. first response status code
3. first response body shape, including inline bootstrap state and linked challenge assets when present
4. seed cookie state from the first response before local execution
5. exact cookie or token written after executing the returned JS
6. exact outbound `Cookie` header on the replay request when egress evidence is available
7. second request differences
8. whether later pages change headers such as `User-Agent`
9. whether the page also keeps a parallel in-memory value that must be refreshed
10. semantic anchors that prove the replayed page is real business content, not just a shell

## 3. Fastest stable strategy

Prefer the smallest working path:

1. request the endpoint
2. if `data` is not the final array, treat it as challenge JS
3. execute the returned JS in a minimal sandbox
4. extract the derived cookie or token
5. replay the same request with the new state

This usually beats fully deobfuscating the payload before delivery.

If the first response is a challenged document page rather than JSON:

1. request the document URL once
2. if the response is non-final HTML such as `412`, freeze the inline bootstrap state, linked challenge JS, and seed cookies on that same session chain
3. execute the challenge locally in a minimal sandbox
4. extract the final replayable cookie or full outbound `Cookie` header, not just one cookie name
5. replay the same document URL from Python
6. verify semantic anchors in the returned HTML before scaling pagination

If the bootstrap logic already lives on the page:

1. call the exposed refresh function
2. update any timestamp slot the page passes as a request param
3. replay from the same browser context

Variant:

1. bootstrap JS wraps `XMLHttpRequest.prototype.open` (or `fetch`) and rewrites `arguments[1]`
2. the live token appears as a query suffix on each request
3. `document.cookie` for the same parameter name stays short or static
4. page 1 may accept session-only traffic while page 2+ returns `403` without the query token
5. recovery is: persistent local world installs the hook, Python calls hooked `open` without `send` to read the mutated URL, Python owns the real POST/GET

Do not hunt the short cookie as the live gate when egress URLs already carry a long query token.

Variant:

1. the first business GET returns HTTP `200` HTML challenge chrome (not `202`/`412` JSON) with a rotating script plus inline bootstrap state
2. local execution completes by navigating the **same** business URL, writing a new query slot rather than wrapping `open`/`fetch`
3. the script may also mint cookies or window globals of similar shape
4. ablation: missing query slot stays challenge HTML; the query slot present on the same session replays as business JSON; cookie-only replay does not admit
5. recovery is: capture the navigation URL in a fresh local world, then Python GETs that URL on the seed-cookie session

Do not treat every locally minted cookie as the admit condition when same-URL navigation already wrote a query slot. Do not copy a previous job's query-slot name, cookie name, or IIFE name; re-identify the slot by omission on the current target.

Variant:

1. each business call GETs a fresh obfuscated JS body, often HTTP `202`
2. algorithm, salt, location check, and write slot can all rotate
3. recovery is fetch-and-eval per call in a fresh local world, then read cookie and the same-name window global
4. clear the previous locally-minted cookie before the next script GET
5. HTTP `200` schema-valid JSON with constant filler values is punish, not grant

Related pattern:

1. page installs a global request hook such as `$.ajaxSetup(beforeSend)`
2. business code appears to send plain form data
3. hook rewrites body into encrypted payload and adds signing headers
4. response keeps outer JSON readable but encrypts the `data` field only
5. recovery requires porting both hook-time request mutation and response-field decryption

## 4. Minimal sandbox checklist

Most bootstrap payloads only need a small subset of browser APIs:

- `window`
- `document.cookie`
- `navigator.userAgent`
- `location.href`
- `Date`
- `Math`
- `setTimeout` / `setInterval`
- `atob` / `btoa`
- `encodeURIComponent` / `decodeURIComponent`
- enough parser and script-order fidelity to run inline bootstrap state before the linked challenge script when that order matters
- `document.readyState` plus `addEventListener` for `load` and `DOMContentLoaded`
- `localStorage` / `sessionStorage` sibling writes, not cookie only

Start with the minimum. Add more only when runtime errors prove they are needed.

## 4A. Event latch after document-complete

Some bootstrap scripts do not mint during `eval`. They finish a collector pass, then register `window.addEventListener('load'|'DOMContentLoaded', ...)`.

If the helper evaluates after `document.readyState === 'complete'`, the native events will not fire again. Firing a synthetic event immediately after `eval` is usually too early: the collector-ready object is not populated yet, so the listener does not exist.

Required contract:

1. evaluate the returned script
2. wait for a public collector-ready signal, such as key fields appearing on an exposed object
3. then synthesize the matching `load` or `DOMContentLoaded` event
4. observe both `document.cookie` and storage; high-PC string tables are not write points

Do not treat host-scalar parity (`userAgent`, arch, eval-length, or similar) as mint proof. Matching those scalars and still seeing no cookie means the latch was missed, not that the sandbox identity is globally wrong.

Mutating fields on an already-collected object is not equivalent to invoking the mint path. Post-hoc field edits can also poison later heartbeats or reports.

Related host-contract work stays in `references/environment-patch-playbook.md` and `references/local-challenge-executor-playbook.md`.

## 4B. Rotating per-page JS and dual write slots

Some endpoints return a fresh obfuscated JS body on every GET, often with HTTP `202`. The algorithm, salt, location check, and write slot can all rotate.

Rules:

1. fetch and evaluate a new payload for each business call; do not vendor one snapshot as the collector signer
2. after eval, read both `document.cookie` and the same-name in-memory global; the page may prefer the global when it is set
3. clear the previous locally-minted cookie before the next bootstrap-script GET; a leftover mint can change the returned JS or branch
4. HTTP `200` with schema-valid JSON whose every row is the same filler value as the unsigned or negative-control payload is punish, not grant
5. an incomplete Node `document`/`cookie` host can write a mint-shaped decoy; a native-looking `document`/`screen`/`createElement` host can change the artifact. Mint shape is not acceptance.
6. if mint ends in same-URL navigation, ablate the new query slot against any cookies the script also wrote; cookie mint is not automatically the admit condition

Keep Python as the HTTP owner. The local host only evals the current payload and returns the candidate slot values.

## 5. Parsing the result

After executing the returned JS:

1. confirm mint happened after the delayed event, not merely that `eval` returned
2. read the final `document.cookie`, any sibling storage writes, and same-name in-memory globals
3. extract the target cookie or same-name in-memory global the page actually reads
4. ignore extra attributes such as `path=/` unless they matter to the replay

When parsing, never trust the whole raw cookie string blindly. Extract the specific value needed for replay.

## 6. Delivery recommendation

Preferred structure:

- `extract_m.js` or `extract_cookie.js`
- `fetch_all.py` or `fetch_all.js`
- `README.md`

The helper should:

1. accept the returned JS payload
2. execute it in a sandbox
3. return the derived cookie or token

The main collector should:

1. fetch challenge payload
2. call the helper
3. replay the endpoint
4. aggregate results

## 7. Verification checklist

Call it done only after:

1. the helper consistently extracts the cookie, token, window global, or full replayable `Cookie` header
2. mint is gated by the collector-ready event latch when the script registers listeners after document-complete
3. the replay returns real data, not another challenge payload, shell page, or schema-valid filler JSON
4. semantic anchors such as expected DOM blocks, pagination markers, or value diversity versus the unsigned filler sentinel prove the replayed page is the real target content
5. all requested pages succeed
6. any page-specific header rules or explicit user-provided timing limits are documented
7. the final script prints or saves the requested output directly
8. if navigation wrote a query slot, a cookie-only negative control still returns challenge HTML
