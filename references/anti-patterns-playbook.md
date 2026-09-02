# Anti-Patterns Playbook

Use this file when a shortcut feels faster than the next proof.

This file exists because soft principles are easy to agree with and easy to ignore.
Counterexamples constrain better when they answer four questions:

1. what tempting move is showing up
2. why it is false progress
3. what the smallest honest next move is
4. what one self-check can stop the slide

## Contents

- [How to use it](#how-to-use-it)
- [Anti-pattern 1: Browser-backed replay dressed up as a temporary collector](#anti-pattern-1-browser-backed-replay-dressed-up-as-a-temporary-collector)
- [Anti-pattern 2: Hardcode the current rotating cookie, token, or header because it works once](#anti-pattern-2-hardcode-the-current-rotating-cookie-token-or-header-because-it-works-once)
- [Anti-pattern 3: Scale after one lucky success](#anti-pattern-3-scale-after-one-lucky-success)
- [Anti-pattern 4: Jump multiple rungs because the current one is frustrating](#anti-pattern-4-jump-multiple-rungs-because-the-current-one-is-frustrating)
- [Anti-pattern 5: Install broad hooks before a clean baseline](#anti-pattern-5-install-broad-hooks-before-a-clean-baseline)
- [Anti-pattern 6: Reverse the visible helper or visible param instead of the wire mutation point](#anti-pattern-6-reverse-the-visible-helper-or-visible-param-instead-of-the-wire-mutation-point)
- [Anti-pattern 7: Treat helper load success, fewer exceptions, or browser-shaped output as protocol success](#anti-pattern-7-treat-helper-load-success-fewer-exceptions-or-browser-shaped-output-as-protocol-success)
- [Anti-pattern 8: Overwrite stable scaffolding with volatile captures](#anti-pattern-8-overwrite-stable-scaffolding-with-volatile-captures)
- [Anti-pattern 9: Believe page text that a cookie or session id participates in the signer](#anti-pattern-9-believe-page-text-that-a-cookie-or-session-id-participates-in-the-signer)
- [Anti-pattern 10: Treat a standard digest library as done because the algorithm name matches](#anti-pattern-10-treat-a-standard-digest-library-as-done-because-the-algorithm-name-matches)
- [Anti-pattern 11: Treat account login cookies as the finished business session](#anti-pattern-11-treat-account-login-cookies-as-the-finished-business-session)
- [Anti-pattern 12: Trust the switch API and skip final identity reread](#anti-pattern-12-trust-the-switch-api-and-skip-final-identity-reread)
- [Anti-pattern 13: Submit UI labels as protocol ids or pick the first fuzzy match](#anti-pattern-13-submit-ui-labels-as-protocol-ids-or-pick-the-first-fuzzy-match)
- [Anti-pattern 14: Treat HTTP 200 as async export create success](#anti-pattern-14-treat-http-200-as-async-export-create-success)
- [Anti-pattern 15: Reuse the newest historical export task](#anti-pattern-15-reuse-the-newest-historical-export-task)
- [Anti-pattern 16: Promote regenerate traffic into the first-create contract](#anti-pattern-16-promote-regenerate-traffic-into-the-first-create-contract)
- [Anti-pattern 17: Treat the only decompiled short signer as the only writer](#anti-pattern-17-treat-the-only-decompiled-short-signer-as-the-only-writer)
- [Anti-pattern 18: Call sample exact replay "protocol automation"](#anti-pattern-18-call-sample-exact-replay-protocol-automation)
- [Anti-pattern 19: Keep reversing encrypt after redirect already carries the artifact](#anti-pattern-19-keep-reversing-encrypt-after-redirect-already-carries-the-artifact)
- [Anti-pattern 20: Merge app signer and WAF or challenge verifier into one problem](#anti-pattern-20-merge-app-signer-and-waf-or-challenge-verifier-into-one-problem)
- [Anti-pattern 21: Treat automation-browser hand-slide failures as trajectory truth](#anti-pattern-21-treat-automation-browser-hand-slide-failures-as-trajectory-truth)
- [Anti-pattern 22: Keep tuning tracks after structure is already accepted](#anti-pattern-22-keep-tuning-tracks-after-structure-is-already-accepted)
- [Anti-pattern 23: Call verifier-semantic success a finished collector](#anti-pattern-23-call-verifier-semantic-success-a-finished-collector)
- [Anti-pattern 24: Call MCP families that are only on disk](#anti-pattern-24-call-mcp-families-that-are-only-on-disk)
- [Anti-pattern 25: Force dual browser first-pass on pure artifacts](#anti-pattern-25-force-dual-browser-first-pass-on-pure-artifacts)
- [Anti-pattern 26: Run chrome-devtools and js-reverse target actions together](#anti-pattern-26-run-chrome-devtools-and-js-reverse-target-actions-together)
- [Anti-pattern 27: Treat environment provider start as protocol success](#anti-pattern-27-treat-environment-provider-start-as-protocol-success)
- [Anti-pattern 28: Treat passive capture or PCAP as signer recovery](#anti-pattern-28-treat-passive-capture-or-pcap-as-signer-recovery)
- [Anti-pattern 29: Keep MCP browser runtime inside the collector](#anti-pattern-29-keep-mcp-browser-runtime-inside-the-collector)
- [Entry format for new anti-patterns](#entry-format-for-new-anti-patterns)
- [Final rule](#final-rule)

## How to use it

When you notice yourself thinking:

- "I can just ship this temporary browser-backed collector"
- "the cookie looks fresh enough"
- "the helper loads now, good enough"
- "I should jump to a heavier runtime"
- "I already got page 1 once, let's scale"

stop and match the temptation below before editing more code.

## Anti-pattern 1: Browser-backed replay dressed up as a temporary collector

Temptation:

- call page `fetch`
- drive CDP or Playwright for the final request
- keep a browser profile around as a hidden dependency

Why it is false progress:

- the unresolved protocol state stays unexplained
- replay proof depends on a page world, not local artifacts
- the handoff becomes impossible to reason about or maintain

Smallest honest next move:

- identify the decisive artifact the browser is adding
- harvest that artifact at the nearest stable boundary
- hand it back to Python for the real HTTP replay

Self-check:

- if the browser process disappears, does the collector still work?

## Anti-pattern 2: Hardcode the current rotating cookie, token, or header because it works once

Temptation:

- paste the current cookie header into config
- freeze one token or sidecar that still happens to pass
- treat a current sample as a refresh strategy

Why it is false progress:

- it proves only one snapshot, not writer or refresh path
- expiry, slot placement, or session binding remain unknown
- later failures get misdiagnosed as signer bugs

Smallest honest next move:

- prove who writes the artifact
- prove where it is consumed on the wire
- rebuild or refresh only the authoritative artifact that replay actually needs

Self-check:

- can the collector recover the artifact again without manual recapture?

## Anti-pattern 3: Scale after one lucky success

Temptation:

- start pagination after one good page
- add concurrency before one stable replay path exists
- shrink runtimes before a fresh chain is proven twice

Why it is false progress:

- one lucky pass can hide stale state, session-chain coupling, or page-specific tolerance
- failures later get mixed together with scale effects

Smallest honest next move:

- replay the same minimal request at least twice
- prove page 2 or one next cursor with the same collector path
- only then widen scope

Self-check:

- does the same single-page request still succeed on a fresh repeat?

## Anti-pattern 4: Jump multiple rungs because the current one is frustrating

Temptation:

- Python mismatch -> broad embedded runtime
- local runtime loads -> broad host patching
- one blocked route -> route-wide transport cargo cult

Why it is false progress:

- the real blind spot stays unnamed
- comparison baselines get destroyed
- heavier layers hide simpler unresolved mistakes such as slot placement or serialization

Smallest honest next move:

- write the ladder log
- prove the exact failure at the current rung
- move up one rung only

Self-check:

- can you name the exact blind spot the heavier layer is supposed to answer?

See `references/escalation-ladder-playbook.md` for the rung model.

## Anti-pattern 5: Install broad hooks before a clean baseline

Temptation:

- inject global hooks immediately because the target looks hard
- set broad breakpoints before one clean request is captured
- treat hook-induced failure as evidence the site is browser-only

Why it is false progress:

- observer effect can change timing, identity, or verifier behavior
- the clean contract gets lost before it is frozen

Smallest honest next move:

- capture one untouched baseline request and response pair
- move hooks outward toward the narrowest stable boundary
- compare hooked and clean behavior explicitly

Self-check:

- did the failure mode change only after your instrumentation landed?

## Anti-pattern 6: Reverse the visible helper or visible param instead of the wire mutation point

Temptation:

- chase a page-level `sign` because it looks named
- code against the visible endpoint instead of the live route
- trust the business payload before wrapper rewrite

Why it is false progress:

- the real contract may live in a wrapper, interceptor, or egress mutation
- a correct blob in the wrong slot still fails

Smallest honest next move:

- trace the canonical mutation point
- capture the final wire-shaped request
- rebuild what actually crosses the boundary

Self-check:

- does the thing you are reversing exactly match what the wire sends?

## Anti-pattern 7: Treat helper load success, fewer exceptions, or browser-shaped output as protocol success

Temptation:

- token length looks closer
- the runtime throws less
- cookie shape looks more realistic

Why it is false progress:

- these are only local health signals
- they do not prove the real request replays

Smallest honest next move:

- run the real business request
- validate response semantics, not just status or shape
- repeat the replay

Self-check:

- does the actual target request now succeed repeatedly?

## Anti-pattern 8: Overwrite stable scaffolding with volatile captures

Temptation:

- replace user-maintained fixtures with fresh target blobs
- edit stable helpers directly with run-specific artifacts
- blur reusable code and volatile capture state

Why it is false progress:

- later diffs become unreadable
- the stable path gets contaminated by one run
- upgrade analysis loses its clean baseline

Smallest honest next move:

- keep fresh captures in task-local cache
- generate temporary runners from volatile artifacts
- update stable scaffolding only after the lesson is proven reusable

Self-check:

- could you rerun the diff from a clean stable base tomorrow?

## Anti-pattern 9: Believe page text that a cookie or session id participates in the signer

Temptation:

- hardcode `sessionid` into the token preimage because the page warns that it matters
- refuse to prototype an anonymous list collector until login is solved
- mix submit-account requirements into every list or detail request

Why it is false progress:

- page copy is not wire evidence
- list, detail, and submit chains often have different session contracts
- a wrong preimage wastes reverse time on a crypto problem that does not exist

Smallest honest next move:

- capture the real request with and without the claimed cookie
- classify fields from the wire: static, server time, signer output, account state
- keep anonymous collection available when the business response already succeeds without login
- require the session only for the chain that actually 401s or changes answers

Self-check:

- does removing the cookie change the business response, or only the later submit path?

## Anti-pattern 10: Treat a standard digest library as done because the algorithm name matches

Temptation:

- swap in stock MD5, SHA, or SM3 after seeing the name in source or UI text
- skip intermediate word checks once the digest length looks right
- port only the happy-path constants and ignore environment-selected branches

Why it is false progress:

- IV, round constants, packing masks, and compress masks are common rewrite points
- one wrong `ROTL` edge case can pass some pages and fail others
- browser-branch constants may differ from Node or fallback branches

Smallest honest next move:

- freeze one captured preimage and digest
- diff IV, constants, packing, and compress steps against the standard algorithm
- reproduce the browser branch locally before the Python port
- add a fixed-input self-check that fails loudly on standard-library substitution

Self-check:

- does the local standard library match the fixed sample, or only the bit length?

## Anti-pattern 11: Treat account login cookies as the finished business session

Temptation:

- stop after the password or token login returns success
- export cookies before tenant, role, or data-range activation
- hand a login-only jar to collectors as if every page were unlocked

Why it is false progress:

- many back offices keep mutable business context after authentication
- collectors then scrape the wrong shop, supplier, or org with a green login status

Smallest honest next move:

- split Gate A login from Gate B business-identity activation
- reread final identity before export
- route multi-layer cases to `references/multi-context-session-playbook.md`

Self-check:

- does the exported session's active context match the task config, not only the account id?

## Anti-pattern 12: Trust the switch API and skip final identity reread

Temptation:

- accept HTTP 200 or `success=true` from an update-session or switch-context call
- omit a required type field because the value field alone "looked enough"
- continue into collection without opening the authoritative identity surface

Why it is false progress:

- partial activation can leave a previous or empty data-range in place
- the failure is silent and later looks like a data or filter bug

Smallest honest next move:

- compare the successful UI payload field-for-field
- reread identity from the final page or introspection endpoint
- fail closed on any missing or mismatched layer

Self-check:

- if the data-range type or value is removed, does your acceptance still pass? If yes, the gate is too weak.

## Anti-pattern 13: Submit UI labels as protocol ids or pick the first fuzzy match

Temptation:

- POST the visible Chinese or localized name because that is what the operator selected
- reuse another account's resource id
- when enumeration returns multiple rows, take index zero

Why it is false progress:

- activation needs live authorization codes or values
- ambiguous matches create wrong-context sessions that still look authenticated

Smallest honest next move:

- resolve labels through the current account's authorization response
- require exactly one match
- stop on zero or many matches

Self-check:

- would a renamed label or duplicate label make your resolver fail loudly?

## Anti-pattern 14: Treat HTTP 200 as async export create success

Temptation:

- stop after a create endpoint returns 200 or a vague success flag
- skip history diff because "the request looked right"
- poll whatever successful task appears first

Why it is false progress:

- empty success and wrong method or body placement often still return 200
- collectors then download someone else's older file

Smallest honest next move:

- snapshot task ids before create
- require a new task id and condition match
- route to `references/async-export-job-playbook.md`

Self-check:

- can you name the task id that did not exist before this run?

## Anti-pattern 15: Reuse the newest historical export task

Temptation:

- grab history row zero
- reuse a pre-create successful task to "save time"
- ignore filter or field-set mismatches

Why it is false progress:

- you prove download, not create
- wrong date range or thinner columns get persisted as if fresh

Smallest honest next move:

- isolate by create-returned id or post-create new id
- match business filters and requested fields
- fail if only old tasks are visible

Self-check:

- was this task id absent from the pre-create snapshot?

## Anti-pattern 16: Promote regenerate traffic into the first-create contract

Temptation:

- copy method and body from "regenerate old task"
- sign the wrong serialization because a nearby route worked
- mark first-create solved without a dedicated capture

Why it is false progress:

- regenerate may require an old task id and different placement of filters
- the signer can pass on one route and fail on the other

Smallest honest next move:

- capture one clean first-create request
- compare method, query, body, content-type, and signer coverage
- keep unproven boundaries explicit

Self-check:

- does your create proof come from first-create wire evidence, or only from regenerate?

## Anti-pattern 17: Treat the only decompiled short signer as the only writer

Temptation:
- a short hash or compress path is fully recovered offline
- the field name matches the live verifier param
- self-check vectors look perfect

Why it is false progress:
- the wire-success value may be a longer challenge-written body with a different writer
- live still returns challenge HTML even though the short generator is correct for its own path
- packaging the short generator freezes a research path as product delivery

Smallest honest next move:
- compare short research outputs to successful wire lengths and prefixes
- map every writer stack for that field name
- live-accept only the success class

Self-check:
- do successful live requests actually carry your short token shape?

## Anti-pattern 18: Call sample exact replay "protocol automation"

Temptation:
- saved absolute URLs with long tokens still return business JSON
- jobs.csv fills from sample mode

Why it is false progress:
- exact replay does not prove fresh timestamp, page, or session regeneration
- rotating challenge state remains unsolved
- delivery gate requires repeated live success, not archive playback

Smallest honest next move:
- regenerate on a new timestamp or page through the real writer or challenge executor
- keep sample mode as diagnostic only

Self-check:
- can you mint a new URL-bound artifact without copying the old final token?

## Anti-pattern 19: Keep reversing encrypt after redirect already carries the artifact

Temptation:
- challenge helper or runtime already navigates to a URL with the decisive param
- local executor still throws navigation or DOM noise
- the encrypt module looks unfinished

Why it is false progress:
- the nearest stable artifact is already enough for Python replay
- post-artifact exceptions are often noise
- full encrypt reverse may still be useful later, but it is not the first delivery gate

Smallest honest next move:
- harvest `redirectUrl` or cookie string
- replay from Python
- only resume encrypt reverse if regeneration still fails without it

Self-check:
- is there already a Python-replayable artifact in helper output?

## Anti-pattern 20: Merge app signer and WAF or challenge verifier into one problem

Temptation:
- browser requests show both HMAC/sign headers and challenge params
- one reverse ticket tries to solve every field at once

Why it is false progress:
- the gates can be independent
- challenge-retry paths may not need the app signer
- app signer recovery can succeed while verifier recovery remains blocked, or the reverse

Smallest honest next move:
- prove each gate's necessity with ablation
- deliver the minimum set that clears live business responses

Self-check:
- which fields are necessary, optional, or browser-only according to live ablations?

## Anti-pattern 21: Treat automation-browser hand-slide failures as trajectory truth

Temptation:
- a human slides inside DrissionPage, CDP-driven Chrome, or a hooked profile and still fails
- the team concludes the track algorithm is wrong and starts trajectory search

Why it is false progress:
- automation marks, debug ports, injected hooks, and new profiles can fail a risk gate even with genuine human motion
- contaminated negatives teach the wrong surface
- clean ordinary-browser success samples may already prove the track family is acceptable

Smallest honest next move:
- capture one clean positive sample outside automation ownership when possible
- compare clean success, contaminated failure, and protocol replay under the same session assumptions
- read `references/positive-sample-hygiene-playbook.md`

Self-check:
- do you have at least one success sample from a non-automated browser path before blaming track generation?


## Anti-pattern 22: Keep tuning tracks after structure is already accepted

Temptation:
- final verify returns a risk-like rejection after token structure, checksum, and sidecar HTTP success look fine
- more synthetic trajectories, distance scales, and sleep jitter are tried next

Why it is false progress:
- risk rejection can come from shared-state inconsistency, missing telemetry semantics, impossible wall-clock timing, or environment score
- track search multiplies noise without localizing the failure surface
- consecutive failures can themselves worsen environment risk

Smallest honest next move:
- localize the error family with controlled ablations
- re-check baseline/sparse consistency and real timeline
- only then change behavior or answer payloads
- if environment risk is implicated, change exit/IP or sample hygiene before more track variants
- read `references/verifier-error-localization-playbook.md`

Self-check:
- which single controlled omission changes the rejection family, and is it track-related?


## Anti-pattern 23: Call verifier-semantic success a finished collector

Temptation:
- the verifier endpoint returns the platform accepted code or flag
- delivery stops before the first business request consumes the grant

Why it is false progress:
- verifier success can be intermediate
- token placement, query names, cookie slots, success-param aliases, and body packaging still decide business acceptance
- a collector that cannot re-fetch the original document or API is not delivered

Smallest honest next move:
- prove the first downstream consumer on the same round
- define business-pass checks by content fingerprint, not only HTTP status
- keep verifier and consumer packaging on one session chain

Self-check:
- after verifier acceptance, does the original business URL return non-challenge content through the regenerated grant?



## Anti-pattern 24: Call MCP families that are only on disk

Temptation:
- a checkout or download folder contains chrome-devtools, js-reverse, reqable, or other MCP sources
- the agent routes as though those servers are mounted

Why it is false progress:
- availability is the active session tool registry, not a directory listing
- invented initiator or mutation claims then look complete while no tool actually ran

Smallest honest next move:
- inspect mounted tools first
- record `missing_mcp` and fall back to available surfaces or a lower shape

Self-check:
- did the chosen MCP family appear in the live tool schema before the first target action?

## Anti-pattern 25: Force dual browser first-pass on pure artifacts

Temptation:
- the user supplied HAR, request text, or a passive capture
- both browser families are opened to satisfy live-target ceremony

Why it is false progress:
- artifact-only work must not invent browser proof
- dual first-pass is for fresh web live targets only; APK/app/mini-program primary work is out of scope for this skill

Smallest honest next move:
- stay on `evidence-reuse` or offline routes until live acceptance is required
- label live acceptance unproven when no browser pass was authorized

Self-check:
- would the next answer still hold if no browser MCP existed?

## Anti-pattern 26: Run chrome-devtools and js-reverse target actions together

Temptation:
- open the page in both families at once to save turns

Why it is false progress:
- profile and ownership conflicts destroy clean baselines
- initiator and wire evidence become incomparable

Smallest honest next move:
- keep one `TARGET_ACTIVE` family
- complete sequential handoff before switching

Self-check:
- is only one browser family performing target actions in this tool batch?

## Anti-pattern 27: Treat environment provider start as protocol success

Temptation:
- AdsPower or another profile manager opens cleanly
- delivery or live understanding is declared without baseline and mutation proof

Why it is false progress:
- ENV providers only supply a surface
- attach, baseline, mutation, and replay remain unproved

Smallest honest next move:
- obtain a debuggable endpoint
- run chrome then js-reverse evidence under attach ownership

Self-check:
- was a business request captured and correlated after profile start?

## Anti-pattern 28: Treat passive capture or PCAP as signer recovery

Temptation:
- reqable or WireMCP shows traffic, so sign reconstruction is skipped
- a collector is declared because captures look complete

Why it is false progress:
- stores prove egress history, not local regeneration
- PCAP visibility is not transport-profile or algorithm proof by itself

Smallest honest next move:
- extract moving fields from captures
- rebuild offline with fixed vectors before browser-free replay

Self-check:
- can the request be regenerated without reusing the captured one-time values as hard-coded secrets?

## Anti-pattern 29: Keep MCP browser runtime inside the collector

Temptation:
- Playwright, CDP page driving, or MCP browser calls remain in the final run path as a temporary fallback

Why it is false progress:
- browser-backed replay is not a protocol collector
- delivery gates forbid browser automation as the final path

Smallest honest next move:
- demote to `evidence` or `local-proof` until pure HTTP replay works
- remove MCP runtime imports from `main.py` / `collector/main.py`

Self-check:
- does the right-click entrypoint succeed with browser MCP servers stopped?
## Entry format for new anti-patterns

When a shortcut recurs across more than one job, add it in this shape:

```markdown
## Anti-pattern N: <short name>

Temptation:
- ...

Why it is false progress:
- ...

Smallest honest next move:
- ...

Self-check:
- ...
```

Keep it generic.
Do not copy live cookies, secrets, or one-off values here.

## Final rule

If a shortcut cannot survive one direct self-check, it is not a shortcut.
It is debt disguised as progress.
