# Server-JS Cookie Bootstrap Playbook

Use this reference when:

- an API first returns `202` or another non-final status with a JavaScript payload
- `JSON.data` contains executable JS instead of the expected data array
- the page succeeds only after a cookie such as `m` is created by running returned code
- the same endpoint must be called twice: once to get the challenge and once to get the data
- a page script exposes a refresh function that can be rerun to renew cookies or request parameters

## 1. Recognize the pattern

Typical flow:

1. call the target endpoint without the derived cookie or token
2. receive a challenge response, often `202`
3. challenge payload contains executable JS
4. executing the payload sets `document.cookie`, storage, or a token variable
5. replay the same endpoint with the new state
6. receive the real data array

Do not treat the first response as an error if the site clearly uses it as a bootstrap step.

Variant:

1. page load downloads obfuscated bootstrap JS from a separate script endpoint
2. inline page code exposes a function such as `_$KS()`
3. rerunning that function refreshes cookies or request params
4. an extra in-memory timestamp such as `$_zw[23]` must also be updated
5. replay succeeds only after both pieces are refreshed

## 2. What to capture

Record all of these:

1. first request URL, method, query, headers, and cookies
2. first response status code
3. first response body shape
4. exact cookie or token written after executing the returned JS
5. second request differences
6. whether later pages change headers such as `User-Agent`
7. whether the page also keeps a parallel in-memory value that must be refreshed

## 3. Fastest stable strategy

Prefer the smallest working path:

1. request the endpoint
2. if `data` is not the final array, treat it as challenge JS
3. execute the returned JS in a minimal sandbox
4. extract the derived cookie or token
5. replay the same request with the new state

This usually beats fully deobfuscating the payload before delivery.

If the bootstrap logic already lives on the page:

1. call the exposed refresh function
2. update any timestamp slot the page passes as a request param
3. replay from the same browser context

Related pattern:

1. page installs a global request hook such as `$.ajaxSetup(beforeSend)`
2. business code appears to send plain form data
3. hook rewrites body into encrypted payload and adds signing headers
4. response keeps outer JSON readable but encrypts the `data` field only
5. recovery requires porting both hook-time request mutation and response-field decryption

## 4. Minimal sandbox checklist

Most bootstrap payloads only need a small subset of browser APIs:

- `window`
- `document.cookie`
- `navigator.userAgent`
- `location.href`
- `Date`
- `Math`
- `setTimeout` / `setInterval`
- `atob` / `btoa`
- `encodeURIComponent` / `decodeURIComponent`

Start with the minimum. Add more only when runtime errors prove they are needed.

## 5. Parsing the result

After executing the returned JS:

1. read the final `document.cookie`
2. extract the target cookie value
3. ignore extra attributes such as `path=/` unless they matter to the replay

When parsing, never trust the whole raw cookie string blindly. Extract the specific value needed for replay.

## 6. Delivery recommendation

Preferred structure:

- `extract_m.js` or `extract_cookie.js`
- `fetch_all.py` or `fetch_all.js`
- `README.md`

The helper should:

1. accept the returned JS payload
2. execute it in a sandbox
3. return the derived cookie or token

The main collector should:

1. fetch challenge payload
2. call the helper
3. replay the endpoint
4. aggregate results

## 7. Verification checklist

Call it done only after:

1. the helper consistently extracts the cookie or token
2. the replay returns real data, not another challenge payload
3. all pages succeed
4. any page-specific header rules are documented
5. the final script prints the total result directly
