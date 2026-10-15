# Verifier Replay Playbook

Use this reference when:

- data requests are gated behind captcha, one-shot verification, or click-order challenges
- there is no meaningful business signer, but requests still fail until a verifier passes
- browser clicks appear to unlock the next request

## Contents

- [Challenge-HTML business route](#challenge-html-business-route)
- [Core rule](#core-rule)
- [Multi-stage settle](#multi-stage-settle)
- [Working method](#working-method)
- [Transcript manifest](#transcript-manifest)
- [Sidecar discovery and controls](#sidecar-discovery-and-controls)
- [Sidecar ablation matrix](#sidecar-ablation-matrix)
- [Shared baseline and sparse delta](#shared-baseline-and-sparse-delta)
- [Real timeline](#real-timeline)
- [Dynamic assets and helper versions](#dynamic-assets-and-helper-versions)
- [Acceptance ladder](#acceptance-ladder)
- [Layered acceptance and grants](#layered-acceptance-and-grants)
- [Implementation order](#implementation-order)
- [Retry contract](#retry-contract)
- [Issued-image consumption](#issued-image-consumption)
- [Soft-reject diagnostic ladder](#soft-reject-diagnostic-ladder)
- [Smoke levels L1-L4](#smoke-levels-l1-l4)
- [Common traps](#common-traps)
- [Delivery rule](#delivery-rule)

## Challenge-HTML business route

When the business route itself returns challenge HTML instead of JSON:

1. freeze one fail -> solve -> success triplet on the same session chain
2. treat linked challenge scripts as same-session bootstrap assets
3. harvest the nearest replayable artifact, usually a rewritten URL or cookie header
4. only then model pagination or concurrency

If short and long tokens share one field name, use `references/dual-writer-param-playbook.md` before locking the product generator.

## Core rule

The verifier contract may be the whole ordered transcript, not only the final
answer, token, or track request.

Verifier-endpoint success alone may still be only an intermediate milestone.
Required warm-up, device, log, telemetry, or behavior sidecars and the first
downstream business acceptance are part of the same proof.

## Multi-stage settle

Some verifier and risk-control flows require several sidecar or collector-like
requests before the downstream business route trusts the session. Do not stop a
local runtime, timer loop, or transcript replay after the first non-empty output
when the clean browser trace shows more stages.

Compare these surfaces before rewriting the algorithm:

- sidecar request count and order
- body-size or frame-size sequence
- content type and wrapper shape
- response status and application acknowledgement
- state transition from one request to the next
- whether a later route-local sidecar fires after the first document or business page

If the browser trace is multi-stage and the local run is single-stage, first
inspect lifecycle, timers, input settle, response-cookie mirroring, and missing
sidecar branches. Token shape, cookie length, or one sidecar HTTP 200 is not
acceptance without the downstream consumer.

## Working method

1. classify the verifier family and failure surfaces before lifting fields:
   - slider, point-click, ordered-click, icon-select, sequence-select, rotate, or another verifier branch
   - same SDK or same challenge page can still expose multiple families; a model, mode, risk type, or protocol selector is a new family until proved otherwise
   - submit-count (one-shot versus multi-hit), coordinate space, and answer encoding family are discriminators, not cosmetic UI details
   - a sibling subtype may share a crypto or PoW shell while the answer schema is still new
   - old and new generations of one vendor can still have incompatible fields and proof builders
   - protocol, compute, perception, behavior, telemetry, session, and transport
2. freeze one verifier round end to end as one ordered transcript:
   - prehandle or load response
   - callback ids or random keys
   - asset URLs and downloaded images
   - config, device, warm-up, log, telemetry, and status routes
   - verifier token, work factor, or round id
   - complete profile baseline and later delta-shaped payloads when present
   - final verify request and response
   - the first downstream business request and response that consumes verifier output
3. inventory every observed request by sequence, initiator, session, role, state writes, and semantic response
4. determine what output authorizes the next business request and where it enters that request:
   - direct header, cookie, query, or body field
   - pre-sign or pre-encrypt plaintext that is later wrapped by another signer
5. determine the freshness model before reusing anything:
   - single-use versus reusable
   - same-round bound versus cross-round valid
   - coupled to page, body, timestamp, or signer context versus independent
6. use one-variable sidecar controls when the main proof looks correct but acceptance still fails
7. map every shared field or derived relation across baseline, sidecars, delta payloads, and final verify
8. split the answer path by verifier type:
   - point-click, icon-select, or sequence-select: prompt extraction, hit localization, proof packaging, and whether the wire wants one hit or an ordered list
   - slider or image-derived: restored-image coordinate, display coordinate, submitted coordinate, behavior trace
   - prove display versus natural or restored-image space before converting pixels into proof fields; a visible float bar is not the clickable image
   - prove which live writer is posted: piece CSS `left`, handle travel, or a scaled display value; they can be equal or they can differ
   - search the full canvas (`0 .. width - piece_width`); an arbitrary cap below the right edge misses real holes and latches onto leftover dark columns
   - a filled gap is a piece-sized rectangle. Score left/right **and** top/bottom edges. Tall dark objects in the same y-band are decoys
   - classify the wire encoding before porting numbers: float-plus-timestamp, integer-scaled pairs, and display-normalized clicks are different builders; a separate total passtime is not a per-click timestamp
9. separate declared timestamps and event deltas from real wall-clock elapsed time
10. solve or reconstruct the required outputs locally
11. validate fixed inputs at every stable encoding, signing, packing, and envelope boundary
12. replay the full verifier transcript in protocol form
13. send the downstream business request in the same round ordering with the resulting token, cookie, coordinates, or grant

## Transcript manifest

Record one complete accepted or best-known round with this shape:

```markdown
Verifier Transcript
- Round id or local capture id:
- Session scope:
- Active asset and helper hashes:
- Step 1: route, role, request hash, response family, state writes, elapsed offset
- Step 2: route, role, request hash, response family, state writes, elapsed offset
- Final verifier semantic result:
- First downstream consumer result:
```

For each step distinguish:

- request transport success
- application envelope success
- sidecar or telemetry acceptance
- final verifier acceptance
- downstream business acceptance

Do not collapse all of these into one `success` flag.

## Sidecar discovery and controls

When a correct-looking answer or track still fails, inventory adjacent request
families before tuning behavior again. Inventory is not collector membership.
Unknown risk-control defaults to reversing the rejected request, not adding
unproven URLs. Unproven extra routes are at most one per round, and only after
controlled omission changes the oracle. Required sidecars that pass omission
and restoration stay in the contract.

Candidate families:

- device or fingerprint collection
- log, status, telemetry, or risk-event upload
- warm-up, preflight, config, or time-sync calls
- resource-backed state initialization
- post-answer but pre-verify sidecars

Use browser initiators and wire order to identify candidates. Then run a narrow
control matrix:

1. preserve one accepted or human-confirmed answer path
2. block or omit one sidecar route family at a time
3. keep the session, answer, track, timing policy, and all other routes fixed
4. restore that route and repeat on a fresh round
5. compare final verifier semantics, not only the sidecar HTTP response

A sidecar becomes protocol-relevant when controlled omission changes the final
acceptance family and restoration recovers it. One correlation without a
negative and recovery control is not enough.

Keep header or transport exceptions route-local. A landing route that needs a
different header set does not prove that telemetry and verify routes need the
same exception.

## Sidecar ablation matrix

Before tuning answers or trajectories, freeze one ablation matrix for the same
session assumptions. Save it under the task cache as a secret-free table.

| condition | action | final verifier semantic | first downstream consumer | conclusion |
|---|---|---|---|---|
| full transcript | all required sidecars present | | | baseline |
| no telemetry/device domain | block or omit that host family | | | sidecar necessity |
| omit one warm-up or log stage | remove only that step | | | stage necessity |
| keep sidecars, drop final token field | omit one decisive verify field | | | structure family |
| keep structure, break shared baseline link | regenerate baseline and delta independently | | | consistency family |
| keep all packets, remove real waits | send declared multi-second track immediately | | | timeline family |

Rules:

- change one variable at a time
- record request order, elapsed offsets, and state writes for every row
- a sidecar HTTP 200 is not enough; record application acknowledgement and whether final semantics changed
- if omitting a sidecar flips a clean success into rejection, that sidecar is part of the contract
- do not start trajectory search while the matrix still has unresolved necessity or consistency questions

## Shared baseline and sparse delta


Some verifier families first upload a complete device or environment baseline
and later send a sparse delta, compact state token, or behavior update derived
from that baseline.

Build a shared-state contract before generating requests:

| Field class | Writer | Baseline use | Delta use | Relation | Scope |
|---|---|---|---|---|---|
| identity | bootstrap or profile builder | full | copied or retained | equal | round/session |
| time | clock or server seed | initial | monotonic update | derived | round |
| counter | collection stage | source | copied or transformed | derived | round |
| environment | profile builder | full | subset | subset | profile/round |
| checksum | packet builder | packet-local | packet-local | recomputed | request |

Use only observed categories and relations. Do not copy this example as a fixed
schema.

Prove whether the baseline is profile-, session-, or round-scoped. Establish one
baseline instance for that scope and make every dependent request in the round
derive from the same instance. Do not independently randomize fields that must
be equal, subsetted, monotonic, checksum-linked, or counter-linked across
requests.

Each packet can decrypt, parse, sign, and pass its own checksum while the whole
round still fails because the packets describe different device states. Packet
validity does not prove transcript consistency.

### Shared-state consistency checklist

Prove these before blaming answer or track quality:

- one session or round id binds init, sidecars, verify, and first consumer
- one complete baseline instance is created once for that scope
- sparse or delta packets derive from that same instance rather than a second random profile
- counters, gather costs, checksum seeds, or monotonic fields remain linked across packets
- dynamic fields that must match (ip, server time, local collect start, certify or round id slots) are copied, not re-rolled
- if each packet validates alone but the round fails, first repair consistency, not trajectory noise
- when multiple dynamic slots must describe one round, apply the same-world gate in `references/parameter-ownership-playbook.md`

If the baseline remains a captured opaque profile, route its provenance and
delivery classification through `references/opaque-runtime-profile-playbook.md`.

## Real timeline

Treat time as three separate surfaces:

- absolute timestamps written into payloads
- event deltas inside tracks or telemetry
- actual wall-clock delay between requests

A transcript that claims several seconds of interaction but sends every stage
immediately can be internally contradictory even when every timestamp is
well-formed.

Prove:

- monotonic ordering within each clock domain
- relationship between server time, local time, and event offsets
- actual wait before behavior completion, telemetry upload, and final verify
- whether retries require a new round or can reuse the current state

Use real waits only as long as the proved contract requires, and preserve any
user-defined hard timeout or honeypot cap.

### Timeline operations checklist

- retime captured tracks onto the current wall clock instead of replaying stale absolute timestamps
- keep declared interaction duration and actual sleep before verify in the same order of magnitude
- place telemetry completion before final verify when the clean transcript does so
- if a track claims about one second of motion, do not emit the whole chain in tens of milliseconds
- when retrying, decide whether the round can be reused or must be fully re-initialized

## Dynamic assets and helper versions

A changing script URL, asset suffix, or cache-busting path does not by itself
prove that the verifier algorithm changed.

Before re-reversing:

1. hash the active asset
2. compare the public helper or VM boundary
3. rerun deterministic fixed vectors
4. compare stage traces when the output changed
5. create a new helper version only when behavior, framing, or vectors diverge

Keep a tiny host-independent local JS or WASM helper when it is the narrowest
faithful implementation. Python must still own HTTP, session ordering, state,
timeouts, and acceptance checks.

## Acceptance ladder

Validate from narrow to final:

1. challenge or initialization response is semantically valid
2. required sidecars return their expected application-level acknowledgement
3. baseline and delta state relations hold
4. answer, behavior, and helper fixed vectors match
5. final verifier response contains the platform-specific accepted semantics
6. the first downstream business request consumes the verifier result

HTTP 200, a generic success envelope, a token-shaped value, or sidecar upload
acknowledgement cannot replace the final applicable gate.

Platform transport wrappers such as JSONP `callback({message:"success"})` or HTTP
200 are envelope success. Read the platform semantic bit (`PASS`/`REJECT`, risk
level, grant, inner `result`, fail count, or equivalent). Envelope success plus
semantic reject is structure-pass, not a solve. An outer status can accept while
an inner result still rejects.

Treat error or subcode changes as localization evidence. Prove their meaning
with controlled state changes; do not promote one target's codes into universal
verifier doctrine. Build a task-local semantic map with
`references/verifier-error-localization-playbook.md`.

### Downstream consumer contract

Verifier acceptance is intermediate until the first business request consumes it.

Record:

- which grant fields leave the verifier: token, cookie, query, header, body, or success alias
- where those fields enter the original business URL or follow-up API
- whether alternate aliases exist and which ones the live browser actually sends
- the business-pass oracle: content fingerprint, magic bytes, non-challenge HTML markers, or JSON schema
- same-round packaging: do not mix grants from round A with consumers from round B

If verifier semantics pass and the consumer still returns challenge HTML or empty shells, debug packaging and session binding before reopening answer generation.

## Layered acceptance and grants

Record four booleans separately. Do not collapse them into one "success":

1. `precursorAccepted` — load/init/report or equivalent accepted the round
2. `verifierGatewayAccepted` — verify/submit semantic accept for this challenge
3. `serverGrantPresent` — server issued the pass cookie/token on that response
4. `businessOraclePassed` — original business route returns non-challenge business data

Rules:

- gateway accept without business pass is stage success only
- server grants are `server-owned`: parse them; do not hardcode or cross-round reuse (`references/parameter-ownership-playbook.md`)
- HTTP 200 on verify, report, or business with punish/challenge headers or challenge HTML is not business pass
- a consumed challenge id cannot host a second causal ablation row

## Implementation order

When building a browser-free path, prefer:

```text
parser + round key -> jar/context -> precursors -> host-owned probes -> verify transport -> parse grant -> optional post-grant report -> business oracle -> fresh round
```

Keep fixed vectors per layer. Full detail: `references/parameter-ownership-playbook.md`.



## Retry contract

When verify fails inside one round and a retry is legal:

1. regenerate the materials that the same-world gate marks as per-attempt, not just one header
2. emit any required failure/report sidecar once before the next verify, in the live order
3. keep roundKey, identity cookies, and protocol profile unchanged unless the server issued a new round
4. record `attemptSequence` and the actual attempts used, not only configured max attempts
5. do not raise max attempts to hide a wrong backend, wrong profile, or broken lifecycle

If a clean success sample passes on attempt 1 or 2 while local needs a large attempt budget, treat that gap as ownership/backend evidence first.

## Issued-image consumption

When the browser issues a challenge image or token before each later page:

1. consume every issued round with a verify POST. Do not GET a fresh image to "skip a hard one" on a session you will keep using
2. a submitted wrong answer may be retryable on a newly issued round; an unused issue often is not
3. if a confidence filter fires, abandon the session instead of leaving the artifact unused
4. split accept-body cumulative pass-rate from reject-body closeness; the same field name can carry both
5. the first downstream page is the grant oracle. Verifier accept below the stated session floor is not pagination success
6. search-range, four-edge geometry, and coordinate-space proof live in the working-method slider branch; do not retune tracks until unused-issue is ruled out

See `references/challenge-state-envelope-playbook.md` for the session-rate table.

## Soft-reject diagnostic ladder

For semantic rejects that still return HTTP 200 or a soft envelope, walk this order before track folklore:

1. fresh roundKey and unconsumed challenge state
2. protocol profile identity versus the success class
3. transport, jar, and shared-state consistency
4. request-slot materials and canonical bytes
5. host lifecycle / token rebuild blocks
6. behavior or trajectory last

Stop at the first broken layer. Pair with `references/parameter-ownership-playbook.md` same-world and profile gates.

## Smoke levels L1-L4

| Level | Meaning | May claim |
|---|---|---|
| L1 | helper emits non-empty local artifacts; isolated network if required stays zero | local smoke only |
| L2 | fresh verify/check accepted semantically | verifier stage success |
| L3 | server grant present when required and first business oracle passes | browser-free round success |
| L4 | multiple independent fresh rounds keep the hard-gate rate | stability evidence |

Package only at L3+. L1/L2 must be named as intermediate.

## Common traps

- raising retry budgets to compensate for profile or backend mismatch
- calling L1 helper smoke a collector or business pass
- tuning tracks before the soft-reject ladder clears session/profile/material layers
- hunting for a fake business-layer signer while ignoring the verifier
- automating clicks instead of understanding the verifier payload
- treating the verifier as UI-only behavior
- treating verifier-response success as proof that the business flow is solved
- tuning trajectories repeatedly before checking omitted warm-up or telemetry sidecars
- treating sidecar HTTP success as proof that its state matches the final verify request
- building the complete baseline and sparse delta from independently randomized state
- fabricating plausible timestamps while sending the transcript with impossible wall-clock timing
- re-reversing every dynamic asset path before checking boundary and fixed-vector parity
- mixing token, images, callbacks, or proof fields across adjacent verifier rounds
- treating prompt OCR or image matching alone as proof of verifier success
- mixing restored-image pixels, rendered UI coordinates, and submitted proof coordinates
- reusing a verifier artifact without proving whether it is fresh, single-use, or same-round bound
- injecting a verifier artifact after sign or encrypt when the live flow feeds it into the pre-sign plaintext instead
- carrying fields from one verifier family or generation into another because the page role looks similar
- reusing slider distance or trajectory builders on a select-family challenge because they share a vendor SDK
- treating envelope `success` or JSONP wrapper success as verifier-semantic pass
- treating an outer status accept as a solve when an inner result or fail count still rejects
- reusing a sibling subtype crypto shell as proof that the answer schema is the same
- submitting coordinates from a previous load after a new challenge image was issued
- fetching a new challenge image and skipping verify because contrast or margin looked weak
- capping gap search below `width - piece_width` and then blaming the edge scorer
- treating accept-body `rate` as this-answer closeness, or reject-body `rate` as the session floor
- normalizing clicks against the natural image size when the proof uses the displayed surface
- treating automation-contaminated hand-slide failures as trajectory truth
- continuing trajectory search after structure and sidecars already validate and only a risk-like semantic remains
- declaring delivery complete at verifier-semantic success without a same-round downstream consumer proof
- ignoring environment risk after consecutive rejects on one exit or automation profile
- treating a server grant cookie/token as locally computable
- reusing a consumed challenge id after gateway accept as if it were a fresh ablation oracle
- labeling length/charset resemblance as the verify ciphertext algorithm

## Delivery rule

Do not simulate UI interaction in the final solution. Reproduce the verifier as
an ordered protocol transcript. Report required sidecars, shared-state rules,
actual timing, helper boundaries, final semantic acceptance, and the first
downstream consumer. Label captured-profile delivery as snapshot-driven rather
than fully algorithmic.

Also report:

- ablation matrix path
- task-local error semantic map
- positive-sample hygiene grade for any human or browser oracle
- whether environment risk was implicated
- dual-runtime helper packaging when a local JS or WASM helper remains
