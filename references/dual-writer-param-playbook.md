# Dual-Writer Param Playbook

Use this playbook when one request field name can be written by more than one client path, and a short offline token shape is not the same as the live wire-success shape.

## Contents

- [Route here when](#route-here-when)
- [Core idea](#core-idea)
- [Fast execution path](#fast-execution-path)
- [High-value checks](#high-value-checks)
- [Common traps](#common-traps)
- [Delivery guidance](#delivery-guidance)
- [Minimal handoff notes](#minimal-handoff-notes)

## Route here when

- the same query, header, or body key sometimes carries a short token and sometimes a long token
- offline recovery of one writer (hash, LZW, short signer) succeeds, but live replay still returns a challenge or empty shell
- call stacks show more than one path touching the field: open rewrite, send retry, challenge navigate, cookie-to-query injection
- sample exact-URL replay works, but fresh timestamps with the recovered short generator fail
- a session-stable prefix plus a URL-bound body appears on success, while research samples only produce compact compressed tokens
- one product keeps different live signers on HTTP, websocket, protobuf, or report surfaces
- an easy business route accepts one generation of a field while a hard or antispam route rejects it
- the same param name is written as a cookie and as an in-memory global, and page code prefers one when set

## Core idea

A parameter name is not a single algorithm.
A product is not a single signer.

Prove the **wire-success writer** on the current surface and on the hardest live route before deep-porting any candidate writer.
Offline self-check on a secondary path or a soft route is research evidence, not delivery proof.

Inventory signers by surface first: HTTP query, websocket, protobuf, and sidecar report can each keep a different live helper. Reuse across surfaces only after the current surface proves it.

## Fast execution path

1. Freeze two or more successful wire values for the same field.
   Record for each value:
   - length
   - fixed prefix / session segment
   - separators (`-`, `|`, `_`)
   - alphabet membership
   - URL, timestamp, page, or body binding
   - which request attempt produced it (first miss vs retry)

2. Classify writers, not just values.
   Common classes:
   - **short signer**: compact compress/hash of `url|ts|flag` style plaintexts
   - **long body**: session or environment prefix plus high-entropy or multi-segment body
   - **challenge rewrite**: challenge HTML/JS navigates or retries with a rewritten business URL
   - **cookie projection**: cookie material injected into query by an open hook
   - **generation switch**: same field name, newer algorithm required on the hard route
   - **surface-local signer**: a helper that is live on one request surface and foreign on another
   - **in-memory global vs cookie**: same name on a window global and `document.cookie`; the page prefers the global when it is set, else the cookie. Both values can be mint-shaped. Shape is not acceptance.

3. Map each class to a call stack.
   Prefer initiator stacks from live open/send/fetch hooks over source-only guesses.
   One field may be written by different classes under different gates (`kn`-style mode switches, captcha loaded, first failure HTML).

4. Live-accept only the class present on successful business responses.
   If short tokens never appear on successful wire samples, do not deliver a short-token generator as the product path.
   If long tokens appear only after challenge HTML, route to challenge artifact harvest first.
   If the page-priority writer still yields schema-valid filler JSON, try the other writer from the same mint before rebuilding the host.

5. Prove binding and refresh separately.
   - URL-bound: changing timestamp/page invalidates the body
   - session-bound: prefix stable inside one challenge/session chain
   - cookie-bound: requires companion cookies
   - echo-bound: replay may need the original URL reflected in an extra field

6. Report dual-writer status explicitly.
   Name:
   - the research writer that was recovered but rejected live
   - the delivery writer that actually clears the gate
   - the remaining uncertainty if more than one success class still exists

## High-value checks

- Do successful samples share one length band, or two disjoint bands?
- Does the short path exist in SDK source but only run when a mode flag is zero/one?
- Does the long path appear only on the second attempt after HTML challenge?
- Does app-layer HMAC/sign exclude the verifier param while still being required on browser XHR?
- Can the challenge path succeed without the app signer, or the reverse?
- After mint, did the helper write cookie, window global, or both, and which slot does page code read first?
- If business JSON is schema-valid but every row is the unsigned filler sentinel, try the other writer on the same mint before blaming the host.

## Common traps

- treating the only fully decompiled writer as the only real writer
- concatenating a known session prefix onto a short body and calling it long-token recovery
- declaring protocol automation done after sample exact replay
- continuing encrypt reverse after a challenge helper already emits the rewritten URL
- merging app signer recovery and verifier recovery into one unfinished ticket
- proving a signer on a soft or detail route and calling the hard or antispam route done
- porting one recovered site signer onto websocket or protobuf because the product name matches
- treating the HTML-instructed function name as the same writer as a differently cased runtime export that wraps extra local bytes
- treating the HTML ajax helper as the writer after the runtime replaced `$.ajax` or `fetch` with a VM export
- collecting the VM-native body after an interceptor discarded the original send and rebuilt a sibling-shaped form
- treating a short same-name cookie as the live token when `open`/`fetch` already appended a long query value
- treating a mint-shaped cookie as the live token when the page prefers a same-name in-memory global
- treating 32-hex or other mint-shaped tokens as live acceptance
- skipping the other writer after HTTP 200 filler/punish JSON

## Delivery guidance

Preferred order:

1. identify the wire-success class
2. harvest or regenerate that class on a fresh URL
3. only then paginate
4. keep rejected writers in analysis notes as misleading signals
5. when cookie and in-memory global share a name, read both, prefer the page-priority slot, and retry the other writer on punish JSON

Helper I/O, when the success class is challenge rewrite:

- Python owns live HTTP
- local helper returns `redirectUrl` and/or `cookieString`
- Python replays and validates business JSON/HTML anchors

## Minimal handoff notes

Report:

- field name and success shape summary (length bands, prefix rule)
- writer classes found
- which class is live-accepted
- which class is misleading
- binding: URL / session / cookie / echo
- whether app signer and verifier gates are independent
