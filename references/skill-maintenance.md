# Skill Maintenance

Use this file when modifying `spider-king` itself.

## Contents

- [Validation](#validation)
- [Forward-test Evidence](#forward-test-evidence)
- [Reproducible Experience Gate](#reproducible-experience-gate)
- [Deposition Rules](#deposition-rules)

## Validation

Validate against `references/official-self-test-task-suite.md` before calling the edit complete.

Pass conditions:

- the route stays protocol-first
- every fresh web target classified as `live-target` begins with sequential `fingerprint-baseline` then `debugger-trace` evidence before any page/runtime-understanding claim; default means are `chrome-devtools` then `js-reverse`, and the baseline host may upgrade to Camoufox or another managed profile only on proved fingerprint pressure or clean-baseline failure (never default Camoufox for ordinary low-risk work); the only endpoint-scoped delivery exception is the strict transport-only direct-endpoint gate in `startup-triage-playbook.md`, which keeps role gaps explicit and exits on any signer/bootstrap/decode/browser-state surface; `artifact-only` web routes do not invent browser evidence, and APK/app/mini-program primary tasks stay out of scope
- sequential role evidence stays serial: only one browser or engine-capture family owns `TARGET_ACTIVE`; `js-reverse` and `silent-value-capture` never share a parallel target batch with baseline; silent-value never owns `compact-replay`/`collector`
- lifecycle wording distinguishes `PARKED` from confirmed closure and uses `RETAINED_EXCEPTION` rather than destroying unique unreplayable state
- browser-mode and cleanup guidance reflects installed tool capabilities instead of inventing `close_browser`, headless, headful, or CloakBrowser controls
- intake routing distinguishes `live-target`, `artifact-only`, and `continuation` without forcing ceremonial browser startup or inventing live proof
- the tool playbook contains only supported core methods or explicit optional-method fallbacks, and every live-target gate emits a capability snapshot
- browser acquisition roles are capability-aware, may hand off sequentially, and never become a vendor-specific one-route-for-the-whole-job mandate
- hook timing guidance distinguishes preload, early-breakpoint, controlled-reload, and post-load-only evidence without inventing unavailable methods
- official tasks are structurally parsed into prompt, expected routes, and required conclusions instead of being validated by headings alone
- the canonical official-suite contract digest covers every task prompt, route, conclusion, and failure signal; update it only after intentional suite review
- reports redact secrets by default and require a secret-free `analysis/proof_manifest.json`
- capability-specific delivery gates allow honest `evidence` and `local-proof` completion without collector-only replay or entrypoint requirements
- provider writes require a writable mode, a non-empty inherited `allowedPaths`, resolved containment, and reparse-point rejection
- the implementation brief is conditional for ambiguous or authority-widening `compact-replay` / `collector` work and never blocks bounded `evidence`, `local-proof`, or an implementation choice the user already made
- environment diagnostics report project-root, virtual-environment coherence, runtime versions, and explicitly requested lockfile fingerprints without hardcoded machine paths or default global-interpreter rejection
- compact replay and collector handoffs summarize endpoint, moving-state writer and slot, session refresh, proof, runtime split, and saved paths without proliferating project documentation
- default validation never executes candidate scripts; use `--run-trusted-self-tests` only for the trusted current root
- trusted self-tests recursively reject symlinks, reparse points, hard-linked dependencies, and root escapes across the full local `scripts/` tree, then terminate their process tree on timeout
- static Python validation recursively parses every shipped `.py` file outside cache directories, including tests and reusable examples
- generated tool caches (`.pytest_cache`, `.ruff_cache`, `.mypy_cache`, `__pycache__`, `.cache`, `htmlcov`, `node_modules`, venvs) are package errors; scanners may skip their contents only to avoid duplicate noise
- generated local noise (`.pyc`, `.log`, `.tmp`, `.DS_Store`, coverage files) and test-runner dumps (`tests/_err_*.txt`, `tests/_out_*.txt`) are package errors and must stay gitignored
- run unit tests with `PYTHONDONTWRITEBYTECODE=1` (also enforced by `tests/conftest.py`, which auto-cleans leaked cache/dumps on session finish)
- to scrub known dirt then re-validate: `python scripts/validate_skill.py --clean-hygiene`
- `agents/openai.yaml` parses with typed `interface` metadata, a 25-64 character short description, a `$spider-king` default prompt, and a boolean implicit-invocation policy; when PyYAML is absent, the validator's fallback accepts only the reviewed two-level mapping/scalar subset and rejects complex YAML constructs
- final delivery never depends on browser automation
- final delivery is Python collector first, with JS limited to local parameter restoration only
- minimal missing evidence is requested instead of broad homework for the user
- the chosen references match the real symptom instead of generic cargo-cult loading
- output reports the real endpoint, real moving parts, and proof artifacts
- static `validation=PASS` is only a structural result and must never be described as real-world forward-test or anti-decay proof
- behavioral claims require an external `scripts/forward_test_report.py` report produced by a fresh runner and an independent reviewer; keep that report outside the skill tree
- structured transport, decode chains, stateful sessions, and delivery gates are handled correctly when present
- challenge-generated state and shared envelope-family cases are handled correctly when present
- transport pre-gates, challenge artifact harvest, and route-local bypasses are handled as generic patterns when present
- native transport escalation requires repeated runtime captures, a proved backend expressiveness gap, route-local scope, and clean-package replay
- reproducible evidence deposits record a normalized package path and hash, the first meaningful chain divergence when one exists, and a proof-manifest artifact hash
- official evidence tasks route directly to `scripts/evidence_normalizer.py`, `scripts/transcript_diff.py`, and `scripts/practice_lab.py`
- the skill-owned loopback practice lab stays a direct-HTTP fixture and does not trigger the fresh live-target browser gate
- the entry `SKILL.md` stays lean enough to route to detailed references instead of duplicating them; put new reusable knowledge only in the most specific playbook/reference
- every Markdown reference longer than 100 logical lines retains a top-level `## Contents` section
- every profile handoff is capability-aware: use an installed specialist when available and name an executable Spider fallback when unavailable
- every profile-local `references/` or `scripts/` route resolves from either the profile root or the skill root
- profile dependency installation occurs only in an approved task-local copy, never in the skill directory

## Forward-test Evidence

Use `references/forward-testing-playbook.md` for the execution contract. The validator does not call a model or arbitrary command: it verifies an already-produced report, its current `SKILL.md`, package, and official-suite hashes, every response artifact, and each independent route/conclusion judgment.

- `scope=smoke` may cover a deliberate subset and is reported as smoke evidence only
- `scope=full` must contain all 191 unique official tasks before it can be reported as a full pass
- runner and reviewer identities must differ; both contexts must be fresh and the review must be explicitly independent
- every route and conclusion judgment needs an exact excerpt found in the referenced response file
- response files stay under the report directory and must not be symlinks, reparse points, hard links, or path escapes
- preserve the report and response artifacts outside the skill package; do not turn static validation into a behavioral claim

## Reproducible Experience Gate

Use the fields and storage lifecycle in `references/experience-card-schema.md`.

Before promoting a practical lesson:

- keep a one-off result task-local until the same invariant recurs in two independent jobs
- attach one minimal secret-free fixture or deterministic generator and record its path and SHA-256; exact JSVMP vectors also freeze or replay time, entropy, counters, session/round state, canonical bytes, and profile identity in one capsule
- define a positive oracle that checks the decisive downstream behavior, not merely helper load or plausible output shape
- define one negative control that fails for the intended protocol reason
- record the first divergent state transition and the boundary where the lesson stops applying
- promote the repeated invariant to an experience card; promote it to a generic playbook or helper script only when the same decision or deterministic operation remains useful across independent cases
- do not count a prose-only prompt, copied live artifact, or unscored successful replay as reusable experience

## Deposition Rules

After a successful job, preserve only the reusable lesson:

- convert site-specific pain points into generic pattern language
- preserve family-triage lessons and observer-effect lessons as generic routing rules
- preserve shell-versus-data lessons as render-contract rules, not "the HTML looked empty on site X"
- preserve success-flag lessons as response-validation rules, not one vendor's `errorCode`; outer accept or status can mean the request was processed while an inner result or fail count still rejects
- preserve symptom-versus-root-cause lessons: a visible slider, SMS wall, or verifier page can be downstream presentation of missing trust or bootstrap state, not the first gate to attack
- keep fixed-input validation habits, not endpoint trivia
- preserve server-issued-state lessons as inventory, scope, expiry, and refresh-path rules, not copied session ids or challenge configs
- preserve clean-anonymous-baseline lessons as environment-selection rules, not copied account cookies
- preserve cookie provenance lessons as writer and refresh-path rules, not copied cookie values
- preserve signer-boundary lessons: when one synthetic request through a hooked transport acquires signer params automatically, record the injection boundary separately from the business payload schema
- preserve observation-boundary lessons: a quiet cookie, storage, header, or request hook only clears one writer boundary, not every issuance path
- preserve mixed-transport lessons: silence on one `fetch`, XHR, wrapper, worker, or message channel is not proof that sibling channels are inactive; an XHR `open` substring filter misses relative URLs, so filter on the resolved URL
- preserve evidence-surface-separation lessons: initiator and source traces prove where logic lives, wire or egress proves what crossed the boundary, environment traces prove host truth, and downstream business replay proves actual acceptance
- preserve page-owned-world lessons: console or isolated-world misses can be tooling-bound, so repeat the proof in the page-owned world before deleting the hypothesis
- preserve request-bound logging lessons: values tied to target, event, method, URL, field, or caller age better than raw dumps
- preserve method-argument and returned-object lessons: decisive gaps can hide in call arguments or child-object shape, not only in named property reads
- preserve observe-only lessons: default hooks should preserve original behavior and return paths unless mutation is itself the experiment
- preserve cheap-codec lessons: solve weak field obfuscation locally and leave only the truly environment-bound signer in the hard bucket
- preserve standard-primitive-plus-concat lessons: an unsalted textbook digest or key miss is not proof of a patched compress function until constant-pool prefix, suffix, derived-slice, and extra constant or match-number joins fail, including delimiter-bearing suffixes; a statement-split named JSEncrypt/JSBN/RSA helper is still PKCS#1 v1.5; freeze the pad string first; random type 2 makes gold-token inequality the wrong custom-port trigger, while a proved constant PS makes gold-token equality a valid oracle
- preserve host-import-existence lessons: Window/document/body imports without property reads are existence gates, not automatic preimage material
- preserve host-function-existence and instanceof IV/shift/packing/compress-mask branch lessons: `typeof require`, `__dirname`, native-looking `print`, `setImmediate`, native `Date.now`, and prototype identity can select digest constants; Node eval of a harvested digest file is a different environment and can hang; port the browser branch as a local replica before porting IVs
- preserve decoder-integrity-loop lessons: obfuscator-style decoder prototypes that grow arrays forever are anti-debug, not missing strings
- preserve per-byte packing-collision lessons: even/odd ASCII digits can collide after `& 0xfe`; same-clock digest equality is packing evidence, not interchangeable pages
- preserve Function-wrapped debugger lessons: `Function("debugger")` can hang page-world evaluate or a live js-reverse re-call; a dead `!==` around one constructor does not make attach safe; skip js-reverse attach, harvest and rewrite offline; neutralize Function in an authorized initScript only when that is the remaining path; do not re-issue a hung live re-call
- preserve page-state versus request-state lessons as separate moving-part classes, not vendor header names
- preserve verifier-family lessons: slider, point-click, icon-select, sequence-select, and risk-gate flows that look similar at the page level can still have incompatible state models and proof builders; a shared crypto shell does not prove a shared answer schema
- preserve verifier-success-scope lessons: verifier-endpoint success can be intermediate, while downstream business acceptance is the final authority
- preserve same-world multi-slot lessons: locally valid fields can still fail when roundKey, identity cookies, shared events, or canonical request bytes disagree across helpers
- preserve protocol-profile lessons: viewport or UA cosplay is not a mobile/desktop protocol solve; freeze one profile across helpers
- preserve formal-backend lessons: promote runtimes by fresh server acceptance and layered parity, not local ciphertext equality or retry patience
- preserve positive-sample hygiene lessons: automation-contaminated failures are environment evidence first, not trajectory truth
- preserve verifier error-localization lessons: structure, sidecar, consistency, timeline, answer, and environment are ordered surfaces; vendor codes stay task-local
- preserve environment-risk lessons: exit reputation and consecutive rejects are a separate failure surface from algorithm regressions
- preserve family-evidence-threshold lessons: family-specific scaffolds and playbooks need corroboration across more than one evidence surface, not one lucky marker
- preserve local-noise-versus-gate lessons: server-looking names do not prove server issuance; prove writer, tolerance, and blocking value
- preserve locally minted state lessons: session-looking or fingerprint-looking cookies can be local protocol artifacts with exact UUID, digest, or compact-JSON structure, not copied `Set-Cookie` values
- preserve slot-placement lessons: a blob can be right in value and still wrong in position; field placement is part of the protocol contract
- preserve transport pre-gate lessons as narrow admission matrices and route-local exceptions, not frozen vendor UA cargo cults
- preserve page-local exception lessons: keep sibling pages on the ordinary profile, prove the exceptional page with a one-variable negative control, and do not promote an unablated last-page header
- preserve type-strict page-oracle lessons: HTTP 200 plus a string, hint, or mixed-type array is a trap, not pagination success
- preserve source-versus-live-contract lessons: saved source is capture-time client code; current wire and the typed business oracle decide today's contract, including omitted writers and newly required fields
- preserve pre-HTTP identity lessons: copied `User-Agent`, headers, or cookies do not clear a gate decided by ClientHello or HTTP/2 profile before normal request semantics exist
- preserve transport-summary lessons: JA3, JA4, or similar hashes are summaries of a deeper transport contract, so store the raw ClientHello, ALPN, and H2 rules rather than one lucky hash
- preserve closest-stack lessons: prefer the nearest real transport family or a narrow route-local adapter before hand-patching a distant default TLS stack field by field
- preserve runtime-over-enum lessons: implemented ciphers, groups, or extensions are not emitted-profile evidence until enablement, policy, platform, ordering, and packet captures agree
- preserve coherent-profile lessons: independently randomized ciphers, extensions, groups, ALPN, or H2 settings can create a client family no real browser emits
- preserve proxy-termination lessons: prove whether CONNECT tunnels end-to-end TLS or an intermediary replaces the ClientHello before attributing a fingerprint to the local backend
- preserve native-package lessons: a native adapter must retain pooled session behavior, hard timeouts, bounded bodies, typed diagnostics, wheel provenance, and clean-environment loading
- preserve bootstrap-collapse lessons as issuance-versus-consumption rules: inject or refresh server-issued state only as far as replay truly requires, not as far as the original page happened to go
- preserve session-admission lessons: a minted cookie or current-user success may prove bootstrap reachability without proving business permission
- preserve issuer-replayability lessons: replay one captured issuance payload before rebuilding the issuer from scratch, so you know whether live regeneration is actually required
- preserve auth-grant-versus-session lessons: a success envelope, redirect handle, or ticket may still need post-auth session materialization before business access works
- preserve context-layer lessons: authentication session and active tenant, shop, org, or workspace context can be separate mutable layers with different concurrency implications
- preserve verifier-round lessons: tokens, callbacks, images, and final proof belong to one round and should be archived and replayed as one unit rather than mixed from neighboring samples
- preserve issued-challenge consumption lessons: unused image or token fetches can increment a session miss counter; submitted-wrong may be retryable; skip-to-refresh on a kept session is poison; accept-rate and reject-rate may share a field name while meaning different things; search the full canvas and a piece-sized four-edge rectangle before blaming the scorer
- preserve hybrid-verifier-order lessons: verifier artifacts can belong in pre-sign or pre-encrypt plaintext, not only as a final appended field after the signer runs
- preserve session-chain-integrity lessons: first-hop HTML, initial cookies, generated state, preflight tokens, signer params, and replay requests must be proven on one session chain before any artifact is declared reusable
- preserve bootstrap-asset continuity lessons as same-session, same-origin, and same-header acquisition rules for linked challenge assets, not copied runner URLs
- preserve response-side-refresh lessons: application challenge subcodes and seed tuples on business responses can be same-route refresh contracts, not proof that the endpoint itself is wrong
- preserve native-surface gap lessons as environment-routing rules: when cookie, storage, and script injection do not close the gap, test `canvas`, WebGL, layout, style, and native-descriptor surfaces before escalating to broader emulation
- preserve lifecycle-semantic lessons: host objects can be checked through live collection length, indexed-slot persistence, or attach-detach behavior rather than by name presence alone
- preserve heat-versus-causal lessons: a host call can fire while the returned fields still fail ablation; ablate the returned object, do not freeze a computed-name list because the call happened
- preserve page-world-replica-versus-local-host lessons: a JS replica that matches inside Chrome can still miss in jsdom; sniper the next heat surface instead of stacking cosmetics; define host constructors with `window.eval`; apply FTS to the page VM `Function`, not Node `Function.prototype`; do not `Proxy` live collections or freshly created elements
- preserve observer-toxic-primitive-wrap lessons: wrapping `Number.prototype.toString` or `TextEncoder.encode`, or Proxying TypedArray / live collections / freshly created elements, can poison mixers even when FTS looks safe; `encode.length === 0` is a contract
- preserve two-stage-mixer lessons: first mix can be a clock-independent placeholder while second mix is host-bound; hex padding and sign length follow the first-mix hex, not a hardcoded width; freeze same-world HTML, script, and clock before a live POST
- preserve browser-tool lifecycle lessons as target-active ownership, evidence handoff, parked-versus-closed truth, and retained-session exceptions rather than process-killing recipes
- preserve intake-mode lessons as live-evidence requirements, artifact-only epistemic limits, and continuation invalidation rules rather than restarting every investigation from zero
- preserve capability-contract lessons as required methods, optional methods, and supported fallbacks rather than stale tool names
- preserve browser-acquisition-role lessons as fingerprint-baseline, debugger-trace, and approved CDP-bridge evidence surfaces with sequential ownership, not vendor-specific route lock-in
- preserve hook-timing lessons as preload, early-breakpoint, controlled-reload, and post-load epistemic limits rather than one assumed injection API
- preserve implementation-brief lessons as conditional decision records for real ambiguity or authority expansion, not a mandatory phase ceremony
- preserve runtime-coherence lessons as resolved interpreter, project-local environment, tool version, and lockfile provenance checks rather than hardcoded workstation paths
- preserve sensitive-artifact lessons as redacted reports, local-only secret storage, and hashed proof manifests rather than copied credentials or cookies
- preserve dual-writer lessons: same field name can have short research writers and long wire-success writers; deliver only the live-accepted class
- preserve surface-signer lessons: HTTP, websocket, protobuf, and report surfaces can keep different live signers; inventory by surface before the first port
- preserve hard-route-writer lessons: a soft or detail route can accept an older generation while the hard or antispam route accepts only the newer writer
- preserve token-slot lessons: the same token name in cookie, query, and header can be different slots; a stale cookie can poison a query-minted token
- preserve sidecar-mint lessons: a report-sidecar token is not interchangeable with a random fallback; soft-route acceptance of the fallback is not hard-gate proof
- preserve challenge-rewrite lessons: business APIs that return challenge HTML often emit a navigated URL as the decisive artifact before cookies or encrypt rebuilds
- preserve local-challenge-executor lessons as Python-owned HTTP plus minimal host I/O contracts, not browser automation
- preserve independent-gate lessons: app signers and challenge verifiers may both appear while only one is necessary for a given replay path
- preserve continuation sibling-scan lessons: before reopening a long reverse, search the workspace for an existing pure-protocol collector or challenge helper for the same target family
- preserve declared-host-input lessons: browser-shaped values can stay as explicit config inputs when the recovered signer only consumes them as data fields
- preserve deterministic-versus-live lessons: one fixed-seed replay path can prove the reverse while a separate live-generation path handles real traffic
- preserve request-shaped-artifact lessons: suffixes, headers, tokens, and cookie headers tied to page, keyword, body, referer, or timestamp belong inside the live request loop, not in one stale precompute
- preserve load-order lessons: env surfaces, polyfills, hooks, init, and trigger can form one local contract, so a correct patch loaded at the wrong time can fail as hard as a missing one
- preserve config-normalization lessons: bootstrap config can hide key, iv, salt, hash, or cookie-shape inputs behind slice, concat, trim, or embedded-constant steps rather than exposing final values directly
- preserve host-object-contract lessons: once the names exist, prove descriptors, prototype chains, constructor identity, enumeration, and native-looking surfaces before adding more globals
- preserve patch-layering lessons: stabilize base DOM and BOM first, then descriptors and returned-object contracts, then higher-entropy fingerprint surfaces only when evidence proves they matter
- preserve boundary-selection lessons as authoritative-intercept rules: prototypes, constructors, wrapper ingress, and egress beats bypassable instance hooks when the runtime keeps rewriting objects underneath you
- preserve self-contained-helper lessons: extract only the required constants and transforms instead of importing runtime-backed predecessor code that can revive hidden dependencies
- preserve stable-scaffold-versus-volatile-capture lessons: keep user-maintained fixtures and helper wiring separate from fresh captured target artifacts and per-run runtime blobs
- preserve inner-primitive lessons: if orchestration glue fails, salvage the lower serializer, packer, signer, or export instead of discarding the whole SDK path
- preserve response-over-callback lessons: if the decisive value lives in a response or state write, model that authoritative writer instead of immortalizing fragile callback choreography
- preserve VM-boundary lessons: map public VM inputs, outputs, wrapper returns, state writes, or request egress before touching opcode handlers or interpreter internals
- preserve real-engine lessons: failure under Node, jsdom, or a thin shim does not prove a VM is browser-only; record when a closer local engine or embedded runtime collapses the problem
- preserve engine-pin lessons: when helper parity depends on native surface shape, builtin availability, or function-property surfaces, pin and validate the exact local engine version instead of assuming diagnostic and shipped runtimes are interchangeable
- promote transport-shape and decode-chain lessons into generic references, not per-site notes
- preserve JSONP and callback-wrapper lessons as framing rules, not one callback name
- promote public bootstrap and encrypted-envelope lessons into reusable checklists, not vendor folklore
- preserve challenge-generated cookie, storage, and token lessons as bootstrap-state rules, not copied values or browser profiles
- preserve challenge-runtime lessons as getter or egress harvest rules, scheduler-preservation rules, bypass routing rules, and error-class-specific patching rules
- preserve intercept-versus-rebuild lessons: if the runtime already emits the final encrypted body, wrapped payload, decisive headers, or a public multi-arity export with wire-shaped I/O, record that harvest boundary and Python replay path instead of romanticizing a full inner-crypto rebuild; WASM/WAT dumps stay evidence, not collector runtime
- preserve shared envelope lessons as packet-family rules: version, checksum, custom alphabet, state-derived prefix, inner cipher, and payload anchor
- preserve sibling-route family lessons: once one route in a packet family is solved, probe adjacent list, detail, download, and export methods before hunting fresh crypto
- preserve full-request serialization lessons as canonical-input rules: query order, empty fields, and encoding can be part of the contract
- preserve raw-body serialization lessons: some legacy form endpoints care about the exact frontend byte stream, not just equivalent key-value semantics
- preserve verifier decomposition lessons as protocol, compute, perception, and behavior routing, not one captcha project structure
- preserve verifier-sidecar lessons: enumerate warm-up, device, log, status, and telemetry routes on the same round, then prove necessity with one-variable omit and restore controls
- preserve baseline-delta lessons: prove the shared verifier state's profile, session, or round scope, then derive complete baselines, sparse deltas, counters, timestamps, and checksums from one consistent instance instead of randomizing packets independently
- preserve real-timeline lessons: distinguish payload timestamps, event deltas, and actual wall-clock request spacing when elapsed interaction time is part of verifier acceptance
- preserve dynamic-asset lessons: compare active asset hashes, public helper boundaries, fixed vectors, and stage traces before treating a changing path as a new algorithm; the stable identity is arity and I/O, not the URL
- preserve verifier-acceptance lessons: keep sidecar acknowledgements, final verifier semantics, downstream consumption, and project-local error meanings as separate evidence layers
- preserve image-preprocessing and visual-QA lessons as perception-surface rules, not one sprite layout or crop recipe
- preserve CSS-in-HTML sprite lessons as hide-class derivation, in-flow visual x after dropping hidden nodes, and image-byte identity, not one width, digest recipe, or class-name map
- preserve check-finish versus answer-accept lessons as document-warm oracles, not one vendor `finish` field name
- preserve prompt-versus-geometry lessons: ordered-click verifiers require separate handling for prompt recognition, background localization, and proof packaging
- preserve weak-enforcement lessons as route-tolerance rules, not claims that sidecar fields or track blobs never matter
- promote session-bootstrap, frame-family, and media-key lessons into generic references, not chat-app trivia
- preserve build-order lessons such as payload -> compact JSON -> sign -> timestamp -> encrypt -> wrapper when that order matters
- preserve origin-resolution lessons: relative actions inherit the effective entry origin, not the hostname you expected from family resemblance
- preserve helper-cookie-contamination lessons: local bootstrap byproduct cookies can corrupt the main session if merged blindly
- preserve document-lifecycle event-latch lessons: scripts evaluated after document-complete may register load or DOMContentLoaded only after collector-ready; host-scalar parity is not mint
- preserve same-vendor dual-face lessons: a mintable non-final bootstrap response and a hard interstitial with a different probe asset are different doors
- preserve page-bound submit-token lessons: current-document tokens only; HTTP 200 with an empty body is not a grant
- preserve shared-profile occupancy lessons: parking the last Chrome tab is not a user-data-dir release; do not relaunch a second family against the same profile
- preserve Date.now lessons as a wire test: extra local clock or PRNG bytes are decoy until they appear on the request; a server-issued clock that is also sent is preimage; freeze that clock only at the observed writer, including a signer argument or query clock field, and treat a quieter Date.now or inner Date sibling as not that writer until proved; native Date.now can still select round constants without being the request clock
- preserve public-writer-arg lessons: hook the public writer arguments before guessing concat from route names, leftover sibling fields, or debug-UI `"GET " + url + "?"` concatenations
- preserve rotating-source extract lessons: extract the public function by structural anchors rather than frozen ident maps; do not vendor a per-fetch obfuscated bundle as the collector signer; a public function that already mints in a tiny local vm does not justify an inner Huffman/XOR port or an iv8 escalation
- preserve signer-egress-stub lessons: wrap the observed transport callsite and fire the continuation the next request reads; an XHR send stub is not a library-ajax continuation, a returned export or `call` may only be a pager, and the harvest can live in ajax data rather than the export return
- preserve public-codec-exit lessons: `encodeURIComponent`, `unescape`, `Utf8.parse`, and hex nibble join are exits, not inner opcodes
- preserve missing-avalanche lessons: a ciphertext prefix that does not flip across plaintext change is not textbook AES; after concat misses, keep the bundle helper; textbook avalanche still needs packed-key layout, GCM-frame, XOR/end, and inner-field PRNG before a standard library
- preserve sibling-request-shape lessons: leftover UA or a shared `call` name does not copy method, time slot, token width, or export semantics; independently proved concat of path, clock, and page still does not copy the sibling calculator; digest versus RSA/PKCS, and random PKCS#1 versus a constant PS, are different calculators even when concat matches
- preserve unused-second-key lessons: a second harvested SPKI or `document.all` key is an untaken branch until the live writer selects it; the unused branch may swap a whole key or only add a limb delta, so a stored even limb array is not live `n`
- preserve DOM-bootstrap-miss lessons: a missing `meta` content or equivalent host node is a bootstrap miss, not a missing signer
- preserve adapter-body lessons: a path rewrite can also reshape the form; collect the live schema, not the VM-native POST
- preserve product-writer observation lessons: wrapping the cookie setter on a mint host can poison the artifact
- preserve debugger-opcode attach lessons: challenge VMs that embed debugger opcodes can hang CDP attach; harvest offline
- preserve wire-cookie-header lessons: stored cookie state and outbound `Cookie` header can diverge, so keep the egress specimen as the authority when replay gaps remain
- preserve validator-negative-control lessons: a claimed state checker is only trustworthy after tampered or empty session state makes it fail
- preserve coordinate-space lessons: restored-image pixels, rendered UI coordinates, and submitted proof fields may be different spaces even when they describe one gap or click; float-plus-timestamp, integer-scaled pairs, and display-normalized clicks are different encodings
- preserve empty-present-field lessons: an empty string key can still belong in the pre-cipher object; omitting it is a different packet, and ciphertext length is a field-set probe
- preserve assembler-hook lessons: a late global stringify hook is not proof that plaintext assembly never happened
- preserve pagination-route pivots as route-family rules, not copied page URLs
- preserve raw-source-versus-DOM lessons as source-of-truth rules for inline route metadata, not parser-specific hacks
- preserve staged-hydration lessons: enumerate stable ids early, persist raw decoded payloads, and backfill expensive detail routes separately when downstream rules evolve
- preserve embedded-runtime lessons as routing rules: when Python handwrite is enough, when a local host runtime like `iv8` is the cheapest faithful bootstrap, and when true interaction means the collector is still incomplete
- preserve browser-free-versus-runtime-free lessons as delivery-gate rules: an embedded host can be an acceptable intermediate stage without satisfying explicit runtime-removal goals
- preserve live-replay-first lessons: one fresh single-page replay on one session chain should be proven before broad environment patching, runtime shrink, or pagination scaling
- preserve helper-integrity lessons: broken local runtimes, copied package trees, placeholder link files, and path-resolution damage can mimic target-side blocking and should be separated before reverse hypotheses change
- preserve async-observation lessons: baseline mailbox, webhook, queue, or callback observation before triggering the event that emits the decisive artifact
- preserve tiny-bridge lessons: when Python crypto or serializer parity drifts from verified frontend JS, keep the bridge tiny and local instead of shipping a half-correct port or a larger hidden runtime
- preserve self-invalidating-helper lessons: a VM that slices or rewrites its bytecode after the first encrypt is not a pager; isolate or port the encrypt instead of reusing the burned instance
- preserve cross-runtime parity lessons: keep deterministic vectors and intermediate checkpoints when porting JS helpers to Python so live replay is backed by proof instead of approximate similarity
- preserve stable-dispatch lessons: after the public boundary is proven insufficient, trace ordered mode or transform inputs and outputs before widening into opcode-level instrumentation
- preserve atomic-profile lessons: keep one successful runtime capture internally consistent, retain opaque blocks with provenance, and require negative evidence before splicing segments across runs
- preserve delivery-truth lessons: distinguish algorithmic generation, snapshot-driven generation, and pool-backed replay instead of describing every browser-free path as pure generation
- preserve pool-control lessons: use accepted artifact pools as diagnostic controls or explicit bounded fallbacks, require a no-pool test, and keep target rejection separate from transport exceptions
- preserve error-ladder lessons as debugging rules: changing subcodes are progress markers and next-gate hints, not just noise
- preserve anti-pattern lessons as counterexamples when the same tempting shortcut recurs: name the temptation, explain why it was false progress, record the smallest honest next move, and end with one direct self-check
- preserve escalation-ladder lessons: record the last rung that still had proof, the exact failure that forced escalation, and why the next rung was the smallest honest move
- preserve minimal-verifiable-fact lessons: when a family is likely to recur, store 5 to 15 structural facts that can be re-checked after an upgrade instead of only writing a narrative summary
- preserve punitive-disguise lessons: rate limits or abuse cooldowns can masquerade as password or field errors once request pacing gets too aggressive
- preserve cookie-vs-global dual-writer lessons: the same param name can occupy cookie and an in-memory global; prefer the page-priority writer, then try the other writer on punish; mint shape is not acceptance
- preserve filler-json punish lessons: HTTP 200 schema-valid JSON with constant filler values matching the unsigned or negative-control payload is intercept, not grant
- preserve rotating-bootstrap-cookie-clear lessons: rotating challenge JS is fetch-and-eval per call, not one vendored snapshot; a leftover locally-minted cookie on the next script GET can change the returned branch
- preserve native-host-versus-node-decoy lessons: an incomplete Node `document`/`cookie` host can write a mint-shaped decoy; native-looking `document`/`screen`/`createElement` can change the artifact; `try { if (navigator) {} } catch` inside a named cipher can reorder DES key slices, so a Node miss is the catch-path schedule rather than patched AES
- preserve isolate-thread-affinity lessons: an embedded `JSContext` / `page.load` isolate is not safe on a ThreadPool worker; keep it on the creating thread
- preserve exact-Function-hang stubs: stub only exact `Function` bodies such as `debugger;`, `while (true) {}`, and `while(!![])`; do not wait an anti-debug `setInterval` for mint; never `includes("debugger")`
- preserve hasher-internal eval/setInterval stub lessons: a charcode array that reconstructs a function is a side-effect bomb, not T constants or preimage; stub eval and timers; never eval recovered R, especially in Node where `require` exists
- preserve named-digest dual-miss and sibling-200 lessons: ascii hashlib and digit-byte hashlib both miss on a frozen timestamp, so keep the bundled helper; HTTP 403 JSON forbidden on this API while sibling APIs on the same session return 200 is not session death; ablate stdlib versus impersonate on the same admitted bytes before calling it a digest/clock pair
- preserve JSON numeric CR/LF strip, MCP select/attach timeout as `debugger_attach_gap` plus offline harvest, and huge-wrapper versus tiny-writer lessons: chart/painter/SVG modules are decoys until the module that owns the list URL is extracted
- preserve one-host DP lessons: opening DP attaches to the current TARGET_ACTIVE host; js-reverse may own both live roles when DP is already required; never launch a second Chrome and never pretend launch is attach
- preserve curl-impersonate identity lessons: replay UA, Client Hints, navigator, and TLS/H2 lock to the installed curl chrome impersonate; mixing a newer live Chrome major is profile-drift, not a reason to restart signer reverse
- preserve stdlib-403-versus-impersonate-200 lessons: a live-admitted token that still 403s on stdlib while impersonate returns business 200 is transport admission, not a bad helper; do not escalate canvas/audio/WebGL as the remaining HTTP gate after that 200
- preserve impersonate-cookie-hostname lessons: seed curl impersonate cookies with the request hostname; empty-domain session cookies plus host-only rotating tokens split the jar
- preserve placeholder-zero lessons: HTML table or list zeros are not business data when no list XHR or fetch fired; HTTP 200 dummy filler on a sibling REST path does not retire a WebSocket or text list channel
- preserve CDP-webdriver-silence lessons: `navigator.webdriver === true` can make a JSVMP skip the business request; if the prototype property is configurable, delete it in initScript before Camoufox or XHR wraps
- preserve protobuf-or-wasm-public-boundary lessons: `serializeBinary` and wasm `encode(i32,i32)` are public I/O; do opcode work only after that boundary is insufficient; regenerate fresh clock-bucket fields, and a second int32 may be client-chosen if the token remains `encode(t1,t2)`
- preserve UTF-8-binary-dump lessons: MCP or DevTools text saves of protobuf become `U+FFFD`; capture hex at the serializer
- preserve unknown-risk-control reverse-first lessons: reverse the rejected request before adding URLs; unproven extra routes are at most one per round and only after omission changes the oracle
- preserve empty-wrapper-hook lessons: an empty ajax `beforeSend` or no-op IIFE is not a missing signer; freeze the captured body against visible fields and skip token reverse when they match
- preserve named-AES-short-vector lessons: freeze a short plaintext before porting AES-128; 8-byte ciphertext is DES/3DES even when the live token is 16-aligned and the export is `AES.encrypt`
- preserve impersonate-websocket-handshake lessons: freeze handshake header class on the same admitted token bytes; impersonate document defaults include `Sec-Fetch-Mode: navigate` and must not be copied onto a WebSocket handshake
- preserve chrome-devtools-http-log lessons: that family's `list_network_requests` is an HTTP resource inventory, not a WebSocket inventory; empty XHR plus filled DOM after zeros still needs a WS/text-channel proof
- preserve websocket-prefix-frame lessons: classify inbound text frames; skip non-object prefix/ack/heartbeat constants; keep reading until business JSON; one-recv landing on the prefix is not reuse failure
- preserve dynamic-compile-snapshot lessons: the `eval` / `new Function` body after param substitution is key material; a later call is only execution; never wrap global `Function.prototype.apply`/`call` to chase it
- preserve nondeterministic-feed lessons: `Math.random` / `Date.now` / canvas / audio sequences belong to one script hash; never feed a new-session script with an old sequence
- preserve host-fidelity L0-L4 lessons: native count, sequence LCS, value feed, protocol param-set, eval sha256; canvas/navigator JS shims cannot be probe-counted as L0
- preserve webpack-require-sniper lessons: expose `__wpRequire` and call the encrypt export; do not start by completing `$mount`
- preserve timer-queue lessons: `setTimeout` must not run the callback synchronously; drive with `__drainTimers__`; `setInterval` returns 0 on no-native hosts; `fromCharCode` heat (million vs 0) diagnoses VM entry
- preserve source-class-versus-ownership lessons: `fixed` / `plaintext` / `local-algorithm` / `server-issued` / `risk-interactive` are origin labels and stay orthogonal to `python-owned` / `host-owned` / `server-owned`
- preserve visual-oracle-geometry lessons: drag origin is box `x1`, not center; OCR/captcha-platform is diagnostic only and never collector runtime
- preserve graded-degrade lessons: import/`NameError` is our bug and must alarm; external timeout may fallback; key responses go to stderr; stdout stays machine JSON
- prefer new root-level generic references over new site-specific case files
- add helper scripts only when they improve many future jobs, not just one target
