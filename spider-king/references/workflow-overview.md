# Workflow Overview

Use this file as the shortest end-to-end map for a reverse job.

## Phase 0: Fingerprint the target

Before touching code, classify the target:

- decoy endpoint vs real endpoint
- wrapper rewrite vs visible param
- patched helper vs standard helper
- session-bound vs anonymous
- bootstrap asset vs direct data API
- one-page exception vs whole-flow exception
- verifier-gated vs signer-gated
- JSVMP or heavy obfuscation vs normal packed bundle

## Phase 1: Prove the real request

- capture the request that returns useful data
- record its initiator
- record exact query, body, headers, cookies, and response shape

## Phase 2: Isolate the moving state

Treat each moving part separately:

- timestamp
- random fragment
- rotating cookie
- transport wrapper field
- page-specific header
- session contract
- bootstrap output

## Phase 3: Rebuild offline

Choose the cheapest valid path:

1. pure Python
2. Python plus tiny JS helper
3. Python plus tiny WASM helper
4. Python plus local bootstrap executor

## Phase 4: Verify repeatability

- helper outputs match fixed test vectors
- page 1 replays at least twice
- pagination or cursor works
- known exceptions are encoded narrowly

## Phase 5: Deliver

- protocol-only collector
- saved samples
- clear notes about headers, cookies, and instability
