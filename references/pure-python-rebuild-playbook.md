# Pure Python Rebuild Playbook

Use this method when the browser or wire output is already bound to fixed inputs and the goal is to remove JS runtime dependencies. It is not a site-specific profile. A target-specific implementation such as a Douyin `a_bogus` port is only one example of the method.

## Entry Conditions

All conditions must be true before skipping fresh target discovery:

1. The entry, invocation contract, input material, and expected output are known.
2. The relevant version, field layout, or response schema is proven by trace evidence.
3. The user wants pure Python maintenance, primitive regression, request glue, or a deterministic port.
4. The remaining work can be checked with fixed fixtures before live replay.

If the entry, script URL, version, call chain, session bootstrap, transport wrapper, response decoder, or pagination state is still unknown, return to the Spider core loop or hand entry/call-chain discovery to a dedicated reverse skill when available (for example `camoufox-js-reverse`); otherwise continue with `chrome-devtools` / `js-reverse` evidence surfaces.

## Rebuild Loop

1. Freeze fixture A: URL/query/body, headers that enter the algorithm, UA, timestamp, random bytes, server-issued state, and expected output.
2. Decide whether an independent fixture B is required. Require it whenever time, randomness, session state, environment, field ordering, or request serialization can change the result. For a textbook primitive, use one published known-answer vector plus one captured fixture instead.
3. Capture fixture B from an independent run and change at least one decisive input. A copied fixture with only its expected output edited is not independent evidence.
4. Split moving fields into server-issued, request-derived, session-bound, random, time-derived, and locally computed values.
5. Port the smallest primitive first: digest, alphabet, stream transform, packer, key schedule, field builder, or response decoder.
6. Compare against fixture A after each primitive. Save the first divergent byte, field, or branch before changing the next unit. For multi-stage join/time/nonce/key/digest mismatches, use `references/signer-parity-chain-playbook.md`.
7. Before restoring live fields, pass fixture B or the published-vector-plus-capture pair without target-specific branching in the implementation.
8. Only after both parity checks, restore the random and time paths and check shape, length, alphabet, URL roundtrip, or binary envelope invariants.
9. Attach request glue last. Use one coherent `requests.Session` and rebuild request-derived values for every call.

## Rules

1. Treat load success as irrelevant unless the fixed output matches.
2. Keep fingerprints and environmental values as explicit inputs, not hidden browser dependencies.
3. Do not reuse constants, field order, or alphabets across versions without evidence.
4. Do not claim a primitive template is a full generator.
5. Do not add Node, jsdom, iv8, Playwright, Selenium, CDP, or page-context execution to the final dependency path.
6. Final request glue must expose a PyCharm right-click runnable Python entrypoint with no required CLI arguments. Command-line wrappers are optional verification tools, not the delivery interface.
7. Keep target-specific vectors under the task workspace or `references/examples/`; they illustrate the method but do not define Spider ownership.

## Verification Gates

All relevant checks must pass:

1. Fixture A output matches byte-for-byte.
2. Fixture B also matches when dynamic or contextual inputs exist; otherwise one published primitive vector and one captured fixture both pass.
3. Primitive vectors pass independently from the full generator.
4. Serialization and URL/binary roundtrip preserve the final artifact losslessly.
5. Randomized smoke checks preserve shape without replacing fixed-vector parity.
6. Live replay succeeds repeatedly on one coherent session when live replay is approved.
7. The final files import no browser automation or JS runtime unless the task explicitly accepted a narrow local helper.
8. `main.py` or the declared entry file runs from PyCharm defaults without mandatory terminal arguments.

## Failure Modes

| Trigger | Action | Fallback |
|---|---|---|
| Version or field layout unconfirmed | Stop reusing constants | Return to core evidence collection |
| Entry or call chain unknown | Do not start porting | Use a call-chain reverse skill when available; otherwise capture initiator stacks with `js-reverse` / Chrome |
| Primitive passes but full output fails | Compare first divergent field | Do not live replay |
| Shape is valid but server rejects | Check session, cookies, UA, timing, and transport admission | Do not add a browser fallback |
| JS lifecycle proves necessary | Record the failed Python proof | Escalate one rung to a narrow helper, not browser automation |

## Example Fixtures

`references/examples/douyin-bdms-pure/` contains primitive vectors and notes from one fixed-trace-style pure Python signer maintenance case. Use it as an example of fixture discipline and negative boundaries, not as a route selector or complete from-zero specification.
