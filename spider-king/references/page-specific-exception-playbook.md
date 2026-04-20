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

## Common traps

- assuming the signer is broken when the real issue is one header
- spreading a one-page workaround across the whole pipeline
- declaring the target browser-only because one page behaves differently

## Delivery rule

Document the exception explicitly and prove it with before-and-after responses.
