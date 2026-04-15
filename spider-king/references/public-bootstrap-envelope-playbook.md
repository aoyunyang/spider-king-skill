# Public Bootstrap Envelope Playbook

Use this playbook when a page is publicly visible but successful replay still depends on a bootstrap response, entry-route cookies, or an encrypted outer envelope.

## When to route here

Route here when one or more of these symptoms appear:

- the homepage or list page is public, but raw replay fails until an entry route is visited first
- an early endpoint returns a public key, config blob, nonce seed, or short string rather than business data
- the business request posts a wrapper such as `{"param":"..."}` instead of the visible form fields
- list APIs work anonymously, but detail or submit APIs still reject
- the UI tab shows one category, while empty filter values produce a different result set

## Core idea

Public does not mean unsigned.
Anonymous access, bootstrap state, transport envelopes, and permission boundaries are separate layers of the contract.

## Fast execution path

1. Freeze the public entry route.
   Record which first GET seeds cookies, redirects, or cacheable bootstrap state.

2. Freeze the bootstrap artifact.
   Save the exact public key, config blob, nonce seed, or wrapper metadata returned by the bootstrap endpoint.

3. Freeze one good business request.
   Save headers, cookies, body, outer wrapper shape, and the response shape.

4. Recover the envelope build order.
   Prove each stage separately:
   - raw business payload
   - exact JSON serialization shape
   - digest or sign input
   - timestamp or nonce injection
   - final wrapped object
   - encryption or encoding
   - outer field name such as `param`

5. Make hidden state explicit.
   Turn category, mode, tab, page, and sort values into explicit protocol fields rather than trusting UI defaults.

6. Separate permission boundaries.
   Test list, detail, and submit routes independently. Public list success does not prove that detail or submit are public too.

## High-value checks

- Verify whether the hash is computed on the raw business payload or the wrapped payload.
- Verify whether JSON must be compact, key-stable, or non-ASCII-preserving.
- Verify timestamp precision: seconds, milliseconds, or custom offset.
- Verify whether RSA or similar encryption uses chunking for long payloads.
- Verify whether the bootstrap artifact is session-bound, page-bound, or reusable across requests.
- Verify whether cookies come from the entry route, bootstrap route, or both.

## Common traps

- hashing a Python dict repr instead of the exact serialized JSON
- hashing after timestamp injection when the page hashes before injection
- using pretty JSON instead of compact JSON
- forgetting long-message chunking on RSA-wrapped payloads
- assuming empty category fields match the visible tab
- proving only the public list and claiming detail access is solved

## Delivery guidance

Preferred delivery shape:

1. Python collector with explicit bootstrap step
2. local helper for crypto or encoding only if Python port is not yet cheaper
3. no browser dependency in the final path

## Minimal handoff notes

Report these items explicitly:

- real entry route
- real bootstrap endpoint
- exact envelope build order
- cookies or headers that scope the anonymous session
- category and pagination fields that must be explicit
- list-versus-detail permission boundary
