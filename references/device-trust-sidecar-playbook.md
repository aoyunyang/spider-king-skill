# Device-Trust Sidecar Playbook

Use this when a multi-step verifier accepts packaging/track/sign helpers but still rejects on a device/environment companion request (Log2-class, device register, env report) bound to the same session id.

## Contents

- [When to read](#when-to-read)
- [When not to read](#when-not-to-read)
- [Core model](#core-model)
- [Delivery levels L0-L3](#delivery-levels-l0-l3)
- [Knife order](#knife-order)
- [Hard ablations](#hard-ablations)
- [False attributions](#false-attributions)
- [Session freshness](#session-freshness)
- [Reporting](#reporting)
- [Related](#related)

## When to read

- Init + packer + track + verify protocol all look correct, verify still fails
- Blocking or swapping one companion request flips accept/reject
- Same-session ugly payloads sometimes pass; cross-session gold rebinds fail
- Vendor fingerprint SDK (FeiLin-class) appears next to captcha/risk verify

## When not to read

- Pure signer mismatch with no device companion request
- Pure transport/TLS pre-gate failures
- Already-proved collector only needs packaging

## Core model

Many captcha/risk verifiers are **multi-gate**:

```text
session mint (Init)
  -> device-trust sidecar (fingerprint SDK emit / Log2-class)
  -> behavior sidecar (Log3 / track / sensor)
  -> Verify semantic
```

Invariants:

1. **Packer success is not trust success.** Bit-exact rebuild of outer/inner envelopes can be done while the content was never server-trusted for this mid.
2. **Device-trust is usually session-fresh.** Rebinding an old dense/env blob onto a new mid is a high-cost false path.
3. **UI shell is often optional.** The hard gate is the fingerprint runtime + apply path for server-issued device config, not the visible slider widget.
4. **Companion HTTP 200 is soft.** Acceptance is the final verify semantic (or a proved downstream business consume).

Primary surface label: `verifier-sidecar` with secondary tag `device-trust`.

## Delivery levels L0-L3

Name the delivery level honestly:

| Level | Runtime | Meaning |
|---|---|---|
| L0 hybrid | real browser only for SDK emit | control baseline |
| L1 no-UI browser | real browser page without captcha UI shell | proves UI is optional |
| L2 local JS runtime | Node/jsdom/quickjs + host patch runs vendor SDK | browser-free business path; not pure-Python fields |
| L3 pure Python fields | no JS runtime | full field port |

Rules:

- Do not call L2 "pure protocol / fully offline pure Python".
- L2 may be a valid collector if Python owns live HTTP and the local runtime only restores parameters.
- L3 is optional optimization after L2 is stable.

## Knife order

```text
1. Hybrid positive baseline
   native SDK emit for current mid + already-owned Python post-path
2. One-layer ablations on the companion request only
   block / repost / rebuild-same-body
3. Separate surfaces
   device-trust | stale-session | track-bind | rate-lock | packer-crypto
4. Apply-path proof for server-issued config
   Python Init body injected into official apply path vs manual incomplete wiring
5. Offline/local runtime for fingerprint SDK
   crypto global -> config/Br wiring -> host constructors -> capture emit
6. Same-session immediate verify
7. N-run stability (prefer >=10) before collector claim
```

Do not open cosmetic field matrices before steps 1-3.

## Hard ablations

| Experiment | If pass | If fail |
|---|---|---|
| Native companion + Python track/verify | Python post-path owned | post-path still broken |
| Block companion, no post | companion necessary | look elsewhere |
| Capture-block + repost same body | body is the gate; packaging path OK to port | timing/transport side channel remains |
| Rebuild same plaintext with local packer | packing owned | packing not owned |
| Same-mid ugly emit still accepts | cosmetics soft | do not chase cosmetics as mainline |
| Skip first SDK call + one emit | first call not a trust prerequisite | order/bootstrap side effects matter |
| Python-issued Init fulfilled into official apply | Init payload trusted; prior fail was wiring | Init transport/client binding remains |
| Cross-session gold rebind | rare weak enforcement | expected fail; stay session-fresh |
| Stale meta delayed verify | often time/stale family | do not re-open packer |

## False attributions

Stop these early:

1. **"Python Init is untrusted"** before proving apply-path wiring (mr/rn-class DeviceConfig apply, secret proto fields, load order).
2. **"First fingerprint call is mandatory"** without skip-first ablation.
3. **"This cosmetic field is the iron gate"** without same-mid single-field ablations.
4. **"Companion 200 means trusted"** without final verify semantic.
5. **"F/time-like rejects mean packer still wrong"** when meta is stale.
6. **"Track is the wall"** while device-trust sidecar is unproved or unconsumed.
7. **"Random fallback token is good enough"** because a soft route accepted it. A report-sidecar mint and a locally randomized lookalike are different writers.

## Session freshness

- Keep `mid/sessionId/secret/cid` on one chain from Init to Verify.
- Emit device-trust for the **current** mid; do not template-rewrite clocks across sessions as the main strategy.
- Align outer counters (`num` / n1-class) between companion and token builders when the contract requires it.
- If rejects match stale/timeline family, first rerun **fresh Init -> emit -> verify** with no reused meta.
- Name the token writer: report sidecar, login grant, or local random. Hard-gate replay must use the live sidecar mint; keep random fallback for soft-route debugging only.

## Reporting

Always state:

```text
primarySurface: verifier-sidecar
secondaryTags: [device-trust, session-fresh, ...]
deliveryLevel: L0|L1|L2|L3
companionGate: proved|unproved
applyPath: official|manual-incomplete|local-runtime
stability: N/M
```

## Related

- local runtime host patching: `references/local-sdk-env-patch-playbook.md`
- verifier reject localization: `references/verifier-error-localization-playbook.md`
- session contracts: `references/session-contract-playbook.md`
- ablation discipline: `references/positive-sample-ablation-playbook.md`
- failure surfaces: `references/failure-surface-taxonomy.md`
- anti-patterns 30-36: `references/anti-patterns-playbook.md`
