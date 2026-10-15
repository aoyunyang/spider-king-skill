# Page Specific Exception Playbook

Use this reference when:

- pages 1 to 4 work but one page fails
- the last page returns hints, strings, or anti-bot markers
- only one request needs a special header, cookie, or ordering rule

## Core rule

Keep narrow exceptions narrow.

## Working method

1. diff the successful pages against the failing page
2. compare headers, cookies, referer, user agent, and request order
3. test one narrow change at a time
4. encode the verified exception in per-page or per-request settings
5. keep the rest of the collector unchanged

Typical narrow exceptions:

- last-page or one-route `User-Agent` overrides
- one-route referer or origin requirements
- one-route extra header that successful siblings do not send

## Page-local proof gate

Treat a page, cursor, or route exception as a hypothesis until a one-variable
negative control proves it necessary. Compare the ordinary request with the
proposed exception while keeping session, transport, pacing, query, and
response parsing fixed. The control should fail at the same page or route for
the expected protocol reason, and the accepted variant must reach the real
business oracle rather than merely return HTTP 200.

A collector may conservatively mirror one observed narrow request profile
after repeated business acceptance, but it must label necessity and causality
unproven until the negative control exists. Such an unablated profile cannot
be promoted as reusable experience.

Encode the exception as a narrow predicate (for example, a page or cursor
condition) and leave sibling requests on the ordinary profile. Do not promote
a special value, header, or UA string to a global default because it happened
to work on one endpoint. Record the trigger, scope, negative-control result,
and the condition that would retire the exception. Distinguish "used in the
accepted run" from "proved necessary" in manifests and handoffs.

## Type-strict oracle

HTTP 200 plus an array is not acceptance. The business oracle is the typed
payload contract: item kinds, cardinality, and parseable downstream fields.
A success-class response that contains strings, hints, mixed types, or a
shorter marker array is a negative control. Encode that check in the
collector so a typed trap cannot be persisted as a complete page.

## Layered ablation

If more than one last-page hypothesis exists, change one dimension at a time:

1. transport admission
2. page-local request profile
3. signer or token
4. session or permission

A new error class means the next gate opened, not that the page passed.
If sibling pages already return typed business data on both HTTP/1.1 and
HTTP/2, remaining last-page failure is not a transport-family problem.

## Common traps

- assuming the signer is broken when the real issue is one header
- spreading a one-page workaround across the whole pipeline
- declaring the target browser-only because one page behaves differently
- treating HTTP 200 plus a string or hint array as page success
- treating two pages that share a digest as interchangeable requests; keep the page or cursor field the server asked for
- escalating to transport impersonation after both HTTP versions already pass the typed oracle

## Delivery rule

Document the exception explicitly and prove it with before-and-after responses.
Record the type-strict oracle and the one-variable negative control in the
handoff. Do not copy the exceptional profile onto sibling pages.

The secret-free fixture for this family is
`references/experience-fixtures/page-local-exception-matrix.json`.
