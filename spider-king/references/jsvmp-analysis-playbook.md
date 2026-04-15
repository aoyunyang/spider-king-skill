# JSVMP Analysis Playbook

Use this file when the target wraps logic inside a custom VM or bytecode interpreter.

## Recognition signals

- opcode arrays
- dispatch loops switching on byte values
- tiny VM runtime with a large encoded program
- helpers hidden behind interpreter calls instead of direct JavaScript

## Working method

1. locate the VM entry point
2. identify what inputs go into the VM and what outputs come out
3. avoid full VM recovery unless the protocol truly depends on it
4. prefer isolating the one helper output needed for the request
5. move to local execution or helper wrapping before attempting full devirtualization

## Common traps

- trying to devirtualize the whole VM when only one result matters
- missing side inputs passed into the VM entry point

## Delivery rule

If a tiny helper wrapper around the VM output is enough for protocol replay, use that instead of heroic full recovery.
