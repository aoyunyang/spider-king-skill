# Obfuscation Guide

Use this file when the page ships packed, flattened, or string-table-heavy JavaScript.

## Recognition signals

- giant string arrays
- `eval`, `Function`, or self-redefining wrappers
- control-flow flattening
- numeric array dispatch
- tiny side assets controlling the real logic

## Working order

1. search for the real API path first
2. search for transport wrappers before unpacking everything
3. extract only the smallest logic slice needed for the current request
4. save a clean snapshot before each major edit
5. move offline early when anti-debug noise is high

## Common traps

- beautifying the whole bundle before finding the real request
- ignoring inline scripts and side assets
- losing original variable names that are useful for diffing

## Delivery rule

Only deobfuscate as much as the protocol replay requires.
