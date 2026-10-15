import assert from "node:assert/strict";

import {
  FIXED_INPUT,
  FIXED_VECTOR,
  FIXED_VECTOR_CAPSULE,
  LIVE_HTTP_OWNER,
  createBrowserProfile,
  evaluateBusinessAcceptance,
  installAppendCapture,
  installFakeTransports,
  isProfileCoherent,
  loadFakeInterceptorSdk,
  matchesCapturedVectorProfile,
} from "./fixtures/fake-interceptor-sdk.js";

function runtime(family = "chrome") {
  const host = {
    __browserProfile: createBrowserProfile(family),
    __fixedVectorState: FIXED_VECTOR_CAPSULE.dynamic,
  };
  installFakeTransports(host);
  return host;
}

function xhrWire(host, url = FIXED_INPUT.url) {
  const xhr = new host.XMLHttpRequest();
  xhr.open(FIXED_INPUT.method, url);
  return xhr.send(FIXED_INPUT.body);
}

function queryValue(url, name) {
  return new URL(url).searchParams.get(name);
}

{
  const host = runtime();
  const sdk = loadFakeInterceptorSdk(host);
  assert.equal(sdk.loaded, true);
  const wire = xhrWire(host);
  assert.equal(queryValue(wire.url, "sdk_q"), null, "load must not imply activation");
  assert.equal(wire.headers["x-sdk-sign"], undefined);
}

{
  const host = runtime();
  const sdk = loadFakeInterceptorSdk(host);
  assert.equal(sdk.init({ paths: ["/api/items"] }), true);
  const positive = xhrWire(host);
  assert.equal(queryValue(positive.url, "sdk_q"), FIXED_VECTOR.xhrQuery);
  assert.equal(positive.headers["x-sdk-sign"], FIXED_VECTOR.xhrHeader);

  const negative = xhrWire(host, "https://fixture.invalid/api/other?x=1");
  assert.equal(queryValue(negative.url, "sdk_q"), null, "unregistered path is the negative control");
  assert.equal(negative.headers["x-sdk-sign"], undefined);
}

{
  const host = runtime();
  const sdk = loadFakeInterceptorSdk(host);
  sdk.init({ paths: ["/api/items"] });
  const wire = await host.fetch(FIXED_INPUT.url, { method: FIXED_INPUT.method, body: FIXED_INPUT.body });
  assert.equal(queryValue(wire.url, "sdk_f"), FIXED_VECTOR.fetchQuery);
  assert.equal(wire.headers["x-sdk-fetch"], FIXED_VECTOR.fetchHeader);
  assert.equal(queryValue(wire.url, "sdk_q"), null, "fetch is a sibling channel, not XHR proof");
}

{
  const host = runtime();
  const earlyCapture = installAppendCapture(host);
  const sdk = loadFakeInterceptorSdk(host);
  sdk.init({ paths: ["/api/items"] });
  xhrWire(host);
  assert.equal(earlyCapture.length, 0, "SDK-owned polyfill overwrites a premature capture hook");

  const lateCapture = installAppendCapture(host);
  xhrWire(host);
  assert.deepEqual(lateCapture, [["sdk_q", FIXED_VECTOR.xhrQuery]], "capture hook belongs after SDK load");
}

{
  assert.throws(
    () => loadFakeInterceptorSdk({ URLSearchParams }),
    /must exist before SDK load/,
    "transport references belong before SDK load",
  );
}

{
  const firefox = createBrowserProfile("firefox");
  assert.deepEqual(firefox.chromeOnlyApis, [], "Firefox baseline must not gain Chrome-only APIs by default");
  assert.equal("clientHints" in firefox, false);
  assert.equal(isProfileCoherent(firefox), true, "Firefox can be internally coherent");
  assert.equal(matchesCapturedVectorProfile(firefox), false, "Firefox does not match the captured Chrome vector");

  const hybrid = { ...firefox, clientHints: '"Chromium";v="136"', tlsFamily: "chrome" };
  assert.equal(isProfileCoherent(hybrid), false, "mixed browser-family claims are incoherent");
}

{
  const host = runtime("firefox");
  const sdk = loadFakeInterceptorSdk(host);
  sdk.init({ paths: ["/api/items"] });
  const wire = xhrWire(host);
  const candidate = queryValue(wire.url, "sdk_q");
  assert.equal(candidate.length, FIXED_VECTOR.xhrQuery.length, "a coherent but sample-mismatched profile keeps the shape");
  assert.notEqual(candidate, FIXED_VECTOR.xhrQuery, "profile coherence does not imply captured-vector parity");
}

{
  const host = runtime();
  host.__fixedVectorState = {
    ...FIXED_VECTOR_CAPSULE.dynamic,
    randomBytes: [1, 3, 5, 8],
  };
  const sdk = loadFakeInterceptorSdk(host);
  sdk.init({ paths: ["/api/items"] });
  const candidate = queryValue(xhrWire(host).url, "sdk_q");
  assert.equal(candidate.length, FIXED_VECTOR.xhrQuery.length, "changed entropy preserves output shape");
  assert.notEqual(candidate, FIXED_VECTOR.xhrQuery, "exact parity requires the same RNG capsule");
}

{
  assert.equal(evaluateBusinessAcceptance({ statusCode: 200, businessCode: 0, data: [] }), false);
  assert.equal(evaluateBusinessAcceptance({ statusCode: 200, businessCode: 0, data: [{ id: 1 }] }), true);
  assert.equal(LIVE_HTTP_OWNER, "python", "the local SDK helper must not own live HTTP");
}

console.log("jsvmp interceptor contracts: ok");
