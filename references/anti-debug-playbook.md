# Anti Debug Playbook

Use this file when live tooling becomes unstable or the page fights inspection.

## Recognition signals

- repeated debugger pauses
- DevTools-triggered timing changes
- source disappears or self-rewrites after load
- MCP or browser tools time out under inspection
- CDP attach, evaluate, or source walks hang on challenge or chaos-style VMs that embed `debugger` opcodes
- `Function("debugger")` constructors hang page-world evaluate or a live `js-reverse` re-call
- `Function("while (true) {}")` or `Function("while(!![])")` constructors hang local eval
- a dead `!==` around one `Function("debugger")` does not prove the constructor is unreachable
- string-table decoder integrity methods that `push` until array length grows forever
- page-world `evaluate`, CDP `Runtime.evaluate`, or in-app-browser evaluate redirects, blanks, or poisons a page whose challenge is console / DevTools observation
- hasher helpers call `eval` or `setInterval(eval)` on a recovered function string
- page-owned `eval('debugger')` or injected `<script>debugger` loops inside codec helpers pause CDP Debugger
- MCP `select_page` or attach calls time out instead of returning scripts
- a JSVMP loads, HTML shows placeholder zeros, and no list XHR fires while `navigator.webdriver` is true

## Response plan

1. save HTML and inline scripts
2. save downloaded assets
3. move deobfuscation offline
4. use fixed inputs instead of long interactive sessions
5. reduce runtime inspection to the smallest possible hook or snapshot
6. if a probe or bootstrap asset embeds `debugger`, harvest it and run in a local host that ignores the opcode; do not keep attaching a live debugger to that asset
7. if page-world evaluate or a live `js-reverse` re-call hangs on `Function("debugger")`, `Function("while (true) {}")`, or `Function("while(!![])")`, neutralize `Function` only in an authorized initScript or harvest the slice offline; do not keep evaluating or re-instrumenting the live bundle. A hung re-call is the same hang as evaluate: park attach after the first freeze and continue from harvested scripts plus API samples. Strip only an exact body such as `debugger;`, `while (true) {}`, or `while(!![])`. A broad `body.includes("debugger")` rewrite poisons later mint. Do not wait a seconds-long anti-debug `setInterval` if mint already exists after a short drain
8. a dead `!==` around one `Function("debugger")` does not make attach safe; if the live constructor is still reachable, skip `js-reverse` attach, harvest the asset, and rewrite offline
9. record `debugger_attach_gap`; if `silent_backend=absent`, also record `silent_value_capture_gap` and continue offline instead of retrying attach
10. if a decoder eval never returns, skip the integrity prototype that grows arrays forever and keep the decode function
11. if a clean goto shows the challenge title but page-world evaluate redirects or unloads the page, treat evaluate itself as the detection surface: park or close that tab and continue offline; do not attach `js-reverse` to a console-detection challenge
12. if a hasher calls `eval(R)` or `setInterval(eval)`, stub those hosts, keep the digest, and never execute recovered R
13. if MCP `select_page` or attach times out, record `debugger_attach_gap`, harvest the script over ordinary HTTP, and continue offline
14. if the VM never issues the list XHR and `navigator.webdriver` is true, delete the configurable prototype property in an authorized initScript and recapture; this is not an attach hang and not Camoufox pressure

## Common traps

- brute-forcing the live page after anti-debug is obvious
- assuming the protocol is impossible because the page is annoying to inspect
- retrying Chrome CDP attach against a `debugger`-opcode probe after the first hang
- retrying page-world evaluate or a hung `js-reverse` live re-call against a Function-wrapped debugger constructor after the first hang
- treating a dead `!==` around one `Function("debugger")` as permission to attach
- neutralizing `Function` with `body.includes("debugger")` instead of an exact `debugger;`, `while (true) {}`, or `while(!![])` body match; that rewrite can change mint output or get `403` on later pages
- waiting a seconds-long anti-debug interval for mint after the hang constructor is already stubbed
- attaching `js-reverse` after observer-toxic Function-debugger is already proved
- treating a decoder integrity infinite loop as a missing string table
- launching a second Chrome or `chrome-devtools` `new_page` because the user asked to open DP
- treating page-world evaluate as a neutral probe on observer-toxic console / DevTools challenges
- firing a caught exception's `message` getter (or logging the exception so DevTools reads it) on a `document.createEvent('Touch')` failure; that getter is often the desktop DevTools sensor, not the clean handshake
- treating a nested iframe VM as the signer installer when it only posts `{detected:true}` and the parent export appears later on a timer
- executing a function reconstructed from a charcode array because it sat next to MD5 constants
- treating MCP select/attach timeout as a dead target instead of `debugger_attach_gap` plus offline harvest
- treating JSVMP XHR silence plus HTML zeros as a debugger hang or burned baseline instead of checking `navigator.webdriver`
- wrapping XHR or `toString` on a signature-bound VM to force a silent request
- opening Camoufox because CDP `navigator.webdriver` is true
- evaling recovered R in Node because `require` exists there

## Delivery rule

Anti-debug changes the investigation path, not the delivery target. The collector still needs to be protocol-only.
