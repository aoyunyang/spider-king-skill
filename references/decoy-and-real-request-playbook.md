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
- leftover sibling-page copy (last-page UA, five-page integer API, ajax wrappers) remains in the HTML while live probes 404
- a giant chart, painter, or SVG webpack module sits next to a tiny module that owns the list URL
- the instructions name one export (`secretkey`) while the runtime installs another (`SecretKey`) that wraps the real hasher with local timestamp or PRNG bytes
- a visible rotating HTML constant is the live preimage while the named local signer is a decoy
- a visible pager comments out a header while the runtime-replaced `$.ajax` or XHR writer still sends it
- a debug UI concatenates `"GET " + url + "?"` while the signer hashes a different preimage
- a `call()` return or form field `m` is swallowed and never sent
- a second harvested SPKI or `document.all` key sits next to the live writer and is never selected; the unused branch may add a limb delta instead of swapping a whole key
- an XHR `open` filter on a URL substring misses a relative business path
- the HTML table or list is filled with zeros or placeholders while no list XHR or fetch fired
- chrome-devtools `list_network_requests` shows only document/css/js while the DOM later fills, so the operator assumes the packed script is a local data blob
- HTTP GET/POST of a similarly named REST path returns 200 with a constant filler value while the list arrives on a WebSocket or other sibling channel
- ajax exposes `beforeSend` or an IIFE wrapper while the captured body still equals the visible fields

## Working method

1. capture the real network request that returns useful data
2. record method, path, query, headers, cookies, and initiator
3. trace the initiator back to the canonical mutation point
4. document the decoy path explicitly so it does not leak into delivery code
5. code only against the verified live path


## Source versus current live contract

Saved source proves capture-time client code, not today's server contract.

- a source path, writer, or optional field may never fire on the current page
- a source omission may be insufficient because the live server now requires the field
- a commented header in page source is a source omission, not proof the wire omitted it, especially when `$.ajax` or XHR is a replaced runtime export
- decide conflicts with same-session, same-transport, one-variable live tests
- label the result as the current live contract and keep drift as residual risk
- do not keep dead source branches in the collector "just in case"
- do not bulk-add HAR extras, telemetry, or sibling APIs because risk-control is unknown

## Common traps

- trusting inline page code more than fresh network evidence
- preserving dead request paths in the collector "just in case"
- adding five or six unproven extra routes when the rejected business request is still unreversed
- assuming the old endpoint still matters because the page still mentions it
- cloning the previous sibling collector shape before a live status probe proves this page still has that data API
- treating a named window export as the submit hasher because the page text told the operator to call it
- reusing a harvested public suffix/token after a later GET of the same document
- dropping a live header because the visible source commented it out
- treating the debug-UI GET prefix as the signed string
- sending a swallowed `call()` return or field `m` because source assigned it
- encrypting with the unused second key because two public keys were harvested
- filtering XHR `open` on a path substring and concluding the business request never fired
- treating HTML placeholder zeros as business data when the VM never issued the list request
- treating HTTP 200 dummy filler on a sibling REST path as the list API because the path looks like the list
- scraping HTML zeros after a dummy HTTP sibling returned 200 instead of freezing a WebSocket or text frame
- treating a chrome-devtools HTTP-only resource log as proof there is no WebSocket list
- JSON-parsing or summing the first short WebSocket text frame instead of classifying prefix versus business JSON
- treating an empty `beforeSend` hook as proof a hidden token exists

## Delivery rule

The collector should mention the decoy path in notes, but never depend on it.
