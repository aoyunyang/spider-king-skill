# Anti Debug Playbook

Use this file when live tooling becomes unstable or the page fights inspection.

## Recognition signals

- repeated debugger pauses
- DevTools-triggered timing changes
- source disappears or self-rewrites after load
- MCP or browser tools time out under inspection

## Response plan

1. save HTML and inline scripts
2. save downloaded assets
3. move deobfuscation offline
4. use fixed inputs instead of long interactive sessions
5. reduce runtime inspection to the smallest possible hook or snapshot

## Common traps

- brute-forcing the live page after anti-debug is obvious
- assuming the protocol is impossible because the page is annoying to inspect

## Delivery rule

Anti-debug changes the investigation path, not the delivery target. The collector still needs to be protocol-only.
