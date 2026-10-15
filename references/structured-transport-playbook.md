# Structured Transport Playbook

Use this reference when:

- the target uses GraphQL instead of plain REST
- the business contract lives in WebSocket frames
- the body or frame payload is protobuf, msgpack, or another binary envelope
- message IDs, operation names, channels, or opcodes matter as much as the visible business fields

## Core rule

Transport shape is part of the protocol contract.

## Working method

1. identify the transport kind:
   - GraphQL query or mutation
   - WebSocket request-response
   - WebSocket stream
   - protobuf or msgpack over HTTP
   - custom binary envelope
2. freeze one known-good request or frame sample
3. separate:
   - envelope fields
   - business fields
   - sequencing fields
   - signature or token fields
4. determine what the server assigns versus what the client must rebuild
5. replay one stable sample locally before scaling to streams or pagination

## GraphQL notes

- compare `operationName`, `variables`, and persisted-query hashes
- watch for wrapper headers or origin checks
- confirm whether the query text, hash, or both are required

## WebSocket notes

- fingerprint message types before reading individual frames
- identify auth frames, subscribe frames, heartbeat frames, and business frames
- classify inbound text before JSON parse; a short constant prefix, ack, or heartbeat is not the business object
- skip non-object text and keep reading until the business JSON object
- one recv after send that lands on the prefix is not proof the socket cannot multiplex
- do not sum a constant prefix frame and do not treat JSON.parse failure of that frame as a missing signer
- preserve ordering when the server expects a warm-up sequence
- freeze handshake header class separately from token bytes
- impersonate default document headers include `Sec-Fetch-Mode: navigate`; do not copy them onto a WebSocket handshake
- ablate handshake header class on the same admitted token bytes before restarting the signer
- a close after the first business text is reject; an empty open is not accept

## Binary envelope notes

- freeze raw bytes as hex or ArrayBuffer at the serializer or XHR send, not as a UTF-8 MCP or DevTools dump
- identify field boundaries or parser functions
- confirm whether compression happens before structured decode
- `U+FFFD` in a saved body means the dump corrupted binary; recapture hex
- regenerate clock-bucket protobuf fields through the public encoder; a second int32 may be client-chosen if the token remains `encode(t1,t2)` and `t1` is fresh
- stale captured clock-bucket plus token pairs 403 even when the schema is right

## gRPC and grpc-web framing

Treat each message frame as a wire contract:

1. byte 0 is the frame flag
2. bytes 1 through 4 are an unsigned big-endian payload length
3. the next `length` bytes are exactly one message payload
4. repeat until the body or stream is exhausted

Do not treat every nonzero flag as `zlib`. Resolve `grpc-encoding` or the active grpc-web contract from headers and runtime evidence. For grpc-web, distinguish data frames from trailer frames, preserve the transport encoding (`application/grpc-web+proto` versus text/Base64), and parse every frame rather than only the first payload.

Verification gates:

- reject truncated five-byte headers and payload lengths beyond the available bytes
- prove single-frame and multi-frame parsing with fixed bytes
- retain unknown protobuf fields or raw payload bytes when the schema is incomplete
- compare decoded messages and re-encoded frame bytes separately
- use a negative control with a tampered length, flag, or trailer boundary
- do not call HTTP `200` or `grpc-status: 0` sufficient until the intended business message is decoded and consumed

Use `scripts/grpc_frame_inspector.py` for a bounded structural check. By default it emits only flags, kind, length, and offset; it does not print payload bytes, choose a compression codec, or decode protobuf fields. Payload SHA-256 is disabled by default. Enable `--include-payload-sha256` only for task-local correlation, because stable hashes of sensitive payloads are unsafe to publish.

If compression, encryption, or signing wraps the protobuf payload, record the exact order. A common shape is frame parse -> decompress -> protobuf, but captured bytes and the active parser remain authoritative.

## Acceptable handoff

The final collector must still be local protocol code:

- HTTP plus GraphQL body
- WebSocket client plus local frame builder or parser
- Python plus local protobuf or msgpack decoder
