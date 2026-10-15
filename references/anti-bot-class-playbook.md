# Anti-Bot Class Playbook

Use this file in Phase 0 / Startup Gate after intake, before loading family folklore or giant bundles.

The goal is to classify the fight by **how the server binds truth**, not by brand names.

## Contents

- [Core rule](#core-rule)
- [Three classes](#three-classes)
- [Recognition moves](#recognition-moves)
- [Class to method map](#class-to-method-map)
- [Observation allow or deny](#observation-allow-or-deny)
- [Secondary family markers](#secondary-family-markers)
- [Common traps](#common-traps)
- [Related references](#related-references)

## Core rule

Pick one primary class from live wire and runtime evidence:

1. `signature-bound` — environment or host state is part of the signature or challenge answer
2. `behavior-interceptor` — business params are signed or mutated by request interceptors / wrappers
3. `pure-obfuscation` — hard to read, but no meaningful host-environment binding

Family labels (WAF names, SDK filenames, cookie names) are secondary hints only. Confirm class with at least two surfaces via `references/evidence-corroboration-gate.md` before hardening a route.

## Three classes

### `signature-bound`

Signals:

- redirect or status loops such as repeated `412` / `302` then `200`
- large single-file VM or challenge scripts that seed cookies or URL suffixes
- changing host surfaces (navigator, layout, canvas, timers) changes the emitted token
- proxy-style broad host hooks poison the answer; transparent / public-boundary observation is safer

Default method direction:

- harvest public I/O and challenge artifacts first
- prefer local host bootstrap + narrow patch over full deobfuscation
- do not ship browser automation as the refresh path

Primary refs: `references/challenge-state-envelope-playbook.md`, `references/local-challenge-executor-playbook.md`, `references/jsvmp-analysis-playbook.md`, `references/environment-patch-playbook.md`

### `behavior-interceptor`

Signals:

- page loads with ordinary `200` and business JS continues
- XHR/fetch wrappers rewrite URL, headers, body, or append sign params
- signature inputs include query, body, path, UA, cookies, or timestamps without full host fingerprinting
- "feed then cut" works: triggering the real transport inside a controlled host yields the final wire shape

Default method direction:

- prove the transport mutation boundary first (`references/hook-techniques.md`, `references/decoy-and-real-request-playbook.md`)
- use feed-cut capture when interceptors own the final sign (`references/jsvmp-analysis-playbook.md`)
- port pure algorithm when `hot_methods` show standard digests and env reads stay low

Primary refs: `references/transport-wrapper-playbook.md`, `references/patched-helper-playbook.md`, `references/crypto-patterns.md`, `references/jsvmp-analysis-playbook.md`

### `pure-obfuscation`

Signals:

- string tables, CFF, heavy rename, eval/new Function packing
- fixed-input local execution matches browser without host-surface surgery
- server accepts pure Python or tiny JS helper outputs with no env patch growth

Default method direction:

- offline deob / string recovery then fixed-vector port
- do not open broad env patch or silent-value ceremony

Primary refs: `references/obfuscation-guide.md`, `references/offline-inline-deob-playbook.md`, `references/pure-python-rebuild-playbook.md`

## Recognition moves

Do these cheap checks before deep reverse:

1. first navigate or capture **without** invasive hooks when safe, and read status/redirect shape plus whether business JS actually ran
2. capture one clean business request and its preceding bootstrap chain
3. search for interceptors: XHR/fetch wrappers, `open`/`send` overrides, service workers
4. change one host-visible value only if safe, or compare two hosts, to see if the token moves
5. if VM-like dispatch is present, prefer public-boundary heat (`hot_keys` / `hot_methods` style summaries) over opcode tracing
6. dense `String.fromCharCode` rebuild loops are a VM-string signal, not proof of a family name

Record:

```text
antiBotClass: signature-bound | behavior-interceptor | pure-obfuscation
classEvidence: [surface-a, surface-b]
provisional: true|false
```

## Class to method map

| Class | Prefer | Avoid early |
|---|---|---|
| `signature-bound` | public I/O cards, challenge harvest, narrow host bootstrap, sniper env patch | proxy-all host hooks, full VM recovery, browser cookie refresh as delivery |
| `behavior-interceptor` | initiator + wrapper boundary, feed-cut, pure crypto port | full DOM patch, browser as signer |
| `pure-obfuscation` | deob + fixed vectors + pure Python | env diff campaigns, silent-value backends |

Delivery still must pass `references/delivery-gate-playbook.md`. Class choice never authorizes browser-backed collectors.

## Observation allow or deny

Class gates **how** you may observe, not only how you deliver.

| Class | Prefer | Deny or delay |
|---|---|---|
| `signature-bound` | clean baseline first; transparent / egress / source-level observation; public I/O cards; sniper host patch | pre-document hook storms; proxy-all host objects; `Function.prototype.apply` traps that break native-looking surfaces; broad page-world rewrites before a clean sample |
| `behavior-interceptor` | initiator stacks; transport wrappers; first-screen pre-document hooks when challenge installs early; dual-channel XHR/fetch proof | assuming one quiet channel means no interceptor; env-net patching before wrapper proof |
| `pure-obfuscation` | offline deob + fixed vectors | silent-value ceremony and host-surface campaigns without a host-binding proof |

If observation changes tokens or challenge outcomes, treat it as observer effect, restore a clean baseline, and re-enter via a less invasive layer (`references/hook-techniques.md`, `references/jsvmp-analysis-playbook.md` observation degrade ladder).

## Secondary family markers

Family names remain secondary. Use marker clusters only as hypotheses and corroborate with two surfaces via `references/evidence-corroboration-gate.md`.

Typical clusters, not recipes:

- Jiasule-like: cookies matching `__jsl_*`, HTTP `521` plus clearance JS
- EdgeOne / Tencent Cloud WAF-like: `probe.js` or `probev3` assets, cookie prefix families such as `w_tsfp` / `ltv2`, headers such as `x-waf-uuid`, interstitial text naming that WAF

Hard rules:

1. A URL query or path token that merely contains a family-looking substring is not corroboration.
2. The same vendor can expose two doors. A non-final status plus bootstrap or probe JS that mints a cookie is not the same gate as a hard status plus a different probe asset and an interstitial.
3. Require at least cookie-name family plus status, body, or header evidence before naming the family.

Route a mintable bootstrap face to `references/server-js-cookie-bootstrap-playbook.md`. Route a hard interstitial as its own wall, not as a failed mint.

## Common traps

- treating one cookie name or one SDK filename as class truth
- treating a URL or timeline substring such as `jsl` as Jiasule proof
- merging a vendor's mintable `202` + probe face with its hard `403` + interstitial face
- calling every large JS file `signature-bound`
- using broad Proxy hooks on `signature-bound` targets and poisoning the sample
- decompiling a VM when feed-cut already yields the final signed request
- spending days on env patches for `pure-obfuscation` targets
- using pre-inject or proxy hooks on `signature-bound` targets and calling the resulting failure "algorithm hard"

## Related references

- startup placement: `references/startup-triage-playbook.md`
- solution ladder: `references/escalation-ladder-playbook.md`
- failure naming: `references/failure-surface-taxonomy.md`
- symptom routing: `references/symptom-heuristics.md`
