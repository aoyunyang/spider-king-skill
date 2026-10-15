# Crypto Patterns

Use this file when signatures, encryption, or helper outputs look suspicious.

## Contents

- [Standard-looking helpers that are often not standard](#standard-looking-helpers-that-are-often-not-standard)
- [Fast recognition checklist](#fast-recognition-checklist)
- [Fixed-input validation loop](#fixed-input-validation-loop)
- [Cross-runtime porting loop](#cross-runtime-porting-loop)
- [Modified standard digest family](#modified-standard-digest-family)
- [Host-function and instanceof digest branches](#host-function-and-instanceof-digest-branches)
- [Named digest with inner eval keeps the helper](#named-digest-with-inner-eval-keeps-the-helper)
- [JS to Python bitwidth traps](#js-to-python-bitwidth-traps)
- [TEA family fingerprints](#tea-family-fingerprints)
- [Key-in-bytecode recovery](#key-in-bytecode-recovery)
- [RSA ciphertext encoding is part of the contract](#rsa-ciphertext-encoding-is-part-of-the-contract)
- [Block-cipher wire framing](#block-cipher-wire-framing)
- [Signature, key-exchange, and national-crypto formats](#signature-key-exchange-and-national-crypto-formats)
- [Common failure modes](#common-failure-modes)
- [Constant-pool concat before custom compress](#constant-pool-concat-before-custom-compress)
- [Missing block avalanche keeps the bundle](#missing-block-avalanche-keeps-the-bundle)
- [Named AEAD or WASM envelope](#named-aead-or-wasm-envelope)
- [Decoy timestamp or PRNG wrappers](#decoy-timestamp-or-prng-wrappers)
- [Two-stage mix and size-fingerprint ciphers](#two-stage-mix-and-size-fingerprint-ciphers)
- [Delivery rule](#delivery-rule)

## Standard-looking helpers that are often not standard

- `md5`
- `sha1`
- `sha256`
- `sm3`
- `btoa`
- `atob`
- `hmac`
- `aes`
- `rsa`
- `sm2`
- `sm4`
- `ecdsa`
- `ecdh`
- `xxhash`
- `murmurhash`
- `tea`
- `xtea`
- `xxtea`

## Fast recognition checklist

- length matches a common digest size
- alphabet matches hex, Base64, URL-safe Base64, or a custom alphabet
- padding matches a standard encoder
- output changes with timestamp, page, or session state
- helper reads DOM, globals, or side-script state
- output is digest plus a short suffix digest, checksum nibble, or version fragment
- a UUID, nonce, or session value looks standard at first glance but contains an inserted fixed-width segment, prefix, or checksum-derived fragment
- the apparent key, iv, seed, or hash source comes from slicing, concatenating, trimming, or decorating a config field instead of using it directly
- a named national or textbook digest fails fixed-input parity while still producing the expected bit length
- printable strings in a WASM data segment or JS constant pool are prefix, suffix, or key-slice candidates
- Window/document/body imports without property-read helpers are existence gates until a string from that object enters the preimage
- missing contiguous IV bytes does not prove modified IVs; they may be `i32.const` while the T/K table lives in data
- repeated `2654435769` / `0x9E3779B9`, 32-round two-word loops, or 4-character little-endian word packing
- a named AES/GCM/AEAD helper can avalanche and still use a non-textbook nonce/tag order, suffix byte, or second frame
- 32-byte key material in WASM memory may be bitsliced/packed AES state, not raw key bytes
- AEAD open success is not plaintext until a pre-cipher XOR mask and trailing suffix are peeled

## Fixed-input validation loop

When request signatures also depend on method and body serialization, the fixed sample must freeze those exactly. A signature that validates against a nearby regenerate route is not proof for first-create if method or body placement differs. The signer must cover the real method and the real serialized query or body used on the wire.

1. freeze a tiny input such as `"abc"`
2. freeze a live input such as a captured timestamp
3. compare browser output with local output
4. compare intermediate strings, not only final digests
5. for random PKCS#1 RSA, do not require ciphertext equality with a captured gold token; prove padding and live decrypt or typed accept

## Cross-runtime porting loop

When porting JS logic to Python or another runtime:

1. freeze the same config blob, timestamp, nonce, UUID source, and fingerprint vector
2. compare normalization outputs first, such as compact JSON, sliced key material, prefixed payloads, or checksum inputs
3. compare the final cookie, token, or sign output only after the intermediate forms match
4. keep one deterministic parity vector before trusting live traffic
5. when a browser-only branch exists, reproduce that branch locally before porting constants into Python

## Modified standard digest family

Treat `md5`, `sha*`, and `sm3` names as untrusted labels until fixed samples match.

Locate the implementation first, then diff against the standard algorithm in this order:

1. IV or initial chaining value
2. round or message constants such as `Tj` / `K`
3. string-to-bytes or packing helpers, including per-byte masks
4. compress-step masks that replace modular arithmetic
5. expand, FF/GG, P0/P1, padding, and final hex encoding

Working method:

1. freeze one captured preimage and one wire digest
2. search for environment branches such as `typeof X === "function" && String(X) === "function X() { [native code] }"`, page-owned `typeof helper === "function" && helper`, `instanceof` host-class checks, `typeof require` / `__dirname`, native-looking `print`, `setImmediate`, native `Date.now`, and prototype identity
3. record the browser-branch constants and helpers separately from any Node or fallback branch
4. port the browser branch first as a local replica; do not eval the harvested digest file in Node as the oracle, and do not average branches
5. keep standard parts only after each has matched on the fixed sample

Do not promote one challenge's constants into a global "modded SM3" recipe. Preserve the checklist and the parity method, not the one-off IV table.

## Host-function and instanceof digest branches

Use this when a named digest matches neither textbook output nor a local eval of the same file.

A digest can keep textbook round structure while selecting IVs, round constants (`Tj` / `K`), packing masks, and compress masks from host presence, not only from native-code string checks. Those predicates can also be sampled inside the compress loop: a rotating array of `typeof window/document/Worker/fetch/requestAnimationFrame` checks can pick a per-round ternary K. If every Chrome-path check is true, the table collapses to the true branch; missing Node globals such as `Worker` or `requestAnimationFrame` select the other table. That is still a branch selector, not proof the round function is unnamed. Do not average the two K tables.

- `typeof pageHelper === "function" && pageHelper` where `pageHelper` is page-owned, not `[native code]`
- `window instanceof EventTarget` / `Window`, `document instanceof Document`
- presence or absence of host classes such as `WindowProperties`
- `typeof require`, `typeof __dirname`, native-looking `print`, `setImmediate`, native `Date.now`, or `document.__proto__ === HTMLDocument.prototype`
- `try { if (navigator) {} } catch` / `try { if (location) {} } catch` inside cipher `_doReset` or `clamp`

Working method:

1. freeze textbook `md5("abc")` or the named helper's tiny input in the browser
2. do not treat Node or iv8 eval of the harvested digest file as that browser oracle; missing `setImmediate`, present `require`/`__dirname`, or non-HTMLDocument prototypes select a different IV, packing, or compress mask, and anti-debug constructors can hang
3. if those two diverge, the miss is the branch selector, not proof that the compress function is unnamed
4. port the observed browser branch as a local replica; stub page-owned functions or host-presence gates until the tiny input matches the browser
5. only then freeze live preimages and decide whether a Python port is cheaper than keeping the bundled helper

Per-byte packing such as `& 0xfe` collides even/odd ASCII digits. Same-clock tokens on nearby pages are packing evidence, not interchangeable requests; live still refreshes the clock. Flavor text that a session id "may enter" the digest, and debug-UI concatenations such as `"GET " + url + "?"`, are not preimage until the writer reads them. Native `Date.now` can select `Tj`/`K` without being the request clock.

Do not average the fallback branch with the browser branch. Do not eval the harvested digest file in Node to "see what it does". Do not eval a function reconstructed from a nearby charcode array. Do not promote one helper name, IV table, or mask set into a global stub list. `Window` / `Document` instanceof checks remain existence gates until a string from that object enters the preimage.

The same host-presence split applies to named ciphers, not only digests. A `try { if (navigator) {} } catch` or `try { if (location) {} } catch` inside `_doReset` or `clamp` can reassign DES key slices or clamp masks. A Node or iv8 run that omits those hosts takes the catch-path schedule. That miss is not proof the export is patched AES. Port the browser branch (host object present) as the positive replica and keep the catch-path as a negative control.

## Named digest with inner eval keeps the helper

Use this when a CryptoJS-shaped MD5 (`_ff` / `_gg` / `_hh` / `_ii`) sits next to a timestamp field, or a named digest still misses hashlib on a frozen clock.

1. Freeze one timestamp and the bundled digest.
2. Compare ascii hashlib and digit-byte hashlib on that same clock. If both miss, keep the bundled helper; Python owns HTTP.
3. The first large integer array may be charcodes of a function, not T constants. Reconstructing it is not preimage recovery.
4. If `bytesToHex` or a round helper does `eval('!'+R+'()')` or `setInterval(eval, ...)`, stub `eval` and timers, keep the digest, and never execute recovered R. In a browser that eval often fails into `Date.now()`. Node is worse because `require` exists.
5. HTTP 403 JSON forbidden on this API while sibling APIs on the same session return 200 is not session death. Replay the same admitted token bytes on stdlib versus installed curl impersonate before calling it a digest/clock pair. Impersonate business 200 means transport admission; impersonate 403 then freeze the clock and keep the bundled helper.

Do not promote one helper's recovered R payload or module ids.

## JS to Python bitwidth traps

These are recurring port failures when a JS digest is moved into Python:

- `>>> 0` becomes `& 0xFFFFFFFF`; apply the mask after every arithmetic step that JS would force into uint32
- `ROTL(x, n)` must normalize `n %= 32` and treat `n == 0` as identity. Naively writing `((x << n) | (x >> (32 - n)))` breaks when `n == 0` because Python `x >> 32` is `0`, while JS `x >>> 32` is equivalent to `x >>> 0`
- `~x & z` with a bounded positive `z` usually needs no special case beyond a final `& 0xFFFFFFFF`
- per-byte masks such as `& 0xfe` must apply to every emitted byte, not only the first code unit; even and odd ASCII digits then collide, so same-clock digest equality is packing evidence, not interchangeable pages
- mask-before-shift order matters; preserve `sum & mask` versus `(sum >>> 0) & mask` exactly as the page does

Minimum port self-check:

1. one fixed preimage from the live request
2. browser or Node-branch digest
3. Python digest
4. at least one intermediate word or masked byte string when the final hex still disagrees

## TEA family fingerprints

Use this when ALU traces, bytecode constants, or unpacked words look like TEA-family mixing rather than a named digest.

Recognition:

- repeated `2654435769` / `0x9E3779B9` (delta)
- 32-round loops over two uint32 words
- a 128-bit key split into four uint32 words
- JS `>>>` standing in for C unsigned `>>`

A delta hit is family evidence, not a finished ID. Distinguish variants from the mixing shape:

| Variant | Inner mix | Key schedule |
|---|---|---|
| TEA | `((v<<4)+k0) ^ (v+sum) ^ ((v>>5)+k1)` | fixed slots `k0..k3` |
| XTEA | `((x<<4) ^ (x>>5)) + x` | `key[sum & 3]` and `key[(sum >> 11) & 3]` |
| XXTEA | MX-style mix over an array of words | `sum` plus `e` / index terms |

Working method:

1. freeze two adjacent ciphertext blocks from one run
2. overlap their ALU sequences and keep the repeated constants
3. match both the inner mix and the key-index expression
4. port the named variant with `& 0xFFFFFFFF` after every add
5. only then recover key material (`Key-in-bytecode recovery`)

Do not promote one target's round count, padding character, or export name into a global TEA recipe.

## Key-in-bytecode recovery

Use this when the algorithm is identified but the key is not a string, config field, or static hex blob.

This is common when a VM embeds key words in the current bytecode. Treat that key as session material, not a collector constant.

Method:

1. freeze the algorithm and name the unique key-mixing operation (for XTEA: `sum + key[idx]`)
2. list values the algorithm can produce without the plaintext (for XTEA: `sum = (i * delta) & 0xFFFFFFFF` for `i = 0..32`)
3. record operands of that mixing op only; do not dump every add
4. vote the other operand and drop the delta itself
5. if slot order is unknown and the permutation space is tiny (XTEA: `4! = 24`), brute the order
6. accept only against a plaintext oracle: a known JSON prefix, a stable field name, or printable structured text
7. keep the extracted key task-local and bound to the current bytecode hash

Report the port as snapshot-driven / helper-extracted until a later job proves the key is static. Do not search for a 16-byte hex string first, and do not ship a regex that matches one vendor's add handler.

WASM memory may hold bitsliced AES state rather than raw key bytes. If 32 captured bytes look interleaved rather than key-shaped, unpack with the public fixslicing `SWAPMOVE` family (`0x55555555/1`, `0x33333333/2`, `0x0f0f0f0f/4`), then require both 16-byte halves to match. Unequal halves are a capture error, not a reason to invent a new cipher.

## RSA ciphertext encoding is part of the contract

When a login or bootstrap page ships an RSA modulus and exponent:

1. parse the current page values; do not assume they are stable forever
2. encrypt with the page's padding scheme, commonly PKCS#1 v1.5 for legacy forms
3. encode the ciphertext exactly as the page does before putting it into the wire field

Encoding traps:

- the page may require hex, Base64, URL-safe Base64, or another alphabet
- a 2048-bit RSA ciphertext is 256 bytes; hex is 512 characters, while standard Base64 is shorter
- wrong encoding often surfaces as a fake business error such as bad password or system exception

Fixed-input method:

1. freeze modulus, exponent, plaintext password or placeholder, and the page's ciphertext
2. match encoding and letter case before blaming the account
3. keep the verified encoder next to the collector's login path

Named JSEncrypt, SPKI, JSBN, or RSA under statement-split is still PKCS#1 v1.5 until padding and concat miss. Freeze the pad string before choosing an oracle: random type 2 makes gold-token inequality expected and live decrypt or typed accept is the oracle; a proved constant PS makes gold-token equality valid; type 1 `00 01 FF` and textbook raw are different writers. Do not gcd raw `P^e-C` until the padded EM is captured. A second harvested SPKI or `document.all` key is an untaken branch until the live writer selects it; that branch may swap a whole key or only add a limb delta, so a stored even limb array is not live `n` by itself.

## Block-cipher wire framing

The primitive is not the wire field.

After a TEA-family or other 64-bit block cipher, record independently:

1. character or byte packing endianness (often 4 chars -> little-endian uint32)
2. block size and padding character or PKCS-style pad
3. whether output is raw bytes, a JS string of those bytes, hex, Base64, or URL-safe Base64
4. a second encoding such as `urllib.parse.quote` with a non-default `safe` set
5. which request field receives the framed blob

Fixed-input check: the same plaintext and key must match the captured wire field after framing, not only after the last `encrypt_block` call.

The same law applies to AES, GCM, and other AEAD helpers: the primitive is not the wire field. Independently freeze key size; whether memory holds raw key bytes or packed/bitsliced state; nonce and tag sizes; component order (`nonce||ct||tag`, `ct||tag||nonce`, or another layout); a prefix or suffix magic byte; Base64 versus raw; whether a XOR mask or trailing `end` blob sits inside the AEAD plaintext; and whether the same helper emits a second frame on another path. Compare the captured wire field, not only `encrypt_and_digest` output.

## Signature, key-exchange, and national-crypto formats

Treat the primitive name and the wire representation as separate claims.

### SM2 and SM4

- Distinguish SM2 signatures from SM2 public-key ciphertext. A pair of signature integers is not a `C1C3C2` or `C1C2C3` ciphertext.
- Record the SM2 curve, public-key prefix and point encoding, user-id input when signing, ciphertext component order, and final hex/Base64 framing.
- For SM4, freeze mode, key bytes, IV, padding, plaintext encoding, and output alphabet. `ECB` versus `CBC`, zero padding versus PKCS#7, and text keys versus decoded key bytes are independent dimensions.
- Require one published known-answer vector for the primitive and one captured envelope vector for the application-specific framing.

### ECDSA and ECDH

- For ECDSA, record curve, message-versus-prehash input, hash, deterministic or random nonce behavior, low-S normalization, and whether the wire value is ASN.1 DER or fixed-width raw `r || s`.
- For ECDH, record curve, compressed or uncompressed public-key encoding, peer-key validation, shared-secret width, KDF, salt/info/context, and the exact slice used as the downstream key.
- A matching shared secret does not prove a matching envelope. Compare KDF output, nonce/IV construction, authenticated data, tag placement, and ciphertext encoding separately.

### Non-cryptographic hash families

For xxHash, MurmurHash, and similar checksums, freeze algorithm variant, seed, input bytes, signed/unsigned interpretation, bit width, byte order, avalanche output, and final text encoding. Do not infer a cryptographic authenticity guarantee from a checksum-shaped field.

### Hybrid envelope checklist

When a payload combines symmetric encryption with RSA, SM2, ECDH, or another key wrapper, split and verify:

1. normalized plaintext bytes
2. generated or derived content key
3. nonce or IV
4. ciphertext and authentication tag
5. wrapped key or ephemeral public key
6. component ordering and length prefixes
7. final JSON, protobuf, hex, Base64, or custom-alphabet envelope
8. pre-AEAD XOR mask and trailing suffix, verified only after open succeeds
9. whether the same helper is reused with a different frame on another path

Keep keys and captured ciphertext task-local. Promote only the layout and verification method.

## Common failure modes

- standard Base64 library used against a patched alphabet
- standard MD5 or SM3 used against a custom string-to-word packing step
- URL-encoding mismatch before hashing
- wrong timestamp precision
- hidden page or session state included in the input
- correct hash function applied to the wrong JSON serialization, item order, or compactness rule
- standard UUID or random hex used where the protocol expects a structurally constrained local identifier
- apparent key or iv used directly when the page normalizes it through slice, concat, trim, or wrapper removal first
- jumping to a patched digest because unsalted `md5(caller)` missed a constant-pool suffix
- treating wasm-bindgen `document.body` as hashed DOM state when the import is only an existence check
- recomputing an accepted bundle or version hash from current file bytes when the client actually uses an embedded compatibility id
- standard library digest used because the name matched, while IV, round constants, or compress masks were rewritten
- Python ROTL or uint32 truncation that only fails on some pages or some `j` values
- RSA ciphertext encoded with the wrong alphabet or case after a correct encrypt step
- naming TEA, XTEA, or XXTEA from the delta constant without matching the inner mix and key schedule
- treating a bytecode-resident key as a hardcoded collector constant
- matching the cipher but missing little-endian packing, space padding, or post-cipher Base64/URL encoding
- claiming a fully algorithmic port while the key still requires executing the current VM blob
- submitting a named wrapper digest whose preimage includes `Date.now()` or PRNG bytes the server never stored
- treating a clock-independent first mix as proof the preimage is unused, or hardcoding sign length from one sample
- wrapping `Number.prototype.toString` or `TextEncoder.encode` to debug a host mix
- blaming the mixer when HTML and inline script come from different worlds
- discarding a server-issued clock because a previous job taught that `Date.now` wrappers are decoys
- freezing an inner Date constructor while the request clock is a signer argument or query field
- porting Huffman/XOR to chase gold-token equality after live replay already accepted the public writer
- treating a named AES/MD5 helper as a textbook port when two nearby plaintexts share a long unchanged ciphertext prefix
- treating a named AES helper as AES-128 because a longer token is 16-aligned while a short vector is 8 bytes
- treating a Node miss of a named AES helper as patched AES when a navigator/location catch-path reorders DES key slices
- treating named AES/GCM open success as plaintext while a XOR mask or trailing suffix still remains
- assuming one GCM/AEAD helper has one wire frame across request and response paths
- treating WASM memory bytes as a raw AES key without a packed/bitsliced unpack and half-equality check
- treating a local Node or iv8 miss as a patched compress function when a page-owned helper or instanceof gate was never stubbed
- evaling a harvested digest file in Node or iv8 and treating that output as the browser oracle
- averaging a missing-helper fallback branch with the browser-selected IV or shift table
- treating two pages that hash to the same digest as interchangeable requests
- treating same-clock digest equality after a per-byte packing mask as interchangeable pages
- copying debug-UI `"GET " + url + "?"` or flavor-text session claims into the preimage before the writer reads them
- treating native Date.now as the request clock when it only selected round constants
- cloning a sibling digest because path + clock + page concat looks the same while the current writer is RSA, or the reverse
- treating a `$fast_unpack` / magic-`WAFJ` wrapper as the hasher instead of unpacking to the concat and digest
- averaging per-round ternary K tables from Chrome-all-true versus Node-missing-Worker
- encrypting with a second harvested SPKI or document.all key that the live writer never selected
- treating random PKCS#1 ciphertext inequality against a captured token as a broken or custom RSA port
- treating a deterministic PKCS#1 ciphertext as textbook raw RSA, or gcd'ing raw `P^e-C`, before capturing the padded EM
- cloning sibling random PKCS#1 because concat looks similar while the current pad string is a constant PS, or the reverse
- treating a stored even JSBN limb array as `n` when the live writer adds a one-limb delta
- treating a charcode array next to MD5 as T constants, or evaling the reconstructed function in Node
- swapping session or blaming WAF because textbook MD5 got 403 while sibling APIs on the same session return 200
- porting hashlib after ascii and digit-byte both miss a frozen timestamp

## Constant-pool concat before custom compress

Use this before rewriting IVs, round functions, or a WASM `MD5` implementation.

A named digest that misses `standard_md5(caller)` is not yet a patched primitive.
Recover concat and slice material first:

1. freeze one captured caller string and one captured digest
2. compute the unsalted textbook digest
3. recover printable constant-pool or data-segment strings and derived slices
4. test `caller + suffix`, `prefix + caller`, and any documented derived key slice
5. keep the textbook primitive when a join or slice hits
6. after a path + clock (+ page) join hits, still test an extra constant or match-number join, including a delimiter-bearing suffix such as `N$` or `N()`, before calling the primitive patched. A debug flag that only bumps that join is concat evidence, not an IV change
7. only after those joins miss, diff IV, T/K, packing, padding, and compress masks

Concat family is not calculator family. The same join can feed a digest on one job and RSA on the next.

Host-object imports are a separate question. If `document.body` is imported, cloned, and dropped without `innerHTML`, `textContent`, or `getAttribute`, treat it as an existence gate, not as hashed DOM state.

The secret-free fixture is `references/experience-fixtures/standard-primitive-concat-matrix.json`.

## Missing block avalanche keeps the bundle

Textbook AES changes a full 16-byte block when one plaintext byte flips.

If two nearby plaintexts share a long unchanged ciphertext prefix, the named AES or MD5 helper is not a standard-library port yet.

After unsalted and concat or slice checks miss:

1. freeze two captured plaintexts and their wire fields
2. measure whether a 16-byte block actually avalanches
3. if it does not, keep the bundled helper and harvest at the public exit
4. do not invent a Python AES or MD5 from the marketing name

The inverse trap is equally live. Textbook-looking avalanche only proves the inner primitive may be real AES/GCM. It does not prove a standard-library wire. After avalanche hits, still freeze frame, packed-key layout, XOR/end, and inner-field ciphers before shipping a standard AEAD library.

## Named AEAD or WASM envelope

Use this when a helper is named AES, GCM, or an encrypt/decrypt WASM export, including when avalanche already looks textbook.

Named AEAD is a hypothesis. Climb cheapest-first:

1. Harvest a public multi-arity export as an oracle when it already returns wire-shaped ciphertext or plaintext. Do not decompile a megabyte WASM/WAT dump first. Probe minimum input length; too-short buffers may skip key schedule.
2. Freeze the framing matrix from `Block-cipher wire framing` and `Hybrid envelope checklist` before calling a standard library.
3. Locate key and plaintext sites by instruction-sequence templates, not export names. Template hit cardinality classifies raw versus packed layout; mutually exclusive templates must not both match.
4. If memory looks packed, unpack bitsliced AES state and verify both 16-byte halves. See `Key-in-bytecode recovery`.
5. Verify in layers: AEAD open first, then peel trailing `end`, then XOR. Open success is not JSON. If no gold pair `(plaintext, ciphertext, key)` exists, keep the export as the oracle; do not invent a mask.
6. With a gold pair, recover `(xor_key, end)` by XOR against the opened bytes. Replay until mask length breaks, then recapture a longer pair or extend a recovered repeating block. Do not reverse the mask generator first.
7. After JSON appears, numeric-id fields may be a second stream-cipher family. Recover the algorithm class and which constant rotates. Anchor on a stable `i32.const` and keep the smaller enclosing function; discard a giant function that repeats the same constant.
8. Treat WASM/WAT as evidence. Scan with bounded templates. Never dump a megabyte file into the working transcript. Python replays frozen key, frame, mask, and inner PRNG; the dump is not collector runtime.

Keep vendor field IDs, magics, suffix bytes, and export arity flags task-local. Do not freeze one captured frame as a global law. If the export I/O is already wire-shaped, harvest it with `references/challenge-artifact-harvest-playbook.md` before rebuilding the encrypt chain.

## Decoy timestamp or PRNG wrappers

A named export that hashes `Date.now() + caller + localRandom` is not a live verifier unless those extra bytes are also sent.

Before porting that wrapper:

1. freeze the current document's public token, not a saved token of the same length
2. call the inner hasher on that token alone
3. if that misses, try session id plus token
4. only then treat the timestamp/PRNG wrapper as a candidate

Same-session negative control: wrapper digest on the live token must be allowed to fail without disproving the inner hasher on the document token. A later GET of the challenge document can rotate the token; do not reuse a previous HTML constant.

The opposite case is also live until tested: the page replaces `Date.now` with a synchronous server clock, and that same value is sent as a header, query, or body field. Freeze that clock with the digest. If the extra bytes never appear on the wire, the wrapper is still a decoy. If they do, they are preimage, not decoration.

Discriminant:

1. freeze one clock value and confirm the digest is stable
2. check whether those bytes are copied onto the request
3. only then keep or discard the clock as preimage

A server-issued clock is still unbound until it enters the writer the signer actually reads. Freezing `Date.now` does not bind the request clock when the signer copies an ajax-success, callback, signer argument, query clock field, or other host field.

Observed-writer discriminant:

1. name the writer the signer reads
2. inject the server clock into that writer
3. confirm those bytes appear on the request
4. keep a `Date.now` freeze only when that getter is the observed writer

The observed writer can be a signer argument or query clock field, not only an ajax-success callback. An inner `+new Date` or local Date constructor inside the signer is a quieter sibling until those bytes are the ones copied onto the request. Leave the inner Date on the system clock when the request clock is the signer argument.

Gold-token inequality against a hooked browser sample is not a Huffman/XOR or custom-compress trigger when live replay already passes. Inner Date, environment scores, or rotating source can make a gold freeze fail while the public writer remains the accepted calculator.

The secret-free fixture is `references/experience-fixtures/server-clock-observed-writer-matrix.json`.

## Two-stage mix and size-fingerprint ciphers

Some signers run two mixes on the same helper:

1. **Placeholder mix**: can ignore wall clock and even a changing `url|ts` preimage. Hex is often **unpadded**. A stable first mix is a placeholder, not proof the preimage is unused forever.
2. **Host mix**: consumes the first-mix hex as ASCII and is host-bound. Hex is often **padded**. Output length tracks `2 * first_mix_hex.length`; do not hardcode a byte count from one sample.

Discriminants:

- a one-token ajax placeholder replacement that changes host-mix length is payload-in-mixer, not string-pool corruption
- freeze same-world HTML + script + clock before blaming the mixer
- Chrome replica matching on the host mix does not prove a jsdom replica; route host gaps to `references/environment-patch-playbook.md` and `references/env-diff-playbook.md`

Size-fingerprint triage for short opaque blobs. Treat the table as a first textbook hypothesis, then fixed-input:

| Key length | Ciphertext | First textbook try |
|---|---|---|
| 8 bytes | multiple of 8 | DES-ECB + PKCS5/PKCS7 |
| 16 bytes | not 16-aligned, or no PKCS pad | RC4 / stream |
| 16 bytes | multiple of 8, and a short vector is 8 bytes | 2-key 3DES-EDE + PKCS7 |
| 16 bytes | multiple of 16 AND a short vector is 16 bytes | AES-ECB + PKCS7 |

A longer ciphertext that happens to be a multiple of 16 does not prove AES. Freeze a short plaintext such as `"hello"` (5 bytes): 8-byte ciphertext means 64-bit blocks (DES or 2-key 3DES-EDE) even when the key is 16 bytes and the live token is 16-aligned; 16-byte ciphertext means AES-class blocks. CryptoJS `algo.AES.blockSize === 2` / `keySize === 6` is Triple DES wearing an AES name. Do not port AES-128 because the export is `AES.encrypt`. If a local runtime without `navigator` or `location` then diverges, compare the browser key order to the catch-path order before declaring patched AES.

If key and ciphertext are both 16 bytes, treat AES-ECB and RC4 as sibling hypotheses; PKCS pad validity is the discriminant. A second layer can reuse the same fingerprint with a derived key, including the previous plaintext. Strip UI prefixes from fields before a concat digest. Do not freeze one site's field names as the law.

## Delivery rule

Do not call crypto "done" until fixed-input self-checks are in the collector and any cross-runtime port has at least one deterministic parity vector. If key material lives in per-session bytecode, report the delivery as snapshot-driven or helper-extracted, not fully algorithmic.
