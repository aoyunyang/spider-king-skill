# Crypto Patterns

Use this file when signatures, encryption, or helper outputs look suspicious.

## Standard-looking helpers that are often not standard

- `md5`
- `sha1`
- `btoa`
- `atob`
- `hmac`
- `aes`
- `rsa`

## Fast recognition checklist

- length matches a common digest size
- alphabet matches hex, Base64, URL-safe Base64, or a custom alphabet
- padding matches a standard encoder
- output changes with timestamp, page, or session state
- helper reads DOM, globals, or side-script state

## Fixed-input validation loop

1. freeze a tiny input such as `"abc"`
2. freeze a live input such as a captured timestamp
3. compare browser output with local output
4. compare intermediate strings, not only final digests

## Common failure modes

- standard Base64 library used against a patched alphabet
- standard MD5 used against a custom string-to-word packing step
- URL-encoding mismatch before hashing
- wrong timestamp precision
- hidden page or session state included in the input

## Delivery rule

Do not call crypto "done" until fixed-input self-checks are in the collector.
