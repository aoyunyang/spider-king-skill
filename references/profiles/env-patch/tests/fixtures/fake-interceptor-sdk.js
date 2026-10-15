export const FIXED_INPUT = Object.freeze({
  method: "GET",
  url: "https://fixture.invalid/api/items?x=1",
  body: "",
});

export const FIXED_VECTOR = Object.freeze({
  xhrQuery: "X5AF66AD8846973F",
  xhrHeader: "H5AF66AD8846973F",
  fetchQuery: "F5AF66AD8846973F",
  fetchHeader: "G5AF66AD8846973F",
});

export const LIVE_HTTP_OWNER = "python";

const CHROME_PROFILE = Object.freeze({
  family: "chrome",
  userAgent: "Mozilla/5.0 Chrome/136.0.0.0",
  clientHints: '"Chromium";v="136"',
  tlsFamily: "chrome",
  chromeOnlyApis: Object.freeze(["navigator.userAgentData"]),
});

const FIREFOX_PROFILE = Object.freeze({
  family: "firefox",
  userAgent: "Mozilla/5.0 Firefox/128.0",
  tlsFamily: "firefox",
  chromeOnlyApis: Object.freeze([]),
});

export const FIXED_VECTOR_CAPSULE = Object.freeze({
  targetSha256: "fixture-sdk-sha256",
  engineVersion: "fixture-node-1",
  profile: CHROME_PROFILE,
  dynamic: Object.freeze({
    epochMs: 1720000000123,
    timezone: "UTC",
    performanceNow: 42.5,
    performanceTimeOrigin: 1720000000000,
    randomBytes: Object.freeze([1, 3, 5, 7]),
    nonce: "n-01",
    counter: 9,
    sessionState: "round-7",
  }),
});

function stableHex15(value) {
  let first = 0x811c9dc5;
  let second = 0x9e3779b9;
  for (let index = 0; index < value.length; index += 1) {
    const code = value.charCodeAt(index);
    first = Math.imul(first ^ code, 0x01000193);
    second = Math.imul(second ^ code, 0x85ebca6b);
  }
  return `${(first >>> 0).toString(16).padStart(8, "0")}${(second >>> 0).toString(16).padStart(8, "0")}`
    .slice(0, 15)
    .toUpperCase();
}

function makeShapeSign(prefix, method, url, body = "", dynamic = null) {
  const parsed = new URL(url);
  const canonical = `${String(method).toUpperCase()}|${parsed.pathname}${parsed.search}|${body || ""}`;
  return `${prefix}${stableHex15(JSON.stringify({ canonical, dynamic }))}`;
}

export function isProfileCoherent(profile) {
  if (!profile || typeof profile !== "object") return false;
  if (profile.family === "chrome") {
    return Boolean(
      /Chrome\//.test(profile.userAgent || "")
      && /Chromium/.test(profile.clientHints || "")
      && profile.tlsFamily === "chrome"
      && profile.chromeOnlyApis?.includes("navigator.userAgentData")
    );
  }
  if (profile.family === "firefox") {
    return Boolean(
      /Firefox\//.test(profile.userAgent || "")
      && !("clientHints" in profile)
      && profile.tlsFamily === "firefox"
      && Array.isArray(profile.chromeOnlyApis)
      && profile.chromeOnlyApis.length === 0
    );
  }
  return false;
}

export function matchesCapturedVectorProfile(profile, captured = FIXED_VECTOR_CAPSULE.profile) {
  return Boolean(
    profile
    && captured
    && profile.family === captured.family
    && profile.userAgent === captured.userAgent
    && profile.clientHints === captured.clientHints
    && profile.tlsFamily === captured.tlsFamily
  );
}

function hasCompleteDynamicCapsule(dynamic) {
  return Boolean(
    dynamic
    && Number.isFinite(dynamic.epochMs)
    && typeof dynamic.timezone === "string"
    && Number.isFinite(dynamic.performanceNow)
    && Number.isFinite(dynamic.performanceTimeOrigin)
    && Array.isArray(dynamic.randomBytes)
    && typeof dynamic.nonce === "string"
    && Number.isInteger(dynamic.counter)
    && typeof dynamic.sessionState === "string"
  );
}

function matchesPath(url, paths) {
  const pathname = new URL(url).pathname;
  return paths.some((path) => pathname === path || pathname.startsWith(`${path}/`));
}

function appendQuery(host, inputUrl, name, value) {
  const parsed = new URL(inputUrl);
  const params = new host.URLSearchParams(parsed.search);
  params.append(name, value);
  parsed.search = params.toString();
  return parsed.toString();
}

export function createBrowserProfile(family) {
  if (family === "firefox") {
    return FIREFOX_PROFILE;
  }
  if (family === "chrome") {
    return CHROME_PROFILE;
  }
  throw new Error(`unsupported fixture family: ${family}`);
}

export function installFakeTransports(host) {
  class FakeXMLHttpRequest {
    constructor() {
      this.method = null;
      this.url = null;
      this.body = null;
      this.headers = {};
      this.sent = false;
    }

    open(method, url) {
      this.method = String(method).toUpperCase();
      this.url = String(url);
    }

    setRequestHeader(name, value) {
      this.headers[String(name).toLowerCase()] = String(value);
    }

    send(body = "") {
      this.body = body || "";
      this.sent = true;
      return this.wire();
    }

    wire() {
      return {
        transport: "xhr",
        method: this.method,
        url: this.url,
        headers: { ...this.headers },
        body: this.body,
        sent: this.sent,
      };
    }
  }

  host.XMLHttpRequest = FakeXMLHttpRequest;
  host.fetch = async (url, options = {}) => ({
    transport: "fetch",
    method: String(options.method || "GET").toUpperCase(),
    url: String(url),
    headers: { ...(options.headers || {}) },
    body: options.body || "",
    sent: true,
  });
  host.URLSearchParams = URLSearchParams;
}

export function installAppendCapture(host) {
  const Base = host.URLSearchParams;
  const captured = [];
  class CapturedURLSearchParams extends Base {
    append(name, value) {
      captured.push([String(name), String(value)]);
      return super.append(name, value);
    }
  }
  host.URLSearchParams = CapturedURLSearchParams;
  return captured;
}

export function loadFakeInterceptorSdk(host) {
  if (typeof host.XMLHttpRequest !== "function" || typeof host.fetch !== "function") {
    throw new Error("fake XHR and fetch must exist before SDK load");
  }

  const BaseXHR = host.XMLHttpRequest;
  const baseFetch = host.fetch;
  const state = { initialized: false, paths: [] };

  // Simulate an SDK-owned polyfill: a capture hook installed before SDK load is lost.
  host.URLSearchParams = class SdkURLSearchParams extends URLSearchParams {};

  class InterceptedXMLHttpRequest extends BaseXHR {
    send(body = "") {
      if (state.initialized && matchesPath(this.url, state.paths)) {
        const vectorReady = isProfileCoherent(host.__browserProfile)
          && matchesCapturedVectorProfile(host.__browserProfile)
          && hasCompleteDynamicCapsule(host.__fixedVectorState);
        const queryPrefix = vectorReady ? "X" : "Z";
        const headerPrefix = vectorReady ? "H" : "Y";
        const querySign = makeShapeSign(queryPrefix, this.method, this.url, body, host.__fixedVectorState);
        const headerSign = makeShapeSign(headerPrefix, this.method, this.url, body, host.__fixedVectorState);
        this.url = appendQuery(host, this.url, "sdk_q", querySign);
        this.setRequestHeader("x-sdk-sign", headerSign);
      }
      return super.send(body);
    }
  }

  host.XMLHttpRequest = InterceptedXMLHttpRequest;
  host.fetch = async (url, options = {}) => {
    const method = String(options.method || "GET").toUpperCase();
    const body = options.body || "";
    if (!state.initialized || !matchesPath(url, state.paths)) {
      return baseFetch(url, options);
    }
    const vectorReady = isProfileCoherent(host.__browserProfile)
      && matchesCapturedVectorProfile(host.__browserProfile)
      && hasCompleteDynamicCapsule(host.__fixedVectorState);
    const queryPrefix = vectorReady ? "F" : "Z";
    const headerPrefix = vectorReady ? "G" : "Y";
    const querySign = makeShapeSign(queryPrefix, method, url, body, host.__fixedVectorState);
    const headerSign = makeShapeSign(headerPrefix, method, url, body, host.__fixedVectorState);
    const signedUrl = appendQuery(host, url, "sdk_f", querySign);
    return baseFetch(signedUrl, {
      ...options,
      method,
      body,
      headers: { ...(options.headers || {}), "x-sdk-fetch": headerSign },
    });
  };

  return Object.freeze({
    loaded: true,
    init(config = {}) {
      if (!Array.isArray(config.paths) || config.paths.length === 0) {
        state.initialized = false;
        state.paths = [];
        return false;
      }
      state.initialized = true;
      state.paths = [...config.paths];
      return true;
    },
    activationState() {
      return { initialized: state.initialized, paths: [...state.paths] };
    },
  });
}

export function evaluateBusinessAcceptance(response) {
  return Boolean(
    response
    && response.statusCode >= 200
    && response.statusCode < 300
    && response.businessCode === 0
    && Array.isArray(response.data)
    && response.data.length > 0
  );
}
