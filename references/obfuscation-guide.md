# Obfuscation Guide

Use this file when the page ships packed, flattened, or string-table-heavy JavaScript.

## Recognition signals

- giant string arrays
- `eval`, `Function`, or self-redefining wrappers
- control-flow flattening
- numeric array dispatch
- tiny side assets controlling the real logic
- rotate-then-decode string tables common to obfuscator.io-style bundles
- member-map objects such as `{a:0x2aa,b:0x2ad}` feeding decoder calls
- huge webpack, chart, painter, or SVG bundles that hide a tiny module owning the list URL
- large integer arrays that reconstruct a function via `eval` / `setInterval`

## Working order

1. search for the real API path first
2. search for transport wrappers before unpacking everything
3. extract only the smallest logic slice needed for the current request
4. save a clean snapshot before each major edit
5. move offline early when anti-debug noise is high
6. extract the tiny module that owns the list URL; chart, painter, and SVG modules are decoys
7. stub hasher-internal `eval` / `setInterval`; do not execute a function rebuilt from charcodes

## String-table heavy bundles

When the bundle looks like a string array plus decoder plus rotate IIFE:

1. save the raw source bytes first
2. extract the string-array function, decoder function, and rotate IIFE with brace matching rather than brittle line slices
3. execute only that decoder surface in a local Node or equivalent harness to dump the string table
4. if decoder eval never returns, look for an integrity prototype that pushes onto its state array until length grows forever; skip that call and keep the decode function plus the rotate IIFE
5. rewrite call sites in two passes:
   - first expand member-map objects so `decoder(map.a)` becomes `decoder(0x2aa)`
   - then replace `decoder(0xNNN)` and aliased decoder names with the dumped string literals
6. strip the `0x` prefix when matching hex keys if the dump table is keyed by plain hex text
7. beautify only after the first useful rewrite pass, or immediately when the file is one giant line and line numbers are useless
8. resume protocol search on the readable slice; do not spend time cleaning dead branches once the signer input is recoverable

If the first rewrite pass changes nothing, assume the member-map pass or hex-key normalization is wrong before inventing a new deobfuscator.

## Rotating per-fetch bundles

When the same script URL re-obfuscates on every GET:

1. extract the public function by structural anchors such as `function name(`, a trailing IIFE, or an assignment terminator
2. do not freeze identifier maps or vendor one captured source as the live signer
3. download a fresh copy into a tiny local vm when that public function already mints accepted tokens
4. inner Huffman, XOR, or ident-renamed ports are later work, not the first helper
5. write slot can rotate between cookie and an in-memory global; read both after each fresh eval
6. do not send the previous locally-minted cookie on the next GET of the rotating script

Cut before a trailing IIFE or pager assignment unless the public function depends on it.

## Common traps

- beautifying the whole bundle before finding the real request, except when a one-line file makes search unusable
- ignoring inline scripts and side assets
- losing original variable names that are useful for diffing
- replacing only hex literals and missing `decoder(map.key)` forms
- treating dump keys like `"c7"` as non-matches for source tokens like `0xc7`
- reading comma-expression returns as void when the real value is the right-hand call
- treating a decoder integrity infinite loop as proof the string table cannot be dumped
- freezing identifier maps from one snapshot of a per-fetch obfuscated bundle
- vendoring rotating source as the collector signer
- riding a leftover mint cookie into the next GET of a rotating bootstrap script
- treating the first large integer array as round constants when it is charcodes of a function
- executing that reconstructed function to "see what it does"
- reversing the chart/painter bundle because it is the largest file

## Delivery rule

Only deobfuscate as much as the protocol replay requires.
