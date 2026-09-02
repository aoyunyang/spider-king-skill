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
- every fresh web target classified as `live-target` begins with sequential `fingerprint-baseline` then `debugger-trace` evidence; default means are `chrome-devtools` then `js-reverse`, and the baseline host may upgrade to Camoufox or another managed profile only on proved fingerprint pressure or clean-baseline failure (never default Camoufox for ordinary low-risk work); `artifact-only` web routes do not invent browser evidence, and APK/app/mini-program primary tasks stay out of scope
- paired evidence stays sequential: only one family owns `TARGET_ACTIVE`, and both families never appear in the same parallel tool batch
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
- `agents/openai.yaml` parses as YAML with typed `interface` metadata, a 25-64 character short description, a `$spider-king` default prompt, and a boolean implicit-invocation policy
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
- `scope=full` must contain all 160 unique official tasks before it can be reported as a full pass
- runner and reviewer identities must differ; both contexts must be fresh and the review must be explicitly independent
- every route and conclusion judgment needs an exact excerpt found in the referenced response file
- response files stay under the report directory and must not be symlinks, reparse points, hard links, or path escapes
- preserve the report and response artifacts outside the skill package; do not turn static validation into a behavioral claim

## Reproducible Experience Gate

Use the fields and storage lifecycle in `references/experience-card-schema.md`.

Before promoting a practical lesson:

- keep a one-off result task-local until the same invariant recurs in two independent jobs
- attach one minimal secret-free fixture or deterministic generator and record its path and SHA-256
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
- preserve success-flag lessons as response-validation rules, not one vendor's `errorCode`
- preserve symptom-versus-root-cause lessons: a visible slider, SMS wall, or verifier page can be downstream presentation of missing trust or bootstrap state, not the first gate to attack
- keep fixed-input validation habits, not endpoint trivia
- preserve server-issued-state lessons as inventory, scope, expiry, and refresh-path rules, not copied session ids or challenge configs
- preserve clean-anonymous-baseline lessons as environment-selection rules, not copied account cookies
- preserve cookie provenance lessons as writer and refresh-path rules, not copied cookie values
- preserve signer-boundary lessons: when one synthetic request through a hooked transport acquires signer params automatically, record the injection boundary separately from the business payload schema
- preserve observation-boundary lessons: a quiet cookie, storage, header, or request hook only clears one writer boundary, not every issuance path
- preserve mixed-transport lessons: silence on one `fetch`, XHR, wrapper, worker, or message channel is not proof that sibling channels are inactive
- preserve evidence-surface-separation lessons: initiator and source traces prove where logic lives, wire or egress proves what crossed the boundary, environment traces prove host truth, and downstream business replay proves actual acceptance
- preserve page-owned-world lessons: console or isolated-world misses can be tooling-bound, so repeat the proof in the page-owned world before deleting the hypothesis
- preserve request-bound logging lessons: values tied to target, event, method, URL, field, or caller age better than raw dumps
- preserve method-argument and returned-object lessons: decisive gaps can hide in call arguments or child-object shape, not only in named property reads
- preserve observe-only lessons: default hooks should preserve original behavior and return paths unless mutation is itself the experiment
- preserve cheap-codec lessons: solve weak field obfuscation locally and leave only the truly environment-bound signer in the hard bucket
- preserve page-state versus request-state lessons as separate moving-part classes, not vendor header names
- preserve verifier-family lessons: slider, point-click, and risk-gate flows that look similar at the page level can still have incompatible state models and proof builders
- preserve verifier-success-scope lessons: verifier-endpoint success can be intermediate, while downstream business acceptance is the final authority
- preserve positive-sample hygiene lessons: automation-contaminated failures are environment evidence first, not trajectory truth
- preserve verifier error-localization lessons: structure, sidecar, consistency, timeline, answer, and environment are ordered surfaces; vendor codes stay task-local
- preserve environment-risk lessons: exit reputation and consecutive rejects are a separate failure surface from algorithm regressions
- preserve family-evidence-threshold lessons: family-specific scaffolds and playbooks need corroboration across more than one evidence surface, not one lucky marker
- preserve local-noise-versus-gate lessons: server-looking names do not prove server issuance; prove writer, tolerance, and blocking value
- preserve locally minted state lessons: session-looking or fingerprint-looking cookies can be local protocol artifacts with exact UUID, digest, or compact-JSON structure, not copied `Set-Cookie` values
- preserve slot-placement lessons: a blob can be right in value and still wrong in position; field placement is part of the protocol contract
- preserve transport pre-gate lessons as narrow admission matrices and route-local exceptions, not frozen vendor UA cargo cults
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
- preserve hybrid-verifier-order lessons: verifier artifacts can belong in pre-sign or pre-encrypt plaintext, not only as a final appended field after the signer runs
- preserve session-chain-integrity lessons: first-hop HTML, initial cookies, generated state, preflight tokens, signer params, and replay requests must be proven on one session chain before any artifact is declared reusable
- preserve bootstrap-asset continuity lessons as same-session, same-origin, and same-header acquisition rules for linked challenge assets, not copied runner URLs
- preserve response-side-refresh lessons: application challenge subcodes and seed tuples on business responses can be same-route refresh contracts, not proof that the endpoint itself is wrong
- preserve native-surface gap lessons as environment-routing rules: when cookie, storage, and script injection do not close the gap, test `canvas`, WebGL, layout, style, and native-descriptor surfaces before escalating to broader emulation
- preserve lifecycle-semantic lessons: host objects can be checked through live collection length, indexed-slot persistence, or attach-detach behavior rather than by name presence alone
- preserve browser-tool lifecycle lessons as target-active ownership, evidence handoff, parked-versus-closed truth, and retained-session exceptions rather than process-killing recipes
- preserve intake-mode lessons as live-evidence requirements, artifact-only epistemic limits, and continuation invalidation rules rather than restarting every investigation from zero
- preserve capability-contract lessons as required methods, optional methods, and supported fallbacks rather than stale tool names
- preserve browser-acquisition-role lessons as fingerprint-baseline, debugger-trace, and approved CDP-bridge evidence surfaces with sequential ownership, not vendor-specific route lock-in
- preserve hook-timing lessons as preload, early-breakpoint, controlled-reload, and post-load epistemic limits rather than one assumed injection API
- preserve implementation-brief lessons as conditional decision records for real ambiguity or authority expansion, not a mandatory phase ceremony
- preserve runtime-coherence lessons as resolved interpreter, project-local environment, tool version, and lockfile provenance checks rather than hardcoded workstation paths
- preserve sensitive-artifact lessons as redacted reports, local-only secret storage, and hashed proof manifests rather than copied credentials or cookies
- preserve dual-writer lessons: same field name can have short research writers and long wire-success writers; deliver only the live-accepted class
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
- preserve intercept-versus-rebuild lessons: if the runtime already emits the final encrypted body, wrapped payload, or decisive headers, record the nearest stable harvest boundary and Python replay path instead of romanticizing a full inner-crypto rebuild
- preserve shared envelope lessons as packet-family rules: version, checksum, custom alphabet, state-derived prefix, inner cipher, and payload anchor
- preserve sibling-route family lessons: once one route in a packet family is solved, probe adjacent list, detail, download, and export methods before hunting fresh crypto
- preserve full-request serialization lessons as canonical-input rules: query order, empty fields, and encoding can be part of the contract
- preserve raw-body serialization lessons: some legacy form endpoints care about the exact frontend byte stream, not just equivalent key-value semantics
- preserve verifier decomposition lessons as protocol, compute, perception, and behavior routing, not one captcha project structure
- preserve verifier-sidecar lessons: enumerate warm-up, device, log, status, and telemetry routes on the same round, then prove necessity with one-variable omit and restore controls
- preserve baseline-delta lessons: prove the shared verifier state's profile, session, or round scope, then derive complete baselines, sparse deltas, counters, timestamps, and checksums from one consistent instance instead of randomizing packets independently
- preserve real-timeline lessons: distinguish payload timestamps, event deltas, and actual wall-clock request spacing when elapsed interaction time is part of verifier acceptance
- preserve dynamic-asset lessons: compare active asset hashes, public helper boundaries, fixed vectors, and stage traces before treating a changing path as a new algorithm
- preserve verifier-acceptance lessons: keep sidecar acknowledgements, final verifier semantics, downstream consumption, and project-local error meanings as separate evidence layers
- preserve image-preprocessing and visual-QA lessons as perception-surface rules, not one sprite layout or crop recipe
- preserve prompt-versus-geometry lessons: ordered-click verifiers require separate handling for prompt recognition, background localization, and proof packaging
- preserve weak-enforcement lessons as route-tolerance rules, not claims that sidecar fields or track blobs never matter
- promote session-bootstrap, frame-family, and media-key lessons into generic references, not chat-app trivia
- preserve build-order lessons such as payload -> compact JSON -> sign -> timestamp -> encrypt -> wrapper when that order matters
- preserve origin-resolution lessons: relative actions inherit the effective entry origin, not the hostname you expected from family resemblance
- preserve helper-cookie-contamination lessons: local bootstrap byproduct cookies can corrupt the main session if merged blindly
- preserve wire-cookie-header lessons: stored cookie state and outbound `Cookie` header can diverge, so keep the egress specimen as the authority when replay gaps remain
- preserve validator-negative-control lessons: a claimed state checker is only trustworthy after tampered or empty session state makes it fail
- preserve coordinate-space lessons: restored-image pixels, rendered UI coordinates, and submitted proof fields may be different spaces even when they describe one gap or click
- preserve pagination-route pivots as route-family rules, not copied page URLs
- preserve raw-source-versus-DOM lessons as source-of-truth rules for inline route metadata, not parser-specific hacks
- preserve staged-hydration lessons: enumerate stable ids early, persist raw decoded payloads, and backfill expensive detail routes separately when downstream rules evolve
- preserve embedded-runtime lessons as routing rules: when Python handwrite is enough, when a local host runtime like `iv8` is the cheapest faithful bootstrap, and when true interaction means the collector is still incomplete
- preserve browser-free-versus-runtime-free lessons as delivery-gate rules: an embedded host can be an acceptable intermediate stage without satisfying explicit runtime-removal goals
- preserve live-replay-first lessons: one fresh single-page replay on one session chain should be proven before broad environment patching, runtime shrink, or pagination scaling
- preserve helper-integrity lessons: broken local runtimes, copied package trees, placeholder link files, and path-resolution damage can mimic target-side blocking and should be separated before reverse hypotheses change
- preserve async-observation lessons: baseline mailbox, webhook, queue, or callback observation before triggering the event that emits the decisive artifact
- preserve tiny-bridge lessons: when Python crypto or serializer parity drifts from verified frontend JS, keep the bridge tiny and local instead of shipping a half-correct port or a larger hidden runtime
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
- prefer new root-level generic references over new site-specific case files
- add helper scripts only when they improve many future jobs, not just one target
