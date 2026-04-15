# Verifier Replay Playbook

Use this reference when:

- data requests are gated behind captcha, one-shot verification, or click-order challenges
- there is no meaningful business signer, but requests still fail until a verifier passes
- browser clicks appear to unlock the next request

## Core rule

The verifier output is the real dynamic parameter.

## Working method

1. identify the verifier request and response
2. determine what output authorizes the next business request
3. solve or reconstruct that output locally
4. replay the verifier in protocol form
5. send the business request with the resulting token, cookie, or coordinates

## Common traps

- hunting for a fake business-layer signer while ignoring the verifier
- automating clicks instead of understanding the verifier payload
- treating the verifier as UI-only behavior

## Delivery rule

Do not simulate UI interaction in the final solution. Reproduce the verifier as protocol data.
