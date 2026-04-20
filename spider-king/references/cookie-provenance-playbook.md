# Cookie Provenance Playbook

Use this reference when replay depends on a cookie, but it is still unclear who writes it or how it refreshes.

## Core rule

Do not hardcode a rotating business cookie before proving its writer and refresh path.

## Possible writers

A blocking cookie usually comes from one of these places:

1. `Set-Cookie` on a protocol response
2. `document.cookie` from page JavaScript
3. server-returned bootstrap or challenge JS
4. redirect wrappers, iframes, workers, or SDK side effects
5. a derived header or token problem that only looks like a cookie problem

## What to capture

Record the cookie transition around the exact request boundary:

1. request cookies before the call
2. response headers, especially `Set-Cookie`
3. immediate post-response cookie state
4. any JS write such as `document.cookie = ...`
5. whether the value changes on page turn, verifier success, or session refresh

If the cookie appears after a redirect or wrapper page, treat the redirect chain as part of the provenance story.

## Working method

1. capture one successful request and one failure
2. diff cookie state before and after each network step
3. search source for the cookie name and for `document.cookie`
4. identify the writer class:
   - response header
   - inline script
   - returned challenge JS
   - wrapper page or SDK side effect
5. prove the refresh path:
   - same endpoint every time
   - verifier step
   - page-exposed refresh helper
   - session bootstrap
6. only then choose delivery:
   - preserve the protocol response if the server sets it
   - replay local JS if bootstrap JS sets it
   - model it as part of the session contract if it is account-bound

## Common traps

- copying a browser cookie into code without proving who wrote it
- blaming the signer when the real issue is cookie rotation
- reading the final cookie string but not the write path that created it
- refreshing the whole browser page instead of rebuilding the minimal cookie refresh contract locally

## Verification checklist

Call the cookie problem understood only after:

1. the writer is identified
2. the refresh trigger is known
3. the collector regenerates or preserves the cookie without browser automation
4. replay succeeds at least twice with the recovered cookie path
