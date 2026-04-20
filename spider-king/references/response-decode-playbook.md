# Response Decode Playbook

Use this reference when:

- the response returns `200` but the body is unreadable
- useful data appears only after a decode helper, glyph map, protobuf parser, or decompressor
- raw payload, parsed payload, and final business data are clearly different stages

## Core rule

Freeze the raw payload before touching the decoder.

## Recognition signals

- long numeric strings, glyphs, escaped Unicode, or binary-looking bytes
- a response handler calls helper chains before touching business fields
- the network body is stable, but the visible data depends on a local decode step
- content type and actual payload shape do not match

## Working method

1. save the exact raw payload
2. identify the first consumer of that raw payload
3. trace the decode chain in order:
   - decompression
   - Base64 or alphabet conversion
   - byte or char remapping
   - protobuf, msgpack, or JSON parse
   - font or glyph translation
4. rebuild each layer locally
5. verify the final local decode on the captured payload before scaling

## Common traps

- trying to decode after a browser mutation instead of from the raw payload
- skipping intermediate helpers and jumping to the last parser
- assuming the response is encrypted when it is only remapped or compressed
- validating only on one lucky payload

## Acceptable handoff

- local Python decoder when practical
- Python plus tiny local helper when the decoder is exact but not yet worth porting

Do not accept a solution that needs browser rendering or page context just to read the payload.
