# Environment Patch Playbook

Use this file when extracted logic runs in a local runtime but outputs still differ from the page.

## Common mismatch sources

- missing globals
- different user agent branches
- DOM-derived constants
- text encoding assumptions
- `Date.now()` or randomness precision
- helper functions patched by side scripts

## Working method

1. compare helper outputs on the same fixed inputs
2. identify the first diverging intermediate value
3. patch only the smallest missing environment surface
4. keep the patch local to the helper runtime, not a whole browser dependency

## Common traps

- patching the entire DOM when only one global value was needed
- blaming crypto before checking environment-sensitive branches

## Delivery rule

Prefer tiny local patches over browser-backed execution.
