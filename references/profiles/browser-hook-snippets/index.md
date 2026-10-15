# Browser Hook Snippets Profile

## Contents

- [唯一职责](#唯一职责)
- [触发边界](#触发边界)
- [默认输出](#默认输出)
- [工作流](#工作流)
- [数据与请求绑定](#数据与请求绑定)
- [安全与降噪](#安全与降噪)
- [Failure Modes](#failure-modes)
- [资源路由](#资源路由)

## 唯一职责

围绕用户已知的观察点交付一个最小、可恢复、低噪声的浏览器 Hook。本 profile 不负责找到最终函数位置，也不负责把采样代码迁移到本地运行时。

阶段协议沿用 Spider King 主入口与 `references/workflow-overview.md`；本 profile 主要承担 Capture（观察取证）。本文件中的 `scripts/` 和 `references/` 均相对于 `$HOOK_PROFILE=$SKILL_DIR/references/profiles/browser-hook-snippets`。

## 触发边界

应该触发：

1. “给我一段能直接贴到 DevTools 的 hook”。
2. “临时看看谁写了 cookie/token/header/storage”。
3. “只过滤某个 URL，观察 fetch/xhr/WebSocket/worker/crypto/canvas”。
4. “先采样参数和调用栈，暂时不需要函数定位”。

不应触发：

| 用户真正要的结果 | 转交 |
|---|---|
| 脚本 URL、函数位置、initiator 或完整调用链 | capability snapshot 中有专用 JS 逆向技能时转交；否则返回 Spider core loop，用 `chrome-devtools` / `js-reverse` initiator evidence 定位 |
| 整份源码的结构化还原 | AST profile 存在时转交；否则使用 `references/offline-inline-deob-playbook.md` 与 `references/obfuscation-guide.md` 做本地静态恢复 |
| 已知入口在 Node.js/VM 中运行 | `spider-king` env-patch profile |
| 明确 Python + iv8 请求脚本 | capability snapshot 中有 iv8 专用技能时转交；否则报告约束未满足，只有用户接受替代后才使用 env-patch 或 Spider local-helper boundary |
| 多层协议和最终 collector | 退出 profile，返回 Spider core loop |

所有外部转交都先读取 capability snapshot。不得假设某个技能存在；专用技能不可用时必须执行表中的 Spider fallback。

## 默认输出

始终给出：

1. 一段可直接执行的最小脚本。
2. 注入位置和时机。
3. 触发动作与预期日志。
4. 副作用、恢复函数或刷新恢复说明。

用户目标明确时再说明为什么选择该 Hook 点。不要同时堆多个大脚本。

🔴 CHECKPOINT：改写原型链、全局对象、构造器或返回值前，先声明 Hook 点、页面上下文、恢复方式和可检测风险。用户未要求篡改行为时只做观察。

## 工作流

1. 判断目标是属性、方法、构造器还是请求边界。
2. 选择最窄的 Hook 点和 URL/字段过滤条件。
3. 保存原始 descriptor 或函数引用，保持 `this`、参数、返回值和异常语义。
4. 默认只记录类型、长度、去 query/hash 的 URL、时间和调用栈；高频调用加去重或计数。
5. 明确触发动作，验证一次命中。
6. 提供恢复方式；需要落地日志时写入执行项目的 `js_reverse_cache/`。

先声明 intake mode。`artifact-only` 或未要求检查当前页面时，直接交付 Console/Snippets 脚本并标记现场命中未验证；需要与当前目标发生新交互时改为 `live-target`，执行 Spider 主入口规定的顺序双工具取证。只有用户要求直接注入时才修改页面；其他 `live-target` 场景在完成证据采集后交付脚本，不擅自注入。

## 数据与请求绑定

观察请求字段时，尽量输出：

- `target`: fetch、xhr、websocket、form 或 beacon
- `event`: open、send、setRequestHeader、response 或 message
- method、URL、命中的字段名
- 类型和长度；URL 去掉 query/hash
- 可选 `console.trace()` 或一次性 `debugger`

`document.cookie` Hook 只能证明 JS 写入；HTTP `Set-Cookie` 必须结合响应头判断，不能混为同一来源。

## 安全与降噪

1. Cookie、Authorization、token、storage value、body 和响应内容默认只记录类型/长度，不输出片段。
2. ArrayBuffer、Blob、canvas data URL 和 WebSocket 消息只打印类型和长度。
3. 页面存在完整性检测、native 检测或 JSVMP 环境探测时，先说明 JS Hook 可能改变行为。
4. Hook 后请求消失、签名降级或页面异常时，立即恢复并缩小 Hook 点，不继续叠加 Proxy。
5. 不提供持久 `FULL_LOG` 开关；用户明确需要现场值时用一次性 debugger 暂停检查，不把值写入 Console 或公共案例。

## Failure Modes

| 触发条件 | 处理动作 | 兜底 |
|---|---|---|
| 属性不可配置 | Hook 外围调用点或原型方法 | 不强行覆盖 descriptor |
| 页面行为改变 | 恢复原对象并缩小范围 | 改条件断点、initiator 或引擎 trace |
| 日志刷屏 | 加 URL、字段、次数和长度过滤 | 默认关闭完整值 |
| 用户转而要函数位置或调用链 | 停止扩写 Hook | 按上方 capability-aware 转交；不可用时返回 Spider core loop |
| 用户转而要本地执行 | 固定样本和入口线索 | 已知 Node/VM 入口转 env-patch；明确 iv8 时按 capability-aware 转交 |

## 资源路由

按目标只读取一个分类，必要时再补第二个。下列路径均为 skill-root 可解析路径（也可用 `$HOOK_PROFILE/references|scripts/...`）。`references/` 只解释 Hook 点和扩展约束；可执行片段必须从 `scripts/` 的受测实现生成，不能从 reference 文档恢复旧的全值日志：

- `references/profiles/browser-hook-snippets/references/network.md`: XHR、fetch、WebSocket、postMessage
- `references/profiles/browser-hook-snippets/references/storage.md`: cookie、localStorage、sessionStorage
- `references/profiles/browser-hook-snippets/references/crypto.md`: WebCrypto、CryptoJS、随机数和编码
- `references/profiles/browser-hook-snippets/references/dom.md`: DOM 注入、MutationObserver、canvas
- `references/profiles/browser-hook-snippets/references/runtime.md`: JSON、eval、Function、Blob、Worker
- `references/profiles/browser-hook-snippets/references/snippets.md`: 片段索引
- `references/profiles/browser-hook-snippets/references/hook-output-samples.md`: 输出和降噪样本

预置脚本：

- `references/profiles/browser-hook-snippets/scripts/xhr_fetch.js`
- `references/profiles/browser-hook-snippets/scripts/cookie_header.js`
- `references/profiles/browser-hook-snippets/scripts/crypto_api.js`
- `references/profiles/browser-hook-snippets/scripts/storage.js`

修改或迁移 profile 后运行：

```bash
npm test --prefix "$HOOK_PROFILE"
```

完成标准是用户能直接执行脚本、触发一次有效日志、恢复页面状态，并知道何时应升级到调用链定位或本地复现。
