# JSVMP Interceptor Contract

Use this reference when a supplied JSVMP or SDK loads in Node/VM but the expected request mutation is missing, path-dependent, or transport-dependent. Loading is not activation.

## Contract Card

Record before environment widening:

- target script path, SHA-256, version/build marker, browser sample provenance, and the Fixed Vector Capsule from `verification-and-replay.md`
- entry type: public signer, XHR interceptor, fetch interceptor, dual transport, or response/warm-up writer
- `init`/`setup` call, exact config, path whitelist or matcher, feature switches, and call timing
- reference owners captured at SDK load time: `XMLHttpRequest`, `fetch`, URL helpers, header setters, body serializer, worker, or message bridge
- final mutation slots: query, header, body, cookie/storage, response-derived state, and their ordering
- positive trigger: one registered business-shaped method/path/header/body tuple
- negative trigger: one deliberately unregistered sibling path with all other inputs held constant

Do not infer any missing contract field from a non-empty or correctly shaped sign.

## Required Load Order

Start from reference ownership, then verify with controlled reorder tests:

```text
env modules
-> fake XHR/fetch
-> target SDK
-> capture hook
-> init(config)
-> trigger business-shaped request
-> capture final URL/header/body
```

- A transport the SDK snapshots at load time must exist before the SDK.
- A capture surface the SDK may replace or polyfill usually belongs after the SDK.
- `init` must precede the request when it registers matchers or switches.
- Use standard transport calls; do not bypass `open`, header, serialization, or send steps that the SDK owns.

## Activation Matrix

Test channels independently:

| Channel | Positive proof | Negative control |
|---|---|---|
| Public signer | a complete frozen capsule returns the exact expected value | one controlled capsule field changes the value or branch as expected |
| XHR | registered request mutates the final wire slot | unregistered path stays unchanged |
| fetch | registered request mutates the final wire slot | sibling transport/path remains unchanged |
| Dual slot | query/header/body values appear in the proved order | removing required init or config keeps both absent |
| Response/warm-up | proved response writes state used by the next request | skipping warm-up fails at that state edge |

Silence on XHR does not clear fetch, workers, wrappers, or sibling transports. An internal return value is secondary evidence; the wire-shaped URL, headers, and body are authoritative.

Silence on the observation Chrome can also come from `navigator.webdriver === true`. Prove that one-variable control, and do not treat HTML placeholder zeros as activation, before widening the local environment.

## Stop And Exit

Stop patching and return upstream when any holds:

- `init`/matcher/config evidence is incomplete
- two consecutive rounds do not move the first divergence
- only output shape improves while the fixed vector still differs
- Node/VM cannot express the observed host or lifecycle semantics honestly

If activation passes but fixed vectors fail, first confirm that time, entropy, counters, session/round state, canonical bytes, and profile identity came from the same capsule; then use `no-touch-and-profile-coherence.md` before adding any API. If fixed vectors pass but live replay fails, leave env-patch and inspect session, canonicalization, transport, and downstream acceptance in the Spider core loop.
