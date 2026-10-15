# No-Touch Matrix And Profile Coherence

Environment patches change evidence. Add one only when a traced read or a fixed-vector divergence proves the dependency.

## Default No-Touch Matrix

Do not modify these without direct evidence:

| Surface | Default |
|---|---|
| `Error`, error stacks, or error constructors | Preserve host behavior |
| constructor names and prototype identity | Do not rename, reparent, or flatten |
| `Object.prototype` and shared intrinsic prototypes | Do not add target-specific fields |
| instance-level `Symbol.toStringTag` | Do not fake unless the exact instance read is proved |
| `Function.prototype.toString` | Keep one explicit owner; do not stack a second stealth wrapper |
| Canvas, WebGL, Audio, fonts, or media capabilities | Omit until a branch/output dependency is proved |
| browser-family-specific APIs | Omit when they conflict with the selected baseline family |

Prefer absence over a plausible but incoherent value. A field that merely exists can select the wrong JSVMP branch.

## One Coherent Profile

Bind one reproduction chain to one baseline and keep these layers consistent:

- User-Agent and browser family/version
- Client Hints and platform/architecture
- `navigator`, `window`, `document`, locale, timezone, and permissions
- `screen`, device pixel ratio, touch and input capabilities
- Canvas/WebGL/Audio/font claims when proved necessary
- HTTP/TLS/H2 impersonation and header order on the Python request path

Lock the Python impersonate target to the installed curl chrome profile (`DEFAULT_CHROME` / `curl_cffi_chrome_impersonate`). User-Agent, Client Hints, and runtime navigator major must match that impersonate. Do not paste the current desktop Chrome major onto a lower impersonate.

Do not splice a Firefox navigator into Chrome-only APIs, combine a mobile UA with desktop screen/input claims, or use a Chrome JS profile with an unrelated TLS fingerprint. Browser seeds from other sessions are diagnostic comparisons, not patch ingredients.

Keep two judgments separate: `profile-coherent` asks whether one profile agrees with itself; `captured-vector-match` asks whether it is the exact family/version/profile used by the saved vector. A coherent Firefox profile can correctly fail a Chrome vector without becoming an incoherent profile.

## Patch Admission

For each new field record:

1. the traced read or first divergence it explains
2. the baseline source and browser family
3. the minimal descriptor/prototype location
4. the fixed vector expected to change
5. the result of removing the patch again

Reject the patch if removal does not restore the divergence, if it creates a family contradiction, or if it only makes the output length/alphabet look right. Validate with `verification-and-replay.md`.
