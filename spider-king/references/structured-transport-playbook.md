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
- preserve ordering when the server expects a warm-up sequence

## Binary envelope notes

- freeze raw bytes
- identify field boundaries or parser functions
- confirm whether compression happens before structured decode

## Acceptable handoff

The final collector must still be local protocol code:

- HTTP plus GraphQL body
- WebSocket client plus local frame builder or parser
- Python plus local protobuf or msgpack decoder
