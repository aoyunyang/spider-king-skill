# JSVMP Analysis Playbook

Use this file when the target wraps logic inside a custom VM, bytecode interpreter, or interceptor-owned black box.

## Contents

- [Recognition signals](#recognition-signals)
- [Exit-first rule](#exit-first-rule)
- [Nested standard-ISA / memory-image](#nested-standard-isa-memory-image)
- [Signer entry taxonomy](#signer-entry-taxonomy)
- [Working method](#working-method)
- [Public-boundary heat matrix](#public-boundary-heat-matrix)
- [Compile snapshot versus call trace](#compile-snapshot-versus-call-trace)
- [Feed-cut pattern](#feed-cut-pattern)
- [Reverse-trace log method](#reverse-trace-log-method)
- [Gated handler logging](#gated-handler-logging)
- [ALU-overlap algorithm ID](#alu-overlap-algorithm-id)
- [Instrumentation health gate](#instrumentation-health-gate)
- [Observation degrade ladder](#observation-degrade-ladder)
- [Init and registration contract](#init-and-registration-contract)
- [Common traps](#common-traps)
- [Delivery rule](#delivery-rule)

## Recognition signals

- opcode arrays
- dispatch loops switching on byte values
- tiny VM runtime with a large encoded program
- `$fast_unpack`, magic `WAFJ`, or an `LZ.` payload whose unpacker returns JavaScript source
- helpers hidden behind interpreter calls instead of direct JavaScript
- request interceptors that append signs only after XHR/fetch is triggered
- the VM loads and the HTML shows placeholder zeros, but no list XHR fires while `navigator.webdriver` is true
- protobuf `serializeBinary` or a wasm export such as `encode(i32,i32)` sits in front of the unreadable VM
- dense `String.fromCharCode` / char-code table construction inside a hot loop (string rebuild inside a VM)
- repeated ALU constants such as `2654435769` / `0x9E3779B9` across encrypt blocks (TEA family; see `references/crypto-patterns.md`)
- very large single scripts whose useful logic is only reachable through a dispatcher

## Exit-first rule

The interpreter is not the goal. The **public exit artifact** is.

Order:

1. freeze the final wire need: signed query/header/body field, cookie, URL rewrite, or wrapper return
2. prove where that exit becomes visible (transport egress, state write, exported function return)
3. only then chase inputs, host reads, or internal stages that feed that exit
4. stop at the smallest boundary that rebuilds the exit for protocol replay

Do not start from opcode centers and walk outward hoping a signer appears.


## Nested standard-ISA / memory-image

Custom VM work is the wrong first tool when the outer script is only an emulator or loader for a nested standard machine.

Route here when:

- reverse-trace reaches a memory fill, bytecode blob, or linear-memory init before the final artifact
- the inner program decodes as a known ISA or stable WASM export surface with fixed I/O regions
- fixed vectors match after replaying the memory image even though the outer source remains unreadable

Method:

1. keep exit-first: name the wire artifact and public entry
2. dump initialized memory / WASM linear memory at the stable boundary
3. mark input, control, work, and output regions from reads/writes, not from outer function names
4. execute with a standard simulator or minimal export caller
5. version the template hash; treat it as a round/asset fact, not a forever constant
6. retire outer-shell reading once I/O parity holds

Hand opaque staged packing that still needs captured profiles to `references/opaque-runtime-profile-playbook.md`.

## Signer entry taxonomy

Before env patching or local bootstrap, classify how the sign is produced:

| Entry type | Signals | Next move |
|---|---|---|
| `export-fn` | named function on a global/module used by business code | call the export on fixed inputs; skip intercept theater when possible |
| `xhr-intercept` | `XMLHttpRequest` open/send wrapped; sign appears only after send | single-channel feed-cut on XHR egress |
| `fetch-intercept` | `fetch` / Request wrapper mutates URL/headers/body | single-channel feed-cut on fetch egress |
| `dual-channel` | both XHR and fetch wrappers exist | prove **both** channels or prove business traffic uses only one |
| `init-gated` | interceptors or export stay dead until init/config/warmup runs | recover registration order and config object first (`Init and registration contract`) |

Record:

```text
signerEntry: export-fn | xhr-intercept | fetch-intercept | dual-channel | init-gated
channelsProved: [xhr, fetch, other]
initRequired: true|false
```

Wrong entry type is a method error, not an algorithm failure.

## Working method

1. apply the exit-first rule and name the exit artifact
2. classify signer entry with the taxonomy above
3. map the public boundary: inputs into the box and outputs, wrapper returns, state writes, request egress, protobuf `serializeBinary`, or wasm `encode(i32,i32)`
4. when public-boundary values are missing, capture them with the lowest practical observer risk before interpreter surgery; use `references/silent-value-capture-playbook.md` recipe `C` (`vm-public-io`) and promote only correlated fixed-input cards
5. classify anti-bot class with `references/anti-bot-class-playbook.md` and obey its observation allow/deny table
6. test the smallest closer-to-browser local execution path before full VM recovery
7. if output drift looks host-semantic, sniper-patch observed reads before opcode work (`references/environment-patch-playbook.md`)
8. if the public boundary is insufficient and a stable stage dispatcher exists, capture ordered stage I/O before individual opcodes
9. preserve one complete run as an atomic capture; use `references/opaque-runtime-profile-playbook.md` when ports depend on opaque blocks
10. avoid full VM recovery unless the protocol truly depends on it
11. prefer isolating the one helper output needed for the request
12. move to local execution or helper wrapping before full devirtualization
13. if opcode work is still required, use gated handler logging and ALU-overlap ID; do not dump the interpreter

## Public-boundary heat matrix

When observation yields method/property heat summaries (silent-value cards, instrumentation summaries, or narrow hooks), choose strategy by public signals — not by brand folklore:

| `hot_methods` / call heat | env property heat | Preferred next move |
|---|---|---|
| standard digests (`MD5`, `SHA*`, `HMAC`, `SubtleCrypto`, `btoa`) | low | pure algorithm port (`references/crypto-patterns.md`, `references/pure-python-rebuild-playbook.md`) |
| custom function names only | low | extract the smallest callable fragment into a local helper; fixed-vector parity first |
| standard digests or custom names | high | stop chasing opcodes; use public I/O + host bootstrap / sniper env patch |
| interceptor-dominated XHR/fetch mutation | any | feed-cut at the transport boundary before decompilation |
| protobuf `serializeBinary` / wasm `encode(i32,i32)` / public codec exports | any | stop opcodes; freeze hex I/O and replay the encoder |
| dense `slice` / `charCodeAt` / `fromCharCode` word-packing heat | low | word-packing feed-cut (`references/hook-techniques.md`), then TEA-family ID if ALU constants appear |
| `fromCharCode` heat in the millions | any | VM entered and is rebuilding strings; snapshot compile bodies / public I/O |
| `fromCharCode` heat stays 0 after the supposed entry | any | VM never entered; fix init/registration/timer drain before more host cosmetics |

Use `references/signer-parity-chain-playbook.md` when local and browser outputs diverge after a candidate path is chosen.

`fromCharCode` heat is an entry diagnostic, not an algorithm name. Million-scale heat means the interpreter is running. Zero heat after a claimed entry means the VM did not start; more canvas stubs will not create it.

## Compile snapshot versus call trace

A substituted `eval` / `new Function` body is key material. A later call of the compiled function is only execution.

- snapshot the compile body after param substitution (`references/silent-value-capture-playbook.md` recipe G, `references/hook-techniques.md`)
- do not global-wrap `Function.prototype.apply` / `call` to reconstruct the VM
- hash the snapshot and correlate it to the wire field; opcode dumps of the later call are a different, later rung

## Feed-cut pattern

Use feed-cut when the black box mutates the request during transport rather than exporting a clean pure function.

1. install observation at the transport egress for every channel in `channelsProved`
2. inside a controlled local host (embedded runtime / narrow bootstrap executor), feed a real-shaped request that the interceptor expects
3. let the target code append or rewrite the signature itself
4. cut the final method, URL, headers, and body after mutation
5. replay that final wire shape from Python-owned HTTP

Rules:

- Python still owns live HTTP for `compact-replay` / `collector`
- do not keep the capture browser or engine backend in delivery
- if feed-cut only works under a full page session, record the missing bootstrap state and return to session-chain recovery
- if only one of two transport channels was hooked, do not claim the interceptor is absent

## Reverse-trace log method

When logs or traces are large, do not read them top-down.

1. freeze one known exit value from a successful wire sample (fingerprint/hash only in reports)
2. search all observation streams for the **first** appearance of that value or a tight unique suffix/prefix
3. walk **backward** one producer at a time: return value <- call args <- join string <- host read
4. open `references/signer-parity-chain-playbook.md` at the first divergent stage
5. discard uncorrelated high-volume noise; prefer request-id-bound lines

This is usually faster than forward opcode tours.

## Gated handler logging

Only after the public boundary is insufficient and a stable dispatcher exists.

Rules:

1. keep a global gate off during init and registration
2. open the gate only around one public exit (a data-export, interceptor send, or the proved wrapper)
3. whitelist string and word-packing methods; do not log every opcode
4. buffer to a file; never stream unbounded traces to the console
5. if a family magic is already known, ignite a second narrower cap on that constant and close it on the first `fromCharCode` / block emit
6. still pass the instrumentation health gate

Unrestricted handler dumps are not analysis.

## ALU-overlap algorithm ID

L5+ only. This does not replace exit-first or word-packing feed-cut.

When two adjacent encrypt blocks are visible in a gated ALU log:

1. overlap the two op sequences
2. keep repeated constants and repeated shift/xor shapes
3. route the shape to `references/crypto-patterns.md` TEA family fingerprints
4. recover key material with key-in-bytecode recovery if the words are not literals
5. stop once the named primitive plus framing rebuilds the exit

Do not read opcode traces forward from handler 0.

## Instrumentation health gate

Source rewrite, AST install, or broad instrumentation is not success by itself.

Require all of the following before trusting heat logs:

1. install or rewrite acknowledged by the tool (`files_rewritten` / route active / equivalent)
2. runtime marker or first log event proves the rewritten code actually executed
3. at least one correlated business action produced entries tied to the target request id or mutation boundary
4. clean-versus-instrumented comparison rules out observer poison on `signature-bound` targets

`files_rewritten > 0` with no runtime marker is a failed install, not partial success.

## Observation degrade ladder

When public-boundary observation fails, climb one step at a time. Do not jump to browser delivery.

```text
L1: narrow public-boundary / source-level observation with runtime health proof
L2: lighter rewrite or narrower URL/function scope
L3: transparent / non-proxy host observation (prototype getters, egress only)
L4: proxy-style or broad host hooks  -> ONLY if class is behavior-interceptor or pure-obfuscation
L5: local host bootstrap + sniper env patch / feed-cut (rungs 3-5)
L6: lower delivery shape or report blocker  -> NEVER skip to browser-backed collector
```

Rules:

- on `signature-bound`, L3 failure goes to L5, not L4
- every step needs a one-line reason the previous step was insufficient
- record the ladder path in task notes when L5+ is used
- under L5, handler ALU traces are allowed only after public I/O and a local-host word-packing feed-cut have failed; do not satisfy this rung with a live signature-bound String.prototype wrap

Align promotion language with `references/escalation-ladder-playbook.md`.

## Init and registration contract

Treat "signer function missing" and "interceptor never fires" as registration problems until proved otherwise.

Check before algorithm blame:

1. required init/config/warmup calls and their order
2. whether a config object, path list, or feature flag registers the business route
3. whether hooks were installed before the bundle replaced transport primitives
4. multi-script load order: env/surfaces -> polyfills -> target bundle -> init -> trigger

If init is required, put it in the session/bootstrap contract (`references/session-contract-playbook.md`) and in local executor inputs (`references/local-challenge-executor-playbook.md`).

If the interceptor never fires on CDP Chrome, check `navigator.webdriver` before algorithm blame. A configurable `Navigator.prototype.webdriver` can be deleted in an authorized initScript; that is observation activation, not fingerprint pressure.

## Common traps

- treating an `eval`/`Function` compile-body snapshot as a later call trace, or wrapping global `apply`/`call` to chase the VM
- ignoring `fromCharCode` heat (million vs 0) and stacking host stubs while the VM never entered
- touring the outer emulator source after a nested memory image already exposes fixed I/O
- treating every large obfuscated shell as opcode work before testing a standard-ISA dump
- trying to devirtualize the whole VM when only one result matters
- missing side inputs passed into the VM entry point
- instrumenting opcode handlers before proving the public boundary is insufficient
- chasing opcodes after protobuf `serializeBinary` or wasm `encode(i32,i32)` already rebuilds the body
- treating HTML placeholder zeros as business data when the VM never issued XHR
- wrapping XHR or `toString` on a signature-bound VM because the list request stayed silent under `navigator.webdriver`
- collecting unrestricted opcode traces when a public-boundary card would unlock the protocol
- mixing stage fragments from different successful runs before proving independence
- treating a captured final-artifact pool as proof the VM transform was ported
- treating failure under Node, jsdom, or a thin shim as proof the VM cannot run locally
- trusting rewrite counts without runtime execution proof
- using broad Proxy host hooks on `signature-bound` flows and poisoning signatures
- hooking only XHR while business traffic uses fetch (or the reverse)
- calling env patch a failure when init never registered the interceptor
- reading huge traces forward instead of reverse-tracing from the exit value
- starting with unrestricted handler dumps when a word-packing hook or public export would recover plaintext
- identifying an algorithm from a magic constant without distinguishing TEA vs XTEA vs XXTEA
- pinning a packer PRNG with a native-looking wrapper before unpack; some unpackers infinite-loop on native-looking constants
- treating a self-modifying opcode that slices remaining bytecode after the first encrypt as a reusable pager
- treating `$fast_unpack` / WAFJ bytecode as the writer; unpack to source, then recover concat and the named digest
- pinning a packer PRNG with a plain assignment so it *returns*, then treating `typeof signer === 'undefined'` or `Bind must be called on a function` as a missing algorithm; the packer may have halted without installing the inner runtime, and native PRNG plus a subprocess timeout can be the smaller next proof
- saving the string passed to `eval(packer)` and replaying it as `var signer = unpackedIIFE` in a fresh context; the function can exist and still crash because packer init and unpacked body share one world
- replacing `Date.now` with a frozen constant during unpack; time-wait packers never exit, while the host logical clock still advances
- keeping iv8 `time_mode="logical"` for a CPU-heavy packer unpack; `Date.now()` +1ms per call can look like debugger-pause and halt (`typeof unpacked === "undefined"`) or hang. Use `system` for unpack, and pay real `sleep` if the same context later installs a timer export
- treating a 4s timeout as a hang when the instance holds a 10^5+ array and the method (or the probe) logs, stringifies, or enumerates it
- shrinking or replacing that huge trap object before calling checkers; the call returns quickly but the check semantics change
- calling `Function.prototype.toString` on VM methods or getters without a timeout

## Delivery rule

If a tiny helper wrapper around the VM output is enough for protocol replay, use that instead of heroic full recovery. Prefer public VM I/O, wrapper returns, state writes, or request egress over interpreter surgery whenever they solve the protocol. Silent-value capture may supply those public I/O cards; it does not justify shipping the capture backend inside the collector. If a local port still consumes captured runtime profiles, report it as snapshot-driven rather than fully algorithmic. Classify leftover fields with the material table in `references/local-challenge-executor-playbook.md` before calling the port pure.
