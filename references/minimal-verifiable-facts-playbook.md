# Minimal Verifiable Facts Playbook

Use this file when a solved target, target upgrade, or sibling route teaches something likely to recur.

The goal is to preserve a small fact set that survives memory drift and makes future diffs cheap.

Record 5 to 15 minimal verifiable facts.
Less than 5 usually stays too vague.
More than 15 usually turns back into notes instead of a reusable checkpoint set.

## Contents

- [Static analysis six questions](#static-analysis-six-questions)
- [What a good fact looks like](#what-a-good-fact-looks-like)
- [What a good fact is not](#what-a-good-fact-is-not)
- [Fact categories](#fact-categories)
- [Good versus bad examples](#good-versus-bad-examples)
- [Capture template](#capture-template)
- [Upgrade workflow](#upgrade-workflow)
- [Storage rule](#storage-rule)
- [Final rule](#final-rule)

## Static analysis six questions

During Phase 2 source work, answer these before claiming the mutation model is known. Store durable answers as facts when they recheck cleanly.

1. **Scope**: is only one parameter encrypted, or is the whole request chain hijacked (URL rewrite / XHR-fetch intercept)?
2. **Dynamic factors**: do page, timestamp, nonce, cookie, UA, or host environment values enter the transform?
3. **Response side**: is the business payload encrypted, packed, or font-mapped on the way back?
4. **Runtime codegen**: does `eval` / `new Function` / remote script injection build part of the signer?
5. **Precursors**: which warmup, token, config, or challenge requests must precede the business call on one chain?
6. **Chain rewrite**: which wrappers mutate method, URL, headers, body, or cookie after business code "finished"?

If any answer is unknown, keep Phase 2 open. Pair with signer entry taxonomy in `references/jsvmp-analysis-playbook.md` when interceptors or VMs are involved.

## What a good fact looks like

A good fact is:

- observable from a capture, runtime artifact, or local replay
- binary or measurable
- stable enough to re-check on a later run
- tied to the protocol boundary, not a story about the page
- safe to store without copying secrets, live cookies, or full browser state

## What a good fact is not

Do not store these as facts:

- copied secret keys
- live cookie values
- full session headers
- "it looked like Firefox"
- "Python failed so we used a runtime"
- long narratives with no re-checkable boundary

Those are notes, not verifiable facts.

## Fact categories

Choose the smallest mix that captures the family.

### Entry and bootstrap facts

Examples:

- first response is a challenged document, not the final API
- the same document URL becomes replayable after local bootstrap
- one linked challenge asset is required, not the whole bundle tree
- the business route itself first returns a machine refresh tuple and then succeeds after local regeneration on the same route family

### Real request facts

Examples:

- the real list route is `/ui` after page 5, not the static filename family
- the useful data comes from a sibling API, not the visible detail page
- the protocol contract lives in GraphQL envelope fields, not the URL

### Placement facts

Examples:

- the anti-bot blob lives in a custom header, not `ETag`
- the decisive cookie only matters as the outbound `Cookie` header seen at egress
- the wrapped payload is posted in one outer field such as `param`

### Artifact-shape facts

Examples:

- the token is URL-safe Base64 and length stays near 248
- the response prefix is 8 bytes before the real payload anchor
- the cookie shape includes a checksum segment or fixed-width splice
- `document.all.length` changes when one attached element appears or disappears
- `iframe.contentWindow` exists only while the iframe stays attached

### Decode and framing facts

Examples:

- decode order is prefix strip -> Base64 -> protobuf
- compact JSON order matters before signing
- URL query, body, and response share one packet family with field-specific variants

### Session and bootstrap facts

Examples:

- linked bootstrap assets must stay on the same session chain
- page-seeded state and request-scoped signer state are separate moving parts
- repeated helper calls require one VM/context lifetime until a persistent-world versus fresh-world control proves runtime identity irrelevant
- a fresh anonymous session mints transport reachability but not business admission

### Acceptance facts

Examples:

- one fresh single-page replay succeeds twice before pagination is attempted
- the route accepts a simplified sidecar on the public path but not on the business path
- helper output looking browser-shaped is not enough without live replay

## Good versus bad examples

Good:

- page 6 pivots from static filenames to `/ui?page=6`
- the decisive blob is added in a header, not the query
- local runtime egress `Cookie` header differs from `document.cookie`
- the verifier sidecar length roughly doubles after `canvas` and layout surfaces are restored
- the challenged document URL itself is the replay target after bootstrap

Bad:

- use this cookie value
- reuse my browser profile
- the site is very strict
- the answer is probably in the big bundle
- the runtime seems necessary

## Capture template

Use this block after a reusable win or when an upgrade starts to drift.

```markdown
Minimal Verifiable Facts
- Family:
- Fact 1:
- Fact 2:
- Fact 3:
- Fact 4:
- Fact 5:
```

Add up to 15 facts only when each new line narrows a future diff.

## Upgrade workflow

When a previously solved family breaks:

1. capture one fresh minimal sample
2. re-check the old fact set one line at a time
3. split the facts into `still true`, `changed`, and `unknown`
4. reverse only the changed boundary first
5. update the fact set after the new replay is proven

This turns "the whole site changed" into "three facts moved."

## Storage rule

Store facts in the smallest reusable home that fits:

- the owning reference when the lesson transfers broadly
- a task-local analysis note when the lesson is still single-target and uncorroborated
- a future family-specific case note only after the pattern repeats

Prefer structural facts over copied artifacts.

## Final rule

Small facts age better than big summaries.

If a later run cannot quickly tell what changed, the fact set was too vague.
