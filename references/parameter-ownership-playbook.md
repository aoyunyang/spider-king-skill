# Parameter Ownership Playbook

Use this file when a challenge or verifier flow has many dynamic fields and you need to decide what Python may own, what must run in a local host helper, and what only the server can issue.

This is a generic ownership contract. Do not turn vendor field names into a route selector.

## Contents

- [Core rule](#core-rule)
- [Three ownership classes](#three-ownership-classes)
- [Source class versus ownership class](#source-class-versus-ownership-class)
- [Same-round primary key](#same-round-primary-key)
- [Homonym fields](#homonym-fields)
- [Version as round fact](#version-as-round-fact)
- [Layered ownership inside one slot](#layered-ownership-inside-one-slot)
- [Same-world gate](#same-world-gate)
- [Protocol profile identity](#protocol-profile-identity)
- [Acceptance layers](#acceptance-layers)
- [Implementation order](#implementation-order)
- [Report labels](#report-labels)
- [Common traps](#common-traps)
- [Related references](#related-references)

## Core rule

Before rewriting an algorithm, label every decisive field:

1. `python-owned` — HTTP, parsing, jar, orchestration, serialization
2. `host-owned` — must execute current challenge/verifier scripts in a local host helper
3. `server-owned` — parse from a verify/grant response; never invent offline

Wrong ownership is a method error. A locally invented `server-owned` grant is not a protocol port.

After labels exist, still pass the same-world gate before rewrite or send. Slot-local validity is not round validity.

## Three ownership classes

| Class | Owns | Typical contents | Delivery move |
|---|---|---|---|
| `python-owned` | collector runtime | business URL/query, HTML/JSON config parse, cookie jar, warmup/report order, timestamps, transport replay | keep in Python |
| `host-owned` | local challenge/verifier helper | trajectory ciphertext, environment-bound request materials, device/UMID-like tokens, page PassPoint-like blobs | run current scripts; sniper-patch only observed reads |
| `server-owned` | remote verifier/business gate | pass cookie/token returned after verify accept | parse `Set-Cookie` / grant fields; bind to same round only |

Length, alphabet, or "looks like Base64/AES" never upgrades a field from hypothesis to algorithm proof.

## Source class versus ownership class

Source class answers **where the value comes from**. Ownership class answers **who may emit it in the collector**. They are orthogonal. Do not copy a five-letter A-E mix that treats plaintext and local algorithms as the same recovery move.

| Source class | Signal | Typical recovery |
|---|---|---|
| `fixed` | stable page/config/enum constants | copy from current config |
| `plaintext` | user or business identifiers in clear | pass through |
| `local-algorithm` | RSA/AES/HMAC/custom encode from known local inputs | port or run a tiny helper |
| `server-issued` | ticket, UUID, one-time token returned on the wire | parse; never invent |
| `risk-interactive` | fingerprint, challenge payload, VM output, visual oracle | host helper, same-round feed, or separate oracle |

A `local-algorithm` field can still be `host-owned` if it must execute harvested scripts. A `server-issued` field is often `server-owned`, but Python may still own parse-and-echo. Label both columns before rewrite.

## Same-round primary key

Many challenge families mint a server-issued challenge id that must thread the whole round:

- appears in response headers and/or challenge HTML/config
- reused by initialize/report/verify payloads
- must not be client-generated as a replacement
- is often single-use; a consumed or expired id invalidates later ablations on that round

Treat that id as the round primary key in task notes. All host-owned materials and the final business replay must cite the same key.

## Homonym fields

Same parameter name in different requests is not one value by default.

Examples of the pattern (not a vendor checklist):

- multiple `_rand` / `v` / `sig` slots on load-report, initialize, and verify
- an inner JSON field named like an HTTP header material
- page-initial random material versus verify-query random material

Record each by request site:

```text
fieldName: _rand
site: load-report | initialize | verify-query | header
owner: python-owned | host-owned | server-owned
roundKey: <challenge id fingerprint>
```

## Version as round fact

SDK, punish/challenge page, and helper script versions observed in the current round are facts for that round only.

- store them in round context
- compare old projects for structure only
- do not freeze them as skill-level constants or Startup Gate hits


## Layered ownership inside one slot

A single request field can contain more than one ownership class.

Split the slot before choosing a rewrite strategy:

| Layer | Owner | Typical shape | Delivery move |
|---|---|---|---|
| pure-compute sublayer | often `python-owned` | PoW search, standard digest, Base64/packing, standard-ISA memory machine with fixed I/O regions | port or simulate locally |
| lifecycle / closure sublayer | `host-owned` | marker-ordered state machines, event-accumulated signers, stack-sensitive token blocks | run current scripts in order; sniper-patch only proved reads |
| grant sublayer | `server-owned` | pass cookie/token after verify accept | parse from grant response |

Do not treat the whole slot as one pure function when only the first sublayer is separable. Record sublayers in the ownership map:

```text
fieldName: <slot>
site: verify-header | verify-query | ...
layers:
  - name: pow-base
    owner: python-owned
  - name: marker-rewrite
    owner: host-owned
roundKey: <challenge id fingerprint>
```

## Same-world gate

Multi-slot chains share one verification world. Local format success on each slot is not enough.

Before assemble/send, prove:

1. `roundKey` is identical across precursors, host materials, verify, and grant binding
2. identity cookies and device/UMID-like tokens agree in the Python jar and every host helper document/cookie string
3. one behavior/event sequence is fed to every consumer that claims to observe that sequence
4. any canonical URL/request string used by a signer equals the bytes about to be sent
5. no slot was generated from a different challenge, cookie snapshot, or helper process age

If any check fails, stop. Repair same-world consistency before trajectory, packing, or algorithm folklore.

Pre-assemble stop labels:

```text
sameWorld:
  roundKeyAligned: true|false
  identityAligned: true|false
  eventSequenceShared: true|false
  canonicalRequestLocked: true|false
  stopReason: <empty or reason>
```



## Protocol profile identity

Same-world consistency includes one protocol profile for the round.

Freeze a single profile object that every helper reads:

```text
profileId: short hash
sceneOrClientClass: ...
ua: ...
clientHints: ...
platform: ...
touchCapable: true|false
eventSemantics: mouse|touch|mixed
screen: ...
widgetGeometry: ...
fingerprintSurfaces: [...]
```

Rules:

1. device-toolbar or responsive preview is not a profile
2. do not maintain two "mobile" defaults that differ by helper
3. Python session headers/Client-Hints must match the profile the host scripts see
4. if a desktop host runs a mobile protocol profile, say so explicitly; do not call it a desktop-web solve

## Acceptance layers

Label progress with three layers before claiming completion:

1. `bootstrapAccepted` — challenge HTML/config and roundKey are fresh and parseable
2. `verifierAccepted` — verify/slide/check semantics accepted and any server grant is present when required
3. `businessAccepted` — first downstream business replay reaches the target oracle

Helper non-empty output is only local smoke. HTTP 200 or envelope success is not `verifierAccepted`.

## Implementation order

Prefer this layering. Save fixed vectors after each layer.

```text
A. challenge HTML/config parser + round key
B. cookie jar + same-round context
C. precursor report/initialize replay
D. host probes for device/UMID-like materials
E. host capture of trajectory / answer ciphertext
F. host capture of environment-bound request materials
G. assemble verify transport
H. parse server-owned grant
I. post-grant report if the live chain requires it
J. business replay oracle
K. fresh-round validation
```

Do not debug `host-owned` crypto while A/B/C still disagree with the browser transcript.

## Report labels

```text
roundKeyFingerprint: short hash
profileId: short hash
ownershipMap:
  - name: ...
    site: ...
    owner: python-owned | host-owned | server-owned
    sourceClass: fixed | plaintext | local-algorithm | server-issued | risk-interactive
    sourceClass: fixed | plaintext | local-algorithm | server-issued | risk-interactive
sameWorld: ...
acceptance:
  bootstrapAccepted: true|false
  precursorAccepted: true|false
  verifierGatewayAccepted: true|false
  serverGrantPresent: true|false
  businessOraclePassed: true|false
smokeLevel: L1|L2|L3|L4
```

If only gateway accept is true, the report status is "verifier gateway stage success; business replay not accepted".


## Common traps

- collapsing source class into ownership class, or treating plaintext and local-algorithm as one recovery move
- treating device-toolbar or UA-only changes as a protocol profile
- calling helper non-empty output a verifier or business pass
- treating each dynamic slot as an independent signature that can be finished alone
- collapsing layered sub-ownership into one pure-Python rewrite because the outer alphabet matches
- assembling verify while Python jar and host helper identity cookies disagree
- inventing a server grant cookie/token from an old round
- rewriting host-owned materials as pure Python before the public entry is proven
- sharing one random field across every request because the name matches
- treating script version from another project as the current contract
- calling length/charset matching an algorithm identification
- mixing ownership layers while judging a single ablation row

## Related references

- layered acceptance: `references/verifier-replay-playbook.md`
- challenge HTML/state: `references/challenge-state-envelope-playbook.md`
- local helper boundary: `references/local-challenge-executor-playbook.md`
- ablation matrix: `references/positive-sample-ablation-playbook.md`
- soft success: `references/failure-surface-taxonomy.md`
- delivery wording: `references/delivery-gate-playbook.md`
- same-world doctrine: `references/doctrine-index.md` (Doctrine 40)
- protocol profile doctrine: `references/doctrine-index.md` (Doctrine 41)
- retry and smoke ladder: `references/verifier-replay-playbook.md`
- stateful helper driver: `references/local-challenge-executor-playbook.md`
