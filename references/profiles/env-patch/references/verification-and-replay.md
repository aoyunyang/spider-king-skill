# Verification And Replay

Use this reference after `env-diagnose.js` can load the target script. Loading success is only a syntax/runtime milestone; it does not prove the target sign, token, cookie, or encrypted field is accepted by the server.

## Contents

- [Function Verification](#function-verification)
- [Four Verification Levels](#four-verification-levels)
- [Host-fidelity L0-L4](#host-fidelity-l0-l4)
- [Fixed Vector Capsule](#fixed-vector-capsule)
- [Runtime Continuity Check](#runtime-continuity-check)
- [Packaging A Callable Interface](#packaging-a-callable-interface)
- [HTTP Replay Checks](#http-replay-checks)

## Function Verification

`success: true` is not functional success. Verify the target behavior in a task-local runner such as `js_reverse_cache/tasks/<task-id>/env/run.js`, using the same environment modules selected during diagnosis.

Recommended flow:

1. Build `js_reverse_cache/tasks/<task-id>/env/run.js` with the same env modules and the target script.
2. Trigger the target behavior, such as an SDK init call, an XHR send, or a direct sign function call.
3. Check output shape against browser evidence, such as sign length, prefix, segment count, encoding, or cookie name. Treat this as triage only.
4. Compare the exact output and final wire-shaped URL/header/body with a fixed browser vector.
5. Only then package the callable sign/token interface or try HTTP replay.

For hook-style SDKs, keep this loading order:

```text
env modules -> fake XMLHttpRequest -> target JS -> capture hook -> init(config) -> trigger request
```

Important details:

1. Fake `XMLHttpRequest` must exist before loading the target JS if the target patches its prototype at load time.
2. Capture hooks such as `URLSearchParams.append` should be injected after the target JS if the target may replace native APIs with polyfills.
3. SDK `init` or `setup` parameters must be captured from the browser when they decide path matching or feature switches.

Common failures after load succeeds:

| Symptom | Likely Cause | Check |
|---|---|---|
| Sign is `undefined` | Missing crypto/performance dependency | Review selected env modules |
| Hook runs but does not sign | Missing SDK init params or path whitelist | Capture init params in the browser |
| Capture hook never fires | Hook injected before a target polyfill overwrote it | Move capture hook after target JS |
| JSVMP silently fails | Internal try/catch swallowed errors | Instrument known error exits cautiously |
| Sign length differs from browser | Environment fingerprint mismatch | Collect real browser seeds and patch minimally |

## Four Verification Levels

Report the highest level actually passed:

1. `load-pass`: the target parses and initializes far enough to expose the expected surface. This proves no signing behavior.
2. `activation-pass`: after the real `init`/`setup` contract, a registered business-shaped request changes at the expected query/header/body slot while an unregistered control does not. Test XHR and fetch separately when both exist.
3. `fixed-vector-pass`: after every dynamic input is frozen or replayed, the exact output and canonical wire bytes match a browser vector under the captured profile. Correct length, alphabet, prefix, or non-empty output is not enough.
4. `live-acceptance-pass`: Python owns the real HTTP request and a downstream business oracle accepts it. HTTP 200, HTTP 200 with an empty body, or a transport-success wrapper without expected business data does not pass.

If two consecutive environment-patch rounds do not advance the first divergence, or if activation configuration is incomplete, stop widening the environment and return to entry/trace evidence. If Node cannot express the required host semantics honestly, keep the result at `local-proof` or change the runtime boundary explicitly.

## Host-fidelity L0-L4

These levels score local-versus-browser host behavior. They are not the four verification levels above.

| Level | Score | Not this |
|---|---|---|
| L0 count | native `Math.random` / `Date.now` / `eval` order of magnitude | canvas/`navigator` JS-shim probe counts |
| L1 sequence | key native API LCS after noise filter | unfiltered timer-polling noise |
| L2 value feed | consume the same-session recorded values | a new-session script with an old feed |
| L3 protocol | submitted param-name set matches | length/alphabet heuristics |
| L4 eval sha256 | SDK compile-body hash order | third-party script evals |

A host that only shims canvas/navigator cannot claim L0 from those shims. Feed the shim values, or mark the surface unavailable.


## Fixed Vector Capsule

Exact equality is meaningful only when both runs consume the same complete input world. Save a secret-free task-local capsule beside the browser vector with:

- target script hash/build and helper/engine version
- method, URL, ordered query, selected ordered headers, and exact body bytes before every writer
- wall-clock value, timezone, `performance.now()`, `performance.timeOrigin`, elapsed-time inputs, and timer schedule when read
- RNG bytes, nonce, counters, UUID seeds, and any deterministic seed injection
- session/bootstrap/round identifiers or hashed state references, plus writer order and warm-up state
- one coherent browser/transport profile identity and the final query/header/body wire slots

Replay or inject the capsule values before exact comparison. If a dynamic source cannot be observed or controlled, name it and do not call an exact mismatch an environment divergence. Stay at `activation-pass`, or compare a proved deterministic intermediate, until the missing source is captured; live acceptance is separate evidence and does not retroactively manufacture a fixed vector.

## Runtime Continuity Check

When the same target helper is called more than once, runtime lifetime is part
of the fixed-input world until disproved. Run the persistent-world, fresh-world,
and explicit-state-ablation matrix from `../../../runtime-state-continuity-playbook.md` before widening browser APIs or packaging a per-call subprocess.

Record whether the browser keeps one page world, worker, VM/context, module
instance, closure, cache, queue, PRNG, or lazy initialization across calls.
Passing only the visible counter, cookie, bootstrap tuple, or function
arguments is not continuity proof. If the persistent world alone reaches the
downstream business oracle, keep that narrow runtime alive and document its
lifecycle; if all paths agree under a complete capsule, a fresh helper may be
valid. If the persistent world also fails, return to the first divergent wire,
bootstrap, transport, or host boundary.

## Packaging A Callable Interface

After function verification passes, extract the runner into a small callable module, commonly `js_reverse_cache/tasks/<task-id>/env/sign.js`:

```javascript
function sign(url) {
  window.__captured_a_bogus = null;
  const xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.setRequestHeader('Accept', 'application/json, text/plain, */*');
  xhr.send(null);
  return window.__captured_a_bogus;
}

module.exports = sign;

if (require.main === module) {
  const url = process.argv[2] || process.env.SIGN_URL;
  if (!url) {
    console.error('Usage: node sign.js <url>');
    process.exit(1);
  }
  process.stdout.write(sign(url) || '');
}
```

Prefer an HTTP middleware for Python replay when process environment differences affect subprocess execution:

```javascript
const http = require('http');
const sign = require('./sign');
const PORT = 3456;

const server = http.createServer((req, res) => {
  if (req.method !== 'POST' || req.url !== '/sign') {
    res.writeHead(404);
    res.end('Not Found');
    return;
  }

  let body = '';
  req.on('data', (chunk) => body += chunk);
  req.on('end', () => {
    try {
      const { url } = JSON.parse(body);
      const result = sign(url);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ result: result || '', length: (result || '').length }));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
  });
});

server.listen(PORT, () => console.log(`sign server on http://localhost:${PORT}/sign`));
```

## HTTP Replay Checks

Validate in this order:

1. Activation check: run the task-local runner with registered and unregistered paths and capture final URL/header/body for every owned transport.
2. Fixed-vector check: compare exact output and canonical request bytes with the saved browser vector; reject shape-only matches.
3. Middleware check: call the local helper with the same fixed input, if a helper boundary is retained.
4. Request replay: let Python send the real API request with the returned sign and the same browser-side request contract.
5. Business check: require the expected business code, schema, identity, and non-empty data or state transition.

Python request rules:

1. Use `requests.get(base_url, params=params, cookies=cookies)` or the equivalent `curl_cffi.requests` call.
2. Keep `cookies` as a dict or cookie jar; do not stuff a raw cookie string into `headers["cookie"]` unless the target explicitly requires manual header replay.
3. Do not manually pre-quote the generated sign unless browser evidence proves the exact encoded form.
4. Rebuild time-sensitive sign/header/token values inside pagination or retry loops.

Minimal replay skeleton:

```python
from curl_cffi import requests
from curl_cffi.requests.impersonate import DEFAULT_CHROME

SIGN_SERVER = "http://localhost:3456/sign"


def get_sign(url):
    resp = requests.post(SIGN_SERVER, json={"url": url}, impersonate=DEFAULT_CHROME)
    return resp.json().get("result") or None


headers = {"user-agent": "...", "referer": "..."}  # UA major must match DEFAULT_CHROME
cookies = {"ttwid": "...", "odin_tt": "..."}
params = {"aid": "6383", "sec_user_id": "...", "msToken": "..."}

base_url = "https://target.example/api/path/"
prepared = requests.Request("GET", base_url, params=params).prepare()
params["a_bogus"] = get_sign(prepared.url)

response = requests.get(base_url, headers=headers, cookies=cookies, params=params, impersonate=DEFAULT_CHROME)
print(response.status_code, response.text)
```
