# Session Contract Playbook

Use this reference when:

- the page mentions `sessionid`, login, or per-user answers
- fetch and submit appear to need the same account state
- one request works anonymously while another fails without login
- one authenticated session can still switch current tenant, shop, org, locale, supplier, or workspace context without a fresh login
- login succeeds but business data still depends on an extra activation or scope selection

## Contents

- [Core rule](#core-rule)
- [Working method](#working-method)
- [Layer checklist](#layer-checklist)
- [Common traps](#common-traps)
- [Init and registration checklist](#init-and-registration-checklist)
- [Business request contract checklist](#business-request-contract-checklist)
- [Delivery rule](#delivery-rule)
- [Device-trust companion freshness](#device-trust-companion-freshness)

## Core rule

Session state is a protocol contract, not a browser convenience.
Page text is not proof that a cookie enters the signer preimage.
Account login is not automatically the same gate as business-context activation.
Keep the session chain on one baseline; do not splice cookies, storage, or client identity from a second capture. See single baseline purity in `references/env-diff-playbook.md`.

## Working method

1. verify whether the data request depends on login, submission depends on login, or both
2. treat page warnings about `sessionid` or login as hypotheses only; prove them from wire behavior
3. capture the same business route with and without the claimed cookie or header
4. record whether the answer is account-bound
5. if the account can still change tenant, role, shop, supplier, or data-range after login, read `references/multi-context-session-playbook.md`
6. keep fetch and submit on one explicit session chain when the answer or permission is account-bound
7. expose required session inputs in the collector instead of hiding them inside a browser profile
8. separate list or detail collection from submit-account requirements when the wire shows they diverge
9. when durable cookies are reused, re-validate the active business identity before scraping

## Layer checklist

When login is only the first gate, name these layers explicitly:

- account authentication
- tenant or product space
- product host or product face
- role or merchant type
- data-range or resource scope

A home page that loads is not proof that every required layer matches the task.

## Common traps

- assuming login is irrelevant because one endpoint works once without it
- assuming every request needs login because the page text says so
- treating account cookies as a universal key for every business page
- hardcoding a rotating session cookie into a signer preimage without fixed-sample proof
- mixing anonymous collection with account-bound submission without documenting the boundary
- blaming the signer when the only missing piece is the account chain used at submit time
- exporting cookies after login but before business-context validation
- sharing one session across concurrent context switches
- merging sibling-host or product-face cookie jars before proving they are replay-equivalent



## Init and registration checklist

When a signer export is missing or an interceptor never fires, prove registration before algorithm work:

1. list init/config/warmup calls that arm the business route
2. record required config objects, path lists, or feature flags
3. keep multi-script order explicit: surfaces -> polyfills -> bundle -> init -> trigger
4. retest feed-cut or export call only after registration succeeds
5. store durable registration facts via `references/minimal-verifiable-facts-playbook.md`

See also `references/jsvmp-analysis-playbook.md` init and registration contract.

## Business request contract checklist

When a browser success packet exists and local business replay fails, recover the request contract before deepening signer work:

1. compare the exact field set with the accepted business request
2. preserve empty fields, default values, and repeated array keys when the success packet sends them
3. replay warmup or precursor XHR order that mutates cookies, CSRF slots, or route-local state
4. distinguish page-A versus page-B token slots when both exist
5. keep Referer, Origin, and Client-Hints generation coherent with the session baseline
6. if an intermediate hop returns `403` or redirect, fix contract and session continuity before blaming the per-request signer

Record contract diffs as `request-contract` under `references/failure-surface-taxonomy.md`.

## Delivery rule

The collector should expose the required session inputs and document whether the result is account-bound.
If list collection is anonymous and only submit needs login, encode that split explicitly.
If business identity has multiple mutable layers, document the activation order and the final identity reread used as the acceptance gate.

## Device-trust companion freshness

When a verifier also consumes a fingerprint/device companion on the same mid:

- minted Init fields are not admitted until the companion is accepted for that mid
- do not rebind old companion plaintext onto a new mid as the main strategy
- keep Init -> companion emit -> behavior sidecar -> Verify on one continuous chain
- delayed verify after long host-debug loops often surfaces as stale/timeline rejects, not packer failure
- align companion counters (
um / n1-class) with token builders when the contract requires it

Read 
eferences/device-trust-sidecar-playbook.md.
