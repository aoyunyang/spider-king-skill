# Positive Sample Ablation Playbook

Use this file when an official client or clean browser path can pass and the local protocol path cannot, and you need causal isolation rather than more simultaneous changes.

## Contents

- [When to read](#when-to-read)
- [When not to read](#when-not-to-read)
- [Prerequisites](#prerequisites)
- [Protocol](#protocol)
- [Stop rules](#stop-rules)
- [Interpreting results](#interpreting-results)
- [Relation to fixed-input parity](#relation-to-fixed-input-parity)
- [Anti-patterns](#anti-patterns)
- [Bottom line](#bottom-line)

## When to read

- local replay fails after a trusted success sample exists
- transport, session, signer, sidecar, and form fields are all under suspicion
- a previous multi-variable "fix" cannot name the root cause
- verifier or business oracles reject local output that looks structurally plausible

## When not to read

- no trusted positive sample yet; capture hygiene first
- the only task is fixed-input helper parity with no live oracle gap
- the failure is already isolated to one proved surface and one field

## Prerequisites

1. Read `references/positive-sample-hygiene-playbook.md` and keep only clean success samples.
2. Prefer one complete same-round success transcript: request, response, companions, and session state.
3. If the oracle is single-use, budget fresh challenges before the matrix begins.
4. Keep one baseline client stack, UA/Client-Hints generation, and session chain for the experiment set unless the experiment is specifically about that layer.

Hygiene decides whether a sample is trustworthy. This playbook decides how to use it.

## Protocol

Run these steps in order.

### 1. Freeze one positive oracle

Save one server-accepted success round with:

- final request line, headers, and body bytes
- final response status and business envelope
- required sidecars or companion requests
- outbound Cookie header and relevant jar transitions
- challenge/nonce/session identifiers for that round

Do not mix fields from a second round into this oracle.

### 2. Prove the local channel with the untouched success body

Replay the original success body and critical headers through the local HTTP client on a fresh equivalent session only when the protocol allows replay; otherwise reconstruct only the transport-identical envelope.

- pass: local transport/header/cookie carrying path can be removed from the main suspect set for that stack
- fail: fix transport admission, proxy, HTTP version, header set, or cookie export before touching signer logic
- single-use oracle consumed: stop, capture a new success sample, and restart. Do not treat the consumption error as proof about another layer

### 3. Replace one ownership layer at a time

Keep every other layer at the positive-sample value. Replace exactly one layer with the local implementation:

| Layer ownership | Generic contents |
|---|---|
| transport | client stack, ALPN/HTTP version, proxy, profile |
| static client surface | UA, Client-Hints, accept language, fixed headers |
| session chain | cookies, bootstrap artifacts, slot order |
| request contract | field set, empty defaults, serialization, CSRF/token slots, warmup order |
| per-request signer | signed query/body/header fields regenerated locally |
| sidecar/telemetry | companion posts, shared keys, timing companions |
| settle/timing | stage order, timer waits, retry cadence |


For multi-surface verifiers (slider/punish/device companion), prefer this **order of replacement classes** when the gate reject is stable and mint-shaped tokens already exist:

```text
morph (scene/device/UA)
  -> state-chain completeness/order
  -> companion slots (rand/et/pp modes)
  -> token-writer family
  -> track/geometry micro-details
  -> broad env/transport patches
```

If class 1-3 flips the hard gate metric, stop. Do not open track entropy. Details: `references/verifier-morph-and-state-chain-playbook.md`.

Judge only by the final server oracle for that round, not by local aesthetics.

### 4. Stop at first failure and open that layer

When the first single-layer replacement fails:

- stop widening variables
- decode or parse only that layer
- compare hidden envelope, version markers, field topology, timestamps, and association keys
- do not compare only Base64 length or "looks similar"

### 5. Reverse-minimal control

After a candidate fix appears:

1. remove unrelated experiment scaffolding
2. keep only the suspected root-cause change
3. rerun on a fresh round when live replay is authorized
4. only then write the change into the durable implementation

### 6. Record the matrix

Every row needs:

```text
keep:
replace_only:
challenge_or_nonce:
ownership_layer: python-owned | host-owned | server-owned | transport | session | contract | ...
verifierGateway: pass | fail | n/a
businessOracle: pass | fail | n/a
result: pass | fail | invalid-consumed | blocked
notes:
```

Invalid or consumed rounds are not causal conclusions. After gateway accept consumes a challenge id, stop using that id for another replace_only row; capture a fresh positive oracle.

When both oracles matter, a row that keeps gateway pass but loses business pass still isolates the replaced layer for business packaging/session binding, not for "crypto randomly failed".

## Stop rules

- If mint-shaped + stable reject persists across 3 sessions on one morph, stop replacing token layers and ablate morph first (`references/verifier-morph-and-state-chain-playbook.md` K1).
- If the only improved metric is offline similarity to gold, mark the row invalid as causal evidence.

- never conclude root cause from a multi-variable success
- never reuse a consumed one-time token/nonce as the next negative control
- never promote helper-shape parity over the server oracle
- never continue after first layer failure by swapping three more layers "to see"
- never treat intermediate shell success as the ablation oracle when the business endpoint is the real gate
- never ablate the signer or protobuf schema because the HTML shows zeros when no list XHR fired

## Interpreting results

| Pattern | Meaning |
|---|---|
| no list XHR and HTML placeholder zeros | observation/activation first, not payload schema |
| untouched success body fails locally | channel/admission/header/cookie path first |
| only signer layer fails | algorithm, field order, key schedule, or preimage |
| only request-contract layer fails | empty fields, defaults, CSRF slot, warmup, serialization |
| only sidecar layer fails | companion proof or shared-state coupling |
| only transport layer fails | profile/stack admission, not business logic |
| every local layer fails only on one exit | label `egress-environment` and change exit before more reverse work |

## Ownership-aware replaces

Before replacing a field, label it with `references/parameter-ownership-playbook.md`:

- do not replace a `server-owned` grant with a guessed local value and call that an algorithm test
- replace at most one `host-owned` material per row
- keep the round primary key identical inside a valid row

## Relation to fixed-input parity

- fixed-input parity proves a helper against frozen vectors offline
- ablation proves which live layer makes an accepted transcript diverge
- use fixed-input work inside the failing layer after ablation points there

## Anti-patterns

- locking gold morph while skipping morph ablation
- replacing only the hardest token while state-chain/companions stay incomplete
- calling mint-shaped or stable-reject results a layer pass
- changing proxy, UA, signer, and form defaults in one attempt
- calling a lucky pass "root cause found" without reverse-minimal control
- using polluted automation failures as the only negative set
- declaring family-specific recipes from one cookie or field name during ablation

## Bottom line

0. Morph before track when rejects are stable.
1. One trusted success round. One replaced layer. One oracle.
2. First failure owns the next reverse step.
3. Fresh reverse-minimal verification beats multi-variable folklore.
