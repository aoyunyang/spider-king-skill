# Workflow Overview

Use this file as the shortest end-to-end map for a reverse job.

## Startup gate

Before deep work:

- check local tool sanity
- classify the target as `signer-gated`, `verifier-gated`, `decode-gated`, or `session-gated`
- state the smallest acceptable browser-free delivery shape

## Phase 0: Fingerprint the target

Before touching code, classify the target:

- decoy endpoint vs real endpoint
- wrapper rewrite vs visible param
- patched helper vs standard helper
- signer-gated vs verifier-gated vs decode-gated vs session-gated
- session-bound vs anonymous
- bootstrap asset vs direct data API
- one-page exception vs whole-flow exception
- clean-baseline-first vs trace-first vs decode-first vs transcript-first
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
- cookie provenance

## Phase 3: Rebuild offline

Choose the cheapest valid path:

1. pure Python
2. Python plus tiny JS helper
3. Python plus tiny WASM helper
4. Python plus local bootstrap executor

## Phase 4: Verify repeatability

- helper outputs match fixed test vectors
- verifier-gated targets keep working after you remove broad hooks
- page 1 replays at least twice
- pagination or cursor works
- known exceptions are encoded narrowly

## Phase 5: Deliver

- protocol-only collector
- saved samples
- clear notes about headers, cookies, and instability
