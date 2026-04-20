# Stateful Stream E2EE Playbook

Use this reference when:

- the target only becomes useful after login, pairing, QR scan, or another warm-up handshake
- the real business contract lives on a long-lived WebSocket or another stateful stream
- early frames return refs, public keys, client IDs, challenge blobs, or session seeds instead of business data
- later frames are binary, protobuf, or otherwise unreadable until keys, counters, or tags are recovered
- media metadata is easy to see, but media replay or decryption needs a separately derived secret

## Core rule

Stateful session setup is part of the protocol contract.

Do not reduce this class of target to one fake "sign" field.

## Distilled lessons

1. Freeze the session bootstrap, not just the payload.
   Capture the entry route, stream URL, upgrade headers, login or pairing frames, auth ack, heartbeat, and one business frame as a single transcript.

2. Split frame families before parsing payload semantics.
   Group frames into bootstrap, auth, keepalive, business, receipt, reconnect, and media-related buckets first.

3. Recover the key schedule before blaming decode.
   When business frames stay opaque, confirm whether the problem is key derivation, counter drift, tag ordering, compression, protobuf, or a real parser bug.

4. Treat counters and tags as first-class state.
   Message IDs, epochs, counters, and ack tags are not optional noise if the stream dies without them.

5. Keep media derivation separate from chat payload decode.
   The business message may only carry metadata while download or decrypt uses a different derivation path.

## Working method

1. Freeze one successful transcript.
   Save the exact warm-up sequence from first contact to one readable business event.

2. Separate layers.
   Document:
   - transport upgrade and headers
   - login or pairing bootstrap artifacts
   - key schedule or secret update path
   - frame envelope format
   - payload decode chain
   - media derivation path

3. Prove the smallest local milestone.
   Rebuild one local session that reaches one business frame without the browser.

4. Scale only after the session is stable.
   Add subscriptions, pagination, reconnect, receipt handling, and media after the first stable local session works repeatedly.

## Questions that must be answered

- what exact bootstrap artifact makes the stream readable
- which frames are client-required versus server-assigned
- which counters, tags, or epochs must advance locally
- whether auth state is reusable or must be refreshed per session
- whether payload decode is compression, protobuf, custom binary, encryption, or a stack of several layers
- whether media keys derive from the message payload, a side endpoint, or stored session state

## Evidence checklist

- one full successful session transcript
- one raw encrypted or binary business frame
- one decoded business frame tied to the raw frame above
- one fixed-input proof for any recovered key schedule helper
- one note that maps frame families to their role
- one note that states whether media handling is in-scope and how its key path works

## Acceptable handoff

The final collector must still be local protocol code:

- Python with local WebSocket or stream client
- local handshake bootstrap
- local frame builder or parser
- local decoder for protobuf, compression, or binary envelopes
- minimal isolated JS or WASM helper only if a verified port is not yet cheaper

Not acceptable:

- keeping the browser open to stay logged in
- replay through page context or CDP as the final path
- calling the target "browser-only" before key schedule, tag rules, and media derivation are checked
