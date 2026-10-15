# Local SDK Env-Patch Playbook

Use this to run a vendor fingerprint / device-trust SDK outside a real browser page so Python can own HTTP, while a tiny local JS runtime only produces the companion payload.

## Contents

- [When to read](#when-to-read)
- [When not to read](#when-not-to-read)
- [Goal](#goal)
- [Runtime choice](#runtime-choice)
- [Bootstrap order](#bootstrap-order)
- [Crypto global](#crypto-global)
- [Config / Br apply path](#config--br-apply-path)
- [Host constructors](#host-constructors)
- [Capture and handoff](#capture-and-handoff)
- [Common crash ladder](#common-crash-ladder)
- [Delivery honesty](#delivery-honesty)
- [Related](#related)

## When to read

- Device-trust sidecar must be generated for the current mid
- Real browser UI is optional or toxic (automation detection)
- Official SDK is obfuscated; full field port is not yet cheaper than running the SDK
- Target shape is L2 local JS runtime under `references/device-trust-sidecar-playbook.md`

## When not to read

- Packer/track only; no fingerprint SDK
- Final delivery already pure Python (L3)
- You still lack a hybrid positive baseline

## Goal

```text
server-issued device config
  -> local runtime loads vendor SDK
  -> SDK emits companion request body (Log2-class)
  -> Python posts remaining chain and Verify
```

Browser automation is evidence tooling only, never the final collector path.

## Runtime choice

Preference order:

1. **Node + jsdom** (or similar DOM host) when the SDK expects `window/document/navigator`
2. Existing browser page only as temporary L0/L1 control
3. Heavier embedded browsers only if jsdom cannot satisfy native-surface contracts

Do not default to Playwright driving a full site login UI for collector delivery.

## Bootstrap order

Strict order; do not reverse:

```text
1) inject crypto provider expected by the SDK
2) install host constructors and critical BOM/DOM stubs
3) install network capture hooks (XHR/fetch) before SDK init
4) load vendor SDK script for the version returned by Init
5) build config object (deviceConfig + proto secrets) matching official apply shape
6) call official entry (initXxx / initFeiLin-class)
7) wait for companion body capture
8) return body to Python; same-session verify immediately
```

## Crypto global

Fingerprint SDKs often read a page global, not Node `crypto`:

- prove the exact global name from runtime/read of SDK (example family: `__ALIYUN_CRYPT`)
- provider must expose the methods actually called (`AES`, `HmacSHA1`, `MD5`, `enc.Base64`, ...)
- loading the captcha UI shell is not required if the crypto global can be injected directly
- fixed-input encrypt/decrypt parity against browser samples before trusting the provider

## Config / Br apply path

Distinguish three states:

| State | Meaning |
|---|---|
| official apply | SDK/path that decrypts DeviceConfig and extends runtime object (mr/rn-class) |
| manual incomplete | hand-built object missing proto secrets / side effects -> false "Init untrusted" |
| local reconstructed | deliberate reconstruction after dumping required keys/shape from a working apply |

Proof:

1. Capture a working runtime object at SDK entry from hybrid path.
2. Diff own props + prototype secrets against the manual object.
3. Prefer injecting Python Init JSON into official apply before rewriting apply logic.
4. Only then port reconstruction into the local runtime.

Required shape usually includes:

- session fields: key/secret, sessionId/mid, version, timestamp, ip
- endpoints / appKey / appName / scene
- proto secrets used by emit/sign (do not invent; dump from working path)
- logs/initTime if the SDK timestamps trust markers from them

## Host constructors

Missing hosts fail as `ReferenceError` / `TypeError` during SDK load, not only during emit.

Rules:

1. **Never auto-stub real builtins** (`Function`, `Object`, `Array`, `Promise`, `Symbol`, ...). A Proxy that fabricates capitalised names will break `Function.prototype.call.bind`.
2. Stub browser-only constructors the SDK probes: `Worker`, `SharedWorker`, `matchMedia`, storage quota helpers, audio/RTC piles as needed.
3. Prefer capability-complete empty implementations over foreign fingerprint caches.
4. Fix one missing name at a time; keep a crash ladder log.

## Capture and handoff

- Hook `XMLHttpRequest` and `fetch` before SDK init.
- Match companion by Action/path family, not by pretty UI callbacks.
- Preserve raw body encoding (`+` in base64 must not be `parse_qs`-broken).
- Python owns live HTTP when possible; if the runtime posts itself, still capture the body for rebuild/verify alignment.
- Return: companion body, mid, secret handle reference, n1/num if present, timestamps.

## Common crash ladder

Typical progression when offline-loading an obfuscated fingerprint SDK:

```text
missing crypto global (.AES)
  -> missing File/Screen/Location/CSSRule-class names
  -> polluted Function builtin (Proxy stub)
  -> missing matchMedia / webkitTemporaryStorage
  -> missing Worker
  -> SDK loads and emits
  -> verify fails on stale session (not host crash)
```

After emit works, stop host expansion unless a new branch is proved necessary.

## Delivery honesty

- L2 success = Python HTTP chain + local SDK runtime parameter restore
- Still document residual fingerprint ugliness (engine string, empty platform, coarse screen) if present
- Require multi-run stability before claiming collector readiness
- Next optional rung is L3 field port, not more UI automation

## Related

- device-trust gate model: `references/device-trust-sidecar-playbook.md`
- generic env patch surfaces: `references/environment-patch-playbook.md`
- embedded runtime doctrine: `references/embedded-browser-runtime-playbook.md`
- session freshness: `references/session-contract-playbook.md`
