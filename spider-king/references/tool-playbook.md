# Tool playbook

Use this file as the fast map from reverse-engineering task to tool choice.

## Preferred order

1. Find the real request.
2. Trace the initiator.
3. Locate the signer or encoder.
4. Hook and compare runtime values.
5. Reproduce one stable request.
6. Scale collection only after the first request is repeatable.

Prefer hooks over breakpoints and summaries over loading giant bundles into context.

## Recon and network capture

### `js-reverse`

- `new_page` / `navigate_page`: open the target and follow the real landing URL
- `list_network_requests`: list XHR, Fetch, document, script, and preflight traffic
- `get_network_request`: inspect the chosen request in full
- `get_request_initiator`: jump from request back to the caller stack
- `list_websocket_connections`, `analyze_websocket_messages`, `get_websocket_messages`: analyze streaming sites
- `get_storage`: inspect cookies, localStorage, and sessionStorage values

### `chrome-devtools`

- `take_snapshot`: inspect page structure fast
- `wait_for`: wait on target text while triggering filters, search, or pagination
- `list_network_requests` and `get_network_request`: second source of truth when UI flow matters
- `take_screenshot`: capture evidence for hidden panels, captcha gates, or lazy regions

Use browser DevTools when DOM state matters. Use `js-reverse` when JavaScript runtime, request initiators, or hooks matter.

## Static JS analysis

- `list_scripts`: enumerate candidate bundles
- `search_in_sources`: search keywords across all loaded sources
- `find_in_script`: find exact offsets in minified bundles
- `get_script_source`: inspect the exact function neighborhood
- `summarize_code`: get a fast mental model before reading raw code
- `understand_code`: ask for business or security structure in suspicious areas
- `detect_crypto`: identify likely crypto families
- `deobfuscate_code`: unwrap string tables, flow flattening, and obvious packing

Keyword packs:

- request path: `"/api/"`, `"graphql"`, `"fetch("`, `"axios"`, `"XMLHttpRequest"`
- signer: `"sign"`, `"token"`, `"nonce"`, `"timestamp"`, `"trace"`, `"x-sign"`, `"beforeSend"`, `"ajaxSetup"`, `"requestId"`
- crypto: `"md5"`, `"sha"`, `"hmac"`, `"aes"`, `"rsa"`, `"crypto.subtle"`
- environment: `"navigator"`, `"canvas"`, `"webgl"`, `"performance"`, `"webdriver"`

## Dynamic validation

Start with hooks. Breakpoints are for local-variable proof after hooks narrow the target.

### High-value hooks

- `hook_function` for global or object methods such as `fetch`, `XMLHttpRequest.prototype.open`, `XMLHttpRequest.prototype.send`
- `create_hook` plus `inject_hook` for custom hook logic when you need field extraction or storage observation
- `trace_function` when the function is buried inside bundled code but still named
- `get_hook_data` to read the captured arguments, return values, and summaries
- `monitor_events` for search boxes, buttons, scroll triggers, and tab switches when UI actions drive requests

### Breakpoint tools

- `set_breakpoint_on_text`: best when the bundle is minified
- `get_paused_info`: inspect locals and scope
- `evaluate_on_callframe`: print the exact pre-sign string, key, iv, or payload
- `resume`, `step_over`, `step_into`, `step_out`: only after you already know why you are pausing

## Session and environment handling

- `get_storage`: inspect cookies and storage
- `evaluate_script`: rerun page-exposed bootstrap functions, refresh timestamp slots, and verify current in-memory request values
- `evaluate_script`: decode runtime key material or replay helper conversions when key/iv strings are not plain text or hex
- `save_session_state` / `restore_session_state`: preserve login state or replay a warm session
- `inspect_object`: inspect runtime helpers or globals such as `window.__NUXT__`, webpack caches, or SDK objects
- `diff_env_requirements`: compare Node failures against observed browser capabilities

## Failure routing

- `403`, `412`, `429`: compare headers, cookies, sign freshness, and request pacing
- business error with normal `200`: compare payload assembly order and timestamp precision
- decrypt failure after a successful `200`: verify whether the runtime key/iv is transformed through a helper such as digit-pair-to-char before AES is applied
- empty data: verify pagination, filters, referer, login state, and cursor evolution
- occasional success: inspect one-time tokens, session refresh, or concurrent request coupling
- first request works but immediate replay fails: compare cookie mutation, in-memory timestamp slots, and whether a page refresh function must run before every request
- response gibberish: search for decrypt path, compression, protobuf, or msgpack

## Local helper scripts

Use the bundled local scripts when they are faster than re-deriving the same mechanics:

- `scripts/check_reverse_env.py`: confirm the local reverse stack quickly
- `scripts/crypto_fingerprint.py`: classify suspicious digest or alphabet outputs
- `scripts/protocol_diff.py`: compare captured requests or responses and surface the meaningful deltas
- `scripts/scaffold_reverse_project.py`: start a clean Python-first collector layout
