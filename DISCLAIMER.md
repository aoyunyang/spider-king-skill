# Disclaimer / 免责声明

**Last updated / 更新日期:** 2026-09-02

Spider King (“this skill”, “this project”, “the software”) is an educational and engineering skill for **authorized web protocol recovery**: reconstructing how a browser client talks to a server, and turning that evidence into a **browser-free Python collector**.

Spider King（下称「本技能」「本项目」「本软件」）是一份面向 **已获授权场景** 的工程/教学技能，用于网页协议还原：从浏览器客户端收集证据，恢复真实请求、签名、引导态、解码或传输封装，并交付 **无浏览器驱动的 Python 采集路径**。

By cloning, installing, forking, modifying, distributing, or using this project, you acknowledge that you have read, understood, and agreed to this Disclaimer.

凡克隆、安装、分叉、修改、传播或使用本项目，即视为已阅读、理解并同意本免责声明。

## 1. Nature of the Project / 项目性质

This project describes methods, checklists, and tooling conventions for inspecting web scripts, network traffic, cookies, WebSocket / GraphQL / protobuf-shaped transports, WASM helpers, and challenge/bootstrap flows **on a target you are allowed to analyze**, then delivering a protocol collector rather than a stealth browser farm.

本项目描述方法、检查清单与工具约定，覆盖在 **你有权分析的目标** 上观察网页脚本、网络流量、Cookie、WebSocket / GraphQL / protobuf 类传输、WASM 与挑战/引导流程，并交付 **协议采集器**，而不是隐身浏览器集群或通用攻击框架。

This is **not** a hacking-as-a-service kit, malware, exploit pack, credential stealer, account-takeover tool, a promise that every website can or should be collected without a browser, or legal / compliance / pentest certification.

本项目 **不是** 黑客即服务工具包、恶意软件、漏洞利用包、凭据窃取或账户接管工具，也不是「任何网站都能无浏览器采集」的承诺，更不是法律意见、合规认证或渗透测试资质。

## 2. Authorized Use Only / 仅限授权使用

You may use this skill **only** if at least one of the following is true:

1. you own the target system; or
2. you have **written, currently valid authorization** from the owner (bug bounty brief, contract, internal security assessment, research exemption, etc.); or
3. you are analyzing **your own captured artifacts** / a local lab fixture, with no live unauthorized access; or
4. the activity is otherwise lawful in your jurisdiction.

仅在以下情形之一成立时，你才可以使用本技能：目标由你所有；你持有权利人 **现行有效的书面授权**；你只分析自己已合法持有的样本或本地实验夹具；或该行为在你所在法域本身合法。

**If you do not have authorization, do not use this skill against a live site.**
**没有授权，禁止对真实站点使用本技能。**

## 3. Prohibited Uses / 禁止用途

You agree **not** to use this project to:

- access, scrape, replay, or collect from systems **without permission**;
- bypass authentication, payments, rate limits, bot management, WAF, device-trust, or anti-fraud controls **to commit abuse or fraud**;
- steal, forge, traffic, or persist other people’s cookies, tokens, sessions, credentials, or personal data;
- attack, degrade, or overload any service;
- build or distribute malware, exploit payloads, credential stuffers, or unauthorized account automation;
- violate legally binding Terms of Service, copyright, database rights, export controls, or anti-circumvention rules;
- unlawfully process personal data.

你同意 **不得** 将本项目用于未经许可的访问/抓取/重放、为欺诈而绕过鉴权或风控、窃取或持久化他人凭据与个人信息、攻击或压垮服务、编写传播恶意软件或漏洞利用、以及在对你具有法律约束力的范围内违反网站条款、著作权、反规避或数据保护规则。

The authors do not condone, assist, or accept commissions for criminal or clearly unauthorized activity.

作者不认可、不协助、不接受任何犯罪或明显未授权活动的委托。

## 4. You Are the Operator / 使用者自行承担责任

This skill may be executed by a human or by an AI coding agent. In all cases, **the human who runs, directs, or publishes the work is the operator**.

本技能既可能由人直接使用，也可能由 AI 编程代理执行。无论哪种方式，**实际运行、指挥或公开发布成果的人，都是操作者**。

The operator is solely responsible for confirming authorization before any live-target work; complying with local law (including computer-misuse, anti-circumvention, PIPL / GDPR, cybersecurity, and unfair-competition rules); keeping raw cookies, tokens, credentials, and personal data out of git, issues, chat logs, and public artifacts; and any collector, helper, report, or derivative they produce.

操作者须自行确认授权、遵守所在地法律、脱敏秘密，并对其产出的采集器、辅助脚本、报告或衍生作品承担全部后果。

**The project authors, maintainers, contributors, and any AI system that helped generate or execute this skill are not your lawyer, pentester of record, or accomplice.**

**本项目的作者、维护者、贡献者，以及协助生成或执行本技能的任何 AI 系统，都不是你的律师、备案渗透测试方或共犯。**

## 5. No Warranty / 无担保

THE SOFTWARE AND DOCUMENTATION ARE PROVIDED “AS IS” AND “AS AVAILABLE”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, ACCURACY, OR UNINTERRUPTED AVAILABILITY.

本软件及文档按「现状」「现有」提供，**不附带任何明示或默示担保**。

Protocol recovery against hostile clients is inherently brittle. Vendors change scripts, fingerprints, challenges, and transports without notice. Nothing in this skill promises that a collector will keep working, that a bypass is complete, or that replay is currently accepted.

对抗型客户端的协议还原本质上不稳定。本技能不承诺采集器持续可用、绕过已完成，或当前重放仍被服务端接受。

## 6. Limitation of Liability / 责任限制

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THE AUTHORS, MAINTAINERS, CONTRIBUTORS, AND COPYRIGHT HOLDERS SHALL NOT BE LIABLE FOR ANY CLAIM, DAMAGE, LOSS, INVESTIGATION, FINE, ACCOUNT BAN, CIVIL OR CRIMINAL LIABILITY, LOST PROFITS, LOST DATA, BUSINESS INTERRUPTION, OR CONSEQUENTIAL / INCIDENTAL / SPECIAL DAMAGES ARISING FROM your use or misuse of this project, unauthorized access to third-party systems, publication of secrets or collectors, reliance on incomplete or outdated playbooks, or actions taken by an AI agent following this skill.

在适用法律允许的最大范围内，作者、维护者、贡献者及著作权人 **不对** 因使用或滥用本项目、未授权访问、公开秘密或采集器、依赖过时 playbook、或 AI 代理按本技能采取的行动而产生的索赔、损害、罚款、封号或民刑事责任负责。

This Disclaimer does not exclude liability that cannot legally be excluded.

依法不能排除的责任，不受本声明排除。

## 7. Third-Party Systems, Marks, and Code / 第三方系统、标识与代码

Names of websites, CDNs, bot-management vendors, browsers, or JS SDKs appear only as **technical examples**. They do not imply affiliation, sponsorship, or permission.

文中出现的网站、CDN、人机验证厂商、浏览器或 JS SDK 名称仅为 **技术举例**，不表示存在关联、赞助或授权。

Do not copy vendor scripts, WASM blobs, trademarked assets, or copyrighted SDK files into public forks unless you have a license to do so. Prefer describing shapes, hashes, field names, and local helpers you wrote.

除非拥有相应许可，否则不要把厂商脚本、WASM 或受版权保护的 SDK 拷进公开仓库。

## 8. Secrets and Evidence Hygiene / 秘密与证据卫生

If you publish issues, pull requests, reports, or case studies: redact cookies, tokens, `Authorization` values, account IDs, and other personal or secret data; do not commit live session material or production collector configs that still work against a third-party site; keep raw captures in a local, ignored secret store.

公开材料必须脱敏。不要提交仍可打到第三方站点的活会话、私钥或生产采集配置。

## 9. Open Source License vs This Disclaimer / 开源协议与本声明

This Disclaimer is **in addition to**, and does not replace, the MIT License in `LICENSE`.

本免责声明是对 `LICENSE` 中 MIT 许可证的 **补充**，并不取代它。

- The license grants copyright permissions for the **code and text**.
- This Disclaimer states that those permissions **do not grant extra rights in third-party systems**, and do not waive your duty to obey the law.

开源许可证授予的是对本 **代码与文本** 的著作权许可，并不额外授予你对第三方系统的访问权。

If there is a conflict about copyright permissions, the LICENSE file controls. If there is a conflict about acceptable use and liability, this Disclaimer is intended to control to the extent permitted by law.

若冲突涉及著作权许可，以 `LICENSE` 为准。若冲突涉及可接受使用与责任，在法律允许范围内以本声明为准。

## 10. No Obligation to Support Misuse / 无义务支持滥用诉求

Maintainers may refuse, revert, or report contributions, issues, or private requests that target a live system without proof of authorization; ask for weaponized bypasses, exploit PoCs, or malware; include unretracted secrets; or are clearly intended for criminal or fraudulent use.

维护者可以拒绝、回滚或举报无授权线上目标、武器化绕过、未脱敏秘密，或明显用于犯罪/欺诈的请求。

## 11. Indemnity / 补偿

To the extent permitted by law, you agree to indemnify and hold harmless the authors, maintainers, and contributors from claims, damages, losses, and expenses (including reasonable legal fees) arising out of your use of this project or your violation of this Disclaimer or applicable law.

在法律允许范围内，你同意就因你使用本项目、或违反本声明或适用法律而产生的索赔、损害、损失和费用（包括合理律师费），补偿并使作者、维护者与贡献者免受损害。

## 12. Acceptance / 接受

If you do not agree with this Disclaimer, **do not download, install, fork, or use** this project.

若你不同意本声明，请 **不要下载、安装、分叉或使用** 本项目。
