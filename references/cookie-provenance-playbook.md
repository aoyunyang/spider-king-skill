# Cookie Provenance Playbook

Use this reference when replay depends on a cookie, but it is still unclear who writes it or how it refreshes.

## Contents

- [Core rule](#core-rule)
- [Possible writers](#possible-writers)
- [What to capture](#what-to-capture)
- [State transition table](#state-transition-table)
- [Working method](#working-method)
- [Common traps](#common-traps)
- [Multi-hop login and activation chains](#multi-hop-login-and-activation-chains)
- [Verification checklist](#verification-checklist)

## Core rule

Do not hardcode a rotating business cookie before proving its writer and refresh path.
Distinguish server-issued seed state from locally derived replay state, and treat the final outbound `Cookie` header as a first-class artifact when helper assembly or wrapper logic can change what actually crosses the wire.

## Possible writers

A blocking cookie usually comes from one of these places:

1. `Set-Cookie` on a protocol response
2. `document.cookie` from page JavaScript
3. server-returned bootstrap or challenge JS
4. a local builder fed by bootstrap config, fingerprint data, UUID-like state, or other page inputs
5. redirect wrappers, iframes, workers, or SDK side effects
6. a derived header or token problem that only looks like a cookie problem
7. a local helper or runtime that composes the final outbound `Cookie` header from several sources, even when only some pieces are stored as cookies

## What to capture

Record the cookie transition around the exact request boundary:

1. request cookies before the call
2. response headers, especially `Set-Cookie`
3. immediate post-response cookie state
4. any JS write such as `document.cookie = ...`
5. whether the value changes on page turn, verifier success, or session refresh
6. the exact outbound `Cookie` header, including ordering, omitted pieces, and helper-composed segments, if the browser or local runtime can expose request egress
7. any local inputs that feed the cookie, such as config blobs, timestamp slices, UUID variants, fingerprint vectors, or compatibility constants
8. which cookie pieces are bootstrap seed state versus replay state when the first response and final replay use different cookie shapes
9. whether a response-side challenge rotates a seed tuple, a derived replay cookie, or both before the retry succeeds

If a `document.cookie` hook stays silent, read that result narrowly: it only proves no write crossed that JS setter boundary during the observed window. It does not clear `Set-Cookie`, returned bootstrap JS, redirects, workers, or wrapper side effects.

The stored cookie jar and the final outbound `Cookie` header are related but not identical evidence. Path rules, ordering, wrapper mutation, or helper assembly can make the live wire header differ from `document.cookie` or a library-managed jar. When replay still fails, capture the wire header that actually crossed the boundary.

The same token name can also occupy more than one slot: cookie, query, and header. A stale cookie value can poison a request that mints the live token into query or header. Reconcile slots before blaming the signer.

If the cookie appears after a redirect or wrapper page, treat the redirect chain as part of the provenance story.

Session-looking, fingerprint-looking, or telemetry-looking cookie names do not prove server issuance. Some blocking cookies are minted entirely on the client from bootstrap config, compact JSON fingerprints, UUID variants, or embedded compatibility constants, then written locally or emitted only in the final outbound header.

## State transition table

When a cookie, token, or verifier state appears to gate replay, record the
ordered state machine instead of only the final value:

```text
step | route | outbound state hashes/lengths | response status | state writes | next outbound authority
```

Use one row per network boundary. Include document responses, bootstrap assets,
sidecar or telemetry requests, verifier responses, redirects, and the final
business request when they participate in the same chain.

The transition order is part of the protocol. A final cookie, token, or header
that looks correct can still be stale if it was written in the wrong step,
stored under the wrong path, skipped by the next request, or overwritten before
the downstream consumer.

## Working method

1. capture one successful request and one failure
2. diff cookie state before and after each network step
3. separate server-issued seed cookies from locally derived replay state before modeling refresh logic
4. search source for the cookie name and for `document.cookie`
5. compare stored cookie state with the exact outbound `Cookie` header, including ordering or helper-composed pieces, when egress evidence is available
5b. when seeding an impersonate-client jar, bind the request hostname; do not mix empty-domain session cookies with host-only rotating tokens
6. identify the writer class:
   - response header
   - inline script
   - returned challenge JS
   - local minting formula
   - wrapper page or SDK side effect
7. prove the refresh path:
   - same endpoint every time
   - response-side challenge tuple on the business endpoint
   - verifier step
   - page-exposed refresh helper
   - session bootstrap
   - local formula seeded by config JS, fingerprint vector, structured random id, or compatibility constant
8. if the next call fetches rotating bootstrap JS, clear the previous locally-minted cookie before that GET
9. only then choose delivery:
   - preserve the protocol response if the server sets it
   - replay local JS if bootstrap JS sets it
   - rebuild the exact local minting recipe if page code derives it from config or fingerprint or session inputs
   - model it as part of the session contract if it is account-bound

## Common traps

- copying a browser cookie into code without proving who wrote it
- blaming the signer when the real issue is cookie rotation
- reading the final cookie string but not the write path that created it
- treating `document.cookie` or a client jar as the full wire truth when the outbound `Cookie` header differs
- assuming two cookie jars are replay-equivalent when the live outbound header order or composition differs
- refreshing the whole browser page instead of rebuilding the minimal cookie refresh contract locally
- treating a session-looking or fingerprint-looking cookie name as proof of `Set-Cookie` provenance
- replacing a structured local id with any random UUID, random hex, or placeholder digest
- recomputing a digest over "equivalent" JSON when the client serializes one exact fingerprint vector and item order
- treating a server-issued seed cookie as if it were already the final replay artifact
- refreshing only one cookie name when the route actually rotates a seed tuple plus one locally derived replay value
- blindly merging helper side-effect cookies into the main session without checking whether the decisive artifact is actually the composed outbound `Cookie` header
- wrapping the live mint setter on a success host and treating the poisoned cookie as algorithm failure
- observing only `document.cookie` while the mint also writes storage
- treating host-scalar parity as proof that local mint ran
- saving only the login POST cookies and dropping later activation cookies
- treating one-time handoff tickets as long-lived session cookies
- exporting a jar before business-identity validation passes
- leaving a stale same-name cookie in the jar when the live request mints that token into query or header
- leaving a stale locally-minted cookie on the next bootstrap-script GET; that cookie can change the returned JS or branch
- seeding an impersonate-client cookie with an empty domain while a rotating token is host-only; `get_dict(domain=host)` can drop the session cookie even if send-time host fill still happens



## Multi-hop login and activation chains

When cookies accumulate across login, redirect handoff, async sync, business proxy, and session-update calls:

1. keep the whole chain on one session object
2. classify each artifact as seed cookie, handoff ticket, async sync cookie, activation cookie, or final business cookie
3. consume short-lived handoff tickets and async URLs immediately; do not promote them into durable credential files
4. export only after the final business identity has been reread and accepted
5. if a refreshed candidate jar fails identity validation, refuse to overwrite the previous durable file

A single response's `Set-Cookie` is rarely the whole story for multi-context back offices.

## Verification checklist

Call the cookie problem understood only after:

1. the writer is identified
2. the refresh trigger is known
3. locally minted cookies, if any, have proven structure, inputs, and write path
4. helper-assembled or wrapper-mutated outbound `Cookie` headers, including ordering when it matters, are proven and not inferred from the jar alone
5. if a response-side challenge rotates a tuple, the collector updates the whole tuple consistently before retry
6. the collector regenerates or preserves the cookie path without browser automation
7. replay succeeds at least twice with the recovered cookie path
