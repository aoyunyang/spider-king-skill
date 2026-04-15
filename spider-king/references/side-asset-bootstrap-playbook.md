# Side Asset Bootstrap Playbook

Use this reference when:

- a tiny side script, `.wasm`, font file, or challenge JS changes request behavior
- the main bundle is noisy but a small asset controls the real signer or decoder
- the first response returns executable JS, offsets, or assets needed by the next request

## Core rule

Small side assets often carry the whole secret.

## Asset classes to inspect early

- `.wasm` signers
- side scripts such as `/offset`
- server-returned JS bootstrap payloads
- dynamic fonts or glyph maps
- responses that set cookies and return executable code in the same step

## Working method

1. identify which asset changes the next request's state
2. execute or emulate that asset locally
3. carry the resulting cookies, globals, keys, or mappings into the next request
4. keep the asset step as a local helper, not a browser dependency

## Common traps

- over-reversing the main bundle while ignoring a tiny side asset
- treating bootstrap JS as noise
- rendering fonts in a browser instead of decoding them locally

## Delivery rule

If the side asset is part of the protocol contract, keep it in the collector as a local helper or decoder.
