# Challenge State Envelope Playbook

Use this playbook when entry HTML and challenge JavaScript seed environment-bound state before business replay works, when a business response itself returns a machine-readable refresh contract that must be consumed before retry, and when several later fields appear to share one encoded envelope family.

## Contents

- [When to route here](#when-to-route-here)
- [API-body challenge HTML variant](#api-body-challenge-html-variant)
- [Core idea](#core-idea)
- [Challenge primary key and round binding](#challenge-primary-key-and-round-binding)
- [Fast execution path](#fast-execution-path)
- [High-value checks](#high-value-checks)
- [Page-bound submit tokens](#page-bound-submit-tokens)
- [Answer-accept versus complete latch](#answer-accept-versus-complete-latch)
- [Issued-challenge consumption and dual rate fields](#issued-challenge-consumption-and-dual-rate-fields)
- [Dual gate note](#dual-gate-note)
- [Common traps](#common-traps)
- [Delivery guidance](#delivery-guidance)
- [Minimal handoff notes](#minimal-handoff-notes)

## When to route here

Route here when one or more of these symptoms appear:

- first-page HTML plus challenge JS must run before token or business requests stabilize
- a business endpoint returns a machine challenge, subcode, or refresh tuple that must be consumed before retrying the same request family
- a derived cookie, storage item, or preflight token appears after challenge execution and gates later requests
- URL query, form body, response body, and cookie all look structurally related
- the same target uses a version marker, checksum, custom alphabet, dynamic prefix, or inner encrypted payload across several fields
- a business preflight or token endpoint returns the same encoded family as the later business endpoint
- decrypting one field is not enough because another field still needs current state bytes, storage state, or challenge output
- a business JSON API returns HTTP `200` with the expected schema, but every row is the same filler/sentinel that the unsigned or negative-control request also returns

## API-body challenge HTML variant


Also handle the non-HTML twin: business JSON that only carries a punish/config URL or challenge token fields. Follow that URL on the same session jar, parse config, then continue the state-chain. Do not treat the JSON error envelope alone as the verifier grant.

Also route here when:

- a business JSON API returns `Content-Type: text/html` with challenge chrome such as inline bootstrap state, meta tags, and a linked challenge script
- HTTP `200` still carries punish/challenge response headers or a punishment HTML body instead of the business schema
- HTTP `200` still carries schema-valid JSON whose values are constant fillers matching the unsigned or negative-control payload
- the first request has no long verifier param and fails; the second request carries a long URL-bound param and succeeds
- app-layer request signing may exist in parallel but is not automatically the same gate as the HTML challenge

In this variant, prefer:

1. same-session challenge harvest
2. local challenge executor if needed
3. Python replay of the rewritten URL or derived cookies

Do not begin with deep reverse of an unrelated short signer only because it writes a similar-looking parameter name.

## Core idea

Challenge output is protocol state, not decoration.
A response-side refresh tuple is part of that protocol state, not a generic error payload.
When one target reuses the same envelope family across URL, body, response, and cookie, separate packet framing from inner crypto and prove both.

## Challenge primary key and round binding

Identify the server-issued challenge id / token that keys the round as early as headers or challenge HTML allow.

Rules:

1. prefer the server value over any client-generated UUID of similar shape
2. thread the same id through initialize/report/verify/business packaging for that round
3. keep cookies, host-owned materials, and grants on that same round key
4. after gateway accept or explicit expiry, treat the id as consumed; capture a new round for new causal tests
5. record ownership with `references/parameter-ownership-playbook.md`

HTTP `200` with punish/challenge headers or punishment HTML remains an intercept, not business success.
HTTP `200` with schema-valid JSON and constant filler values matching the unsigned control remains an intercept, not business success.

## Fast execution path

1. Freeze one fresh two-stage trace.
   Save:
   - entry HTML
   - challenge script URLs or inline challenge code
   - linked config JS or encrypted bootstrap blobs when present
   - initial cookies
   - post-challenge cookie and storage state
   - one failing business response that carries refresh fields when present
   - one preflight token request and response when present
   - one business request and response

   Keep all of those artifacts on one session chain unless reuse is separately proven.
   Do not splice entry HTML, initial cookies, challenge scripts, generated cookie state, preflight tokens, and business replay from neighboring sessions just because their shapes still look compatible.
   If the failure page points to a config asset or encrypted bootstrap variable, freeze that asset on the same session chain too instead of redownloading it later from a detached client because the URL looked static.
   If the same business route first returns a machine challenge and then succeeds after local refresh, freeze that fail -> refresh -> success triplet before searching for alternate endpoints.
   Before broad environment patching, pagination scaling, or runtime-shrink work, prove one minimal business replay on that exact fresh chain.

2. Separate seven proof layers.
   Keep these as distinct questions:
   - bootstrap-config decode
   - environment model
   - state transition
   - packet framing
   - key normalization
   - inner cipher
   - business plaintext or decoded JSON

3. Map the envelope family once.
   For each related field, record:
   - wire field name
   - version marker or fixed prefix
   - checksum scope
   - alphabet or byte remap
   - state-derived prefix or slice
   - inner encrypted segment
   - payload anchor or parser rule

4. Prove state dependency explicitly.
   Check whether the URL param, body field, or cookie can be rebuilt from business plaintext alone, or whether they also need current state bytes, storage state, challenge outputs, or a response-side refresh tuple from the immediately previous failure.

5. Validate the family with small checkpoints.
   Use exact checks such as:
   - cookie length or segment count
   - token length or format
   - checksum OK
   - expected prefix length
   - JSON anchor found
   - expected schema keys present

## High-value checks

- Verify whether several fields share one custom alphabet or packet prefix instead of independent encoders.
- Verify whether the business response itself acts as the refresh oracle: same URL fails with a machine challenge, local refresh consumes that tuple, and the same URL then succeeds.
- Verify whether the checksum covers plaintext, ciphertext, framed body, or the whole outer packet.
- Verify whether the response payload starts at byte zero or only after a fixed or state-derived prefix.
- Verify whether a linked config JS or short bootstrap blob hides encrypted config that later expands into keys, ivs, salts, cookie names, or compatibility constants.
- Verify whether the apparent AES key or iv is direct, sliced, concatenated, wrapped, XOR-masked, length-decorated, or otherwise normalized before use.
- Verify whether the preflight token response uses the same decode chain as the later business response.
- Verify whether the environment-bound cookie is just a stored token or a structured packet with several typed segments.
- Verify whether the server returns only seed fields while the decisive replay token remains locally derived and must be merged back into the same cookie or header bundle.
- Verify whether session-like or fingerprint-like cookies are locally minted from UUID variants, fingerprint vectors, or config-derived constants instead of server-issued as opaque values.
- Verify whether an accepted bundle hash, version tag, or compatibility token is an embedded constant rather than the digest of the file you just fetched locally.
- Verify whether submit or verify tokens printed in the challenge HTML are bound to that document. A previous page's page id, seq, or callback token can return HTTP `200` with an empty or still-challenged body.
- Verify whether an empty string field is still written into the pre-cipher object. Omitting the key is not the same as sending `""`.
- Verify whether ciphertext or packet length shifted by one field or cipher block; that often diagnoses a field-set mismatch, not a wrong cipher.
- Verify whether schema-valid JSON is still the unsigned filler sentinel. Constant values across every row are punish, not transport success.

## Page-bound submit tokens

Some verifier posts accept a ticket plus a document-scoped id harvested from the current challenge HTML.

Rules:

1. freeze the token from the same document that displayed the challenge
2. do not carry a previous page's token just because the field name and length still look valid
3. treat HTTP `200` with empty business bytes or remaining challenge chrome as silent reject, not a grant
4. the downstream business page or JSON schema is the grant oracle only after values are diverse versus the unsigned filler sentinel

This is a same-session bind, not a reason to invent a new endpoint.

Also apply this when the challenge HTML itself embeds a short rotating public token (hex, nonce, or quoted constant) and a local named export looks like the submit hasher:

5. freeze the token from the same document response that will back the submit; a previous screenshot or saved HTML of the same length is stale
6. a GET of the challenge document can rotate the token; hash and POST on that response without a second document GET
7. if the named export prepends `Date.now()` or appends local PRNG bytes, treat it as a decoy wrapper until a same-session live test hits; try the inner hasher on the current document token first

## Answer-accept versus complete latch

Some check or submit JSON splits "the number is correct" from "this challenge is marked complete".

Rules:

1. Treat answer-accept (`status`, `status_code`, `message`, `state`, or equivalent) and complete (`finish`, `done`, `complete`, or equivalent) as separate oracles.
2. A cookie-only POST of the answer can accept while complete stays false.
3. Warm GET the challenge document on the same session jar before or with the check POST, then require both flags.
4. If that document GET also rotates a submit token, the page-bound token rule still wins: hash and POST that response without a second document GET.
5. Stops when no complete flag exists, or complete is documented as an all-course flag rather than this challenge.

Negative control: skip the document GET, keep the same cookie and answer; accept can stay true while complete stays false. Do not call collector success until both oracles pass.

## Issued-challenge consumption and dual rate fields

Some verifiers issue a round artifact (image, token, puzzle, work factor) and keep a **session pass-rate** that later business pages consume. Issuance itself can increment the denominator.

Split three events before changing the answer algorithm:

| Event | Typical wire | Session-rate effect | Next move |
|---|---|---|---|
| Issue then skip | GET/init of a new challenge, no verify POST | often counts as a miss | do not continue this session; mint a fresh chain or submit the issued round |
| Issue then wrong answer | verify semantic reject | often only fails this round; browser re-issues | retry a **new** issued round on the same chain |
| Issue then accepted answer | verify semantic accept | may still expose a **cumulative** rate | send the first downstream page only if that cumulative stays above the proved floor |

Rules:

1. Freeze one issued round and consume it. An unused fetch is not a free refresh.
2. Confidence filters (weak contrast, low margin, OCR doubt) that skip submission on a session you will keep using are session poison, not accuracy hygiene.
3. If confidence is too low to submit, abandon the session. Do not leave the artifact unused and then paginate.
4. The same field name (`rate`, `score`, `percent`, `message`) can mean two things: on accept, a **cumulative session floor**; on reject, **this-answer closeness**. Prove the split with one unused-issue control and one wrong-answer control.
5. Verifier accept plus a cumulative below the page-stated floor (commonly 90% or 95%) is not a business grant. The next list/detail call 403s or returns punish HTML. That is a session-gate, not proof the coordinate algorithm is wrong.
6. Sequential pages may each require a freshly consumed challenge on the **current** chain. Identical page values across sessions do not authorize jumping to page N.

Negative control: issue twice, submit once correctly. If the accept body shows a simple fraction such as `1/2` or `2/3` and the next business page fails, unused issuance is on the pass-rate counter. Contrast with: submit a known-wrong answer, then a correct answer on a newly issued round; if the next page still passes, wrong-answer retry is legal and skip-to-refresh is not.

## Dual gate note

App signer gates and challenge verifier gates can be independent:

- browser XHR may require both
- challenge-retry replay may require only the verifier artifact
- recovering one gate never proves the other

Also split verifier gateway accept, server grant presence, and business-oracle pass. Gateway accept alone is not delivery.

Record gates separately in handoff notes. See `references/verifier-replay-playbook.md` layered acceptance.

## Common traps

- treating the cookie as a copied browser value instead of a reproducible protocol artifact
- replacing the server challenge id with a freshly generated UUID because the format "looks right"
- calling HTTP `200` business success while punish/challenge headers or punishment HTML remain
- calling HTTP `200` plus schema-valid JSON a grant while every row is the unsigned filler sentinel
- treating an application-level challenge subcode as a generic failure and hunting a new endpoint before retrying the same route with refreshed state
- submitting a previous document's page id, seq, or callback token and calling the resulting `200` empty body a grant
- calling check-API answer-accept a completed challenge while a sibling `finish` / `done` / `complete` flag stays false because the document was never GETed on that jar
- fetching a new challenge image or token and skipping verify because confidence was low, then treating the later 403 as an algorithm miss
- reading reject closeness and accept cumulative through one `rate` field as if they were the same metric
- hashing a previously saved HTML constant of the same length after a later document GET has rotated the live token
- submitting a named local wrapper whose preimage includes `Date.now()` or PRNG bytes the server never received
- mixing entry HTML, cookies, challenge code, generated state, or preflight tokens across sessions because each artifact still looks fresh in isolation
- leaving the fresh challenge chain to chase offline environment patches before one minimal live replay is proven
- proving only the inner cipher and missing the outer version, checksum, or alphabet layer
- dropping an empty-but-present field to match a remembered ciphertext length
- treating ciphertext length as algorithm proof instead of a field-set probe
- assuming the URL param and body field are unrelated when they are siblings in one packet family
- parsing decrypted bytes as JSON immediately when the real payload starts after a prefix
- assuming business plaintext alone can rebuild the request while hidden state bytes still affect the outer envelope
- updating only the derived token while leaving its seed, timestamp, version, or name fields stale, or updating the seed fields without regenerating the dependent replay artifact
- using the right entropy class but the wrong structure, such as a plain UUID where the client inserts check digits, prefixes, or fixed-width segments
- recomputing a compatibility hash from local asset bytes when the runtime actually uses an embedded id or normalized constant

## Delivery guidance

Preferred delivery shape:

1. Python collector with explicit staged bootstrap: entry, local challenge execution, preflight token when needed, business request, local response decode
2. tiny local JS helper only for unrecovered challenge or packet-family logic when Python porting is not yet cheaper
3. no browser dependency in the final path

When the route itself returns a machine refresh contract, the staged path may be:

`business request -> parse refresh tuple -> local refresh helper -> retry same request -> local response decode if needed`

## Minimal handoff notes

Report these items explicitly:

- which challenge output becomes protocol state
- which response-side refresh tuple, if any, must be consumed before retrying the same route
- which bootstrap config fields or normalized constants drive keys, ivs, checksums, or minted cookie structure
- which cookie, storage item, token, or header is derived from that state
- which fields belong to the same envelope family
- exact packet-family order: version, checksum, alphabet, prefix, cipher, payload anchor
- which later fields still depend on current state bytes
- which artifacts, if any, were proven reusable across sessions
- which submit tokens are document-bound versus session-reusable
- whether check/submit splits answer-accept from complete, and whether a document GET is required for the complete flag
- whether an issued challenge must be consumed, whether unused issuance poisons a session pass-rate, and whether accept-rate versus reject-rate are different metrics
- which fixed checkpoints prove local reconstruction is correct
