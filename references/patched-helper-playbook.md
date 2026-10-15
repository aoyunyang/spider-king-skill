# Patched Helper Playbook

Use this reference when:

- helper names look standard, but outputs do not match standard libraries
- functions named `md5`, `btoa`, `atob`, `sha1`, or similar behave strangely
- local reproduction fails even though the helper name looks familiar

## Core rule

Names do not prove behavior. Fixed-input validation does.

## Minimum validation loop

1. choose a fixed input such as `"abc"` or a captured timestamp
2. record browser or page output
3. if the helper names a page-owned function or host class, stub that exact presence in the local world before declaring the primitive patched
4. run the local candidate implementation
5. compare intermediate states as well as the final output
6. test constant-pool prefix and suffix joins, and derived key slices, before declaring a patched compress function
7. if ascii hashlib and digit-byte hashlib both miss a frozen timestamp, keep the bundled helper and stub hasher-internal `eval` / `setInterval`
8. only then decide whether the helper is standard, patched, or fully custom

One matching vector is not algorithm equivalence. Require several fixed vectors across distinct fields or plaintexts. A vendor-named cipher can match a textbook implementation on a lucky input and diverge on ordinary text.

## Common signs of patching

- the output alphabet differs from normal Base64
- the digest matches neither standard MD5 nor SHA families
- the helper uses DOM state, side scripts, or odd lookup tables
- host-object imports exist, but no property-read imports feed the preimage
- unsalted textbook output misses while a constant-pool concat hits
- output length or padding rules differ from the standard implementation
- one short vector matches the standard library while a second field or longer plaintext diverges
- a local runtime without the page-owned helper diverges on "abc" while the browser helper is stable
- a local runtime missing `navigator` or `location` diverges on a named AES helper while the browser helper is stable; inspect catch-path key order before declaring AES patched
- a named AES.encrypt export yields 8-byte ciphertext on a short vector; the primitive is DES/3DES, not AES-128
- `instanceof` or constructor identity changes IVs or shift tables without reading DOM text

## Delivery rule

Ship fixed-input self-checks with the collector so future site changes fail loudly.

Vendor-blob eval helpers are allowed when they are the narrowest faithful calculator. Label them snapshot-driven. Do not ship an entire captured SDK from a volatile task cache as the official helper; extract the smallest module or pin a hashed snapshot with an explicit load path. A vendor-eval helper is a local calculator, not a browser.

Do not vendor a per-fetch obfuscated bundle as the official helper. Re-fetch or pin a hashed snapshot and extract the public function by structural anchors. If that public function already mints accepted tokens in a tiny Node vm, keep the harvest; do not escalate to iv8 or an inner Huffman/XOR port to chase gold-token equality.
