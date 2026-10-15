# Environment-Diff Playbook

Use this reference when:

- the target redirects to a different domain or a wrapper page
- browser output and local output disagree on the same fixed input
- Node or Python differs from the live page even after obvious patches
- the request looks correct, but server acceptance or local decode still fails

## Contents

- [Core rule](#core-rule)
- [Single baseline purity](#single-baseline-purity)
- [1. Redirect and wrapper-page triage](#1-redirect-and-wrapper-page-triage)
- [2. Separate four layers](#2-separate-four-layers)
- [3. Standard-vs-patched workflow](#3-standard-vs-patched-workflow)
- [4. Narrowing strategy](#4-narrowing-strategy)
- [4A. Page-world replica versus local DOM host](#4a-page-world-replica-versus-local-dom-host)
- [4B. Host-fidelity L0-L4](#4b-host-fidelity-l0-l4)
- [5. Preferred delivery shapes](#5-preferred-delivery-shapes)
- [6. Network sanity checks](#6-network-sanity-checks)
- [7. Verification checklist](#7-verification-checklist)

## Core rule

Environment mismatch is evidence, not a reason to surrender to automation.

## Single baseline purity

Bind one `baseline_id` for a replay chain. Do not mix the following from different captures into one chain:

- UA / Client-Hints / navigator identity
- cookies, storage, and bootstrap artifacts
- screen, locale, timezone, and language
- TLS / HTTP profile and proxy exit
- canvas, WebGL, audio, font, or other fingerprint surfaces

Foreign samples may be diagnostic controls only. If two sources conflict, keep one baseline, label the other as contrast evidence, and restart the chain rather than splicing "best fields" together.

Sensor-like or signer-like payloads that embed client identity must stay generation-matched to the same baseline as the transport and headers.

## 1. Redirect and wrapper-page triage

Before reversing any signer, confirm whether the landing page is a wrapper:

1. record the full redirect chain
2. compare the initial page, final page, and real network request
3. check whether the final page rewrites:
   - request paths
   - headers
   - body fields
   - cookies
4. treat compatibility or migration pages as wrappers, not as canonical business logic

## 2. Separate four layers

Always separate:

1. transport wrapper logic
2. core signer or encoder logic
3. response decoder logic
4. server acceptance conditions

Do not assume a correct hash proves the whole protocol.

## 3. Standard-vs-patched workflow

When a helper looks like MD5, SHA, AES, HMAC, or Base64 but behaves strangely:

1. capture a browser output on fixed inputs
2. run the same helper locally on the same fixed inputs
3. compare:
   - final output
   - input normalization
   - byte conversion
   - intermediate values
4. inspect subordinate helpers, not just the top-level function

Strong signs of a patched helper:

- standard libraries consistently disagree
- intermediate buffers diverge before the final round
- side helpers perform custom masking, swapping, or alphabet translation

## 4. Narrowing strategy

Reduce the problem in layers:

1. live page in browser
2. isolated page helper plus direct dependencies
3. local runtime with the smallest possible environment patch
4. pure Python reimplementation if practical

At every layer, test the same fixed input and preserve the same intermediate values.

Prefer sniper evidence of actually-read host surfaces over net-wide attribute dumps when choosing what to patch (`references/environment-patch-playbook.md`). Keep one pure baseline; do not splice UA, cookies, fingerprint, and transport from different machines.

Goal:

- find the smallest local environment that still reproduces the live output

## 4A. Page-world replica versus local DOM host

A JavaScript host replica that matches **inside Chrome** (page `eval`, iframe, `srcdoc`) is a different environment from jsdom or Node.

- jsdom `url: "about:srcdoc"` throws `DOMException`. Keep an `https` document URL plus `<base href>`. The Chrome oracle iframe href may still be `about:srcdoc`
- wrapping `TextEncoder.encode` is observer-toxic; `encode.length === 0` is a real contract. A `Proxy` on `Uint8Array` makes `ArrayBuffer.isView` false
- wrapping `Number.prototype.toString` is observer-toxic for some mixers even when FTS only hits `Object` / `setInterval`. Do not treat "oracle-safe in one earlier run" as a standing license
- freeze same-world HTML + inline script + server clock before a live POST. Stale-tab script plus fresh HTML constants is not protocol disproof
- if the local mix still diverges after a Chrome replica hits the oracle, sniper the next heat surface; do not keep stacking the replica that already worked in Chrome. See `references/environment-patch-playbook.md`

## 4B. Host-fidelity L0-L4

Score local-versus-browser host fidelity as a ladder. This is not verifier smoke L1-L4 and not device-trust L0-L3.

| Level | Question | Pass hint |
|---|---|---|
| L0 count | native nondeterministic sources fire in the same order of magnitude | `Math.random` / `Date.now` / native `eval` counts |
| L1 sequence | key API order matches after noise filter | LCS of the native API sequence |
| L2 value feed | local host consumes the browser's recorded values | byte-stable deterministic intermediates |
| L3 protocol | submitted param-name set matches the browser request | missing/extra fields are fidelity bugs |
| L4 eval sha256 | dynamic compile-body hashes appear in the same order | SDK decrypt path, not third-party scripts |

Canvas, `navigator`, and other **JS shims cannot be probe-counted as L0**. Native probes do not see them. Feed shim values from the same session, or hardcode proved scalars; do not report shim call counts as engine fidelity.

## 5. Preferred delivery shapes

Choose the smallest acceptable handoff:

### A. Pure Python

Use when the logic is fully understood and easy to port.

### B. Python plus isolated JS helper

Use when:

- the HTTP client should stay in Python
- the exact helper is already stable in JS
- porting today would add more risk than value

### C. Python plus tiny local patch surface

Use when:

- one helper still needs a small patched runtime
- the runtime is local, explicit, and does not depend on a browser session
- all inputs and outputs are fixed-sample verifiable

Never accept:

- browser-backed replay as final delivery
- page-context `fetch` as the collector
- hidden profile state as part of the protocol

## 6. Network sanity checks

Before blaming the signer, compare:

1. URL, method, and serialized body
2. headers and cookies
3. proxy inheritance
4. origin and referer
5. response content type and raw body
6. decode path if the payload shape looks right but the parsed data is wrong
7. whether HTML, inline script, and server clock come from one world



## 6A. Host-local fingerprint cache

Foreign fingerprint or environment caches are contrast only.

- resample host-local fingerprint surfaces on the execution host
- do not splice UA, Client-Hints, canvas/WebGL, screen, and TLS from different machines into one live chain
- keep the protocol profile identity in `references/parameter-ownership-playbook.md` aligned with the execution host claim

## 7. Verification checklist

Call the environment mismatch resolved only after:

1. the smallest local runtime reproduces the live helper output on fixed inputs
2. the final request succeeds at least twice
3. any decode step reproduces the live result on a captured raw payload
4. the final collector runs without browser automation
5. the remaining local patch surface is explicitly documented
