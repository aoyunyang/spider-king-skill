# 环境模块属性映射表

根据 undefined 属性路径前缀匹配对应的 env 模块。

## Contents

- [查找规则](#查找规则)
- [模块映射](#模块映射)

## 查找规则

1. 取 undefinedPath 的**前缀**（如 `navigator.userAgent` → 前缀 `navigator`）
2. 在下表中匹配前缀 → 找到对应模块
3. 如果模块有依赖，先加载依赖
4. 如果没有匹配，需要写 ai-generated 补丁

## 模块映射

### core/ — 核心基础（必须最先加载）

#### `core/ProxyMonitor.js` ⭐ 首选
- **提供**: `watch()`, `safefunction()`, `makeFunction()`, `__ProxyMonitor__`
- **依赖**: 无
- **说明**: 所有其他模块依赖此模块。env-diagnose.js 自动加载，无需手动指定。**覆盖 90% 日常监控需求。**

#### `core/ProxyEnv.js`
- **提供**: 基础的 `document`, `navigator`, `location`, `history`, `screen`, `localStorage`, `sessionStorage` 代理对象
- **依赖**: `core/ProxyMonitor.js`
- **说明**: 提供最小的浏览器环境骨架。env-diagnose.js 仅在未指定 `--env` 时自动加载；一旦显式传入 `--env`，就按你的列表加载，避免和更具体模块发生 `configurable:false` 冲突。

#### 监控模块选择决策

| 需求 | 推荐模块 |
|---|---|
| 基础 watch/safefunction，补环境常规流程 | `core/ProxyMonitor.js` ⭐ |
| 完整的日志分类、查询 API、多类型 mock 存储 | `core/EnvMonitor.js` |
| 元素创建代理追踪、属性变更回调、mock 钩子 | `core/MonitorSystem.js` |

> ⚠️ `EnvMonitor.js` 和 `MonitorSystem.js` **互斥**（均注册 `window.__EnvMonitor__`），不要同时加载。两者都不建议与 `ProxyMonitor.js` 混用。

#### `core/EnvMonitor.js` （高级可选）
- **提供**: `window.__EnvMonitor__`, `window.__logUndefined__`, `window.__logCall__`, `window.__setMock__`, `window.__getMock__`
- **依赖**: 无
- **适合**: 需要按 access/call/DOM/create 分类存储日志、丰富的查询筛选 API（getUndefinedLogs/getCallLogs/getCreateLogs/getDOMLogs/getAllLogs）、日志导出和 undefined 修复标记的场景。
- **冲突**: 与 `core/MonitorSystem.js` 互斥；与 `core/ProxyMonitor.js` 不建议混用。

#### `core/MonitorSystem.js` （高级可选）
- **提供**: `window.__EnvMonitor__`, `window.__setMock__`, `window.__getMock__`, `window.__getUndefined__`, `window.__getStats__`, `window.__createMonitoredElement__`
- **依赖**: 无
- **适合**: 需要元素创建代理（Proxy 包装的 DOM 元素）、属性变更回调（watchedProperties onChange/onAccess）、mock 四阶段钩子（handler/beforeCall/afterCall/condition）的场景。
- **冲突**: 与 `core/EnvMonitor.js` 互斥；与 `core/ProxyMonitor.js` 不建议混用。

### bom/ — Browser Object Model

#### `bom/navigator.js`
- **前缀匹配**: `navigator`
- **提供**:
  - `navigator.userAgent`, `navigator.appCodeName`, `navigator.appName`, `navigator.appVersion`
  - `navigator.platform`, `navigator.product`, `navigator.productSub`, `navigator.vendor`, `navigator.vendorSub`
  - `navigator.language`, `navigator.languages`, `navigator.onLine`
  - `navigator.hardwareConcurrency`, `navigator.maxTouchPoints`, `navigator.deviceMemory`
  - `navigator.cookieEnabled`, `navigator.doNotTrack`, `navigator.webdriver`
  - `navigator.plugins`, `navigator.mimeTypes`
  - `navigator.connection` (downlink, effectiveType, rtt, saveData)
  - `navigator.geolocation`, `navigator.permissions`, `navigator.mediaDevices`, `navigator.serviceWorker`
- **依赖**: 无

#### `bom/location.js`
- **前缀匹配**: `location`
- **提供**:
  - `location.href`, `location.protocol`, `location.host`, `location.hostname`, `location.port`
  - `location.pathname`, `location.search`, `location.hash`, `location.origin`
  - `location.assign()`, `location.replace()`, `location.reload()`, `location.toString()`
- **依赖**: 无

#### `bom/screen.js`
- **前缀匹配**: `screen`
- **提供**:
  - `screen.width`, `screen.height`, `screen.availWidth`, `screen.availHeight`, `screen.availLeft`, `screen.availTop`
  - `screen.colorDepth`, `screen.pixelDepth`
  - `screen.orientation` (angle, type, lock, unlock)
  - `screen.isExtended`
- **依赖**: 无

#### `bom/history.js`
- **前缀匹配**: `history`, `window.history`
- **提供**:
  - `history.length`, `history.state`, `history.scrollRestoration`
  - `history.back()`, `history.forward()`, `history.go()`
  - `history.pushState()`, `history.replaceState()`
  - 内部栈管理和 popstate 事件派发
- **依赖**: `bom/location.js`（pushState/replaceState 需更新 `window.location`）

#### `bom/window.js`
- **前缀匹配**: `window.innerWidth`, `window.innerHeight`, `window.outerWidth`, `window.outerHeight`, `window.screenX`, `window.screenY`, `window.devicePixelRatio`, `window.isSecureContext`, `window.visualViewport`, `window.requestAnimationFrame`, `window.cancelAnimationFrame`
- **提供**:
  - 窗口尺寸: `innerWidth`, `innerHeight`, `outerWidth`, `outerHeight`, `screenX`, `screenY`, `pageXOffset`, `pageYOffset`
  - 视口: `devicePixelRatio`, `isSecureContext`, `origin`, `crossOriginIsolated`
  - 框架: `length`, `frames`, `parent`, `top`, `self`, `opener`
  - `visualViewport` 对象
  - 方法: `alert()`, `confirm()`, `prompt()`, `open()`, `close()`, `focus()`, `blur()`, `print()`, `scroll()`, `scrollTo()`, `scrollBy()`, `requestAnimationFrame()`, `cancelAnimationFrame()`
- **依赖**: 无
- **注意**: 此模块不提供 window 本身（sandbox 已是 window），而是补充窗口级属性

#### `bom/storage.js`
- **前缀匹配**: `localStorage`, `sessionStorage`
- **提供**:
  - `localStorage.getItem()`, `localStorage.setItem()`, `localStorage.removeItem()`, `localStorage.clear()`, `localStorage.key()`, `localStorage.length`
  - `sessionStorage`（同上接口）
  - `StorageEvent` 构造函数
- **依赖**: 无

#### `bom/crypto.js`
- **前缀匹配**: `crypto`
- **提供**:
  - `crypto.getRandomValues()`
  - `crypto.randomUUID()`
  - `crypto.subtle.digest()`, `crypto.subtle.encrypt()`, `crypto.subtle.decrypt()`
  - `crypto.subtle.sign()`, `crypto.subtle.verify()`
  - `crypto.subtle.generateKey()`, `crypto.subtle.importKey()`, `crypto.subtle.exportKey()`
  - `crypto.subtle.deriveKey()`, `crypto.subtle.deriveBits()`
- **依赖**: 无
- **⚠️ 关键**: JSVMP 类加密依赖此模块（如 a_bogus 签名计算）

#### `bom/performance.js`
- **前缀匹配**: `performance`
- **提供**:
  - `performance.now()`, `performance.timeOrigin`
  - `performance.timing`（Navigation Timing）
  - `performance.navigation`
  - `performance.memory`（Chrome 特有）
  - `performance.mark()`, `performance.clearMarks()`, `performance.measure()`, `performance.clearMeasures()`
  - `performance.getEntries()`, `performance.getEntriesByName()`, `performance.getEntriesByType()`
- **依赖**: 无
- **⚠️ 关键**: JSVMP 依赖 `performance.now()` 和 `performance.timeOrigin` 做时间戳

#### `bom/console.js`
- **前缀匹配**: `console`（仅当需要完整 console API 时）
- **提供**: 完整的 `console.*` 方法（log, info, warn, error, debug, assert, group, table, dir, trace, time, count 等）
- **依赖**: 无
- **说明**: env-diagnose.js 已内置基础 console，仅在需要 `console.table` 等高级方法时加载

#### `bom/observers.js`
- **前缀匹配**: `MutationObserver`, `IntersectionObserver`, `ResizeObserver`, `PerformanceObserver`
- **提供**: 上述四个 Observer 类的完整实现
- **依赖**: `core/ProxyMonitor.js`

### dom/ — Document Object Model

#### `dom/event.js`
- **前缀匹配**: `Event`, `CustomEvent`, `UIEvent`, `MouseEvent`, `KeyboardEvent`, `FocusEvent`, `InputEvent`, `WheelEvent`, `TouchEvent`, `PointerEvent`, `SubmitEvent`
- **提供**: 完整的事件类体系 + `addEventListener/removeEventListener/dispatchEvent`
- **依赖**: 无
- **加载顺序**: 应在 document.js 之前

#### `dom/document.js`
- **前缀匹配**: `document`
- **提供**:
  - 元数据: `document.URL`, `document.domain`, `document.referrer`, `document.title`, `document.cookie`, `document.readyState`, `document.contentType`
  - 节点: `document.documentElement`, `document.head`, `document.body`, `document.childNodes`, `document.children`
  - 查询: `document.getElementById()`, `document.getElementsByClassName()`, `document.getElementsByTagName()`, `document.getElementsByName()`, `document.querySelector()`, `document.querySelectorAll()`
  - 创建: `document.createElement()`, `document.createTextNode()`, `document.createDocumentFragment()`, `document.createComment()`, `document.createAttribute()`, `document.createEvent()`, `document.createRange()`
  - 内容: `document.write()`, `document.writeln()`, `document.open()`, `document.close()`
  - 事件: `document.addEventListener()`, `document.removeEventListener()`, `document.dispatchEvent()`
  - 底层类: `Node`, `Element`, `Document`, `CSSStyleDeclaration`, `DOMTokenList`, `NamedNodeMap`
- **依赖**: `core/ProxyMonitor.js`
- **体积**: 103KB — 是最大的模块

#### `dom/elements.js`
- **前缀匹配**: `HTMLElement`, `HTMLDivElement`, `HTMLCanvasElement`, `HTMLImageElement`, `HTMLVideoElement`, `HTMLAudioElement`, `HTMLInputElement`, `HTMLFormElement`, `HTMLScriptElement`, `HTMLStyleElement`, `HTMLIFrameElement` 等
- **提供**: 完整的 HTML 元素类体系（20+ 元素类型）
- **依赖**: **必须在 `dom/document.js` 之后加载**（依赖 Element 基类）

### webapi/ — Web API

#### `webapi/fetch.js`
- **前缀匹配**: `fetch`, `Headers`, `Request`, `Response`
- **提供**: `fetch()` 函数, `Headers`, `Request`, `Response` 类
- **依赖**: 无

#### `webapi/xhr.js`
- **前缀匹配**: `XMLHttpRequest`
- **提供**: 完整的 `XMLHttpRequest` 类（含 readyState, response, events 等）
- **依赖**: 无
- **说明**: env-diagnose.js 已有基础 XMLHttpRequest stub，加载此模块可获得完整实现

#### `webapi/blob.js`
- **前缀匹配**: `Blob`, `File`, `FileList`, `FileReader`, `FormData`
- **提供**: `Blob`, `File`, `FileList`, `FileReader`, `FormData` 类
- **依赖**: 无

#### `webapi/url.js`
- **前缀匹配**: `URL`, `URLSearchParams`
- **提供**: `URL` (含 `createObjectURL`, `revokeObjectURL`), `URLSearchParams`
- **依赖**: 无

#### `webapi/network.js`
- **前缀匹配**: `__NetworkStore__`, `__NetworkMock__`
- **提供**: 网络请求监控和 mock 系统
- **依赖**: `webapi/xhr.js`, `webapi/fetch.js`（需要先有 XHR 和 fetch）
- **说明**: 通常仅在需要网络 mock 时加载

#### `webapi/runtime-contracts.js`
- **前缀匹配**: `MessageChannel`, `MessagePort`, `webpackChunk*`
- **提供**: linked-port 异步消息派发与显式命名的 webpack chunk-array `push` 捕获
- **依赖**: 建议在 `dom/event.js` 与 `bom/window.js` 之后加载；无这些模块时使用最小事件对象
- **说明**: 只在固定样本证明缺口后加载；不模拟 structured clone，不扫描 chunk 名，不执行模块函数

### timer/ — 定时器

#### `timer/timeout.js`
- **前缀匹配**: `setTimeout`, `setInterval`, `clearTimeout`, `clearInterval`
- **提供**: `setTimeout`/`clearTimeout` 宏任务队列、`__drainTimers__`、`__getActiveTimers__`、`__clearAllTimers__`
- **依赖**: 无
- **说明**: 回调绝不能在 `setTimeout` 函数体内同步执行。无原生事件循环时由驱动调用 `__drainTimers__(limit)`。无原生 `setInterval` 时 `setInterval` 返回 0，不模拟周期任务。env-diagnose.js 基础 stub 仍返回 0；需要可驱动队列时再加载本模块。

### encoding/ — 编码

#### `encoding/atob.js`
- **前缀匹配**: `atob`, `btoa`
- **提供**: Base64 编解码
- **依赖**: 无
- **说明**: env-diagnose.js 已内置，通常无需额外加载；替换宿主实现前用 `btoa("\x00\xffAz") === "AP9Beg=="` 验证 Latin1 契约

#### `encoding/textencoder.js`
- **前缀匹配**: `TextEncoder`, `TextDecoder`
- **提供**: `TextEncoder`（UTF-8）, `TextDecoder`（多编码支持：UTF-8, ASCII, ISO-8859-1, GBK, GB2312, GB18030, Windows-1252）
- **依赖**: 无

### Task-only custom patches

Skill 内不捆绑 `ai-generated/` 代码。目标专用补丁写入执行项目的 `js_reverse_cache/tasks/<task-id>/env/ai-generated/<object>-<property>.js`，通过 `--env <明确文件路径>` 单独加载；诊断器不会扫描目录或动态执行文件内容。
