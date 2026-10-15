# Optional env_core Advanced Path

默认优先使用当前 profile 的 `$ENV_PROFILE/scripts/env-diagnose.js` 和 `$ENV_PROFILE/env/` 模块树。只有在下面情况出现时，再启用 `$ENV_PROFILE/scripts/env_core.js` 这条高级手写补环境路径：

1. 需要 `Function.prototype.toString` / `Symbol.toStringTag` / 构造器外形这类 native 伪装。
2. 模块化 env 已能加载，但签名格式与浏览器仍不一致，需要定向监控少数对象。
3. 用户已有明确入口，且希望把补丁集中在项目的 `run.js` 中维护。
4. webpack 模块已定位，需要配合 `$ENV_PROFILE/scripts/webpack_runtime.js` 提取和加载模块。

## Contents

- [落地位置](#落地位置)
- [最小 run.js](#最小-runjs)
- [使用规则](#使用规则)
- [模块契约](#模块契约)
- [常见变体](#常见变体)

## 落地位置

所有临时运行文件写入执行代码工作区下的 `js_reverse_cache/`。如果不存在，先创建：

```text
执行代码工作区/
└── js_reverse_cache/
    ├── source/          # 原始 JS，只读保存
    ├── env/
    │   ├── env_core.js
    │   ├── main.js      # 目标 JS 副本或提取后的模块
    │   └── run.js       # 补环境策略和验证入口
    └── docs/
        └── progress.md
```

不要把逆向数据写到执行代码工作区之外的位置。

`env_core.js` 是 ESM `.js` 文件。复制到目标项目后，优先在 `js_reverse_cache/tasks/<task-id>/env/package.json` 写入 `{ "type": "module" }`，让 `run.js`、`env_core.js` 和可选的 `webpack_runtime.js` 都按 ESM 运行；如果目标项目根目录已经是 ESM，也可以复用根目录配置。

## 最小 run.js

```javascript
import env from './env_core.js';

// This acknowledgment is valid only inside an external disposable sandbox.
process.env.SPIDER_EXTERNAL_SANDBOX_CONFIRMED = '1';

function makeDocument() {
  return {
    cookie: '',
    readyState: 'complete',
    createElement(tag) {
      if (String(tag).toLowerCase() === 'canvas') {
        return {
          getContext() {
            return {
              measureText(text) {
                return { width: String(text).length * 8 };
              },
            };
          },
        };
      }
      return { style: {}, getContext: undefined };
    },
    getElementsByTagName() { return []; },
    addEventListener() {},
    removeEventListener() {},
  };
}

function makeNavigator() {
  return {
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    webdriver: false,
    language: 'zh-CN',
    languages: ['zh-CN', 'zh', 'en-US', 'en'],
    platform: 'Win32',
  };
}

function makeLocation() {
  return {
    href: 'https://example.com/',
    origin: 'https://example.com',
    protocol: 'https:',
    host: 'example.com',
    hostname: 'example.com',
    pathname: '/',
    search: '',
    hash: '',
  };
}

const fakeDocument = makeDocument();
const fakeNavigator = makeNavigator();
const fakeLocation = makeLocation();

const fakeWindow = {
  document: fakeDocument,
  navigator: fakeNavigator,
  location: fakeLocation,
  addEventListener() {},
  removeEventListener() {},
  setTimeout,
  clearTimeout,
  setInterval,
  clearInterval,
  Math,
  Date,
  JSON,
};

fakeWindow.window = fakeWindow;
fakeWindow.self = fakeWindow;
fakeWindow.top = fakeWindow;
fakeWindow.parent = fakeWindow;
fakeWindow.globalThis = fakeWindow;

env.init({
  window: env.createProxy(fakeWindow, 'window'),
  document: env.createProxy(fakeDocument, 'document'),
  navigator: env.createProxy(fakeNavigator, 'navigator'),
  location: env.createProxy(fakeLocation, 'location'),
});

Object.defineProperty(global, 'chrome', {
  value: undefined,
  configurable: true,
  writable: true,
});

try {
  await import('./main.js');
  console.log('entry type =', typeof window.sign);
  env.report();
} finally {
  env.restore();
}
```

## 使用规则

1. `env_core.js` 复制后不改；所有站点补丁写在 `run.js`。它不是隔离器，只能在无凭据、最小挂载、默认断网的外部 sandbox 中运行未知代码。
2. 环境必须在 `await import('./main.js')` 之前初始化。如果目标副本必须用 CommonJS 加载，改用 `createRequire(import.meta.url)`，不要在 ESM `run.js` 里直接调用裸 `require`。
3. 每轮只补一个最小因果单元：一个值、一个函数壳、一个返回对象或一个对象契约。
4. `env.report()` 中 0 error / 0 undefined 只代表外部访问链看起来完整，不代表签名已可用。
5. 签名长度、前缀、编码形态和浏览器不一致时，继续定位 `first divergence`，不要直接迁移 Python / execjs。
6. 如果有 Proxy / gap log，先用 `references/profiles/env-patch/scripts/analyze-gap-log.js` 聚合推荐模块，再决定手写补丁顺序。
7. 如果需要真实浏览器种子，先在 `references/profiles/env-patch/scripts/collect-browser-env.js` 的 `CONFIG` 中列出具体 Cookie/storage key；脚本默认不导出这些值或 canvas。结果只落到当前任务的 `js_reverse_cache/`。

## 模块契约

复杂手写补丁建议按 `references/profiles/env-patch/references/module-contracts.md` 组织：

1. `patchPlan`：准备补哪些点。
2. `patchCode`：补丁代码或代码片段。
3. `runtimeState`：补丁后的运行态。
4. `validation`：本模块检查点。
5. `residualRisk`：仍不能拟真的风险。

## 常见变体

显式存在但值为 `undefined`：

```javascript
Object.defineProperty(fakeWindow, 'ActiveXObject', {
  value: undefined,
  configurable: true,
  enumerable: true,
  writable: true,
});
```

定向监控少数对象：

```javascript
const tracedNavigator = env.monitor(fakeNavigator, 'navigator', {
  getLog: true,
  setLog: true,
});
fakeWindow.navigator = tracedNavigator;
global.navigator = tracedNavigator;
```

同步到 `global`：

```javascript
Object.defineProperty(global, 'chrome', {
  value: fakeWindow.chrome,
  configurable: true,
  writable: true,
});
```

最小 XHR 宿主：

```javascript
function XMLHttpRequest() {}
XMLHttpRequest.prototype.open = function open() {};
XMLHttpRequest.prototype.setRequestHeader = function setRequestHeader() {};
XMLHttpRequest.prototype.send = function send() {};

env.setFuncNative(XMLHttpRequest, 'XMLHttpRequest', 0);
env.setFuncNative(XMLHttpRequest.prototype.open, 'open', 2);
env.setFuncNative(XMLHttpRequest.prototype.setRequestHeader, 'setRequestHeader', 2);
env.setFuncNative(XMLHttpRequest.prototype.send, 'send', 1);

fakeWindow.XMLHttpRequest = XMLHttpRequest;
global.XMLHttpRequest = XMLHttpRequest;
```
