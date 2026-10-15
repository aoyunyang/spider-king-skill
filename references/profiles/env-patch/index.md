# Node/VM Environment Patch Profile

## Contents

- [唯一职责](#唯一职责)
- [准入条件](#准入条件)
- [工具与目录](#工具与目录)
- [核心循环](#核心循环)
- [浏览器 Seed](#浏览器-seed)
- [高级路径准入](#高级路径准入)
- [Failure Modes](#failure-modes)
- [Reference Router](#reference-router)

## 唯一职责

接收已确认的 JS 入口和浏览器样本，完成 `Rebuild -> Patch -> Consolidate`。本 profile 不负责从未知站点寻找入口；完整协议编排仍由 Spider core loop 拥有。

共享阶段与 handoff 字段由 Spider King 主入口、`references/workflow-overview.md` 与任务目录 `js_reverse_cache/tasks/<task-id>/` 约定定义。

## 准入条件

开始前必须具备：

1. 本地目标脚本或明确模块 ID。
2. 入口函数、init/setup 参数或触发方式。
3. 至少一组真实输入和预期输出/格式证据。

如果目标是 JSVMP 或 SDK interceptor，先读取 `references/profiles/env-patch/references/jsvmp-interceptor-contract.md`。脚本能 load 但签名静默时，优先证明 activation、路径白名单和 transport owner，不先扩充 BOM/DOM。

开始分流前读取 capability snapshot，不得假设外部技能已经安装：

| 当前缺口 | 首选路由 | 专用能力不可用时 |
|---|---|---|
| 缺少入口或调用链 | 已安装的专用 JS 逆向技能 | 返回 Spider core loop，用 `chrome-devtools` / `js-reverse` initiator evidence 定位 |
| 只需观察 Hook | Spider browser-hook profile | 直接使用本技能内置 profile |
| 整文件 AST 还原 | `../static-ast/index.md` | 使用 `references/offline-inline-deob-playbook.md` 与 `references/obfuscation-guide.md` 本地恢复 |
| 明确 Python + iv8 | 已安装的 iv8 专用技能 | 报告能力缺失；只有用户接受替代后，才改走 env-patch 或最小 local helper boundary |
| CAPTCHA/TDC collect、行为数据或 verify | 已安装的匹配 specialist primary | 返回 Spider core loop；本 profile 只保留 Node/VM secondary backend |
| 多层协议或最终 collector | Spider core loop | 退出本 profile，不在补环境层扩张协议职责 |

瑞数入口 runtime 已确认且目标是 Node.js/VM 补环境时，本 profile 可以继续；入口尚未定位时执行上表的调用链路由。

## 工具与目录

先设置 profile 根目录。以下命令用 `$ENV_PROFILE` 表示它：

```bash
ENV_PROFILE="$SKILL_DIR/references/profiles/env-patch"
```

```powershell
$ENV_PROFILE = Join-Path $SKILL_DIR "references/profiles/env-patch"
```

本 profile 的工具为：

- `$ENV_PROFILE/scripts/env-diagnose.js`: 默认诊断器
- `$ENV_PROFILE/scripts/analyze-gap-log.js`: 缺口归因
- `$ENV_PROFILE/scripts/collect-browser-env.js`: 浏览器 seed 采集
- `$ENV_PROFILE/scripts/env_core.js`: 高级手写环境引擎
- `$ENV_PROFILE/scripts/webpack_runtime.js`: 最小 webpack runtime
- `$ENV_PROFILE/env/`: 可组合环境模块
- `$ENV_PROFILE/env/webapi/runtime-contracts.js`: opt-in `MessageChannel` 与 webpack chunk 契约

`node:vm` 只是兼容执行上下文，不是安全边界。未知、混淆或第三方目标脚本必须先放入无凭据、最小文件挂载、默认断网的临时 OS/container sandbox；profile 中的确认开关只防误执行，不提供隔离。

可用容器时，先把目标和明确需要的 custom patch 复制到一个不含 `.env`、Cookie、SSH key 或其它项目文件的专用 staging 目录，并设置 `SANDBOX_INPUT` 指向它。诊断进程至少使用 `--network none`、只读最小 mount、内存/CPU 限制、非 root 用户和空 secrets/env。确认参数只能出现在这样的隔离进程内：

```bash
docker run --rm --network none --read-only --memory 512m --cpus 1 \
  --user node -v "$ENV_PROFILE:/profile:ro" -v "$SANDBOX_INPUT:/work:ro" node:22-alpine \
  node /profile/scripts/env-diagnose.js --external-sandbox-confirmed /work/target.js
```

没有等价外部隔离能力时，不执行未知目标，停在源码、Hook/trace 和 handoff 证据。

迁移、打包或修改诊断器后先运行：

```bash
node "$ENV_PROFILE/tests/test-env-diagnose.js"
```

任务补丁、诊断和样本写入项目的 `js_reverse_cache/tasks/<task-id>/env/`，不写入 skill 目录，不修改目标原始源码。每个任务使用独立 `<task-id>`，不得跨任务复用可写 patch、样本或 `run.js`。

## 核心循环

### 0. 固定入口契约

独立 SDK 先确认 init/setup 参数、URL 匹配规则和触发顺序。缺失 init 参数可能让 SDK 静默跳过签名，不能用“加载成功”代替入口验证。

同时记录目标脚本 hash/version、公开 signer 与 XHR/fetch interceptor 的所有权、query/header/body 写入槽位，以及是否存在 response/warm-up 写入。用一个命中路径和一个未命中路径做正负控制；完整合同见 `references/profiles/env-patch/references/jsvmp-interceptor-contract.md`。

### 1. 空环境诊断

```bash
node $ENV_PROFILE/scripts/env-diagnose.js --external-sandbox-confirmed <target.js>
```

保存已脱敏的 error 分类、`undefinedPaths`、descriptor/prototype access 和调用异常作为基线。默认 `consoleOutput` 只保留值类型与长度，不回显目标字符串、对象内容或异常正文。

### 2. 选择最小模块

按 `references/profiles/env-patch/references/env-modules.md` 做路径前缀匹配，并按 `references/profiles/env-patch/references/loading-order.md` 排序。每轮只增加能解释当前 first divergence 的模块。

### 3. 重新诊断

```bash
node $ENV_PROFILE/scripts/env-diagnose.js \
  --external-sandbox-confirmed \
  --env bom/navigator.js,bom/location.js,dom/document.js \
  <target.js>
```

比较缺失路径是否减少、错误是否前移、目标输出是否更接近浏览器样本。

### 4. 处理剩余缺口

优先级固定为：

1. 修正模块加载顺序或依赖。
2. 用 `analyze-gap-log.js` 归因到已有模块。
3. 在 `js_reverse_cache/tasks/<task-id>/env/ai-generated/` 写一个最小 custom patch。
4. 只有真实值参与分支或输出时，才把 `collect-browser-env.js` 复制到任务目录，在项目副本的 allowlist 中加入单一字段并采集一个 baseline；Cookie、storage、query/hash 和 canvas 默认不采集。
5. 模块树无法表达 native 外形、webpack 模块或长期 patch plan 时，才启用 `env_core.js`。

Custom patch 使用 IIFE 和 `Object.defineProperty`，保持稳定语义文件名；不要自动扫描或偷偷加载任务补丁。

任何补丁都必须通过 `references/profiles/env-patch/references/no-touch-and-profile-coherence.md`：无读取证据时不改原型、构造器外形、第二个 `Function.prototype.toString` owner 或高熵 API；UA、Client Hints、navigator、screen、Canvas/WebGL 与 TLS/H2 必须来自同一浏览器家族 profile。

### 5. 循环与退出

继续条件：缺失路径减少、first divergence 前移，或错误变化且有明确因果解释。

停止条件：

- 连续两轮缺失路径和 first divergence 完全相同。
- 剩余依赖超出 Node/VM 可诚实模拟的宿主能力。
- 入口契约或浏览器样本被证明不完整，需要回到上游取证。

### 6. 功能验证

`success: true` 只代表脚本加载，不代表签名、Cookie 或加密功能可用。必须在 `js_reverse_cache/tasks/<task-id>/env/run.js` 中按真实调用顺序触发入口，并依次通过 `load-pass -> activation-pass -> fixed-vector-pass -> live-acceptance-pass`。精确固定向量必须冻结或回放时间、熵、计数器、session/round 状态和 canonical wire bytes；形状检查只能辅助定位。

Hook 型 SDK 的常见顺序是：`env -> fake transport -> target JS -> capture hook -> init -> trigger`。

### 7. 请求验证与收口

固定输入通过后再封装 `sign.js` 或本地 HTTP 中间层，并沿用同一请求契约验证服务端。HTTP 200 但业务码、字段或数据为空仍算失败。

🔴 CHECKPOINT：真实请求前报告 `run.js` 输出、浏览器对照、baseline/session 来源和签名结构；缺任一项不做可用结论。

## 浏览器 Seed

只有目标确实读取真实环境值时才采集：

1. 一条复现链选择一个 baseline，不混拼 UA、Cookie、storage、screen、canvas 或 TLS 来源。
2. 记录 URL、时间、session、未采集字段和输出路径。
3. 原始快照只写任务目录，不进入公开 case。
4. 被风控阻断且需要反检测基线时，使用 capability snapshot 中可用的专用浏览器逆向技能采证；不可用时返回 Spider core loop，执行顺序 `chrome-devtools` / `js-reverse` 取证后再交回。

🔴 CHECKPOINT：写入 seed 前声明唯一 baseline、session 关联和目标 patch；来源冲突时先停。

## 高级路径准入

只有满足一项才启用 `env_core.js` 或 `webpack_runtime.js`：

- 需要 native `toString`、构造器外形或 `Symbol.toStringTag` 契约。
- 模块化环境能加载，但固定输入在明确位置分歧。
- 已知 webpack 模块 ID，需要最小 runtime 调用。
- 项目需要长期维护集中式 patch plan。

高级路径仍不能跳过 fixed fixture 和服务端验证。

`env_core.js` 会在 host Node realm 中运行代码，风险高于诊断器。只允许在上述外部隔离环境中使用，并要求设置 `SPIDER_EXTERNAL_SANDBOX_CONFIRMED=1`；执行完成必须在 `finally` 调用 `env.restore()`。

## Failure Modes

| 触发条件 | 处理动作 | 兜底 |
|---|---|---|
| 入口或 init 参数缺失 | 停止补环境 | 转上游补齐调用链证据 |
| parse/load 失败 | 记录第一条真实错误 | 不一次加载全部 env 模块 |
| 两轮没有推进 | 回查 first divergence 和加载顺序 | 升级高级路径或报告边界 |
| 浏览器 seed 冲突 | 保留一个 baseline | 其它样本只作诊断对照 |
| load 成功但输出不一致 | 比较固定输入和关键中间值 | 不封装请求层 |
| 服务端拒绝 | 检查 session、序列化、时间和 transport | 必要时退出 profile，由 Spider core loop 协调协议层 |

## Reference Router

- `references/profiles/env-patch/references/env-modules.md`
- `references/profiles/env-patch/references/loading-order.md`
- `references/profiles/env-patch/references/architecture.md`
- `references/profiles/env-patch/references/module-contracts.md`
- `references/profiles/env-patch/references/env-core-advanced.md`
- `references/profiles/env-patch/references/browser-stubs.md`
- `references/profiles/env-patch/references/path-upgrade-checklist.md`
- `references/profiles/env-patch/references/node-detection.md`
- `references/profiles/env-patch/references/webpack.md`
- `references/profiles/env-patch/references/runtime-contracts.md`
- `../../runtime-state-continuity-playbook.md`
- `references/profiles/env-patch/references/jsvmp-interceptor-contract.md`
- `references/profiles/env-patch/references/no-touch-and-profile-coherence.md`
- `references/profiles/env-patch/references/verification-and-replay.md`
- `references/profiles/env-patch/references/limitations.md`

修改或迁移 profile 后运行：

```bash
npm test --prefix "$ENV_PROFILE"
```

完成报告包含入口契约、加载模块、first divergence 修复、fixture 结果、请求验证和剩余宿主边界。
