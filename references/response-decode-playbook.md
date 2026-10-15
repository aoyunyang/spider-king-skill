# Response Decode Playbook

Use this reference when:

- the response returns `200` but the body is unreadable
- useful data appears only after a decode helper, glyph map, protobuf parser, or decompressor
- raw payload, parsed payload, and final business data are clearly different stages
- the JSON is readable, but business values are HTML of stacked images or spans with extra CSS classes and `left` / `background-position` offsets

## Contents

- [Core rule](#core-rule)
- [Recognition signals](#recognition-signals)
- [Working method](#working-method)
- [CSS-in-HTML sprite and offset glyphs](#css-in-html-sprite-and-offset-glyphs)
- [JSON numeric strings with CR or LF](#json-numeric-strings-with-cr-or-lf)
- [Common traps](#common-traps)
- [Acceptable handoff](#acceptable-handoff)

## Core rule

Freeze the raw payload before touching the decoder.

## Recognition signals

- long numeric strings, glyphs, escaped Unicode, or binary-looking bytes
- a response handler calls helper chains before touching business fields
- the network body is stable, but the visible data depends on a local decode step
- content type and actual payload shape do not match
- list or detail JSON is schema-valid, yet each row is HTML of stacked `img` / `span` / `i` nodes rather than a plain number
- companion fields such as `key`, `value`, or `IV` sit next to that HTML and a page script derives a hide class from them
- schema-valid JSON numeric strings fail `int()` or the sum drifts because of CR/LF

## Working method

1. save the exact raw payload
2. identify the first consumer of that raw payload
3. trace the decode chain in order:
   - decompression
   - Base64 or alphabet conversion
   - byte or char remapping
   - protobuf, msgpack, or JSON parse
   - font or glyph translation
   - CSS hide-class, in-flow offset placement, and image-byte identity
4. rebuild each layer locally
5. verify the final local decode on the captured payload before scaling

## CSS-in-HTML sprite and offset glyphs

Use this when the hardness is response rendering, not a request signer.

Recognition:

- the list POST or GET body is only a page index or id; no sign field appears on the wire
- each cell stacks digit or glyph images with extra classes and a CSS `left` or `background-position`
- a page helper computes one extra class from companion JSON fields and hides those nodes

Rules:

1. Freeze the raw HTML plus companion fields before mutating.
2. Hide token: an extra class may be derived from companion fields by a short named primitive chain. Prove that chain on a fixed vector. A common family is `digest(btoa(concat) with '=' stripped)`, but do not assume that exact recipe. Negative control: keeping hidden glyphs, or hiding the wrong class, must change the integer.
3. Drop hidden nodes first. Then the visual x of remaining nodes is `inFlowWidth * visibleIndex + leftOffset`, or the CSS equivalent. Source order is not visual order.
4. Glyph identity is a hash of decoded image bytes or normalized pixels, not CSS class names. Class names can be hide tokens or decoys. Remap only when sprite bytes rotate.
5. Tag the family `decode-gated`. Do not invent a signer because the HTML looks obfuscated.
6. After decode, HTTP `200` with schema-valid JSON whose values are one repeated sentinel remains punish, not grant.

Fixed-vector self-check before pagination:

- hide-class on a known companion-field pair
- one cell where DOM order and visual order differ
- unknown image hash fails closed instead of guessing a digit

This is a local Python decode. Do not OCR the sprites in the collector, and do not keep a browser just to read `getComputedStyle`.

## JSON numeric strings with CR or LF

Use this when the JSON is schema-valid but integer parse fails or sums drift.

Recognition:

- numeric string fields look like digits but carry `\r` or `\n`
- `int(value)` raises, or the sum changes after stripping control characters

Rules:

1. Freeze the raw JSON.
2. Strip CR/LF and surrounding whitespace before `int` or sum. Do not treat parse failure as a new cipher.
3. Do not drop or dedupe rows because a CR made two strings look different.
4. HTTP 200 with one repeated sentinel after strip remains punish, not grant.

Fixed-vector self-check: `"12\r"` and `" 34\n"` decode to 12 and 34.

## Common traps

- trying to decode after a browser mutation instead of from the raw payload
- skipping intermediate helpers and jumping to the last parser
- assuming the response is encrypted when it is only remapped, offset-placed, or compressed
- validating only on one lucky payload
- OCRing stacked digit images, or hunting a request signer, because the HTML looks hostile
- sorting by source order instead of in-flow visual x after hidden nodes are dropped
- treating CSS class names as glyph identity when the class is the hide token
- calling HTTP `200` plus schema-valid HTML a grant while every decoded value is the unsigned filler sentinel
- treating `int()` failure on a numeric JSON string as encryption instead of stripping CR/LF

## Acceptable handoff

- local Python decoder when practical
- Python plus tiny local helper when the decoder is exact but not yet worth porting

Do not accept a solution that needs browser rendering or page context just to read the payload.
