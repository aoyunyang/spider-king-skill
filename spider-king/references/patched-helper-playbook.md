# Patched Helper Playbook

Use this reference when:

- helper names look standard, but outputs do not match standard libraries
- functions named `md5`, `btoa`, `atob`, `sha1`, or similar behave strangely
- local reproduction fails even though the helper name looks familiar

## Core rule

Names do not prove behavior. Fixed-input validation does.

## Minimum validation loop

1. choose a fixed input such as `"abc"` or a captured timestamp
2. record browser or page output
3. run the local candidate implementation
4. compare intermediate states as well as the final output
5. only then decide whether the helper is standard, patched, or fully custom

## Common signs of patching

- the output alphabet differs from normal Base64
- the digest matches neither standard MD5 nor SHA families
- the helper uses DOM state, side scripts, or odd lookup tables
- output length or padding rules differ from the standard implementation

## Delivery rule

Ship fixed-input self-checks with the collector so future site changes fail loudly.
