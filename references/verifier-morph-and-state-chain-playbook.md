# Verifier Morph and State-Chain Playbook

Use this when a multi-surface verifier (slider, punish page, device companion, risk gate) can mint plausible tokens but the live gate still rejects with a stable semantic code.

Browser tooling is for evidence only. Final delivery remains browser-free HTTP owned by Python. Local JS/WASM helpers are allowed as L2 algorithm runtimes and must be labeled honestly.

This file is not only doctrine. It is the **stop-loss and experiment protocol** for multi-day verifier jobs that drift into false progress.

## Contents

- [When to read](#when-to-read)
- [Core model](#core-model)
- [Hard gate metric](#hard-gate-metric)
- [Wall taxonomy and signatures](#wall-taxonomy-and-signatures)
- [False-progress metrics blacklist](#false-progress-metrics-blacklist)
- [Mandatory kill-switches](#mandatory-kill-switches)
- [Day-card before more reverse](#day-card-before-more-reverse)
- [Morph before track](#morph-before-track)
- [Human-gold divergence protocol](#human-gold-divergence-protocol)
- [State-chain checklist](#state-chain-checklist)
- [Companion signature slots](#companion-signature-slots)
- [Retry semantics](#retry-semantics)
- [Ablation order](#ablation-order)
- [Experiment matrix template](#experiment-matrix-template)
- [Acceptance ladder](#acceptance-ladder)
- [Delivery honesty](#delivery-honesty)
- [Consumer oracle is product-specific](#consumer-oracle-is-product-specific)
- [Challenge restart vs in-challenge retry](#challenge-restart-vs-in-challenge-retry)
- [Writer honesty: pool, local VM, pure port](#writer-honesty-pool-local-vm-pure-port)
- [Pitfall catalog from multi-day failure modes](#pitfall-catalog-from-multi-day-failure-modes)
- [Related files](#related-files)
- [Bottom line](#bottom-line)

## When to read

Read this when several of these are true:

- helper output has the expected prefix/length family
- submit returns structured JSON rather than transport/HTML noise
- the gate code is stable (for example a fixed reject code) across retries
- a human or historical positive sample exists, yet local desktop-shaped rebuild stays rejected
- a same-family solved skeleton is available for another host/path of the same product generation
- the job has spent more than a few hours improving mint/env similarity without a hard-gate flip

Do not open this file for pure fixed-vector offline decode work with no live verifier.

## Core model

Separate four layers before deepening any one of them:

| Layer | Question | False progress if ignored |
|---|---|---|
| `envelope` | alphabet, framing, header magic, codec | treat decode success as gate success |
| `morph` | device class, scene, UA/mobile hints, geometry profile | lock one positive sample form as the only mainline |
| `state-chain` | ordered bootstrap reports, device/UMID/init, same-session continuity | mint token without the session machine |
| `token-writer` | local profile pool, local JS SDK VM, pure port | assume the hardest field is the only root cause |

A solved envelope does not prove morph, state-chain, or token-writer.

## Hard gate metric

Declare the hard metric before experiments:

```text
gate_pass = verifier semantic success + issued grant artifact (cookie/header/body field)
```

Not gate pass:

- non-empty mint
- helper exception cleared
- stable reject JSON
- codec/unit tests green
- offline similarity to human gold (prefix/length/common bytes)
- bootstrap/report telemetry HTTP 200
- one lucky pass without N-run repeatability

For stability claims, run a bench of repeated fresh sessions (recommend 10-20) and report success rate, not a single anecdote.

## Wall taxonomy and signatures

Name **one primary wall** before another reverse day. Do not open a deeper wall while a shallower one is untested.

| Wall id | Signature | Next action | Forbidden next action |
|---|---|---|---|
| `envelope-wall` | cannot decode/mint expected family; wire not parseable | recover alphabet/frame/header | track tuning |
| `morph-wall` | mint-shaped + stable reject; only one scene/device class tried; human gold may be another morph | ablate morph once end-to-end | more offline mint variants on same morph |
| `state-chain-wall` | submit without ordered bootstrap/device-init on same jar | rebuild transcript machine | blaming token entropy |
| `companion-wall` | missing/wrong rand-et-pp modes or off-session companions | restore companion slots and retry modes | denser host FP patches |
| `writer-wall` | morph+chain+companions complete; writer family still rejects | switch pool / local VM / pure port | optimize common-prefix to gold |
| `track-wall` | only after writer-wall is the first failing layer | geometry/track micro-details | reopening codec |
| `egress-wall` | same build flips only when exit changes | change exit / label egress | algorithm rewrite |

If you cannot name the wall in one line, fill the day-card first.

## False-progress metrics blacklist

These metrics may rise while the gate never flips. **Do not use them as mainline success scores.**

1. common-prefix / Hamming closeness of binary bodies to human gold
2. token length approaching gold length
3. count of offline mint variants (type/version/force-join/full-fp)
4. fewer helper exceptions or greener local logs
5. stable structured reject code ("server understood us")
6. broader host env surface patched (plugins, canvas, webgl stubs)
7. more CDP/browser automation slide attempts
8. hours spent without a morph ablation row in the matrix
9. report/telemetry endpoints returning success
10. single-parameter "looks more real" narrative without hard-gate delta

If the only improvement in a session is a blacklist metric, the session is **debt**, not progress. Log it as false progress and run a kill-switch check.

## Mandatory kill-switches

These are hard stops, not suggestions. Violating them is an anti-pattern.

| Trigger | Required action before any more token/track work |
|---|---|
| **K1** 3 consecutive fresh sessions: mint-shaped + same stable reject + same morph | run one alternate morph end-to-end (scene/device/UA class) |
| **K2** envelope solved, >=5 offline mint variants, gate still reject | freeze offline mint expansion; prove live state-chain+companions on one morph |
| **K3** human gold captured | within the next working session, attempt at least one non-gold morph or same-family skeleton migrate |
| **K4** same-family solved skeleton available (user or workspace) | within 2 hours attempt host/path/state-chain migrate; do not open new behavior-wall mainline first |
| **K5** optimizing common-prefix/similarity for >=2 iterations with no hard-gate flip | abandon similarity mainline; return to morph/state-chain/companion matrix |
| **K6** >=1 full day on token/env without a completed ablation matrix row for morph | stop reverse; fill day-card + matrix; only then continue |
| **K7** in-challenge retries exhausted on one config | whole-challenge restart once under admitted morph before declaring writer impossible |
| **K8** claiming stability | N-run bench on hard gate metric (10-20 when practical); no anecdote claims |

Kill-switches create evidence, not vibes. Record pass/fail of the required action.

## Day-card before more reverse

Before starting another reverse day on a multi-surface verifier, answer in the task log:

```text
1. hard_gate_metric =
2. primary_wall =
3. current_morph = scene/device/UA/geometry
4. alternate_morph_tested? yes/no + result
5. state-chain complete on one jar? list missing steps
6. companions present? rand/et/pp modes tried
7. writer_class = pool | local-VM-L2 | pure-L3
8. sibling_skeleton_available? path/class template|current-proof
9. blacklist_metrics_chased_yesterday =
10. kill_switches_due = K1..K8
11. today's single variable =
12. stop_condition_for_today =
```

If items 1-4 or 10 cannot be answered, do not open fireye/track/env patches yet.

## Morph before track

Positive samples prove *a* path can pass. They do not prove the current optimal morph.

Common morph axes:

- desktop web vs mobile/H5 scene names
- UA / Client-Hints mobile bit / platform string
- slider geometry and input modality (mouse vs touch)
- page/sdk version tags carried on reports

Rules:

1. Label every success sample with morph fields (`scene`, device class, UA class, geometry class).
2. When local rebuild matches envelope but fails the gate, ablate morph before track micro-entropy.
3. If switching morph flips the gate while token writer stays equivalent, stop track tuning and adopt the admitted morph.
4. Desktop human gold plus long local desktop failure is a **morph-wall suspect**, not proof that tracks are the root cause.

## Human-gold divergence protocol

When a clean human/browser gold sample exists and local protocol rebuild fails:

1. freeze gold morph labels and hard-gate proof
2. do **not** set mainline = gold morph by default
3. extract only envelope + field slots + state-chain order from gold
4. run one alternate morph with the same state-chain skeleton
5. if alternate morph passes, gold becomes existence proof; mainline follows the admitted collector morph
6. if all morphs fail with incomplete companions, fix state-chain/companions before track parity to gold
7. binary common-prefix to gold is supporting diagnostics only, never the optimization objective

## State-chain checklist

Many verifiers are transcript machines, not single-shot signers. Rebuild the ordered bootstrap on one session before blaming token quality:

1. open business route and obtain punish/challenge config on the same jar
2. handle JSON business envelopes that only carry a punish/config URL (non-HTML twin)
3. emit required load-success / module-success reports in the live order
4. fetch server-issued device/UMID material when the chain requires it
5. run initialize/register style sidecars with the same scene morph
6. only then mint submit tokens and post the verify request
7. keep host/path binding consistent with the business route being unlocked

Missing early empty-input rand reports, missing UMID, or wrong initialize href/scene is a state-chain defect, not proof that tracks are fake.

## Companion signature slots

Treat companion headers/query slots as first-class ownership layers:

- stateful rand that must see empty bootstrap input before the submit payload
- request et/sign headers bound to method/path/query
- wasm or local pp/sign companions that may have mini/append/repow modes
- ppt/timing fields that mirror companion compute elapsed time
- optional wait-before-slide aligning server timeline

Do not declare token-writer failure while companions are absent, constant-faked, or generated on a different session.

## Retry semantics

Some gates expect a failure transition before the next accept:

- first submit returns a known soft-reject code
- client reports verifyFail / equivalent transition
- second submit uses a different companion mode (for example mini then append)
- whole challenge restart after N soft rejects is allowed

Model retries as protocol state, not as blind spam. Cap attempts and cool down on rate-lock evidence.

## Ablation order

Run one variable class at a time. Preferred order for morph/state-chain verifiers:

```text
1. morph (scene/device/UA class)
2. state-chain completeness and order
3. companion slots (rand/et/pp and modes)
4. token-writer family (local SDK VM vs profile pool vs pure port)
5. track/geometry micro-details
6. only then broaden env patches or transport profile
```

Stop at the first flip of the hard gate metric. Record the matrix with keep/replace/oracle columns from `references/positive-sample-ablation-playbook.md`.

## Experiment matrix template

Copy into the task log. One row = one variable class change.

```text
| id | keep | replace | morph | state-chain | companions | writer | oracle | hard_gate | blacklist_metric_only? | next |
|----|------|---------|-------|-------------|------------|--------|--------|-----------|------------------------|------|
| E1 | ... | morph=H5 | H5 | full | full | L2 | reject/pass | 0/1 | no | ... |
```

Rules:

- no row may change morph and writer and companions together
- after three reject rows on one morph, K1 applies
- rows that only improve blacklist metrics are marked `blacklist_metric_only=yes` and do not justify another day on the same axis

## Acceptance ladder

Climb only with evidence:

1. **mint-shaped**: prefix/length/family checks pass offline
2. **server-parseable**: verifier returns structured app JSON, not transport garbage
3. **gate-pass**: hard metric true on one fresh session
4. **repeatable**: N fresh sessions with reported success rate
5. **consumer-pass**: first downstream business request accepts the grant (product-specific oracle)

Do not call step 1 or 2 a collector.

## Delivery honesty

| Label | Meaning | Allowed claim |
|---|---|---|
| L1 browser-free HTTP | Python owns live HTTP; helpers optional | compact-replay / collector candidate |
| L2 local algorithm VM | Node/jsdom/WASM executes vendor logic locally | browser-free, not pure-Python field port |
| L3 pure field port | no vendor JS runtime required for the field | pure offline algorithm claim |

Never call L2 "fully pure Python protocol". See anti-pattern 36.

## Consumer oracle is product-specific

After gate grant, the first downstream consumer check is route-family specific:

- do not hardcode another product's success status as the only consumer oracle
- define consumer-pass from the business route under collection
- a foreign status code can be supporting evidence only when wire-proved on this route

## Challenge restart vs in-challenge retry

Separate two retry classes:

1. **in-challenge retry**: same challenge material/session; companion mode flip; optional verifyFail transition
2. **whole-challenge restart**: new punish/config; full state-chain again

Do not treat exhausted in-challenge retries as proof the token-writer family is impossible until at least one whole-challenge restart has been tried under the admitted morph.

## Writer honesty: pool, local VM, pure port

When minting opaque behavior/device tokens:

- label `pool-backed`, local algorithm VM (L2), or pure field port (L3) honestly
- a pool/profile that only passes offline shape checks is not gate-pass
- if pool-backed mint stays rejected after morph/state-chain/companions are complete, switch writer family before more track entropy
- cross-read `references/opaque-runtime-profile-playbook.md` and anti-pattern 36

## Pitfall catalog from multi-day failure modes

These are generic restatements of real multi-day drifts. Use them as pre-mortems.

| Pitfall | What it looks like | Correct recovery |
|---|---|---|
| P1 Gold-morph lock | days of desktop rebuild because human gold was desktop | force alternate morph; gold is existence proof |
| P2 Envelope confetti | codec solved, then endless offline mint types | K2; live state-chain first |
| P3 Similarity treadmill | common-prefix/length to gold becomes the scoreboard | blacklist; K5 |
| P4 Hardest-field tunnel | only fireye/track/env deepens | wall taxonomy; ablate 1-3 first |
| P5 Skeleton denial | sibling solved pure-protocol exists; still reverse behavior wall | K4 migrate host/path/chain |
| P6 Soft-success theater | mint works, reject stable, reports 200, helper quieter | acceptance ladder only |
| P7 Env sprawl | PluginArray/canvas/webgl patches expand after envelope works | companions/morph before host FP |
| P8 Automation folklore | CDP/hand-slide failures used as trajectory truth | anti-pattern 21; structure first |
| P9 One-shot skeleton reject | one 300 on migrated skeleton, declare skeleton useless | whole-challenge restart + companion modes + N attempts |
| P10 Foreign consumer oracle | copy another route's success status as proof | product-specific consumer-pass |
| P11 Retry class confusion | only spam same challenge; never restart config | K7 |
| P12 Scope thrash | reopen finished business collectors while gate unfinished | continuation sibling scan: gate first |

## Related files

- positive sample trust: `references/positive-sample-hygiene-playbook.md`
- single-layer causal tests: `references/positive-sample-ablation-playbook.md`
- same-family reuse: `references/case-reuse-playbook.md`
- surface labels: `references/failure-surface-taxonomy.md`
- device-trust companions: `references/device-trust-sidecar-playbook.md`
- verifier replay: `references/verifier-replay-playbook.md`
- opaque pool vs algorithmic honesty: `references/opaque-runtime-profile-playbook.md`
- delivery false completion: `references/delivery-gate-playbook.md`
- anti-patterns 7/21/22/36-44: `references/anti-patterns-playbook.md`

## Bottom line

1. Envelope solved is not gate solved.
2. If blacklist metrics are the only thing improving, you are not progressing.
3. Kill-switches force morph/state-chain/skeleton moves before more token folklore.
4. Name one wall; change one class; judge only the hard gate metric.
5. Stability is an N-run rate; L2 helpers must be labeled honestly.