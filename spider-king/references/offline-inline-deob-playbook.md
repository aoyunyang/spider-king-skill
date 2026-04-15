# Offline Inline-Deob Playbook

Use this reference when:

- browser DevTools or `js-reverse` become unstable because of anti-debug code
- the page embeds large inline scripts instead of loading all logic from external files
- a signer depends on a packed payload such as `eval(atob(...))`
- a standard hash does not match the in-page result even though the function name looks familiar
- a request parameter contains unusual delimiters or unicode separators

## 1. When to stop fighting the live page

If any of these occur, switch to offline extraction instead of repeatedly poking the live runtime:

- debugger loops or `setInterval(debugger, ...)`
- console floods from anti-debug code
- MCP evaluation calls time out repeatedly
- reverse tools disconnect after page load

Fallback path:

1. save the full HTML
2. extract all inline scripts
3. save relevant external assets
4. deobfuscate and test locally

## 2. Extract the page structure first

Before decoding anything, record:

1. script tag count
2. inline script order
3. external script order
4. whether the page monkey-patches `$.ajax`, `fetch`, or XHR before the packed code runs

Do not assume script count is cosmetic. Some pages derive offsets from values such as:

- `$('script').length`
- DOM node counts
- element attributes
- query-string flags

These values can directly change the decoded payload.

## 3. Inline payload recovery pattern

Common sequence:

1. a giant encoded string is assigned to `window.a`
2. a loop transforms each character with an index-based offset
3. the result becomes a base64 string
4. `atob(...)` yields a second-stage script
5. `eval(...)` runs the real logic

Recommended workflow:

1. extract the encoded string and decoder
2. reproduce the exact offset math locally
3. recover the base64 payload
4. base64-decode it to the second-stage source
5. isolate only the signer or crypto section needed for replay

## 4. Legacy hash warning

Do not assume that `md5`, `sha1`, or similar names mean standard library equivalence.

Things to verify:

- custom `chrsz` or string-width settings
- custom string-to-word conversion
- little-endian vs big-endian assumptions
- patched constants or altered rounds
- hex encoding order

If the page ships a self-contained hash implementation, preserve that implementation first. Only replace it with a standard library version after proving the outputs match on fixed inputs.

## 5. Unicode delimiter safety

If a request value contains unusual separators, keep them explicit.

Examples:

- use `\\u4e28` instead of pasting `丨`
- use escaped strings in generated JS and Python output
- avoid trusting terminal or shell display for correctness

Why this matters:

- console output can replace the character with `?` or another glyph
- copied values can be silently corrupted by encoding
- a valid hash plus a broken delimiter still fails server validation

## 6. Practical delivery rule

For pages like this, prefer:

1. offline deobfuscation to recover the true signer
2. isolated `signer.js` that preserves the bundled hash or decoder
3. Python or Node collector that calls the isolated signer

This is usually more stable than trying to keep a hostile browser runtime alive.
