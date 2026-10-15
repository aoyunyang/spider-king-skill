# Case Reuse Playbook

Use this when an existing solved helper, prior collector, fixed-vector bundle, experience card, or case-like directory looks reusable for a new or continued target.

## Contents

- [User-delivered solved skeletons](#user-delivered-solved-skeletons)
- [Core Rule](#core-rule)
- [Selection Gate](#selection-gate)
- [Reuse Classes](#reuse-classes)
- [Read Order](#read-order)
- [Verification Loop](#verification-loop)
- [Sanitization](#sanitization)
- [Writeback](#writeback)
- [Failure Modes](#failure-modes)

## Core Rule

Reuse process and structure first, not live state.

A historical helper or case can suggest the next proof. It does not prove the current target until fresh fixed vectors or live acceptance pass under the current scope.

## Selection Gate

Select a reusable case only when one of these is true:

- exact scheme, host, port, route family, product generation, and protocol boundary match
- at least two independent high-confidence signals match, such as SDK family, cookie transition, request field placement, endpoint chain, verifier subtype, transport wrapper, or fixed-vector behavior

Never select from:

- one generic parameter name such as `sign`, `token`, `a_bogus`, or `_0x`
- one status code such as `403`, `412`, or `429`
- one cookie name without writer and transition evidence
- one non-empty helper output
- a comment, README claim, or stale chat transcript

When two cases match the same signals, do not choose by directory order. Ask for or collect a discriminator: product version, runtime family, request route, algorithm subtype, negative signal, or fixed vector.

## Reuse Classes

Label reused material honestly:

| Class | Meaning | Can prove current target? |
|---|---|---|
| `template` | historical process or shape only | no |
| `fixture-proof` | deterministic vectors pass offline | local proof only |
| `current-proof` | fresh target vectors or approved live replay pass | yes, within scope |
| `helper-only` | one narrow artifact generator | only the artifact boundary |

Do not describe snapshot-driven generation, artifact pools, or copied browser exports as pure algorithmic generation. Use the truth labels from `references/opaque-runtime-profile-playbook.md` when opaque state remains.

## Hit-case constraint internalization

A case hit is not a code drop and not a license to skip the reverse loop.

When a reusable case or experience card matches:

1. extract hard constraints first: no-touch surfaces, UA branch bans, required bootstrap order, rejected writers, negative controls
2. treat those constraints as active gates during implementation; re-open the case when a step fails instead of improvising around it
3. still prove fixed vectors on the **current** target before live claims
4. never copy secrets, cookies, profile exports, or historical tokens into the new delivery
5. leftover last-page UA text or a shared `call` name is not permission to copy method, time slot, token width, export-versus-pager semantics, or a sibling token alphabet
6. independently proved same preimage concat still does not copy the sibling calculator; identify the current writer family first (tiny-input digest, or freeze-pad-then-oracle for PKCS#1) before copying any sibling helper. Extra join delimiters such as `N$` versus `N()` are also current-target evidence, not sibling copy

If only the high-level direction is reused while constraints are ignored, count that as failed reuse.

## Read Order

Prefer the current workspace before the skill library:

1. Existing project `analysis/proof_manifest.json`
2. Existing `js_reverse_cache/tasks/<task-id>/handoff.json`
3. Current stable helper or collector entrypoint
4. Fixed fixtures and tests
5. Minimal verifiable facts or experience card
6. Generic playbook

Read only enough to confirm or reject reuse. Do not load sibling cases after one case mismatches current evidence unless a new discriminator points to that sibling.

## Verification Loop

Before adapting a reusable helper:

1. Freeze the current target inputs and expected output.
2. Run fixed vectors first.
3. Compare the canonical wire boundary, not only the helper return value.
4. Confirm query/body/header/cookie slot placement.
5. Confirm current server-issued state and session scope.
6. Run one approved live replay only when the user requested and authorized it.

If fixed vectors fail, save the first divergence and stop live replay. If live `200` returns a challenge shell, empty business payload, or wrong content type, treat reuse as unproved.

## Sanitization

Reusable material may preserve:

- route shapes
- field names
- state provenance
- transform order
- fixed synthetic vectors
- hashes and lengths
- negative controls
- exact acceptance gates

Reusable material must not preserve:

- cookie/token values
- Authorization headers
- account identifiers
- browser profile exports
- full private HAR bodies
- absolute local paths
- one-time verifier rounds unless redacted and synthetic

When current state is required, pull it at runtime from an explicitly approved session and keep it out of the reusable case.

## Writeback

Offer writeback only after a successful delivery or local-proof that has:

- a stable import-safe entry
- fixed vectors or named checkpoints
- current-target acceptance status
- sanitized artifacts
- a negative control or first-divergence note
- no raw secrets

Default writeback is a small experience card or minimal verifiable facts. Create a structured case registry only when multiple independent tasks would benefit from machine selection.



## User-delivered solved skeletons

When the user supplies a solved pure-protocol skeleton for the same SDK/verifier generation:

1. Classify it as `template` until the current host path is re-proved.
2. Prefer migrating business TARGET/host/punish/slide binding and scene morph over re-deriving behavior walls.
3. Keep Python as the live HTTP owner; keep local JS/WASM helpers as labeled L2 algorithm runtimes.
4. Promote to `current-proof` only after the current target hard gate metric passes on fresh sessions.
5. If selection signals match (SDK family, field layout, bootstrap chain, companion slots) and the skeleton already passes elsewhere, do not spend the mainline re-animating tracks first.

This is process reuse, not secret reuse. Copy no cookies, grants, or account material.

## Third-party and legacy material

Treat external repositories, README support claims, and historical generators as facts to verify, not as availability proof.

- require current fixed-vector and live-oracle checks before reuse
- default-untrusted any legacy generator path until the current target accepts it
- copy no code from materials without a clear license; facts and structural notes are enough
- brand or family folklore is not a selection signal by itself; use the ordinary multi-signal selection gate
- never promote copied secrets, cookies, account tokens, or browser profiles into a reusable case

## Failure Modes

| Trigger | First fix | Stop condition |
|---|---|---|
| User gave a same-family solved skeleton but work restarted at track capture | migrate host/path/state-chain first | no mainline track rewrite until morph/state-chain ablation fails |
| Case matches one marker only | collect a second independent signal | no reuse |
| Third-party README claims current support | require fixed vectors and live oracle | no reuse on claim alone |
| Historical helper emits a plausible token | run fixed vectors and wire slot diff | no live replay |
| Current endpoint changed shape | record mismatch and return to normal loop | no sibling guessing |
| Secret appears in the reusable material | redact and replace with shape/hash/provenance | no writeback until clean |
| Browser profile is required | extract the artifact boundary or mark retained exception | not a reusable collector |
| Neighbor leftover UA or a shared `call` name looks reusable | freeze current method, time slot, token width, and export/harvest boundary against live traffic | no copy of sibling request shape |
| Independently proved concat of path + clock + page looks like the last signer | identify the current writer family; tiny-input digest for a hasher, freeze the RSA pad string before gold-token or live-decrypt policy | no copy of the sibling calculator |
