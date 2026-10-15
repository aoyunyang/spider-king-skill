# Positive Sample Hygiene Playbook

Use this when verifier-gated recovery needs human or browser oracles, especially
behavior-sensitive sliders, click orders, or risk-scored transcripts.

Browser tooling is for evidence only. Final delivery remains browser-free.

## Contents

- [Morph labels are mandatory](#morph-labels-are-mandatory)
- [Why hygiene matters](#why-hygiene-matters)
- [Sample grades](#sample-grades)
- [Capture preference order](#capture-preference-order)
- [Collaborative capture protocol](#collaborative-capture-protocol)
- [Minimum fields for a usable success sample](#minimum-fields-for-a-usable-success-sample)
- [How to use samples](#how-to-use-samples)
- [When samples disagree with local replay](#when-samples-disagree-with-local-replay)
- [Post-hygiene behavior calibration](#post-hygiene-behavior-calibration)
- [Hard bans](#hard-bans)
- [Delivery notes](#delivery-notes)

## Why hygiene matters

A real human action inside an automation-owned browser can still fail.

Common contaminants:

- CDP or remote-debugging ownership
- invasive hooks such as global function patches or stringify interceptors
- brand-new empty profiles with no ordinary browsing age
- consecutive reject history on one exit IP
- mixed rounds in one capture dump

Contaminated failures are useful as environment evidence. They are weak as proof
that the answer or track algorithm is wrong.

## Sample grades

Label every oracle:

| grade | meaning | authority |
|---|---|---|
| `clean-success` | ordinary browser or non-instrumented path, verifier accepted, downstream consumer passed | highest positive oracle |
| `clean-failure` | ordinary path failed with no automation ownership | strong negative for protocol or risk policy |
| `contaminated-failure` | automation, hooks, debug ports, or poisoned profile involved | environment evidence first |
| `partial` | missing sidecars, verify body, or downstream consumer | incomplete; do not over-interpret |

Never promote `contaminated-failure` into "trajectory family rejected" without a
clean contrast sample.

## Capture preference order

From best to worst for positive oracles:

1. User or operator ordinary browser, no automation attachment, export HAR or exact verify and consumer requests
2. Non-instrumented browser listen-only capture that does not inject page hooks
3. Automation browser used only to open a page, with no hooking, accepted only if clean ordinary capture is impossible
4. Hooked automation capture for initiator and field discovery, not as final positive truth

If the operator can pass in an ordinary browser and fails under automation, treat
that as environment risk until proved otherwise.

## Collaborative capture protocol

When protocol replay is stuck and a clean success sample is needed:

1. state exactly which URLs and actions the operator should perform
2. prefer the operator's daily browser over any agent-owned profile
3. ask for Network export of the full verifier round plus the first successful business response
4. if live listening is used, disable invasive hooks first
5. store the capture under the task cache and grade it immediately
6. redacted chat reports; raw tokens stay task-local

Ask only for the missing sample. Do not demand broad homework.

## Minimum fields for a usable success sample

- ordered request list with elapsed offsets
- init/load response family
- required sidecar requests and application acknowledgements
- final verify request and semantic success body
- answer or track payload if behavior-sensitive
- first downstream consumer request and business-pass body
- active helper or asset hashes when dynamic scripts are involved
- environment notes: ordinary vs automation, hooks on/off, exit changed or not
- **morph labels (mandatory for multi-surface verifiers):** `scene` / device class / UA class / geometry or input modality class / page or SDK version tag when present
- hard gate metric used for that sample (semantic success field + grant artifact name), never mint-shaped alone

## Morph labels are mandatory

For slider, punish-page, or device-companion gates:

1. Store morph labels with the sample before using it as an oracle.
2. Treat the sample as existence proof of one admitted morph, not as a mandate to rebuild only that morph.
3. When local replay fails, ablate alternate morphs before track micro-tuning (`references/verifier-morph-and-state-chain-playbook.md`).
4. Never promote a sample that lacks morph labels into a cross-job mainline assumption.

## How to use samples

- do not lock gold morph as the only mainline; samples feed ablation, not folklore
- prefer same-family solved skeletons for process shape, then re-prove the current host path
- diff `clean-success` against protocol replay first
- use `contaminated-failure` to avoid false algorithm conclusions
- rebuild fixed vectors from clean success boundaries only when possible
- if only contaminated samples exist, say so and limit claims

## When samples disagree with local replay

If a clean success sample exists and the local path still fails, do not change multiple layers at once.

1. Keep sample trust decisions in this file.
2. Run causal isolation with `references/positive-sample-ablation-playbook.md`.
3. Name the primary failure surface with `references/failure-surface-taxonomy.md` when the failing layer is still unclear.

Hygiene decides whether a sample may be used. Ablation decides which owned layer causes the oracle gap.


## Post-hygiene behavior calibration

Only calibrate behavior after sample hygiene and same-world consistency already hold. This section does not override Doctrine 25/36.

When behavior is the remaining owned surface:

1. freeze geometry and the event-phase skeleton
2. stabilize event counts before changing durations
3. adjust stage durations without simultaneously retuning step distributions
4. only then tune step sizes, noise, pauses, and candidate filters
5. offline: many seeds must produce distinct sequences; measure generator retry cost
6. online: new session, new roundKey, no verify retry when measuring hard-gate rate
7. record reject codes as rejects; do not invent which feature the server hit

If URL, roundKey, or identity cookies disagree, stop calibration and return to the same-world gate.

## Hard bans

- do not use common-prefix or length-to-gold as the main optimization objective
- do not start another reverse day after human gold without scheduling an alternate-morph or skeleton-migrate attempt
- do not treat mint-shaped output or stable reject JSON as gate pass
- do not erase morph labels when redacting a sample for reuse
- do not spend primary effort on track entropy while morph/state-chain ablation is unrun
- do not tune tracks solely against automation hand-slide failures
- do not inject broad hooks just to "make capture easier" on the only positive path
- do not mix grants from a success round into a later failed round
- do not call a sample complete when the downstream consumer is missing

## Delivery notes

Report:

- sample grade
- capture path in task cache
- whether environment risk is implicated
- which clean boundaries were promoted into fixed vectors

Final collector still must replay without browser automation.
