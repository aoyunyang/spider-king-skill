# Environment-Diff Playbook

Use this reference when:

- the target redirects to a different domain or a wrapper page
- browser output and local output disagree on the same fixed input
- Node or Python differs from the live page even after obvious patches
- the request looks correct, but server acceptance or local decode still fails

## Core rule

Environment mismatch is evidence, not a reason to surrender to automation.

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

Goal:

- find the smallest local environment that still reproduces the live output

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

## 7. Verification checklist

Call the environment mismatch resolved only after:

1. the smallest local runtime reproduces the live helper output on fixed inputs
2. the final request succeeds at least twice
3. any decode step reproduces the live result on a captured raw payload
4. the final collector runs without browser automation
5. the remaining local patch surface is explicitly documented
