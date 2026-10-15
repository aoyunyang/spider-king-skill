/**
 * Minimal webpack runtime template for extracted modules.
 *
 * Copy this into the execution workspace's js_reverse_cache/tasks/<task-id>/env/ when a known
 * crypto entry lives inside a webpack bundle. Fill __webpack_modules__
 * with extracted module functions, then call __webpack_require__(entryId).
 */

var __webpack_modules__ = {
  // 12345: function(module, exports, __webpack_require__) { ... },
};

var __webpack_module_cache__ = {};

function __webpack_require__(moduleId) {
  var cachedModule = __webpack_module_cache__[moduleId];
  if (cachedModule !== undefined) return cachedModule.exports;

  var module = __webpack_module_cache__[moduleId] = {
    id: moduleId,
    loaded: false,
    exports: {},
  };

  if (typeof __webpack_modules__[moduleId] !== 'function') {
    throw new Error('webpack module not found: ' + moduleId);
  }

  __webpack_modules__[moduleId].call(
    module.exports,
    module,
    module.exports,
    __webpack_require__
  );

  module.loaded = true;
  return module.exports;
}

__webpack_require__.o = function (obj, prop) {
  return Object.prototype.hasOwnProperty.call(obj, prop);
};

__webpack_require__.d = function (exports, a, b) {
  if (typeof a === 'string') {
    if (!__webpack_require__.o(exports, a)) {
      Object.defineProperty(exports, a, { enumerable: true, get: b });
    }
    return;
  }
  for (var key in a) {
    if (__webpack_require__.o(a, key) && !__webpack_require__.o(exports, key)) {
      Object.defineProperty(exports, key, { enumerable: true, get: a[key] });
    }
  }
};

__webpack_require__.r = function (exports) {
  if (typeof Symbol !== 'undefined' && Symbol.toStringTag) {
    Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
  }
  Object.defineProperty(exports, '__esModule', { value: true });
};

__webpack_require__.n = function (module) {
  var getter = module && module.__esModule
    ? function () { return module['default']; }
    : function () { return module; };
  __webpack_require__.d(getter, { a: getter });
  return getter;
};

__webpack_require__.t = function (value, mode) {
  if (mode & 1) value = __webpack_require__(value);
  if (mode & 8) return value;
  if (mode & 4 && typeof value === 'object' && value && value.__esModule) return value;
  var ns = Object.create(null);
  __webpack_require__.r(ns);
  Object.defineProperty(ns, 'default', { enumerable: true, value: value });
  if (mode & 2 && typeof value !== 'string') {
    for (var key in value) {
      __webpack_require__.d(ns, key, (function (k) { return value[k]; }).bind(null, key));
    }
  }
  return ns;
};

__webpack_require__.e = function () {
  return Promise.resolve();
};

__webpack_require__.m = __webpack_modules__;
__webpack_require__.c = __webpack_module_cache__;
__webpack_require__.p = '';

if (typeof globalThis !== 'undefined') {
  globalThis.__wpRequire = __webpack_require__;
}

export { __webpack_modules__, __webpack_module_cache__, __webpack_require__ };
export default __webpack_require__;
