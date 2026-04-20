# Delivery Gate Playbook

Use this reference when you need to decide whether the current path is a real collector or a dressed-up shortcut.

## Core rule

If the final handoff still depends on live page context, it is not done.

## Acceptable delivery shapes

- pure Python HTTP collector
- Python plus isolated local JS helper
- Python plus local WASM helper
- Python plus local bootstrap executor
- Python plus local decoder for fonts, protobuf, msgpack, or compressed payloads

## Unacceptable delivery shapes

- browser automation as the collector
- CDP or page-context `fetch` as the steady-state path
- manual cookie export as an operating requirement
- "works only with my browser profile" handoff
- hidden verifier clicks instead of protocol replay

## Gate checklist

1. real endpoint confirmed
2. moving parts named explicitly
3. signer or decoder has fixed-sample proof
4. request succeeds repeatedly
5. decode or parser path is local when applicable
6. required session state is explicit
7. no browser dependency remains in the final run path

## Escalation rule

If one gate fails, do not package the current path as "good enough".
Keep reversing until the failing gate is resolved or the blocker is truly external.
