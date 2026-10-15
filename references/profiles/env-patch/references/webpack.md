# Webpack Module Extraction

当已定位的加密入口位于 webpack bundle 中时使用。入口未知时不要先做本流程，按 profile 入口的 capability-aware 契约转交；专用技能不可用时返回 Spider core loop。

## 识别模式

webpack 5 chunk push：

```javascript
(self.webpackChunkapp = self.webpackChunkapp || []).push([["chunkId"], {
  12345: function(module, exports, __webpack_require__) { /* ... */ },
}]);
```

webpack 4 IIFE：

```javascript
(function(modules) { /* runtime */ })({
  0: function(module, exports, __webpack_require__) { /* ... */ },
});
```

## 提取步骤

1. 从已确认的入口函数追溯到模块 ID。
2. 提取入口模块和它的 `__webpack_require__(id)` 依赖。
3. 将模块按 `id: function(module, exports, __webpack_require__) { ... }` 填入 `references/profiles/env-patch/scripts/webpack_runtime.js` 的副本。
4. 在运行入口里先补环境，再 `import runtime from './webpack_runtime.js'`，最后调用 `runtime(entryId)`。
5. 报 `webpack module not found` 时，回 bundle 中继续提取缺失 ID。

## 落地位置

把 `webpack_runtime.js` 复制到执行代码工作区的 `js_reverse_cache/tasks/<task-id>/env/`。如果任务目录不存在，先按项目产物契约创建。

`webpack_runtime.js` 是 ESM `.js` 文件。复制后确保 `js_reverse_cache/tasks/<task-id>/env/package.json` 含 `{ "type": "module" }`，或目标项目根目录已启用 ESM，否则 `import runtime from './webpack_runtime.js'` 会在 CommonJS 项目中失败。

## Expose require, skip UI mount

When encrypt/sign is inside a webpack IIFE, do not complete Vue `$mount` / layout / transition trees in a headless host.

Patch the bootstrap so the require function is exported before the entry call:

```javascript
// bootstrap ends like: return R.m = mods, R.c = cache, R.p = path, R(0);
// insert before R(0): globalThis.__wpRequire = R,
```

Then `__wpRequire(moduleId)` returns the encrypt/sign exports. Feed frozen args. Patch UI crash points only after proving that export is unreachable.

`scripts/webpack_runtime.js` assigns `globalThis.__wpRequire = __webpack_require__` after the runtime object exists.

## 注意

1. 环境补丁必须在加载目标模块前完成。
2. 不要修改原始 bundle；提取物放到 `js_reverse_cache/tasks/<task-id>/source/` 或 `js_reverse_cache/tasks/<task-id>/env/`。
3. 如果模块依赖异步 chunk，先记录 chunk 变量名，再决定是否补 chunk push 拦截。

## 已知 chunk 名的捕获

只有当前 bundle 已证明 chunk 数组名时，才加载 `env/webapi/runtime-contracts.js` 并调用：

```javascript
const capture = __installWebpackChunkCapture__(globalThis, 'webpackChunkKnownName');
// 执行已隔离、已捕获的本地 chunk 加载步骤
const evidence = capture.records;
capture.restore();
```

`records` 只包含有界的 chunk ID 与 module ID，不包含模块源码、请求体或环境值。捕获器不扫描全局对象，不执行模块函数，也不替代 `references/profiles/env-patch/scripts/webpack_runtime.js` 的显式模块提取流程。
