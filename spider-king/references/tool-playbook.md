# Tool playbook

Use this file as the fast map from reverse-engineering task to tool choice.

## Preferred order

1. Capture one clean baseline request.
2. Find the real request.
3. Trace the initiator.
4. Diff the moving fields.
5. Add the narrowest runtime proof that still preserves the sample.
6. Reproduce one stable request.
7. Scale collection only after the first request is repeatable.

Prefer clean baselines, initiator stacks, and narrow proofs over broad hooks. Prefer focused source reads over loading giant bundles into context.

## Recon and network capture

### `js-reverse`

- `new_page` / `navigate_page`: open the target and follow the real landing URL
- `list_network_requests`: list XHR, Fetch, document, script, and preflight traffic
- `list_network_requests(reqid=...)`: inspect the chosen request in full
- `get_request_initiator`: jump from request back to the caller stack
- `get_websocket_messages(analyze=true)`: group streaming traffic by message family
- `get_websocket_messages(frameIndex=...)`: inspect one exact frame in full
- `evaluate_script`: inspect `document.cookie`, `localStorage`, `sessionStorage`, or page globals when state matters

### `chrome-devtools`

- `navigate_page` / `new_page`: open the page when UI flow evidence matters
- `take_snapshot`: inspect page structure fast
- `wait_for`: wait on target text while triggering filters, search, or pagination
- `list_network_requests` and `get_network_request`: second source of truth when UI flow matters
- `take_screenshot`: capture evidence for hidden panels, captcha gates, or lazy regions

Use browser DevTools when DOM state matters. Use `js-reverse` when JavaScript runtime, request initiators, or hooks matter.

## Static JS analysis

- `list_scripts`: enumerate candidate bundles
- `search_in_sources`: search keywords across all loaded sources
- `get_script_source`: inspect the exact function neighborhood
- `save_script_source`: dump a full bundle locally when a file is too large to inspect in slices

Fallback recipes when you wanted a missing helper:

- no `find_in_script`: use `search_in_sources`, then `get_script_source`
- no automatic code summary: read the initiator stack first, then the smallest source slice around the mutation point
- no automatic crypto detector: search helper names, compare fixed inputs, and route to `references/crypto-patterns.md`
- no automatic deobfuscator: use `search_in_sources`, `save_script_source`, and `references/obfuscation-guide.md`

Keyword packs:

- request path: `"/api/"`, `"graphql"`, `"fetch("`, `"axios"`, `"XMLHttpRequest"`
- signer: `"sign"`, `"token"`, `"nonce"`, `"timestamp"`, `"trace"`, `"x-sign"`, `"beforeSend"`, `"ajaxSetup"`, `"requestId"`
- crypto: `"md5"`, `"sha"`, `"hmac"`, `"aes"`, `"rsa"`, `"crypto.subtle"`
- environment: `"navigator"`, `"canvas"`, `"webgl"`, `"performance"`, `"webdriver"`

## Dynamic validation

Start with a clean baseline. Then use initiator stacks and request diffs. Add runtime proofs only after you know why you are instrumenting.

### Baseline-first proof flow

1. capture one clean request and response pair
2. use `get_request_initiator` to jump from the request to the caller stack
3. use `search_in_sources` and `get_script_source` to inspect the smallest relevant code region
4. use `trace_function` when a named helper is stable enough to trace without poisoning the target
5. use `break_on_xhr` when you need to stop at the exact request boundary
6. use `inject_before_load` only for narrow boundary hooks that you can justify
7. if the target is verifier-gated or behavior-sensitive, remove invasive instrumentation and recapture a clean baseline the moment behavior changes

### Breakpoint tools

- `set_breakpoint_on_text`: best when the bundle is minified
- `get_paused_info`: inspect locals and scope
- `evaluate_script(frameIndex=...)`: print the exact pre-sign string, key, iv, or payload in the paused call frame
- `pause_or_resume`: resume execution after inspection
- `step(direction='over'|'into'|'out')`: only after you already know why you are pausing

## Session and environment handling

- `evaluate_script`: inspect `document.cookie`, storage values, bootstrap globals, or runtime helper outputs
- `evaluate_script(mainWorld=true)`: inspect page-owned globals such as webpack caches, SDK objects, or exposed bootstrap helpers
- `inject_before_load`: patch or observe a narrow environment branch before the page script runs
- `save_script_source`: preserve suspicious bundles for offline diffing when environment mismatch remains unclear

## Failure routing

- `403`, `412`, `429`: compare headers, cookies, sign freshness, and request pacing
- business error with normal `200`: compare payload assembly order and timestamp precision
- decrypt failure after a successful `200`: verify whether the runtime key/iv is transformed through a helper such as digit-pair-to-char before AES is applied
- empty data: verify pagination, filters, referer, login state, and cursor evolution
- occasional success: inspect one-time tokens, session refresh, or concurrent request coupling
- first request works but immediate replay fails: compare cookie mutation, in-memory timestamp slots, and whether a page refresh function must run before every request
- response gibberish: search for decrypt path, compression, protobuf, or msgpack
- hooked page fails but clean page works: suspect observer effect, remove invasive hooks, and recapture the baseline before deeper tracing

## Local helper scripts

Use the bundled local scripts when they are faster than re-deriving the same mechanics:

- `scripts/check_reverse_env.py`: confirm the local reverse stack quickly
- `scripts/crypto_fingerprint.py`: classify suspicious digest or alphabet outputs
- `scripts/protocol_diff.py`: compare captured requests or responses and surface the meaningful deltas
- `scripts/scaffold_reverse_project.py`: start a clean Python-first collector layout
