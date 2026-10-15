# Signer Parity Chain Playbook

Use this file when a local signer or encoder almost matches the browser but live acceptance still fails, or fixed-input outputs diverge.

The goal is to locate the **first divergent transform stage** before rewriting large code blocks.

## Contents

- [Core rule](#core-rule)
- [Seven-stage chain](#seven-stage-chain)
- [Ordered request-failure ladder](#ordered-request-failure-ladder)
- [Fast localization tactics](#fast-localization-tactics)
- [Acceptance rules](#acceptance-rules)
- [Related references](#related-references)

## Core rule

Compare browser truth and local truth stage by stage on the **same frozen inputs**.

- change one stage hypothesis at a time
- stop at the first mismatch
- do not jump to TLS, env patch, or full re-reverse while an earlier stage still diverges
- wire egress remains authoritative over intermediate getters

For local-versus-success ablation after sample hygiene, also use `references/positive-sample-ablation-playbook.md`.

## Seven-stage chain

Compare these stages in order. Record expected vs actual at each stage.

### 1. Raw business inputs

- parameter names, case, underscore style
- hidden empty fields that still enter the signer
- path, method, and which slots are in-scope

### 2. Normalization and concatenation

- sort order (lexicographic, stable insert order, custom)
- separators and whether keys are included
- empty-value inclusion
- URL encoding before vs after join
- charset (UTF-8 vs other) for non-ASCII

### 3. Time fields

- second vs millisecond precision
- string vs number type
- timezone assumptions
- whether sign-time and send-time must be identical

### 4. Nonce / random fields

- length and alphabet
- generator source and whether it is frozen in fixtures
- whether the same nonce is reused across nested digests

### 5. Keys, salts, IVs

- literal key bytes vs derived key
- hex/utf8/base64 decoding of key material
- IV/salt presence and mutability
- constant-pool or WASM data-segment strings as prefix/suffix candidates
- unsalted textbook miss is not yet patched-compress proof

### 6. Intermediate digests / transforms

- multi-round hash intermediate hex
- custom uint32 ops, table lookups, packing
- order of compress / encode / encrypt steps
- two-stage mix: first mix can be a clock-independent placeholder (often unpadded hex); second mix can be host-bound on that hex as ASCII (often padded); output length tracks `2 * first_hex.length`

### 7. Final encoding and slot placement

- hex case, base64 vs url-safe base64, custom alphabet
- truncation, prefixes, multi-field splits
- final query/header/body/cookie slot and serialization

Minimum log shape:

```text
parityStage: 1-7 name
inputFingerprint: short hash or length
browserValueFingerprint: short hash
localValueFingerprint: short hash
firstDivergence: stage name + field
```

Never paste raw secrets into chat or skill files.

## Ordered request-failure ladder

When live replay fails and the failing layer is unclear, walk this order **before** large signer rewrites. Map the stop point onto `references/failure-surface-taxonomy.md`.

1. **Session / cookie freshness** — jar vs outbound `Cookie`, expiry, missing HttpOnly slots (`session-chain`)
2. **Bootstrap / warmup omission** — prior init/token/config requests on the same chain (`session-chain` / `request-contract`)
3. **Timestamp / nonce contract** — precision, reuse, skew window (`request-contract` / `signer-confidence`)
4. **Header and body contract** — Content-Type, Origin/Referer, Client-Hints, exact serialization (`request-contract`)
5. **Environment-bound inputs** — only after proving those values enter the signer or verifier (`signer-confidence` / `verifier-sidecar`)
6. **Pacing / rate / egress** — 429, punitive disguise, exit-only flips (`egress-environment`)

Silent reject pattern: HTTP `200` with empty business body, wrong content-type, or stable business error code is **not** success. Classify under `business-oracle` or the earlier surface that still explains it; see soft-success traps in `references/failure-surface-taxonomy.md`.

## Fast localization tactics

1. **Binary search stages** — if stage 3 matches and stage 6 fails, inspect 4-5 next, not stage 1.
2. **Fixed-input fixtures** — freeze time/nonce/key material; never debug parity on live jitter alone.
3. **Print the pre-digest string** — most "crypto bugs" are join/encoding bugs.
4. **Boundary capture** — initiator stacks, narrow hooks, or silent-value cards at the mutation boundary beat broad dumps.
5. **Slot check last-mile** — correct blob in the wrong header/query slot is still `request-contract`.
6. **Reverse-trace from exit value** — search logs for the first appearance of the known final artifact, then walk producers backward (`references/jsvmp-analysis-playbook.md`).

Use `scripts/transform_trace_diff.py` and `scripts/transcript_diff.py` when staged traces exist.

## Acceptance rules

Call signer parity good only when:

1. stages 1-7 match on at least one frozen fixture
2. an independent second fixture matches when time/nonce/session can move outputs
3. final wire slot placement matches the accepted business request
4. live acceptance, if claimed, repeats on a fresh generation without browser runtime

If only stage 7 matches by accident while earlier stages were not compared, keep the claim provisional.

## Related references

- rebuild loop: `references/pure-python-rebuild-playbook.md`
- crypto pitfalls: `references/crypto-patterns.md`
- troubleshooting symptoms: `references/troubleshooting-playbook.md`
- first-divergence packaging: `references/reproducible-evidence-playbook.md`
- ablation: `references/positive-sample-ablation-playbook.md`
