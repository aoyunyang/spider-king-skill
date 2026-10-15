# Failure Surface Taxonomy

## Contents

- [When to read](#when-to-read)
- [When not to read](#when-not-to-read)
- [Purpose](#purpose)
- [Primary surfaces](#primary-surfaces)
- [Diagnostic order](#diagnostic-order)
- [Stuck next action](#stuck-next-action)
- [Soft-success traps](#soft-success-traps)
- [Labels for reports](#labels-for-reports)
- [Mapping to nearby files](#mapping-to-nearby-files)
- [Bottom line](#bottom-line)

Use this file to name the primary failure surface before deep patching, and to keep reports honest when a path looks almost done.

## When to read

- local and browser results disagree
- failures are intermittent or exit-dependent
- an intermediate page or token looks successful but the business route still fails
- troubleshooting symptoms span transport, session, signer, and form concerns at once
- the next browser or API move is unclear and the temptation is to add extra routes or open another Chrome

## When not to read

- pure offline decode/sign fixed-vector work with no live failure
- the task is only to package already-proved evidence

## Purpose

Spider King is general-purpose. Failures should be classified by protocol surface, not by guessed vendor folklore. Pick one primary surface, test it, then move.

For symptom-specific pages after classification, use `references/troubleshooting-playbook.md`.

## Primary surfaces

| Surface id | Meaning | Typical evidence |
|---|---|---|
| `egress-environment` | exit IP, reputation, environment risk, node quality | browser and local both fail on one exit; same build passes after exit change |
| `transport-admission` | TLS/H2/client stack/profile admission before app semantics | identical app payload differs by client profile only; live Chrome major copied onto a lower curl impersonate |
| `session-chain` | bootstrap order, cookie slots, freshness, chain continuity | first hop works, replay loses state, jar and outbound Cookie diverge |
| `request-contract` | serialization, empty defaults, warmup order, CSRF/token slots | field set or ordering differs from accepted business request |
| `signer-confidence` | per-request signature/encoding confidence | fixed-input mismatch or only signer-layer ablation fails |
| `verifier-sidecar` | companion proofs, shared state, timing of verifier rounds | main body looks fine; required sidecar/state missing or stale |
| `business-oracle` | business semantics, tenant/role/permission, final envelope | auth shell works; target business route still rejects or returns wrong scope |

Secondary tags may attach, especially `transport-gated`, but reports still need one primary surface.

### Verifier-sidecar subtypes (captcha / device-trust families)

For multi-surface slider/punish gates, also name a process wall from `references/verifier-morph-and-state-chain-playbook.md` (`envelope-wall` / `morph-wall` / `state-chain-wall` / `companion-wall` / `writer-wall` / `track-wall`) when planning the next day of work.

When `primarySurface` is `verifier-sidecar`, add one secondary tag:

| Secondary tag | Meaning | Typical recovery |
|---|---|---|
| `device-trust` | fingerprint/env companion content not trusted for this mid | session-fresh SDK emit; prove apply path |
| `stale-session` | mid/meta/timeline too old or cross-certify reuse | fresh Init->emit->verify only |
| `track-bind` | behavior/track sidecar inconsistent with session | fix after device-trust is admitted |
| `rate-lock` | temporary lock after burst verifies | quiet period; stop hammering |
| `packer-crypto` | envelope crypto/format wrong | fixed-vector packer parity |
| `morph-mismatch` | scene/device/UA class not the admitted form | ablate morph before track tuning |
| `state-chain-incomplete` | bootstrap reports/UMID/init order missing | rebuild ordered transcript on one jar |
| `companion-sign-mismatch` | rand/et/pp slots wrong mode or off-session | fix companions before token entropy |

Do not open track tuning while `device-trust` is unproved.
Do not open track tuning while `morph-mismatch` or `state-chain-incomplete` is untested.
See `references/device-trust-sidecar-playbook.md` and `references/verifier-morph-and-state-chain-playbook.md`.

## Diagnostic order

Default order when the failing layer is unclear:

```text
egress-environment
  -> transport-admission
  -> session-chain
  -> request-contract
  -> signer-confidence or verifier-sidecar
  -> business-oracle
```

Rules:

1. Do not rewrite a signer while the same implementation flips to success on another exit.
2. Do not broaden environment patches while request-contract diffs remain uncompared.
3. Do not treat a challenge shell, privacy interstitial, or intermediate `200` as `business-oracle` success.
4. Climb only one surface at a time when designing the next experiment.

## Stuck next action

When the next move is unclear, pick **one** row. Do not add a second experiment in the same round. Required sidecars that pass omission and restoration stay in the contract.

| Signal | Primary surface | Next action | Forbidden |
|---|---|---|---|
| User asked to open DP / initiator needed, and a second browser would be launched | `egress-environment` | Attach/select the current `TARGET_ACTIVE` host; if DP is already required, let `js-reverse` own both roles | Launch a second Chrome; record `launch` as `attach` |
| Replay 403/challenge changed after copying a newer live Chrome major onto a lower curl impersonate | `transport-admission` | Lock UA, Client Hints, navigator, and TLS/H2 to the installed curl impersonate chrome major | Restart signer or risk-control reverse for that drift |
| Site admits only a newer ClientHello than the installed impersonate | `transport-admission` | Record `impersonate_ceiling` and escalate transport honestly | Mix majors (newer UA + older TLS/H2 impersonate) |
| Known business request is risk-blocked and the writer is unknown | `request-contract`, `signer-confidence`, or `verifier-sidecar` after naming one surface | Reverse the rejected URL: same-URL diff, initiator, writer, cookie mint | Bulk-add telemetry/config/log/sibling URLs |
| Tempted to add an unproven extra route | same | At most one unproven extra route per round, and only after omission changes the oracle | Add 2+ unproven routes this round |
| Two expansion rounds left the oracle unchanged | same | Freeze the request set and keep reversing the rejected request | Keep adding unproven APIs |
| Launch/CDP Chrome is marked automation while ordinary browsing is expected to pass | `egress-environment` | Record `launch` ≠ `attach`; upgrade to Camoufox/managed host only on proved fingerprint pressure | Launch a second automation Chrome; default Camoufox on low-risk work |
| Initiator of the rejected request is still missing | `debugger-trace` gap | Open DP / breakpoint / silent-value capture on the current host | Widen the business workflow first |

## Soft-success traps

These are not completion of `compact-replay` or `collector`:

- stable structured reject code with mint-shaped token
- bootstrap/report telemetry success without grant
- envelope/codec unit tests green without gate grant
- one gate accept without N-run success rate
- intermediate challenge or interstitial document returns `200`
- cookie or token length changes in a familiar direction
- helper returns a non-empty plausible blob
- one HTTP `200` without repeated fresh success
- local logs look cleaner after a broad patch
- a path works only after manual browser state export
- success appears only when the exit node changes and the implementation did not
- HTTP `200` with empty business body, wrong content-type, challenge shell HTML, or a stable business error envelope (silent reject)
- HTTP `200` with punish/challenge response headers or punishment HTML while the caller expected business JSON
- verifier/report gateway accept (`code=0` / envelope success) without a server grant or with business replay still challenged
- helper or local bootstrap returns a non-empty token while the business route still yields empty data

If changing exit alone restores success, label `egress-gated` / `egress-environment` and keep the implementation hypothesis stable until the exit variable is controlled.

Silent reject is usually `business-oracle` only after session-chain, request-contract, and signer-confidence have been checked. Do not call empty-body `200` a collector success.

## Labels for reports

Use compact labels in phase notes and final reports:

```text
primarySurface: egress-environment | transport-admission | session-chain | request-contract | signer-confidence | verifier-sidecar | business-oracle
secondaryTags: [transport-gated, gateway-without-business, ...]
softSuccessRejected: true|false
egressGated: true|false
verifierGatewayAccepted: true|false
serverGrantPresent: true|false
businessOraclePassed: true|false
nextExperiment: one sentence
```

Unfinished work must not be renamed as a temporary collector.

## Mapping to nearby files

| Need | File |
|---|---|
| symptom recipes after surface choice | `references/troubleshooting-playbook.md` |
| stuck next browser/API move | this file, then `references/troubleshooting-playbook.md` |
| signer stage parity | `references/signer-parity-chain-playbook.md` |
| sample trust | `references/positive-sample-hygiene-playbook.md` |
| single-layer causal tests | `references/positive-sample-ablation-playbook.md` |
| verifier morph/state-chain | `references/verifier-morph-and-state-chain-playbook.md` |
| field ownership / round key | `references/parameter-ownership-playbook.md` |
| claim upgrade / handoff readiness | `references/evidence-corroboration-gate.md` |
| final shape acceptance | `references/delivery-gate-playbook.md` |

## Bottom line

1. Name one primary failure surface before patching broadly.
2. Channel and contract before algorithm.
3. Soft success and exit flips are labels, not green delivery.
4. When stuck, take one next action; never bulk-add unproven extra routes.
