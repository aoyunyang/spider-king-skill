# Decoy And Real Request Playbook

Use this reference when:

- page code points at one endpoint but the wire uses another
- the UI talks about one route while the real data comes from a different path
- old notes, screenshots, or snippets disagree with fresh network traffic

## Core rule

Trust the wire, not the page text.

## Recognition signals

- page code hooks `/api/match/...` but the network sends `/api/question/...`
- the first visible request is a decoy and the real request is triggered by a wrapper
- the request path changes after redirects, wrappers, or compatibility pages
- the visible form submit is not the real business request on the wire

## Working method

1. capture the real network request that returns useful data
2. record method, path, query, headers, cookies, and initiator
3. trace the initiator back to the canonical mutation point
4. document the decoy path explicitly so it does not leak into delivery code
5. code only against the verified live path

## Common traps

- trusting inline page code more than fresh network evidence
- preserving dead request paths in the collector "just in case"
- assuming the old endpoint still matters because the page still mentions it

## Delivery rule

The collector should mention the decoy path in notes, but never depend on it.
