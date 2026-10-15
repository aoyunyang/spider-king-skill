# Evidence Corroboration Gate

Use this file before promoting a hypothesis into a gate-family claim, escalating one rung, or handing a blocker to an installed specialist.

## Contents

- [When to read](#when-to-read)
- [When not to read](#when-not-to-read)
- [Purpose](#purpose)
- [Two-surface rule](#two-surface-rule)
- [Evidence surfaces](#evidence-surfaces)
- [What never counts alone](#what-never-counts-alone)
- [Upgrade decisions](#upgrade-decisions)
- [De-branded patterns](#de-branded-patterns)
- [Recording template](#recording-template)
- [Relation to nearby files](#relation-to-nearby-files)
- [Bottom line](#bottom-line)

## When to read

- one status code, cookie name, token name, or old note tempts a hard classification
- two reverse paths look plausible and one is heavier
- a specialist skill exists and might own the next artifact
- the report is about to say "confirmed" rather than "suspected"

## When not to read

- pure offline fixed-vector work with no classification claim
- already-proved known-boundary Hook/AST/env-patch routes that do not change family ownership
- ordinary evidence capture that only records observations

## Purpose

Keep Spider King general-purpose. Classification and escalation must come from independent evidence, not folklore, brand names, or a single familiar marker.

## Two-surface rule

Any of the following claims requires at least two independent evidence surfaces:

1. a gate-family label such as `signer-gated`, `verifier-gated`, `decode-gated`, `session-gated`, or a secondary `transport-gated` tag treated as decisive
2. a route upgrade that widens runtime, patch surface, transport profile, or helper boundary
3. specialist or focused-owner handoff for a proved blocker

One surface may justify a working hypothesis. One surface alone must not justify "confirmed", specialist transfer, or a heavier delivery shape.

## Evidence surfaces

Treat these as distinct only when they are independently observed:

| Surface | Examples of independent proof |
|---|---|
| wire request/response | exact method, URL shape, body bytes, status, response envelope |
| state transition | cookie/header/slot changes across ordered hops |
| runtime mutation | initiator, call boundary, pre-wire object, worker message |
| transport admission | profile/stack differences on the same application payload |
| challenge/verifier envelope | challenge document, proof round, shared-state companion |
| business oracle | downstream business success/failure, not a shell page |

Correlated copies of the same fact do not count as two surfaces. Example: a cookie name in HTML and the same cookie name in a jar note are one surface if neither shows an independent transition or consumer.

## What never counts alone

- one HTTP status (`403`, `412`, `429`, `200`)
- one cookie, token, header, or field name
- plausible length, alphabet, or "looks signed"
- helper load success or local exception absence
- an old case note, README claim, or remembered family label
- one transport glitch without an application-layer corroboration
- one browser screenshot without wire or state proof

## Upgrade decisions

| Evidence state | Allowed action |
|---|---|
| zero solid surfaces | stay in Observe/Capture; do not classify |
| one surface only | record hypothesis; continue the universal loop |
| two agreeing surfaces | may label gate family, climb one escalation rung, or request specialist handoff |
| two conflicting surfaces | return to the earliest uncertain stage; do not average them into confidence |
| specialist missing after confirmation | keep Spider ownership; name the unmet capability; use the smallest generic fallback |

Escalation still follows `references/escalation-ladder-playbook.md` one rung at a time. This gate decides whether the claim is earned, not which patch to write.

## De-branded patterns

Use structural wording only:

- `stage-2 POST rotates cookie-A and only then the business route accepts` plus initiator proof -> session/bootstrap claim may harden
- same body accepted on one client stack and rejected on another, with browser success preserved -> transport-admission hypothesis earns a secondary tag
- business oracle fails while an intermediate challenge shell returns `200` -> do not promote the shell to success

Do not invent a vendor-specific path from a familiar name. If an installed specialist exists and the blocker matches its declared scope with two surfaces, hand off through `references/specialist-handoff-contract.md`. If it does not exist, remain on the generic Spider loop.

## Recording template

Record before the upgrade or handoff:

```text
claim:
surface_1:
surface_2:
counter_evidence:
decision: hypothesis | confirmed-for-route | handoff | rollback
fallback_if_owner_missing:
```

Redact secrets. Store hashes and task-local paths when files exist.

## Relation to nearby files

- hygiene and ablation decide sample trust and causal isolation
- this gate decides whether a classification or ownership change is justified
- specialist handoff carries the envelope after this gate passes
- delivery gates still own final shape acceptance

## Bottom line

1. Two independent surfaces to confirm; one surface only to suspect.
2. Missing specialist means generic fallback, not a fake family shortcut.
3. Conflicting surfaces send you backward, not upward.
