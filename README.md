# Spider King
<img width="591" height="250" alt="image" src="https://github.com/user-attachments/assets/cfbb487e-8def-4a6c-b8da-0d1bd0e83771" />

`Spider King` 是一套面向 Web 协议恢复与参数还原场景的逆向工程 Skill。

它的目标不是“把网页点通”，也不是“用浏览器把请求糊过去”，而是把看起来依赖浏览器环境的目标，拆回到可复现、可验证、可长期维护的纯协议采集链路中。

- 先证据，后结论
- 先协议，后自动化
- 先还原动态状态，再谈分页、规模化
- 最终交付必须脱离浏览器运行

## 核心定位

`Spider King` 解决的不是“怎么自动点按钮”，而是下面这类问题：

- 页面代码写的是一个接口，真实网络请求走的是另一个接口
- 业务层构造了 `sign` / `token`，但真正发包前又被 wrapper 改写
- 请求能发出去，但响应体仍然要经过解码、解密、字形映射或二进制解析
- 页面能用，协议重放不稳定，表现为 `403`、`412`、`429`、偶发成功、只第一页成功等
- 签名、Cookie、挑战脚本、WASM、WebSocket 会话、协议包装、响应侧解码纠缠在一起

一句话概括：

> 它是一套“把 hostile web client 还原成 stable protocol collector”的方法论与执行框架。

## 核心能力

当前版本围绕 `chrome-devtools` 与 `js-reverse` 两套 MCP 工具展开，强调轻量双工具侦察、离线还原、Python 优先交付。

主要能力包括：

- 协议路径恢复：识别假接口、真实接口、包装层、跳转链与兼容页
- 动态参数定位：区分签名、随机片段、时间戳、旋转 Cookie、包装字段、挑战产物
- 协议包装还原：处理 GraphQL、WebSocket、protobuf、msgpack、加密信封、请求 wrapper
- 响应侧恢复：处理解密、压缩、字形映射、分层编码、二进制帧解码
- 环境差异分析：识别“标准函数被补丁化”“本地输出与页面输出不一致”等问题
- 挑战与引导链恢复：处理服务器返回 JS、启动引导、Cookie 写入、预热请求
- 状态流恢复：处理登录、配对、心跳、ack、会话密钥、媒体派生密钥等流式协议
- Python-first 交付：最终采集器优先使用 Python，只在必要时保留极小 JS / WASM helper

## 这套 Skill 不做什么

为了保证最终交付可靠、可迁移、可维护，`Spider King` 明确不把以下做法视为合格答案：

- Playwright / Selenium / CDP 驱动页面作为最终交付
- 隐式依赖浏览器 profile、手工登录状态、手工点击流程
- 用页面内 `fetch` 代替真正的协议恢复
- 只做一次幸运重放，不验证重复性
- 把动态 Cookie、一次性 token、挑战结果直接硬编码进最终代码

这不是一个浏览器自动化 Skill。

这也不是一个“只要能跑就行”的抓包脚本模板。

它是一套以“纯协议交付”为终点的逆向工作流。

## 方法论概览

`Spider King` 的最短主线可以概括为五步：

1. 先做 `Startup Gate`
2. 用 `chrome-devtools` 与 `js-reverse` 做轻量双工具侦察
3. 找到真实请求与真实动态状态
4. 在本地离线重建这些动态状态
5. 交付脱离浏览器运行的 Python 采集器

更细一点的执行逻辑如下：

### 1. Startup Gate

在正式深入分析前，先完成三件事：

- 环境与工具可用性检查
- 目标家族分流
- 最终交付意图声明

当前 Skill 将目标优先分成四类：

- `signer-gated`
- `verifier-gated`
- `decode-gated`
- `session-gated`

这一步的意义不是“写模板”，而是尽早判断这到底是哪种仗，避免一上来就钻进大 bundle 或把页面样本弄脏。

### 2. 轻量双工具侦察

每个 fresh target 都要先过一轮轻量 paired pass：

- `chrome-devtools` 负责页面状态、跳转链、首轮网络视图、可见流程
- `js-reverse` 负责 initiator、源码搜索、wrapper 追踪、首轮 mutation 假设

这里强调的是“轻量”。

也就是说，fresh target 必须双工具起手，但不代表一上来就要做重型 Hook、深度断点或侵入式浏览器操作。

### 3. 识别真实动态状态

Skill 的核心原则之一是：

> 真正变化的东西，不一定叫 `sign`。

真实动态状态可能是：

- 旋转 Cookie
- 页面专属 header
- 请求 wrapper 字段
- 服务器返回的引导 JS
- 动态字体
- WASM 导出
- 响应侧解码链
- 会话绑定状态

### 4. 离线重建

一旦确认了真实动态状态，交付路径按成本和稳定性排序：

1. 纯 Python
2. Python + 极小 JS helper
3. Python + 极小 WASM helper
4. Python + 本地 bootstrap executor

最终目标始终不变：

- 不依赖浏览器
- 不依赖手工动作
- 不依赖隐藏页面上下文

### 5. 重复性验证

`Spider King` 不接受“这次跑通了”作为完成条件。

至少要验证：

- 同样逻辑能稳定成功 2 到 3 次
- 分页 / cursor 能前进
- 关键动态状态能正确再生
- 页面特例、账号边界、列表/详情权限边界被明确记录

## 为什么这套 Skill 更适合复杂目标

`Spider King` 的优势不在“工具多”，而在“把复杂目标拆成稳定问题”。

它特别适合处理这些复杂症状：

- 页面显示的接口和网络层真实接口不一致
- 签名函数名称看着标准，但输出和标准实现不一致
- 只有最后一页失败，或者某一页需要特殊头
- 页面公开可见，但真实业务请求仍依赖引导配置、Cookie 或包装层
- 响应不是直接数据，而是加密字段、乱码、字体字形、二进制帧
- WebSocket 建立后要经历 auth / subscribe / heartbeat / ack 才能拿到数据
- 挂 Hook 以后反而更容易失败，出现明显 observer effect

## 目录结构

当前仓库结构如下：

```text
spider-king/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── check_reverse_env.py
│   ├── crypto_fingerprint.py
│   ├── protocol_diff.py
│   └── scaffold_reverse_project.py
└── references/
    ├── workflow-overview.md
    ├── startup-triage-playbook.md
    ├── tool-playbook.md
    ├── official-self-test-task-suite.md
    ├── crypto-patterns.md
    ├── obfuscation-guide.md
    ├── jsvmp-analysis-playbook.md
    ├── structured-transport-playbook.md
    ├── response-decode-playbook.md
    ├── server-js-cookie-bootstrap-playbook.md
    ├── cookie-provenance-playbook.md
    ├── stateful-stream-e2ee-playbook.md
    └── ...
```

其中：

- `SKILL.md` 是主技能定义文件，也是最高优先级规则入口
- `references/` 是按症状路由的通用参考手册
- `scripts/` 是高频辅助脚本，用来缩短重复劳动
- `agents/openai.yaml` 用于技能代理配置

## 关键参考文档

如果你第一次接触这个仓库，建议按下面顺序阅读：

1. `SKILL.md`
2. `references/workflow-overview.md`
3. `references/startup-triage-playbook.md`
4. `references/tool-playbook.md`
5. `references/official-self-test-task-suite.md`

按场景继续深入时，再按症状跳转：

- 参数不一致、wrapper 重写：`transport-wrapper-playbook.md`
- 标准函数不标准：`patched-helper-playbook.md`
- 浏览器输出与本地输出不一致：`env-diff-playbook.md`
- JSVMP / 重混淆：`jsvmp-analysis-playbook.md`
- 服务器返回 JS 引导 Cookie：`server-js-cookie-bootstrap-playbook.md`
- 响应需要本地解码：`response-decode-playbook.md`
- WebSocket / 长连接会话：`stateful-stream-e2ee-playbook.md`
- 挑战或 verifier：`verifier-replay-playbook.md`

## 辅助脚本说明

仓库中自带 4 个辅助脚本：

### `scripts/check_reverse_env.py`

快速检查本地 reverse 环境是否具备最小运行条件。

适合在 fresh target 开始前先确认：

- Python 是否可用
- Node / npm / curl / git 是否可用

### `scripts/crypto_fingerprint.py`

用于快速判断可疑输出更像哪一类摘要、Base64、字母表变种或自定义编码。

### `scripts/protocol_diff.py`

用于对比多组请求 / 响应样本，把真正有意义的差异筛出来。

适合排查：

- 哪个字段才是真正动态字段
- 某一页为什么失败
- 某次响应为什么和成功样本不同

### `scripts/scaffold_reverse_project.py`

用于生成 Python-first 的协议恢复项目骨架。

适合在确认交付形态之后，快速落出一个结构清晰的项目目录，而不是把所有逻辑塞进一个 `main.py`。

## 安装方式

你可以将本仓库放入支持 Skill / Agent 能力的工具目录中，例如：

```bash
git clone <your-repo-url> ~/.codex/skills/spider-king
```

如果你的工具支持通过 `SKILL.md` 自动加载技能定义，那么只要仓库目录结构保持一致即可。

## 适用场景

建议在以下场景触发 `Spider King`：

- 已拿到目标页面 URL、接口 URL、请求样本、Cookie 样本或 JS 片段
- 明确需要恢复参数、协议包装、响应解码或状态流
- 最终目标是可复现、可长期维护的协议采集器
- 需要将签名 / bootstrap / 解码逻辑落到 Python 或本地 helper 中

## 不适用场景

以下情况不建议使用这套 Skill 作为主路径：

- 需求本质只是标准 UI 自动化
- 目标本身没有公开协议恢复价值，只是简单页面操作录制
- 最终交付允许长期依赖浏览器 profile、人工点击、人工登录维持
- 没有任何合法授权边界，不适合进入实际协议恢复流程

## 交付标准

一个通过 `Spider King` 完成的任务，理想上应包含以下产物：

- 真实接口路径说明
- 动态状态分类结论
- 关键固定输入 / 输出验证样本
- Python 采集器
- 必要时的极小 JS / WASM helper
- 原始请求 / 响应样本
- 风险与不稳定点说明

合格交付至少满足：

- 不依赖浏览器自动化
- 不依赖手工页面操作
- 重放逻辑可重复成功
- 关键动态状态可解释、可验证、可再生

## 自检与防漂移

这个仓库已经开始把“技能回归检查”纳入设计：

- `references/official-self-test-task-suite.md` 用于验证主路线是否仍然 protocol-first
- `Startup Gate` 用于确保 fresh target 不会一上来就乱冲
- `tool-playbook.md` 强调只使用当前真实可用的 MCP 能力，不依赖不存在的工具方法

后续如果继续演进这个仓库，推荐始终把这三类内容一起维护：

- 主技能规则
- 参考手册路由
- 自测任务与回归标准

## 一句话总结

`Spider King` 不是让浏览器替你干活。

它是让你把浏览器里看起来神秘、脆弱、依赖上下文的行为，拆回成一条可验证、可复现、可长期运行的本地协议链路。
