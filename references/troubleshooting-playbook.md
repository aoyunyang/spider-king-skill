# Troubleshooting Playbook

Use this file when replay logic almost works but still fails.

## Failure surface first

When the failing layer is unclear, read `references/failure-surface-taxonomy.md`, choose one primary surface, then jump to the matching symptom section below. If the next experiment is unclear, take exactly one Stuck next action from that file before adding routes or opening another browser. Do not rewrite signer logic while `egress-environment`, `transport-admission`, `session-chain`, or `request-contract` still explain the oracle.

For local-versus-positive-sample disagreement, use `references/positive-sample-ablation-playbook.md` after sample hygiene.

## Contents

- [Failure surface first](#failure-surface-first)
- [Ordered failure ladder](#ordered-failure-ladder)
- [Symptom routing](#symptom-routing)
- [Multi-context login and activation](#multi-context-login-and-activation)
- [Async export and report download](#async-export-and-report-download)
- [Verifier and sample hygiene](#verifier-and-sample-hygiene)
- [Final rule](#final-rule)

## Ordered failure ladder

When replay almost works, walk this order before rewriting large signer blocks. Full stage detail lives in `references/signer-parity-chain-playbook.md`.

1. session / cookie freshness and outbound `Cookie` parity
2. missing bootstrap, warmup, or token prefetch on the same chain
3. timestamp / nonce precision and reuse contract
4. header, body, and serialization contract
5. environment-bound inputs only after they are proved to enter the signer or verifier
6. pacing, rate limits, and egress-only flips

For local vs browser signer mismatch, compare the seven-stage parity chain (inputs → join → time → nonce → key → intermediates → final encoding/slot) and stop at `firstDivergence`.

Silent reject: HTTP `200` + empty business body / wrong content-type / stable business error is not success. Name a primary surface via `references/failure-surface-taxonomy.md`.

## Symptom routing

### `403`, `412`, `429`

- compare headers
- compare cookies
- compare pacing
- compare sign freshness
- compare whether the challenged document URL itself succeeds after local bootstrap instead of after a guessed API pivot
- if failures start only after hooks or breakpoints, suspect observer effect and recapture a clean baseline
- if the same implementation succeeds or fails by exit, browser-check the same route on the same exit before rewriting protocol logic

### `200` with business error

- compare query and body serialization
- compare timestamp precision
- compare transport wrapper outputs
- compare whether a verifier or cookie refresh step is now missing
- if subcodes change across attempts, map the ladder instead of treating each failure as unrelated noise
- if the body is empty or non-business while status is `200`, treat it as silent reject and run the ordered failure ladder before claiming signer success
- when local sign bytes disagree with browser, use `references/signer-parity-chain-playbook.md`

### `200` with gibberish or strings

- check decrypt path
- check fonts
- check hint arrays for page-specific header clues
- treat HTTP 200 plus strings, hints, or mixed-type arrays as a failed page, not a parse quirk
- if sibling pages already pass on both HTTP versions, do not escalate the last page to a transport family first
- if raw bytes decode cleanly but saved files or terminal output still look garbled, separate local encoding or render issues from target-side decode gates before changing the protocol hypothesis

### the chosen login or session validator always looks valid

- tamper one decisive cookie, token, or session field and rerun the validator as a negative control
- if empty or tampered state still returns `200` or a page shell, treat that route as a false validator rather than proof of login
- find one stricter authenticated business endpoint that fails deterministically on bad state before persisting cookies or session artifacts

### first request works, replay fails

- check rotating cookies
- check in-memory refresh fields
- check whether bootstrap must run before each request
- prove cookie provenance before blaming the signer
- keep first-hop HTML, linked bootstrap assets, seed cookies, and generated state on one fresh session chain before widening environment patches
- if runtime egress exposes a full outbound `Cookie` header, compare that against the jar before blaming one cookie name or one refresh helper

### login looks accepted, but the target business route still redirects or rejects

- treat grant tickets, redirect handles, async follow-up URLs, and auth acks as authentication artifacts, not finished session proof
- capture post-auth callbacks, redirect exchanges, or session-establishing follow-up requests before changing the signer again
- diff cookie state before and after each post-auth hop so you know which step actually materializes the usable session

### local helper matches names, not outputs

- move back to fixed-input comparison
- assume helper is patched until proven standard
- live replay remains the authority; fewer thrown errors or more browser-shaped output is only a hint

### local helper fails in a way that looks like target blocking

- check local runtime integrity first: broken symlinks, placeholder link files from copied `node_modules`, missing transitive deps, bad paths, and encoding-induced path resolution failures
- rerun the helper on frozen inputs and separate helper bootstrap failure from protocol failure before changing the signer hypothesis
- if the helper cannot load its own dependency tree, repair the local runtime before reopening target-side reverse work

### clean capture works, hooked capture fails

- suspect observer effect
- remove broad global hooks and debugger pauses
- capture one untouched baseline request and response
- move instrumentation outward toward the request boundary
- prefer initiator stacks and diffs before invasive monkey patches

### async artifact never appears or cannot be matched to one attempt

- establish the observation baseline first: mailbox cursor, webhook receiver, queue offset, or polling window
- trigger the flow only after the baseline is live
- diff pre-trigger and post-trigger artifacts so the attempt-to-artifact mapping is explicit
- treat timing, cursor state, and delayed delivery as part of the protocol workflow, not just operational noise

### user-defined latency threshold or honeypot budget

- if the user says a request or helper step that crosses `N` seconds should be treated as suspicious, encode that as a hard timeout in the collector
- abort immediately when that threshold is crossed instead of silently retrying it away
- report where the threshold is enforced so the handoff reflects the real safety contract

### the same request degrades into password-like or field-like errors after tight pacing

- repeat one previously understood request after a sufficient cooldown before changing fields that already matched
- compare the failure text or subcodes across slow and fast pacing, not just across code edits
- suspect punitive disguise or abuse cooldown when a field-looking error appears only after repeated attempts
- prefer cookie refresh or existing-session reuse over aggressive relogin loops when the target is rate-sensitive

### intermittent access denied or route reset by exit

- classify with `references/failure-surface-taxonomy.md` before algorithm rewrites

- keep implementation, session shape, and target route fixed while changing only the network exit or cooldown
- browser-check the document or business route on the same exit before blaming local signer, verifier, CSRF, or form serialization
- if browser and protocol both fail on that exit, label the condition `egress-gated` and change exit or wait; do not rewrite algorithms first
- if browser succeeds but protocol fails, compare transport identity coherence, sidecar count, cookie transitions, and exact request serialization
- save the last successful output separately from fresh failure diagnostics so a bad exit does not overwrite accepted proof

### error or subcode shifts as each patch lands

- treat the changing sequence as evidence that one gate has been cleared and the next gate is now exposed
- distinguish "same failure again" from "different failure after progress"
- update the missing-gate hypothesis before rewriting the signer, wrapper, or bootstrap from scratch
- use the new code to decide whether the next move is cookie provenance, session admission, wrapper slot placement, verifier state, or simple pacing backoff



## Multi-context login and activation

### login works, business data is wrong

- confirm tenant, role, and data-range separately
- reread final identity; do not stop at the switch API envelope
- route to `references/multi-context-session-playbook.md`

### switch succeeds but scope is unchanged

- diff the full activation payload against a known-good UI capture
- check whether a type field must accompany the value field
- refuse export until identity reread matches the task config

### password login looks rejected after a correct password

- verify RSA or other password encoding alphabet and length
- confirm the modulus and exponent were parsed from the current login page
- route encoding questions to `references/crypto-patterns.md`

### reused cookies scrape the wrong shop

- run a pre-collection identity probe
- do not share one session across concurrent context switches
- re-activate and re-validate before scrape



## Async export and report download

### create returns 200 but no new task

- diff method, query versus body placement, content-type, and referer
- confirm signer coverage uses the same serialization
- snapshot history before and after create
- route to `references/async-export-job-playbook.md`

### export finishes too fast with wrong dates or fields

- check whether polling reused a pre-create historical task
- require create-returned id or post-create new id plus condition match

### download is not the expected artifact

- inspect whether the body is JSON error, login page, or challenge page
- verify magic bytes or content family before parse
- confirm secondary verify and side-channel material belong to this run

### file parses but columns are incomplete

- compare requested field count to downloaded columns
- fail closed before persistence
- re-check whether create dropped the field array during serialization or signing

### side-channel codes keep failing

- baseline mailbox or message cursor before send
- accept only post-baseline messages
- do not mix login-scene codes with download-scene codes

## Verifier and sample hygiene

### verifier semantic looks good, business still challenged
- prove first downstream consumer packaging on the same round
- check grant placement: query, cookie, header, body, or success alias
- define business-pass by content fingerprint, not only HTTP status
- read `references/verifier-replay-playbook.md` downstream consumer contract

### sidecars return 200 but final verify still rejects
- distinguish transport success from application acknowledgement
- run the sidecar ablation matrix before track search
- check shared baseline versus sparse delta consistency
- read `references/verifier-error-localization-playbook.md`

### ordinary browser passes, automation or protocol fails
- grade samples: clean-success versus contaminated-failure
- remove hooks and debug ownership before collecting another positive oracle
- consider exit reputation and consecutive reject history as environment risk
- read `references/positive-sample-hygiene-playbook.md`

### reject code changes after each local patch
- treat code shifts as localization evidence, not random noise
- map each code to structure, sidecar, consistency, timeline, answer, or environment with one-variable ablations
- do not import another job's code table as universal truth

### dynamic helper path changed and output broke
- hash assets and compare helper boundaries before full re-reverse
- rerun fixed vectors
- only then rebuild the local helper version


### browser shows more bootstrap stages than local

- diff stage count, timing, body size/framing sequence, and state transitions before rewriting signers
- drain timers, promises, and input settle on one session chain; do not stop after the first local post if the browser continues
- only after repeated independent business successes may a missing stage be labeled non-gating for the current route; keep the evidence
- classify unsettled multi-stage gaps under `session-chain` or `signer-confidence` via `references/failure-surface-taxonomy.md`, and follow the multi-stage settle rule in `references/workflow-overview.md` (cross-cutting; not a separate phase number)

## Final rule


When stuck, name one primary surface in `references/failure-surface-taxonomy.md`, then take exactly one Stuck next action from that file. Do not randomly mutate five things at once, and do not bulk-add unproven extra routes.
