# Local MCP Environment

Shareable attach and host-capacity notes for Spider King. Generic routing doctrine stays in `references/mcp-routing-playbook.md` and `references/tool-playbook.md`.

This file ships machine-agnostic defaults and placeholders only. Put operator-private paths, API keys, profile directories, and one-off ports in a local overlay outside the skill tree, or fill the placeholders below without committing real secrets.

## Contents

- [Purpose](#purpose)
- [Expected local roles](#expected-local-roles)
- [Auto-judge local means](#auto-judge-local-means)
- [Common endpoints](#common-endpoints)
- [Chrome debug profile](#chrome-debug-profile)
- [Camoufox host notes](#camoufox-host-notes)
- [Local overlay convention](#local-overlay-convention)
- [Preflight checks](#preflight-checks)

## Purpose

Record how a workstation can expose optional MCP-related endpoints and host providers. Do not treat these notes as proof that a Codex session has the corresponding MCP server mounted. Never hardcode personal drive letters, home directories, cloud-sync folders, or account-bound profile paths into the shared skill package.

## Expected local roles

| Role | Local means |
|---|---|
| Default browser baseline / debugger | `chrome-devtools`, `js-reverse` when mounted in the agent session |
| High-fingerprint baseline host | Camoufox or managed anti-detect profile when installed and required by Auto Judge |
| Passive wire-store | Reqable report ingest when configured |
| ENV / profile provider | AdsPower Local API when installed |
| Wire visibility | WireMCP + tshark when installed |
| Debug profile dir | dedicated Chrome user-data-dir, not the daily browsing profile |

## Auto-judge local means

Use these local facts only after the skill Auto Judge chooses the branch:

| Auto Judge branch | Prefer on this machine |
|---|---|
| `artifact-only` | files / Reqable history only; do not launch Camoufox or Chrome for ceremony |
| low-pressure `live-target` | `chrome-devtools` on the Chrome debug profile, then `js-reverse` |
| high-pressure `live-target` | start Camoufox/managed host for clean baseline first |
| debugger needed after host baseline | attach `js-reverse` or `chrome-devtools` only if a debuggable endpoint exists |
| no attach endpoint after Camoufox baseline | keep HAR/request exports and continue offline with `debugger_attach_gap` |

## Common endpoints

Typical defaults. Override from the live process or operator config when values differ.

| Service | Typical local value | Placeholder / override |
|---|---|---|
| Chrome remote debugging | `http://127.0.0.1:9222` | `<chrome-debug-url>` |
| Reqable MCP ingest | `http://127.0.0.1:18765/report` | `<reqable-report-url>` |
| Reqable WS events | `http://127.0.0.1:18765/ws/events` | `<reqable-ws-url>` |
| AdsPower Local API | `http://127.0.0.1:50325` with API key when required | `<adspower-local-api>` / `<adspower-api-key>` |
| Camoufox / custom host debug | record the real local debug port or Playwright connect endpoint when enabled | `<camoufox-debug-endpoint>` |

## Chrome debug profile

Use a dedicated debug profile directory that is not the operator's daily browser profile.

Recommended layout:

```text
<mcp-host-root>/
  ChromeDebug/                 # user-data-dir for attach-only Chrome
  start_chrome_debug.bat       # or .sh / shell function on non-Windows hosts
```

Launch pattern:

```text
chrome.exe --remote-debugging-port=9222 --user-data-dir="<chrome-debug-user-data-dir>"
```

Rules:

1. `<chrome-debug-user-data-dir>` must exist before attach claims.
2. The launcher must resolve to that same directory. If a launcher still points at a stale absolute path, treat attach setup as broken until the path is corrected.
3. Prefer environment variables or a local overlay for absolute paths, for example:
   - `SPIDER_KING_CHROME_USER_DATA_DIR=<chrome-debug-user-data-dir>`
   - `SPIDER_KING_CHROME_DEBUG_URL=http://127.0.0.1:9222`
4. After launch, attach MCP browser families only with the confirmed browser URL or WebSocket endpoint from `/json/version` or the tool schema.
5. Never commit operator-specific absolute paths into this shared skill file.

## Camoufox host notes

Camoufox is optional local host capacity for high fingerprint pressure. It is not an always-on default and not a mounted MCP family by itself.

When using Camoufox:

1. Start it only after Auto Judge selects high-pressure baseline host, or the user explicitly requires it.
2. Use it for clean baseline traffic, page state, and session inventory.
3. Record whether it exposes a debuggable attach surface usable by `js-reverse` / CDP tools as `<camoufox-debug-endpoint>`.
4. If attach is unavailable, export requests/HAR/scripts and continue offline; do not invent debugger proof.
5. Never leave Camoufox inside `compact-replay` or `collector` delivery.

If Camoufox is not installed or not reachable, low-pressure work continues with `chrome-devtools`. High-pressure work must report the host gap instead of silently pretending the clean anti-detect baseline exists.

## Local overlay convention

Keep shared skill docs portable. For machine-private values, use one of:

1. Environment variables such as `SPIDER_KING_CHROME_USER_DATA_DIR`, `SPIDER_KING_CHROME_DEBUG_URL`, `SPIDER_KING_REQABLE_REPORT_URL`, `SPIDER_KING_CAMOUFOX_DEBUG_ENDPOINT`
2. A file outside the skill tree, for example `<workspace>/spider-king.local.md` or an operator notes directory
3. In-chat operator answers for a single session

Do not add `local-mcp-environment.local.md` secrets, API keys, cookies, or home-directory paths into the shared skill package.

## Preflight checks

Before claiming attach mode works:

1. Confirm the debug profile directory referenced by the launcher exists.
2. Confirm `http://127.0.0.1:9222/json/version` or the configured `<chrome-debug-url>` answers for Chromium attach.
3. Confirm the agent session actually lists `chrome-devtools` / `js-reverse` tools.
4. Confirm Camoufox launch/attach only when the Auto Judge branch selected that host.
5. Confirm Reqable ingest only if passive store routing depends on it.

On failure, record a capability blocker and fall back to an available mode or a lower delivery shape.
