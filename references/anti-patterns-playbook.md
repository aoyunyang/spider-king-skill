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
- [Anti-pattern 5A: Ship silent-value capture as delivery runtime or treat unrestricted dumps as success](#anti-pattern-5a-ship-silent-value-capture-as-delivery-runtime-or-treat-unrestricted-dumps-as-success)
- [Anti-pattern 6: Reverse the visible helper or visible param instead of the wire mutation point](#anti-pattern-6-reverse-the-visible-helper-or-visible-param-instead-of-the-wire-mutation-point)
- [Anti-pattern 7: Treat helper load success, fewer exceptions, or browser-shaped output as protocol success](#anti-pattern-7-treat-helper-load-success-fewer-exceptions-or-browser-shaped-output-as-protocol-success)
- [Anti-pattern 8: Overwrite stable scaffolding with volatile captures](#anti-pattern-8-overwrite-stable-scaffolding-with-volatile-captures)
- [Anti-pattern 9: Believe page text that a cookie or session id participates in the signer](#anti-pattern-9-believe-page-text-that-a-cookie-or-session-id-participates-in-the-signer)
- [Anti-pattern 10: Treat a standard crypto library as done because the algorithm name matches](#anti-pattern-10-treat-a-standard-crypto-library-as-done-because-the-algorithm-name-matches)
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

- [Anti-pattern 30: Blame Python or local Init before proving apply-path wiring](#anti-pattern-30-blame-python-or-local-init-before-proving-apply-path-wiring)
- [Anti-pattern 31: Cross-session gold dense rebind as the mainline](#anti-pattern-31-cross-session-gold-dense-rebind-as-the-mainline)
- [Anti-pattern 32: Cosmetic field matrices before companion necessity is proved](#anti-pattern-32-cosmetic-field-matrices-before-companion-necessity-is-proved)
- [Anti-pattern 33: Treat companion HTTP 200 as device-trust success](#anti-pattern-33-treat-companion-http-200-as-device-trust-success)
- [Anti-pattern 34: Auto-stub capitalised host names including Function](#anti-pattern-34-auto-stub-capitalised-host-names-including-function)
- [Anti-pattern 35: Reuse stale mid/meta after local SDK emit finally works](#anti-pattern-35-reuse-stale-midmeta-after-local-sdk-emit-finally-works)
- [Anti-pattern 36: Call L2 local JS runtime "fully pure Python protocol"](#anti-pattern-36-call-l2-local-js-runtime-fully-pure-python-protocol)
- [Anti-pattern 37: Lock the positive-sample morph as the only mainline](#anti-pattern-37-lock-the-positive-sample-morph-as-the-only-mainline)
- [Anti-pattern 38: Treat the hardest token as the only failure surface](#anti-pattern-38-treat-the-hardest-token-as-the-only-failure-surface)
- [Anti-pattern 39: Rebuild a behavior wall while a same-family solved skeleton exists](#anti-pattern-39-rebuild-a-behavior-wall-while-a-same-family-solved-skeleton-exists)
- [Anti-pattern 40: Call mint-shaped or stable-reject progress a gate pass](#anti-pattern-40-call-mint-shaped-or-stable-reject-progress-a-gate-pass)
- [Anti-pattern 41: Optimize offline similarity to human gold as the mainline score](#anti-pattern-41-optimize-offline-similarity-to-human-gold-as-the-mainline-score)
- [Anti-pattern 42: Expand offline mint variants after envelope is solved while live chain is incomplete](#anti-pattern-42-expand-offline-mint-variants-after-envelope-is-solved-while-live-chain-is-incomplete)
- [Anti-pattern 43: Dismiss a same-family skeleton after one soft reject](#anti-pattern-43-dismiss-a-same-family-skeleton-after-one-soft-reject)
- [Anti-pattern 44: Continue token/env reverse without a day-card or kill-switch check](#anti-pattern-44-continue-tokenenv-reverse-without-a-day-card-or-kill-switch-check)
- [Anti-pattern 45: Treat a URL substring as WAF family](#anti-pattern-45-treat-a-url-substring-as-waf-family)
- [Anti-pattern 46: Fire document events immediately after complete-document eval](#anti-pattern-46-fire-document-events-immediately-after-complete-document-eval)
- [Anti-pattern 47: Carry a previous-page challenge token because HTTP 200 looked like success](#anti-pattern-47-carry-a-previous-page-challenge-token-because-http-200-looked-like-success)
- [Anti-pattern 48: Finish each dynamic slot as an independent signature](#anti-pattern-48-finish-each-dynamic-slot-as-an-independent-signature)
- [Anti-pattern 49: Submit a direct host return as the final wire artifact](#anti-pattern-49-submit-a-direct-host-return-as-the-final-wire-artifact)
- [Anti-pattern 50: Tour the outer emulator after a nested memory image is available](#anti-pattern-50-tour-the-outer-emulator-after-a-nested-memory-image-is-available)
- [Anti-pattern 51: Treat viewport spoof as a protocol profile](#anti-pattern-51-treat-viewport-spoof-as-a-protocol-profile)
- [Anti-pattern 52: Raise verify retries to hide a wrong backend](#anti-pattern-52-raise-verify-retries-to-hide-a-wrong-backend)
- [Anti-pattern 53: Pick the formal runtime by local ciphertext equality](#anti-pattern-53-pick-the-formal-runtime-by-local-ciphertext-equality)
- [Anti-pattern 54: Treat HTTP 200 plus a hint or string array as page success](#anti-pattern-54-treat-http-200-plus-a-hint-or-string-array-as-page-success)
- [Anti-pattern 55: Jump to a patched digest because the unsalted standard primitive missed](#anti-pattern-55-jump-to-a-patched-digest-because-the-unsalted-standard-primitive-missed)
- [Anti-pattern 56: Clone a sibling collector before the current endpoint exists](#anti-pattern-56-clone-a-sibling-collector-before-the-current-endpoint-exists)
- [Anti-pattern 57: Pin a packer PRNG so unpack halts, then declare the signer missing](#anti-pattern-57-pin-a-packer-prng-so-unpack-halts-then-declare-the-signer-missing)
- [Anti-pattern 58: Clone a sibling request shape because leftover UA or call looks shared](#anti-pattern-58-clone-a-sibling-request-shape-because-leftover-ua-or-call-looks-shared)
- [Anti-pattern 59: Freeze Date.now because a sibling used a server clock](#anti-pattern-59-freeze-datenow-because-a-sibling-used-a-server-clock)
- [Anti-pattern 60: Clone a sibling signer because the preimage concat looks the same](#anti-pattern-60-clone-a-sibling-signer-because-the-preimage-concat-looks-the-same)
- [Anti-pattern 61: Hunt a signer or OCR because list HTML looks obfuscated](#anti-pattern-61-hunt-a-signer-or-ocr-because-list-html-looks-obfuscated)
- [Anti-pattern 62: Call check-API success complete while finish stays false](#anti-pattern-62-call-check-api-success-complete-while-finish-stays-false)
- [Anti-pattern 63: Treat 403 on a named-digest API as session death or WAF](#anti-pattern-63-treat-403-on-a-named-digest-api-as-session-death-or-waf)
- [Anti-pattern 64: Eval a recovered hasher-side function in Node](#anti-pattern-64-eval-a-recovered-hasher-side-function-in-node)
- [Anti-pattern 65: Launch a second Chrome because the user asked to open DP](#anti-pattern-65-launch-a-second-chrome-because-the-user-asked-to-open-dp)
- [Anti-pattern 66: Copy a newer live Chrome major onto a lower curl impersonate](#anti-pattern-66-copy-a-newer-live-chrome-major-onto-a-lower-curl-impersonate)
- [Anti-pattern 67: Bulk-add unproven APIs when risk-control is unknown](#anti-pattern-67-bulk-add-unproven-apis-when-risk-control-is-unknown)
- [Anti-pattern 68: Treat stdlib 403 of a live-admitted token as a bad signer](#anti-pattern-68-treat-stdlib-403-of-a-live-admitted-token-as-a-bad-signer)
- [Anti-pattern 69: Chase canvas after impersonate already returns business 200](#anti-pattern-69-chase-canvas-after-impersonate-already-returns-business-200)
- [Anti-pattern 70: Seed impersonate cookies without a request hostname](#anti-pattern-70-seed-impersonate-cookies-without-a-request-hostname)
- [Anti-pattern 71: Treat HTML placeholder zeros as business data when no list XHR fired](#anti-pattern-71-treat-html-placeholder-zeros-as-business-data-when-no-list-xhr-fired)
- [Anti-pattern 72: Upgrade Camoufox because CDP navigator.webdriver is true](#anti-pattern-72-upgrade-camoufox-because-cdp-navigatorwebdriver-is-true)
- [Anti-pattern 73: Chase JSVMP opcodes before protobuf serializeBinary or wasm encode I/O](#anti-pattern-73-chase-jsvmp-opcodes-before-protobuf-serializebinary-or-wasm-encode-io)
- [Anti-pattern 74: Trust MCP or DevTools UTF-8 dumps as protobuf bytes](#anti-pattern-74-trust-mcp-or-devtools-utf-8-dumps-as-protobuf-bytes)
- [Anti-pattern 75: Treat an empty ajax beforeSend IIFE as a missing signer](#anti-pattern-75-treat-an-empty-ajax-beforesend-iife-as-a-missing-signer)
- [Anti-pattern 76: Treat a dummy HTTP sibling or HTML zeros as the list while a WebSocket channel is unproven](#anti-pattern-76-treat-a-dummy-http-sibling-or-html-zeros-as-the-list-while-a-websocket-channel-is-unproven)
- [Anti-pattern 77: Port named AES as AES-128 because a longer token is 16-aligned](#anti-pattern-77-port-named-aes-as-aes-128-because-a-longer-token-is-16-aligned)
- [Anti-pattern 78: Treat a chrome-devtools HTTP-only resource log as proof there is no WebSocket list](#anti-pattern-78-treat-a-chrome-devtools-http-only-resource-log-as-proof-there-is-no-websocket-list)
- [Anti-pattern 79: JSON-parse or sum the first short WebSocket text frame as the list](#anti-pattern-79-json-parse-or-sum-the-first-short-websocket-text-frame-as-the-list)
- [Anti-pattern 80: Skip an issued challenge to protect accuracy](#anti-pattern-80-skip-an-issued-challenge-to-protect-accuracy)
- [Anti-pattern 81: Treat an eval/Function compile snapshot as a call trace, or wrap global apply/call](#anti-pattern-81-treat-an-evalfunction-compile-snapshot-as-a-call-trace-or-wrap-global-applycall)
- [Anti-pattern 82: Feed an old nondeterministic sequence into a new-session script](#anti-pattern-82-feed-an-old-nondeterministic-sequence-into-a-new-session-script)
- [Anti-pattern 83: Count canvas or navigator JS-shim probes as host-fidelity L0](#anti-pattern-83-count-canvas-or-navigator-js-shim-probes-as-host-fidelity-l0)
- [Anti-pattern 84: Mount webpack UI instead of exposing require](#anti-pattern-84-mount-webpack-ui-instead-of-exposing-require)
- [Anti-pattern 85: Run setTimeout callbacks synchronously, or ignore fromCharCode heat](#anti-pattern-85-run-settimeout-callbacks-synchronously-or-ignore-fromcharcode-heat)
- [Anti-pattern 86: Mix source class with ownership, drag from box center, ship OCR as collector, or swallow import bugs as platform-down](#anti-pattern-86-mix-source-class-with-ownership-drag-from-box-center-ship-ocr-as-collector-or-swallow-import-bugs-as-platform-down)
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

## Anti-pattern 5A: Ship silent-value capture as delivery runtime or treat unrestricted dumps as success

### Looks like

- leaving an engine-capture or instrumented browser path inside `compact-replay` / `collector`
- declaring victory from megabytes of uncorrelated jscall/opcode/wasm dumps
- refusing silent-value-capture when attach is missing even though a backend is available
- requiring dual-backend cross-proof as ceremony after one correlated fixed-input card already unlocks rebuild

### Why it hurts

- delivery stops being browser-free
- noise replaces protocol proof
- real low-observer capability is underused

### Do this instead

- use `references/silent-value-capture-playbook.md` as a first-class debugger-trace means, never as delivery runtime
- require `fixed_input_ready` plus wire/state correlation
- on no-attach, record `debugger_attach_gap` and continue when a silent backend exists
- stop capture once rebuild material is enough

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
- hook the public writer arguments before guessing concat from route names
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
- hardcode a session id into RSA plaintext because the page says it may enter the token
- copy `"GET " + url + "?"` from a debug UI into the preimage because it looks like the signed string
- refuse to prototype an anonymous list collector until login is solved
- mix submit-account requirements into every list or detail request

Why it is false progress:

- page copy is not wire evidence
- flavor text that a session id may enter RSA is identity-cookie only until the writer reads it
- a debug-UI GET concat is not the writer until the signer reads it
- list, detail, and submit chains often have different session contracts
- a wrong preimage wastes reverse time on a crypto problem that does not exist

Smallest honest next move:

- capture the real request with and without the claimed cookie
- classify fields from the wire: static, server time, signer output, account state
- keep anonymous collection available when the business response already succeeds without login
- require the session only for the chain that actually 401s or changes answers
- freeze the writer arguments; do not copy debug-UI GET prefixes into the preimage

Self-check:

- does removing the cookie change the business response, or only the later submit path?

## Anti-pattern 10: Treat a standard crypto library as done because the algorithm name matches

Temptation:

- swap in stock MD5, SHA, or SM3 after seeing the name in source or UI text
- treat statement-split JSEncrypt or RSA as a custom primitive because gold-token ciphertext differs
- encrypt with the second harvested SPKI after the first key misses
- eval the harvested digest file in Node because the algorithm name matches
- skip intermediate word checks once the digest length looks right
- port only the happy-path constants and ignore environment-selected branches
- treat same-clock page tokens that collide after packing as interchangeable requests
- treat native Date.now as the request clock when it only selected round constants
- swap in stock AES/GCM after an export is named encrypt and avalanche looks textbook
- port named AES as AES-128 because a longer token is 16-aligned
- treat a Node miss of a named AES helper as patched AES without comparing host-object catch-path key order
- chase gold-token equality through a Huffman/XOR port while live replay already accepted

Why it is false progress:

- IV, round constants, packing masks, and compress masks are common rewrite points, including per-round K selected by rotating host-presence checks
- one wrong `ROTL` edge case can pass some pages and fail others
- browser-branch constants may differ from Node or fallback branches; Node eval of the harvested file is a different digest and can hang
- packing collisions are not interchangeable pages; live still refreshes the clock
- native Date.now can select `Tj`/`K` while the request clock is a query field or signer argument
- nonce/tag order, packed/bitsliced keys, XOR/end, and inner-field PRNG are independent of the marketing name
- inner Date, environment scores, or rotating source can make gold freeze fail while the public writer is valid
- statement-split named RSA is still PKCS#1 v1.5; freeze the pad string first
- random type 2 makes gold-token inequality expected; a proved constant PS makes gold-token equality a valid oracle
- a second SPKI or `document.all` key is an untaken branch until the live writer selects it; the unused branch may add a limb delta instead of swapping a whole key

Smallest honest next move:

- freeze one captured preimage and digest
- diff IV, constants, packing, and compress steps against the standard algorithm
- reproduce the browser branch as a local replica before the Python port; do not eval the harvested digest file in Node as the oracle
- add a fixed-input self-check that fails loudly on standard-library substitution
- after avalanche hits, freeze frame, packed-key layout, and gold-pair XOR before a standard AEAD library
- freeze a short plaintext; 8-byte ciphertext is DES/3DES, not AES-128, even when the live token is 16-aligned
- if Node diverges, compare navigator/location catch-path key order to the browser branch before declaring AES patched
- keep PKCS#1 when the named helper is JSEncrypt, JSBN, or RSA; use live decrypt or typed accept unless the pad string is proved constant
- ignore a second harvested key or even stored limb array until the live writer reads it

Self-check:

- does the local standard library match the captured wire field, or only the name, bit length, or avalanche?
- does a short vector show 8-byte or 16-byte blocks, and does the local runtime take the browser host-object branch?

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
- a public function already mints accepted tokens in a tiny local vm, but inner Huffman/XOR still looks undone

Why it is false progress:
- the nearest stable artifact is already enough for Python replay
- post-artifact exceptions are often noise
- full encrypt reverse may still be useful later, but it is not the first delivery gate

Smallest honest next move:
- harvest `redirectUrl` or cookie string
- replay from Python
- if a public function already mints accepted tokens in a tiny local vm, keep that harvest
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

## Anti-pattern 30: Blame Python or local Init before proving apply-path wiring

Temptation:
- local Init returns mid/config but verify fails, so conclude "server rejects non-browser Init"

Why it is false progress:
- the fail may be incomplete DeviceConfig apply (missing proto secrets, load order, side effects)
- fulfill/inject of the same Init body into the official apply path can still pass

Smallest honest next move:
- inject local Init JSON into the official apply path once
- diff working runtime object vs manual object at SDK entry

Self-check:
- did official apply of local Init body ever reach a trusted companion emit?

## Anti-pattern 31: Cross-session gold dense rebind as the mainline

Temptation:
- save one accepted env/dense blob and rewrite clocks/ids onto new mids

Why it is false progress:
- device-trust sidecars are often session-fresh runtime products
- rebinds burn days while same-session local SDK emit would move the gate

Smallest honest next move:
- prove same-session native or local-runtime emit first
- treat rebind only as a negative control

Self-check:
- does the same content accept only on the mid that produced it?

## Anti-pattern 32: Cosmetic field matrices before companion necessity is proved

Temptation:
- flip f43/f88/hash cosmetics because they look suspicious

Why it is false progress:
- many cosmetics are soft under same-mid ablations
- matrices explode time without naming the primary surface

Smallest honest next move:
- block/repost companion body; packer bit-exact; skip-first call
- only then single-field same-mid ablations

Self-check:
- is companion necessity and packing already proved?

## Anti-pattern 33: Treat companion HTTP 200 as device-trust success

Temptation:
- Log2-class endpoint returns 200/Success so trust is done

Why it is false progress:
- final verify semantic can still reject content or stale session
- 200 only proves delivery of bytes

Smallest honest next move:
- close the chain to verify semantic on the same mid immediately

Self-check:
- did verify accept, not only companion ACK?

## Anti-pattern 34: Auto-stub capitalised host names including Function

Temptation:
- Proxy `has()` returns true for every CapitalName and fabricates empty functions

Why it is false progress:
- pollutes real builtins (`Function.prototype.call.bind` breaks)
- creates endless synthetic crashes unrelated to protocol

Smallest honest next move:
- keep real builtins; stub only browser-only constructors one by one

Self-check:
- is `Function ===` the real function constructor inside the runtime?

## Anti-pattern 35: Reuse stale mid/meta after local SDK emit finally works

Temptation:
- keep one meta.json while iterating host patches, then verify much later

Why it is false progress:
- rejects look like packer/content failures (time/stale family)
- hides that emit already works

Smallest honest next move:
- fresh Init -> emit -> verify in one short process
- only then measure stability

Self-check:
- are Init timestamp and verify within one continuous run?

## Anti-pattern 36: Call L2 local JS runtime "fully pure Python protocol"

Temptation:
- no Chrome window, so claim pure offline Python

Why it is false progress:
- Node/jsdom still executes vendor SDK
- delivery gates require honest runtime disclosure

Smallest honest next move:
- label deliveryLevel L2; keep Python as HTTP owner
- L3 only after field port

Self-check:
- can the collector run with node/js runtimes removed?

## Anti-pattern 37: Lock the positive-sample morph as the only mainline

Temptation:
- a desktop human gold sample passed, so rebuild only that desktop scene forever

Why it is false progress:
- a positive sample proves one admitted path, not the current lowest-cost morph
- multi-surface verifiers often admit mobile/H5 or alternate scene forms more reliably for protocol collectors
- track/env polish on the wrong morph burns days while the gate code never moves

Smallest honest next move:
- label the gold sample morph fields (`scene`, device class, UA class)
- ablate one alternate morph on the same state-chain before more track entropy
- route to `references/verifier-morph-and-state-chain-playbook.md` and `references/positive-sample-hygiene-playbook.md`

Self-check:
- did I treat the gold sample as existence proof or as mandatory mainline?

## Anti-pattern 38: Treat the hardest token as the only failure surface

Temptation:
- the obfuscated behavior token is the scariest artifact, so every reject means the token is still fake

Why it is false progress:
- envelope/codec success and mint-shaped output are soft successes
- missing state-chain reports, wrong scene, or companion slots produce the same stable reject code
- more trajectory noise cannot fix an incomplete transcript machine

Smallest honest next move:
- name surfaces with `references/failure-surface-taxonomy.md`
- ablate morph -> state-chain -> companions -> token-writer before track micro-details
- keep the hard gate metric as semantic success plus grant artifact

Self-check:
- if I freeze the token writer and only complete state-chain/companions, does the gate flip?

## Anti-pattern 39: Rebuild a behavior wall while a same-family solved skeleton exists

Temptation:
- ignore a user-provided or sibling solved pure-protocol skeleton and re-derive desktop behavior capture from zero

Why it is false progress:
- same SDK generation often shares preflight, companion, and retry shape across host paths
- re-deriving tracks discards already-proved process structure
- target migration is usually host/path/config binding, not a new physics of mouse paths

Smallest honest next move:
- run the case-reuse selection gate in `references/case-reuse-playbook.md`
- port TARGET/host/punish/slide binding first; keep HTTP ownership in Python
- re-prove current-proof with fresh live gate metrics before claiming reuse done

Self-check:
- did I spend more time re-animating tracks than migrating the solved session machine?

## Anti-pattern 40: Call mint-shaped or stable-reject progress a gate pass

Temptation:
- non-empty tokens, cleared helper exceptions, or stable reject JSON look like almost done

Why it is false progress:
- mint-shaped is step 1 of the acceptance ladder, not collector delivery
- a stable reject code proves the server parsed the request, not that the gate passed
- one lucky accept without N-run rate is anecdote

Smallest honest next move:
- define `gate_pass` before experiments
- climb mint-shaped -> server-parseable -> gate-pass -> repeatable -> consumer-pass
- bench fresh sessions (10-20 when claiming stability)

Self-check:
- can I quote success rate on the hard gate metric, not only that mint works?


## Anti-pattern 41: Optimize offline similarity to human gold as the mainline score

Temptation:
- common-prefix bytes, token length, or binary distance to a human gold sample is improving, so keep optimizing it

Why it is false progress:
- similarity can rise forever on the wrong morph or incomplete state-chain
- the server gate may ignore the dimensions you are matching
- this burns days after envelope is already solved

Smallest honest next move:
- put similarity on the false-progress blacklist
- force morph/state-chain/companion ablation with hard-gate oracle only
- see kill-switch K5 in `references/verifier-morph-and-state-chain-playbook.md`

Self-check:
- if similarity doubled but hard gate never flipped, did I still call it progress?

## Anti-pattern 42: Expand offline mint variants after envelope is solved while live chain is incomplete

Temptation:
- produce typeN/full-fp/force-join mint scripts because live still rejects

Why it is false progress:
- offline mint count is a blacklist metric
- missing bootstrap/companions produce the same reject as a bad token
- env sprawl often increases while gate stays flat

Smallest honest next move:
- freeze mint variant expansion (kill-switch K2)
- complete one live state-chain + companion matrix row on a single morph
- only then change writer family

Self-check:
- can I list missing state-chain steps without opening another mint script?

## Anti-pattern 43: Dismiss a same-family skeleton after one soft reject

Temptation:
- migrated sibling pure-protocol returns one stable reject, so declare the skeleton useless and return to behavior reverse

Why it is false progress:
- first reject is often companion mode, wait timing, or challenge restart class
- skeletons encode process structure worth more than one packet outcome
- one-shot denial recreates multi-day walls already solved elsewhere

Smallest honest next move:
- run in-challenge companion mode flips + verifyFail transition
- whole-challenge restart under the skeleton morph
- multi-attempt bench before abandoning template reuse

Self-check:
- did I spend less time on retry classes than on writing the skeleton off?

## Anti-pattern 44: Continue token/env reverse without a day-card or kill-switch check

Temptation:
- keep patching because yesterday almost looked better

Why it is false progress:
- without wall name, hard metric, and kill-switch status, sunk cost drives the route
- multi-day verifier failures are usually process failures, not missing one stub

Smallest honest next move:
- fill the day-card in `references/verifier-morph-and-state-chain-playbook.md`
- execute any due kill-switch before more reverse
- change one matrix variable only

Self-check:
- can I point to today's single variable and stop condition in writing?

## Anti-pattern 45: Treat a URL substring as WAF family

Temptation:
- a timeline, path, or query token contains `jsl` or another family-looking fragment
- the job is labeled as that WAF and the wrong clearance playbook is loaded

Why it is false progress:
- random URL tokens are not cookie-name or status-body corroboration
- the same vendor can expose a mintable bootstrap face and a hard interstitial as different doors
- the wrong family wastes the session on a clearance cookie that never appears

Smallest honest next move:
- corroborate with cookie-name family plus status, body, or header evidence
- split mintable non-final probe responses from hard interstitials
- read `references/anti-bot-class-playbook.md`

Self-check:
- do I have two independent surfaces, or only a substring?

## Anti-pattern 46: Fire document events immediately after complete-document eval

Temptation:
- the helper evaluates challenge JS into an already-complete document
- `load` or `DOMContentLoaded` is dispatched as soon as eval returns because the host looks ready

Why it is false progress:
- some scripts register those listeners only after a collector pass finishes
- an early synthetic event misses the listener, so no cookie is minted
- matching UA or eval-length then looks like a host-identity failure and starts useless env sprawl

Smallest honest next move:
- wait for a public collector-ready object, then fire the event
- observe cookie and storage after the delayed latch
- read `references/server-js-cookie-bootstrap-playbook.md`

Self-check:
- did the listener exist at the moment the event was fired?

## Anti-pattern 47: Carry a previous-page challenge token because HTTP 200 looked like success

Temptation:
- a page id, seq, or callback token from an earlier document is reused because the field name and length still look valid
- the submit endpoint returns HTTP `200`

Why it is false progress:
- document-bound tokens can yield `200` with an empty body or remaining challenge chrome
- that response is silent reject, not a grant
- the collector then paginates a challenge shell

Smallest honest next move:
- harvest the token from the current challenge HTML on the same session chain
- define grant by business content, not status
- read `references/challenge-state-envelope-playbook.md`

Self-check:
- did the submit token come from the same document that displayed this challenge?

## Entry format for new anti-patterns


## Anti-pattern 48: Finish each dynamic slot as an independent signature

### The tempting shortcut

Token A, random B, header C, and behavior blob D each match length and alphabet, so the verify request should pass when concatenated.

### Why it creates false progress

Multi-slot chains share one round world. Slot-local validity can still combine challenge ids, cookies, events, and canonical URLs from different worlds.

### Smallest honest next move

Run the same-world gate in `references/parameter-ownership-playbook.md` before another algorithm rewrite.

### Self-check

Do all decisive slots cite one roundKey, one identity snapshot, and one event sequence?

## Anti-pattern 49: Submit a direct host return as the final wire artifact

### The tempting shortcut

The local SDK or helper returns the right prefix and length, so paste it into verify.

### Why it creates false progress

Stack-sensitive or host-sensitive blocks can embed local paths, `node:internal` frames, or JSDOM fingerprints while checksums still look locally consistent.

### Smallest honest next move

Collect-then-patch with block checkpoints and recompute checksums; see `references/opaque-runtime-profile-playbook.md`.

### Self-check

Did I compare block-level diffs against a clean browser sample, or only the final string?

## Anti-pattern 50: Tour the outer emulator after a nested memory image is available

### The tempting shortcut

The outer script is huge and obfuscated, so deeper opcode or beautify work must be the path.

### Why it creates false progress

If a nested standard ISA or fixed memory image already owns the transform, outer-shell reading burns days without moving I/O parity.

### Smallest honest next move

Dump initialized memory, label I/O regions, and replay with a standard simulator; see `references/jsvmp-analysis-playbook.md`.

### Self-check

Have I proved the inner entry and output region, or am I still reading loader code?



## Anti-pattern 51: Treat viewport spoof as a protocol profile

### The tempting shortcut

Switch the device toolbar or rewrite UA, then reuse the desktop helper path as a mobile solve.

### Why it creates false progress

Protocol profiles include scene, Client-Hints, platform, touch/event semantics, geometry, and fingerprint surfaces together. Preview cosplay leaves desktop semantics in place.

### Smallest honest next move

Freeze one profile object and make every helper read it; see Doctrine 41 and `references/parameter-ownership-playbook.md`.

### Self-check

Do session headers and host-script surfaces cite the same profileId?

## Anti-pattern 52: Raise verify retries to hide a wrong backend

### The tempting shortcut

Clean samples pass quickly, but local needs a huge attempt budget, so max retries become the "fix".

### Why it creates false progress

Retry count can mask profile mismatch, lifecycle bugs, or the wrong formal backend while producing occasional lucky accepts.

### Smallest honest next move

Apply the retry contract and soft-reject ladder; compare backends by fresh server acceptance, not by patience.

### Self-check

If attempts are far above the clean-sample attempt shape, what owned layer changed?

## Anti-pattern 53: Pick the formal runtime by local ciphertext equality

### The tempting shortcut

Two hosts produced the same token bytes once, so that host is formal.

### Why it creates false progress

Correct runtimes can differ byte-for-byte while both being wrong for the server, or one lucky equal string can hide lifecycle drift.

### Smallest honest next move

Run the formal backend bakeoff: profile → lifecycle → inputs → state → fresh server accept.

### Self-check

Which smoke level and fresh-round gate promoted this backend?

## Anti-pattern 54: Treat HTTP 200 plus a hint or string array as page success

### The tempting shortcut

The last page returned HTTP 200 and an array, so pagination is done.

### Why it creates false progress

A success-class body can still be strings, hints, mixed types, or a shorter marker array. Status and `isinstance(data, list)` do not prove the typed business contract.

### Smallest honest next move

Keep session, transport, query, and parser fixed. Flip only the hypothesized page-local request profile. Require the typed payload contract, and keep sibling pages on the ordinary profile.

### Self-check

Would this body pass the exact item-kind and cardinality oracle, or only `HTTP 200` plus "it was an array"?

## Anti-pattern 55: Jump to a patched digest because the unsalted standard primitive missed

Temptation:

- `md5(caller)` misses the captured digest, so the compress function must be custom
- WASM name-section `MD5` plus missing contiguous IV bytes looks like a modified digest
- Window/document/body imports look like DOM state that belongs in the preimage
- JSEncrypt ciphertext differs from a captured token, so the RSA must be custom

Why it is false progress:

- a textbook primitive plus a constant-pool prefix, suffix, or derived slice is still the same primitive
- IVs often live as `i32.const` in the hash function while the T/K table sits in the data segment
- bindgen host imports can be existence gates that are cloned and dropped without property reads
- random PKCS#1 padding makes inequality expected; a constant PS makes gold-token equality valid; named JSEncrypt or JSBN is still the standard padding family

Smallest honest next move:

- freeze the captured digest and test unsalted, prefix, and suffix joins against recovered constant-pool or derived strings
- keep the textbook primitive when a join hits; only then open packing, encoding, IV, and round-function checks
- instrument host imports; if the object is dropped without property reads, leave it out of the preimage
- for RSA, prove PKCS#1, the pad string, and concat including extra constant or delimiter-bearing joins before inventing a custom encrypt

Self-check:

- did unsalted miss and caller-plus-suffix hit before any custom compress work started, or did PKCS#1 plus concat hit before any custom RSA work started?





## Anti-pattern 56: Clone a sibling collector before the current endpoint exists

Temptation:

- the previous sibling used a five-page integer data API, so this page must too
- leftover last-page UA text or an ajax wrapper is still in the HTML, so keep the old request builder

Why it is false progress:

- sibling-shaped paths can 404 on the current live contract while the HTML still carries template copy
- a decoy wrapper that stores `data.m` and never sends is not a business API
- cloning the old collector hides the real request (or the fact that there is no data API)

Smallest honest next move:

- probe the hypothesized sibling path with the current session and require a live non-404 plus the typed payload contract
- if it 404s, record it as decoy/leftover text and recover the current page's actual exit
- do not promote leftover UA or pagination folklore until a data API exists

Self-check:

- did a same-session status probe prove the current endpoint exists before the sibling collector shape was copied?

## Anti-pattern 57: Pin a packer PRNG so unpack halts, then declare the signer missing

Temptation:

- wrapNative or a plain `Math.random = () => 0.05` makes the packer stop crashing, so keep the pin
- `eval(packer)` returned a function, so harvest that string and replay it in a fresh iv8/Node world
- construct the trap, probe for 50-200ms, and conclude the export was never installed

Why it is false progress:

- a native-looking PRNG pin can hang unpack; a plain constant pin can halt unpack without building the inner signer runtime
- iv8 `time_mode="logical"` advances `Date.now()` by 1ms per call; a packer anti-debug delta can halt or hang even with native `Math.random`
- the string passed to `eval(packer)` is not a self-contained module when packer init and unpacked body share one world; the harvested function exists and then crashes on call
- some parent VMs install `window` exports on a timer; a short post-construct probe is not absence proof
- `checkEnv === true` with every risk flag false can be a stale handshake bit, not the signer gate

Smallest honest next move:

- retry unpack with native PRNG under a subprocess timeout instead of keeping the pin
- if native unpack still halts or hangs, switch iv8 `time_mode` to `system` before more PRNG experiments
- run `var x = eval(packer)` in the same world that will call `x`
- advance logical time (`eventLoop.sleep`) before claiming an export is absent
- distinguish a dirty iframe getter (`exception.message` read) from the clean timer path

Self-check:

- did the signer call succeed after native unpack, `time_mode="system"` when unpack is time-sensitive, plus an explicit timer settle, without firing DevTools getters?

## Anti-pattern 58: Clone a sibling request shape because leftover UA or call looks shared

Temptation:

- the previous sibling used POST, a time header, a 64-hex `call(page)` return, and a frozen `Date.now`, so keep that request builder
- leftover last-page UA text or a `window.call` name is still in the HTML
- the current path + clock + page concat looks shared, so keep the sibling request builder and its calculator

Why it is false progress:

- method, time slot, token width, and export-versus-pager semantics are independent contracts
- a pager `call` that triggers ajax is not a token-returning export
- GET plus a query clock plus a 32-hex named digest is still a different contract from POST plus a time header plus a 64-hex pager return
- leftover UA text can be a real last-page exception on the current route and still not license the rest of the sibling shape
- independently proving the same concat shape does not prove the same calculator

Smallest honest next move:

- recover the current method, time writer, token alphabet or width, and whether `call` returns or only dispatches
- reuse only the page-local exception after a typed negative control
- keep leftover UA as a hypothesis, not as a collector clone

Self-check:

- did method, time slot, token width, and export/harvest boundary each pass a current-target wire check before any sibling request field was copied?

## Anti-pattern 59: Freeze Date.now because a sibling used a server clock

Temptation:

- a nearby job froze Date.now to a server-issued clock and the request accepted, so freeze Date.now again

Why it is false progress:

- Date.now is only one clock-looking sibling
- a signer can read ajax success, a callback, a rewritten getter, a signer argument, or a query clock field
- an inner Date constructor is another quiet sibling until those bytes are copied onto the request
- freezing the quiet sibling leaves the request clock unbound

Smallest honest next move:

- name the writer the signer reads, including a signer argument or query clock field
- inject the server clock into that writer
- keep a Date.now or inner Date freeze only after that getter is the observed writer

Self-check:

- did the frozen server clock enter the observed writer, and did the same bytes appear on the request?

## Anti-pattern 60: Clone a sibling signer because the preimage concat looks the same

Temptation:

- the current path, clock, and page concat looks like the last job, so reuse that Huffman/XOR, named inner codec, textbook digest, last Python helper, or RSA encrypt
- independently proving the same concat shape feels like proving the same calculator

Why it is false progress:

- concat shape is the preimage contract; the calculator is a separate writer
- extra join delimiters such as `N$` versus `N()` are current-target concat evidence, not permission to copy the sibling helper
- a 32-hex token and a Base64 RSA ciphertext are different writer families even when both queries carry `token` and `now`
- a named inner codec, Huffman/XOR mix, textbook digest, host-branch digest, and PKCS#1 RSA can all consume the same concat family
- gold-token equality against the sibling helper does not prove the current writer; random PKCS#1 makes gold-token equality the wrong oracle, while a current constant PS still does not copy the sibling random writer

Smallest honest next move:

- identify the current writer family independently of concat shape
- for a digest writer, freeze a tiny-input digest; for PKCS#1 RSA, freeze the pad string first, then use gold-token equality only if PS is constant, otherwise live decrypt or typed accept
- keep the sibling helper only after that current-writer check matches
- if it misses, recover this page's calculator instead of porting the last codec

Self-check:

- did the current writer family and current-writer proof match before any sibling calculator was copied?

## Anti-pattern 61: Hunt a signer or OCR because list HTML looks obfuscated

Temptation:

- the list cells are stacked images with extra classes, so there must be a missing `sign` field
- OCR or a browser `getComputedStyle` read will be faster than reconstructing CSS placement

Why it is false progress:

- a page-only POST with schema-valid HTML is often `decode-gated`, not signer-gated
- extra classes can be hide tokens derived from companion JSON fields
- source order is not visual order; OCR and class-name maps miss in-flow offsets and hide-class drops

Smallest honest next move:

- freeze raw HTML plus companion fields
- prove the hide-class chain on a fixed vector, drop those nodes, then place remaining glyphs by `inFlowWidth * visibleIndex + leftOffset`
- identify glyphs by image-byte hash
- route to `references/response-decode-playbook.md`

Self-check:

- does the wire body contain only a page index or id, and does hiding the wrong class change the integer?

## Anti-pattern 62: Call check-API success complete while finish stays false

Temptation:

- `status_code=1` / `message=success` already came back, so the challenge is done
- skip GET on the challenge document because the collector already has the session cookie

Why it is false progress:

- answer-accept and complete can be separate oracles
- a cookie-only POST can accept the number and leave `finish` / `done` / `complete` false
- packaging that response as collector success hides a missing document-warm latch

Smallest honest next move:

- warm GET the challenge document on the same jar, then POST check
- require both answer-accept and complete
- if the document GET rotates a token, follow the page-bound submit-token rule

Self-check:

- did complete flip after the document GET, and would skipping that GET still leave complete false?

## Anti-pattern 63: Treat 403 on a named-digest API as session death or WAF

Temptation:

- textbook MD5 of the timestamp got HTTP 403 JSON forbidden, so the cookie is dead
- rotate the session, change UA, or blame WAF before the digest/clock pair is proved

Why it is false progress:

- sibling APIs on the same session can still return 200
- 403 forbidden on this API is not session death
- the same 403 can be a bad digest/clock pair or a stdlib TLS miss; do not pick one until the same admitted token bytes are replayed on impersonate
- hashlib ascii and digit-byte both missing the frozen vector is helper evidence only after impersonate still 403s

Smallest honest next move:

- compare sibling-API 200 vs this-API 403 on the same jar
- replay the same live-admitted token or cookie bytes on stdlib versus installed curl impersonate
- if impersonate returns business 200, stop signer reverse and keep the transport exception; see anti-pattern 68
- if impersonate still 403s, freeze one timestamp and the bundled digest; keep the helper after dual hashlib miss

Self-check:

- did sibling APIs still return 200, and did stdlib-versus-impersonate on the same admitted bytes decide transport versus digest before the session was rotated?

## Anti-pattern 64: Eval a recovered hasher-side function in Node

Temptation:

- a large integer array sits next to MD5 T/K, so reconstruct and run it to recover constants
- Node eval of recovered R will show the real digest branch

Why it is false progress:

- that array can be charcodes of a function, not T constants
- hasher `bytesToHex` / round helpers may `eval` or `setInterval(eval)` as a side-effect bomb, not as preimage
- in a browser the eval often fails and falls through to `Date.now()`
- Node has `require` and process-spawn surfaces, so executing recovered R is hostile

Smallest honest next move:

- stub `eval` and timers, keep the digest, never execute recovered R
- harvest the helper and run it under stubs; Python owns HTTP

Self-check:

- does the digest still match the frozen vector with eval/timers stubbed, and was recovered R left unexecuted?

## Anti-pattern 65: Launch a second Chrome because the user asked to open DP

Temptation:

- the user said open DP, so start `chrome-devtools` and `js-reverse`
- a second view of the same page will make initiator capture safer

Why it is false progress:

- `chrome-devtools` MCP launch Chrome is an automation-marked host
- DP means attach/select on the current `TARGET_ACTIVE` host
- a second browser changes the fingerprint and can trip the gate before any signer work starts

Smallest honest next move:

- if DP/initiator work is already required, let `js-reverse` own baseline and debugger-trace on one host
- record `launch` vs `attach`; never pretend launch is attach
- if attach is missing, record `debugger_attach_gap` and continue silent-value or offline

Self-check:

- did opening DP launch any Chrome that was not already the single `TARGET_ACTIVE` host?

## Anti-pattern 66: Copy a newer live Chrome major onto a lower curl impersonate

Temptation:

- desktop Chrome is 152, curl_cffi latest is chrome146, so paste 152 into UA and Client Hints
- the new challenge page means the old risk-control reverse is worthless

Why it is false progress:

- TLS/H2 impersonate, UA, Client Hints, and navigator major are one capsule
- mixing majors creates a new challenge family and makes every reverse look stale
- that is `transport-admission` / profile-drift, not a missing signer

Smallest honest next move:

- lock replay to the installed curl impersonate chrome major from `scripts/check_reverse_env.py`
- match evidence-host major to that impersonate when possible
- repair the capsule before restarting application-layer reverse

Self-check:

- do impersonate, UA, Client Hints, and navigator all share one chrome major from the installed curl profile?

## Anti-pattern 67: Bulk-add unproven APIs when risk-control is unknown

Temptation:

- the known business request is risk-blocked, and HAR shows five or six extra URLs
- adding telemetry, config, log, and sibling business calls might be the missing gate

Why it is false progress:

- unknown risk-control is usually a writer, cookie, token, or identity problem on the rejected request
- bulk-adding unproven routes dirties the transcript and hides the real oracle
- sidecar membership requires omission that changes the oracle, then restoration

Smallest honest next move:

- reverse the rejected request first: same-URL diff, initiator, writer, cookie mint
- unproven extra routes are at most one per round
- keep sidecars that pass omission and restoration; freeze the request set after two no-change rounds

Self-check:

- if this extra route is deleted, does the clean-browser business oracle change?

## Anti-pattern 68: Treat stdlib 403 of a live-admitted token as a bad signer

Temptation:

- an in-page or clean-browser fetch already returned business 200 with this token, but stdlib still gets HTTP 403 JSON forbidden, so the helper, canvas, or clock must be wrong
- sibling APIs return 200 on stdlib, so this 403 cannot be transport

Why it is false progress:

- sibling-200 plus this-route-403 is not session death and is not automatically a bad digest
- copied headers and cookies on stdlib can still die at TLS/H2 while impersonate admits the same bytes
- restarting signer or fingerprint reverse hides a transport-admission miss

Smallest honest next move:

- freeze the admitted token or cookie bytes
- replay those exact bytes on stdlib versus installed curl impersonate
- if impersonate returns business 200, keep the route-local impersonate exception and stop token reverse
- lock UA, Client Hints, navigator, and TLS/H2 to that impersonate chrome major

Self-check:

- did the same admitted bytes 403 on stdlib and 200 on impersonate before any helper rewrite?

## Anti-pattern 69: Chase canvas after impersonate already returns business 200

Temptation:

- the mint helper touches canvas, audio, or WebGL, so those surfaces are the remaining HTTP gate
- fake local canvas is too crude; rebuild a realistic fingerprint host

Why it is false progress:

- once impersonate plus the local cookie-mint helper already returns diverse business JSON, fingerprint APIs are not the remaining HTTP gate
- extra canvas/WebGL/audio work is host gold-plating after transport admission

Smallest honest next move:

- keep the tiny local helper that already admitted
- Python owns HTTP on the admitted impersonate
- escalate fingerprint surfaces only if impersonate plus that helper still fails a business oracle

Self-check:

- did impersonate plus the current helper already return business 200 before canvas/audio reverse resumed?

## Anti-pattern 70: Seed impersonate cookies without a request hostname

Temptation:

- `Cookies.set(name, value)` with an empty domain is fine because curl will fill the host later
- keep the session cookie domain-less and bind only the rotating token to the hostname

Why it is false progress:

- empty-domain cookies and host-only cookies split the jar
- `get_dict(domain=host)` can drop the session cookie while a host-only token remains
- submit or list calls then look signed but are missing identity

Smallest honest next move:

- seed every impersonate-client cookie with the request hostname
- replace same-name cookies on that host; do not mix empty-domain and host-only writers
- compare the outbound `Cookie` header, not only `get_dict()`

Self-check:

- do session and rotating tokens share one request hostname, and does the outbound header carry both?

## Anti-pattern 71: Treat HTML placeholder zeros as business data when no list XHR fired

Temptation:

- the table already shows numbers, so scrape the DOM
- zeros mean the API returned empty rows

Why it is false progress:

- placeholder markup is not the list contract
- if the VM never issued the list request, those zeros are render defaults
- summing them produces a wrong numeric answer

Smallest honest next move:

- prove a list XHR, fetch, or WebSocket/text channel exists before treating DOM numbers as data
- if no list request fired, debug observation or activation, not the payload schema
- if a similarly named REST path returns HTTP 200 with constant filler, treat it as a dummy sibling, not the list

Self-check:

- did a list request or WebSocket frame return the values, or did the HTML render zeros with an empty or dummy network log?

## Anti-pattern 72: Upgrade Camoufox because CDP navigator.webdriver is true

Temptation:

- Chrome CDP shows `navigator.webdriver === true`, so the baseline is burned
- wrap XHR or `toString` to force a silent JSVMP to talk
- switch to Camoufox or a managed profile immediately

Why it is false progress:

- a JSVMP can skip the business XHR while webdriver is true and still render placeholder zeros
- `Navigator.prototype.webdriver` is often configurable; deleting it in an authorized initScript can unblock the request on the same Chrome owner
- wrapping `toString` or XHR on a signature-bound VM poisons the run
- Camoufox is fingerprint-pressure escalation, not a webdriver-boolean fix

Smallest honest next move:

- if the property is configurable, delete it in initScript and recapture the list XHR
- record `launch` vs `attach`; do not pretend the CDP session is a clean user Chrome
- escalate the baseline host only after that one-variable control still shows fingerprint refusal

Self-check:

- did deleting configurable `navigator.webdriver` make the list request appear before Camoufox was opened?

## Anti-pattern 73: Chase JSVMP opcodes before protobuf serializeBinary or wasm encode I/O

Temptation:

- the page is a huge VM, so the token must live in bytecode
- dump handlers because the request body is unreadable

Why it is false progress:

- protobuf `serializeBinary` and a wasm export such as `encode(i32,i32)` are public boundaries
- opcode tours delay a replay that only needs field numbers plus a two-arg encoder
- captured stale clock-bucket fields 403 even when the encoder is correct

Smallest honest next move:

- freeze one request hex and one response hex at the serializer or XHR send
- identify wasm or export arity and protobuf field numbers
- regenerate fresh clock-bucket inputs through the same encoder; a second int32 may be client-chosen if the token remains `encode(t1,t2)`

Self-check:

- can one public serializer plus one wasm or export I/O rebuild the body before any opcode log exists?

## Anti-pattern 74: Trust MCP or DevTools UTF-8 dumps as protobuf bytes

Temptation:

- save the network request or response from the MCP tool and parse it
- the body looks binary in the UI, so the saved file is the wire

Why it is false progress:

- text-oriented MCP or DevTools dumps decode binary as UTF-8 and write `U+FFFD`
- those replacement bytes are not the protobuf
- a Python decoder then looks broken and the reverse restarts at the VM

Smallest honest next move:

- capture ArrayBuffer or hex at `serializeBinary`, XHR send, or a binary-safe save
- compare hex length and leading field tags, not printable strings

Self-check:

- does the saved body contain `U+FFFD` or a length that is not the XHR `byteLength`?

## Anti-pattern 75: Treat an empty ajax beforeSend IIFE as a missing signer

Temptation:

- the ajax call has a `beforeSend` hook, so a token writer is missing
- the hook is an empty or no-op IIFE, so hunt JSVMP or mint a sign field

Why it is false progress:

- a hook that adds no header, query, cookie, or body slot is not a mutation point
- if the captured body already equals the visible business fields, there is no extra signer
- token reverse delays the real next gate, usually transport admission

Smallest honest next move:

- freeze the captured body and diff it against the visible fields
- if they match, skip signer reverse
- ablate stdlib versus installed curl impersonate on those same bytes

Self-check:

- did the captured body gain any extra slot after `beforeSend`, or did it stay the visible fields?

## Anti-pattern 76: Treat a dummy HTTP sibling or HTML zeros as the list while a WebSocket channel is unproven

Temptation:

- the table already shows zeros, so scrape the DOM
- GET/POST of the similarly named REST path returned HTTP 200 JSON, so sum that body
- a list-shaped URL exists, so the WebSocket is telemetry

Why it is false progress:

- placeholder markup is not the list contract
- HTTP 200 with a constant filler value is a dummy sibling, not grant
- mixed-transport silence or dummy on one channel does not retire a WebSocket or text channel

Smallest honest next move:

- freeze one live WebSocket or text business frame before summing
- treat dummy HTTP filler and HTML zeros as decoys in notes, never as collector inputs
- only scrape DOM numbers after the same values appear on the proved list channel

Self-check:

- did the summed values come from a WebSocket or list frame with business semantics, or from HTML zeros / a constant HTTP dummy?

## Anti-pattern 77: Port named AES as AES-128 because a longer token is 16-aligned

Temptation:

- the export is `AES.encrypt` with ECB PKCS7 and a 16-byte key
- the live token length is a multiple of 16, so textbook AES-128 is done
- Node without `navigator` diverges, so the cipher is patched AES; strip `debugger` until gold matches

Why it is false progress:

- a short vector such as `"hello"` that yields 8-byte ciphertext is a 64-bit block cipher (DES/3DES), not AES-128
- 16-byte keys plus 16-aligned longer tokens are still 3DES when the block size is 8
- `try { if (navigator) {} } catch` can reorder DES key slices; a Node miss is the catch-path schedule
- stripping `debugger` to force gold equality poisons clamp/cipher math

Smallest honest next move:

- freeze a short plaintext and measure ciphertext length before a standard AES library
- port the browser host-object branch; keep the missing-navigator order as a negative control
- require live business accept, not token length or alphabet

Self-check:

- does the short vector show 8-byte or 16-byte blocks, and does the local replica use the browser key order?

## Anti-pattern 78: Treat a chrome-devtools HTTP-only resource log as proof there is no WebSocket list

Temptation:

- `list_network_requests` showed only document, css, and js
- there was no XHR, so the filled DOM must be inline packed data
- HTML started as zeros and later showed numbers, so scrape the table

Why it is false progress:

- chrome-devtools `list_network_requests` is an HTTP resource inventory, not a WebSocket inventory
- mixed-transport silence on HTTP does not retire a WebSocket or text channel
- placeholder zeros plus later DOM numbers still need a list-channel proof

Smallest honest next move:

- hook `WebSocket` constructor/send/message, or use `js-reverse` `get_websocket_messages`
- freeze one live WebSocket or text business frame before summing
- keep dummy HTTP siblings and HTML zeros as decoys

Self-check:

- did the HTTP resource log actually include WebSocket frames, or was the list channel never visible to that tool?

## Anti-pattern 79: JSON-parse or sum the first short WebSocket text frame as the list

Temptation:

- the first inbound text is short and arrived right after send, so parse it as JSON
- the short constant looks numeric, so add it into the page sum
- the next send's first recv is the same constant, so the socket cannot multiplex and the signer must be wrong

Why it is false progress:

- prefix, ack, and heartbeat frames can be non-object text before the business JSON
- JSON.parse failure of the prefix is frame class, not a missing cipher
- one recv landing on the prefix does not prove reuse failed

Smallest honest next move:

- classify inbound text before parse
- skip non-object frames and keep reading until the business JSON object
- require `status=1` plus the expected value count before summing

Self-check:

- did the summed values come from a business JSON object after skipping non-object frames, or from the first short text?

## Anti-pattern 80: Skip an issued challenge to protect accuracy

Temptation:

- contrast, margin, or OCR confidence looks weak, so GET a fresh image instead of POSTing `distant` / the answer
- a search cap below the canvas right edge already found a dark column, so skip this round
- verifier returned `success` with `rate=66.67%`, so keep paginating

Why it is false progress:

- unused issuance often increments the session miss counter; the next business page 403s even though the later answer was correct
- submitted-wrong is frequently retryable on a newly issued round; unused-issue is not
- accept-body `rate` can be a cumulative floor; reject-body `rate` can be this-answer closeness
- an arbitrary search cap misses real holes near `width - piece_width`

Smallest honest next move:

- consume every issued round, or abandon the session
- prove unused-issue versus wrong-answer with one-variable controls
- search the full canvas and score a piece-sized four-edge rectangle before retuning tracks
- send the first downstream page only when the cumulative stays above the proved floor

Self-check:

- if I issue twice and submit once correctly, does the next page still pass? If no, skip-to-refresh is session poison.

## Anti-pattern 81: Treat an eval/Function compile snapshot as a call trace, or wrap global apply/call

Temptation:

- wrap `Function.prototype.apply` / `call` globally because the VM dispatches through them
- treat the string passed to `eval` / `new Function` as a call-stack dump
- hook only after the compiled function runs

Why it is false progress:

- global `apply`/`call` wraps are observer-toxic and hang mixers
- the compile body after param substitution is the key material; the later call is only execution
- a call trace without the substituted body misses dictionaries and recovered helpers

Smallest honest next move:

- Proxy the `Function` constructor or wrap `eval`, snapshot the body after substitution, then restore
- correlate the snapshot with silent-value recipe G
- never patch global `Function.prototype.apply` or `.call`

Self-check:

- did I capture the substituted compile body, or only the later invocation?

## Anti-pattern 82: Feed an old nondeterministic sequence into a new-session script

Temptation:

- reuse yesterday's `Math.random` / `Date.now` / canvas / audio feed on a freshly downloaded SDK
- splice two traces because the counts look similar

Why it is false progress:

- dynamic scripts re-randomize per session; seq alignment belongs to one atomic run
- a new script consuming an old feed crashes or mints a different artifact

Smallest honest next move:

- freeze script hash, config/ticket, and feed from the same run
- recapture for a new session; replay the old script if you need the old values

Self-check:

- is the feed's script hash identical to the script I am about to execute?

## Anti-pattern 83: Count canvas or navigator JS-shim probes as host-fidelity L0

Temptation:

- report L0 pass because `canvas.toDataURL` or `navigator` was called N times locally
- treat JS shims as native engine probes

Why it is false progress:

- L0 counts native sources (`Math.random`, `Date.now`, native `eval`); JS shims are invisible to native probes
- shim probe-count is heat, not fidelity

Smallest honest next move:

- score L0 native count, L1 sequence LCS, L2 value feed, L3 protocol param-set, L4 eval sha256
- feed shim values from the same session; do not probe-count them

Self-check:

- did the L0 number come from native engine sources, or from a JS shim I wrote?

## Anti-pattern 84: Mount webpack UI instead of exposing require

Temptation:

- patch Vue `$mount`, transitions, and layout until the SDK encrypts
- treat missing DOM as a reason to keep adding UI stubs

Why it is false progress:

- UI rendering is a sinkhole; encrypt usually lives in a webpack module
- crash points keep moving right through cosmetics

Smallest honest next move:

- patch webpack bootstrap to expose `__wpRequire`
- call the encrypt export with frozen args
- patch UI crash points only if that export is unreachable

Self-check:

- can I call the encrypt export without `$mount`?

## Anti-pattern 85: Run setTimeout callbacks synchronously, or ignore fromCharCode heat

Temptation:

- implement `setTimeout(f)` as `f()` because there is no event loop
- keep adding env patches when `fromCharCode` heat is 0

Why it is false progress:

- a sync `setTimeout` turns polling/retry into a recursive hang
- million-scale `fromCharCode` vs 0 diagnoses VM entry, not missing canvas

Smallest honest next move:

- queue macros and drive with `__drainTimers__`; `setInterval` returns 0 on no-native hosts
- if `fromCharCode` heat is 0, fix VM entry/init before more host cosmetics

Self-check:

- does `setTimeout` return before the callback runs, and did VM-entry heat move?

## Anti-pattern 86: Mix source class with ownership, drag from box center, ship OCR as collector, or swallow import bugs as platform-down

Temptation:

- treat plaintext and local-algorithm as one recovery move, or copy source class onto ownership class
- drag from box center `(x1+x2)/2` because the box looks centered on the gap
- import an OCR/captcha-platform client into the collector
- `except Exception` around optional extras so import/`NameError` looks like "platform down"

Why it is false progress:

- source class is origin; ownership class is who may emit the value; mixing them picks the wrong rewrite
- center origin overshoots by half a gap width
- OCR is a diagnostic for a visual oracle, never collector runtime
- a wide except hides our bugs as vendor outages and leaves stdout polluted

Smallest honest next move:

- label source class and ownership class on separate columns
- use box `x1` as drag origin
- keep OCR off the delivery path
- alarm import/`NameError` on stderr; fallback only on typed external timeout; keep stdout machine JSON

Self-check:

- if the optional extra is missing, do I see our bug on stderr, and is stdout still JSON?

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


