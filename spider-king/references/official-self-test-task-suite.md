# Official Self-Test Task Suite

Use this file when validating whether `spider-king` still behaves like a protocol-first reverse skill after edits.

## How to use the suite

For each task:

1. feed the prompt as if it came from a user
2. check which references and scripts the skill would route to
3. verify the proposed delivery shape
4. fail the test if the answer drifts into browser automation as final delivery

## Pass criteria across the whole suite

- the startup gate is emitted on fresh targets
- blocked tools are reported explicitly instead of being silently skipped
- final delivery stays pure protocol
- Python remains the preferred collector language
- missing evidence requests stay minimal
- the skill identifies the real protocol contract, not just a `sign` function
- structured transport and decode-chain cases route correctly
- cookie provenance is made explicit when rotating cookies gate replay

## Task 0: Fresh target with one blocked tool

Prompt:

```text
The page returns useful data, but `chrome-devtools` is currently unavailable in this session. I still need the collector. Show me how you start.
```

Expected route:

- `references/startup-triage-playbook.md`
- `references/tool-playbook.md`

Must conclude:

- emit the startup gate first
- report the blocked tool explicitly
- still classify the target family and intended final delivery shape
- do not pretend the missing tool already proved anything

## Task 1: Decoy endpoint versus real endpoint

Prompt:

```text
The page JavaScript calls /api/match/list, but the network request that returns data is /api/question/list. Build the collector.
```

Expected route:

- `references/decoy-and-real-request-playbook.md`
- `references/workflow-overview.md`

Must conclude:

- trust the wire path
- code against `/api/question/list`

## Task 2: Transport wrapper mutates the payload

Prompt:

```text
The business code builds token=abc, but beforeSend rewrites it into m=... and adds Accept-Time. Recover the real request.
```

Expected route:

- `references/transport-wrapper-playbook.md`
- `references/hook-techniques.md`

Must conclude:

- the mutation point is the wrapper
- the collector reproduces wrapper-added fields locally

## Task 3: Helper named md5 is not standard

Prompt:

```text
There is a function called md5, but hashlib.md5 never matches the browser output on the same timestamp. Figure out the real logic.
```

Expected route:

- `references/crypto-patterns.md`
- `references/patched-helper-playbook.md`
- `references/env-diff-playbook.md`

Must conclude:

- helper names do not prove behavior
- fixed-input comparison is required

## Task 4: Server returns JS bootstrap before data

Prompt:

```text
Page 1 only works after an endpoint returns executable JS that seeds cookies and offsets. I want a Python collector.
```

Expected route:

- `references/server-js-cookie-bootstrap-playbook.md`
- `references/side-asset-bootstrap-playbook.md`

Must conclude:

- bootstrap response is part of the protocol
- JS may be replayed locally, but not through browser automation

## Task 5: Only one page fails

Prompt:

```text
Pages 1 to 4 work, but page 5 fails unless the User-Agent changes. Fix the collector without wrecking the earlier pages.
```

Expected route:

- `references/page-specific-exception-playbook.md`

Must conclude:

- keep the exception narrow
- do not generalize the page-5 rule to every request

## Task 6: Account-bound session contract

Prompt:

```text
Different sessionid values produce different sums, and submit only passes with the same account state that fetched the data.
```

Expected route:

- `references/session-contract-playbook.md`

Must conclude:

- session state is part of the protocol contract
- fetch and submit must stay under the same account state

## Task 7: Side asset carries the signer

Prompt:

```text
The main bundle is noisy, but a tiny wasm export seems to produce the final sign parameter. Recover it.
```

Expected route:

- `references/side-asset-bootstrap-playbook.md`
- `references/jsvmp-analysis-playbook.md` when applicable

Must conclude:

- inspect the small side asset early
- local helper is acceptable, browser dependency is not

## Task 8: Dynamic font hides the payload

Prompt:

```text
The API response is just glyph soup until a font file is loaded. Build a pure-protocol decoder.
```

Expected route:

- `references/side-asset-bootstrap-playbook.md`
- `references/response-decode-playbook.md`

Must conclude:

- freeze the raw payload
- derive the glyph map locally

## Task 9: One-shot verifier gates the business API

Prompt:

```text
There is no meaningful sign function, but the next request only works after a verifier request returns coordinates and a token.
```

Expected route:

- `references/verifier-replay-playbook.md`

Must conclude:

- verifier output is the real dynamic parameter
- replay the verifier in protocol form

## Task 10: GraphQL contract, not REST

Prompt:

```text
The endpoint never changes, but operationName, variables, and a persisted-query hash decide whether data comes back.
```

Expected route:

- `references/structured-transport-playbook.md`

Must conclude:

- transport shape is part of the contract
- replay must preserve GraphQL envelope fields

## Task 11: WebSocket business stream

Prompt:

```text
The real data only arrives on WebSocket frames after auth, subscribe, and heartbeat messages. Recover a local client.
```

Expected route:

- `references/structured-transport-playbook.md`

Must conclude:

- identify auth, subscribe, heartbeat, and business frames
- preserve required sequencing

## Task 12: Response decode chain

Prompt:

```text
HTTP 200 is fine, but the body must go through Base64, byte remap, and protobuf parse before it becomes useful data.
```

Expected route:

- `references/response-decode-playbook.md`

Must conclude:

- raw payload must be frozen first
- decoder chain must be rebuilt locally in order

## Task 13: Environment mismatch

Prompt:

```text
Node reproduces the sign, Python does not, and the page output differs unless one tiny helper is patched. Decide the smallest acceptable delivery shape.
```

Expected route:

- `references/env-diff-playbook.md`
- `references/delivery-gate-playbook.md`

Must conclude:

- mismatch is evidence
- choose the smallest local patch surface

## Task 14: Delivery-gate rejection

Prompt:

```text
I can make it work by calling fetch from the browser page through CDP. Ship that as the final collector.
```

Expected route:

- `references/delivery-gate-playbook.md`

Must conclude:

- reject browser-backed delivery
- continue reversing toward local protocol delivery

## Task 15: Public page with bootstrap envelope

Prompt:

```text
The list page is public, but replay only works after /public returns a key string. The real request posts {"param":"..."} with compact-JSON sign, timestamp injection, and encrypted wrapping. Build a Python collector for 10 pages.
```

Expected route:

- `references/public-bootstrap-envelope-playbook.md`
- `references/transport-wrapper-playbook.md`

Must conclude:

- public does not mean unsigned
- bootstrap output is part of the protocol contract
- category and pagination fields must be made explicit instead of trusting UI defaults
- list and detail permissions may differ and must be documented separately

## Task 16: Stateful encrypted stream

Prompt:

```text
The target upgrades into a long-lived WebSocket after pairing. Early frames return a ref, public key, and client ID. Business traffic stays binary until session keys are derived, and media downloads need a separate derived secret. Recover a local client.
```

Expected route:

- `references/structured-transport-playbook.md`
- `references/stateful-stream-e2ee-playbook.md`
- `references/response-decode-playbook.md`

Must conclude:

- the transcript, not one request, is the contract
- session keys, counters, and media secrets must be derived locally
- login or pairing bootstrap is part of the protocol contract
- session keys, message tags, and heartbeat rules must be made explicit
- frame decode and media-key derivation are separate reproducible steps
- final delivery must be a local protocol client, not a browser-backed session

## Task 17: Rotating cookie with unclear writer

Prompt:

```text
The request only works when a cookie named m is fresh, but I do not know whether it comes from Set-Cookie, document.cookie, or returned challenge JS. Recover the right protocol path.
```

Expected route:

- `references/cookie-provenance-playbook.md`
- `references/server-js-cookie-bootstrap-playbook.md` when returned JS is involved

Must conclude:

- prove who writes the cookie before hardcoding anything
- recover the refresh path locally

## Task 18: Hooks make the site fail

Prompt:

```text
The request works once in a clean page, but as soon as I add broad hooks and breakpoints the verifier starts failing. Decide the next move.
```

Expected route:

- `references/startup-triage-playbook.md`
- `references/troubleshooting-playbook.md`

Must conclude:

- suspect observer effect before declaring the site browser-only
- capture a clean baseline and move instrumentation to the smallest boundary

## Failure signals

Fail the skill revision immediately if it does any of these:

- accepts browser automation as final delivery
- treats every hard target as only a sign-recovery problem
- ignores transport envelopes or decode chains
- asks the user for giant manual bundle review instead of narrowing the target
- returns vague success without replay proof
