# Report Templates

Use these headings to keep progress crisp and comparable across investigations.

## Contents

- [Sensitive data rule](#sensitive-data-rule)
- [Phase delta report](#phase-delta-report)
- [Recon report](#recon-report)
- [Dynamic validation report](#dynamic-validation-report)
- [Conditional implementation brief](#conditional-implementation-brief)
- [Compact protocol handoff](#compact-protocol-handoff)
- [Final delivery report](#final-delivery-report)
- [Proof manifest](#proof-manifest)
- [Recommended collector tree](#recommended-collector-tree)
- [Run path and cache](#run-path-and-cache)

## Sensitive data rule

Reports are redacted by default.

- report credential, token, header, and cookie names plus provenance, scope, expiry, and a short hash or fingerprint
- do not paste raw secret values into chat, reports, screenshots, fixtures, or version control
- when exact values are operationally required, keep them in a task-local ignored secret store and reference only its path and hash
- redact raw payload samples unless the payload is proven public and non-sensitive
- report endpoints without userinfo or raw query values; retain only query-field names and other structural details needed to reproduce the protocol

## Phase delta report

```markdown
Phase Delta
- New evidence:
- Changed hypothesis:
- Capability or intake-mode change:
- Debugger means: js-reverse / silent-value-capture / both / none
- Silent recipe or gap: A-F / debugger_attach_gap / silent_value_*_gap / n/a
- browser_mode: launch | attach | unavailable
- curl_impersonate: default=chromeXXX; max=chromeXXX
- capsule_major: chromeXXX
- business_request: found | candidate | missing
- unproven_routes: 0 | 1
- next_action: one Stuck next action from failure-surface-taxonomy
- Evidence package path and SHA-256:
- First divergence: step / path / kind / or not yet compared
- Proof manifest artifact hash: SHA-256 computed after the manifest is written
- Saved artifact paths and hashes:
- Next smallest proof:
```

## Recon report

```markdown
Recon
- Target URL:
- Final landing URL:
- Page type: SSR / CSR / SPA / MPA / hybrid
- Useful data source: HTML / XHR / Fetch / GraphQL / WebSocket / asset / binary / other

Real request candidates
- Request 1:
  - URL:
  - Method:
  - Purpose:
  - Transport kind:
  - Paging fields:
  - Key headers: names / provenance / redacted fingerprints
  - Key cookies: names / writer / scope / expiry / redacted fingerprints
  - Decode needed:

Misleading signals
- 1.
- 2.

Next hypothesis
- 1.
- 2.
```

## Dynamic validation report

```markdown
Dynamic Validation
- Target function or request:
- Validation method: hook / diff / replay / fixed-input helper test
- Inputs:
- Observed outputs:
- Raw payload sample: redacted excerpt or local path plus hash
- Evidence package path and SHA-256:
- First divergence: step / path / kind / or no divergence
- Morph labels: scene / device class / UA class / geometry class (if verifier-gated)
- Hard gate metric: semantic success field + grant artifact name
- Writer class: algorithmic / local VM L2 / pool-backed / pure port L3
- N-run rate: passes/total on hard gate metric (if claiming stability)

What changed on the wire
- Query:
- Body:
- Headers: names, changed slots, and redacted fingerprints
- Cookies: names, writers, scopes, and redacted fingerprints
- State-chain completeness: bootstrap reports / init / companions present or missing

Conclusion
- Verified helper or protocol rule:
- Verified decode or parser rule:
- Primary failure surface if not green:
- Remaining unknowns:
```

## Conditional implementation brief

Use this only when the declared shape is `compact-replay` or `collector` and at least one material implementation or authority choice remains. Examples include competing implementation forms, unresolved runtime escalation, dependency choice or installation authority, durable path or retention scope, and live or session permissions. Do not force it for `evidence`, `local-proof`, explicit no-write analysis, or an already-proved route whose gated actions are fully covered; a concise route note is sufficient in the latter case.

This records a decision; it is not approval. It cannot widen scope, budgets, permissions, or `allowedPaths`, and it does not add a user-confirmation stop beyond the existing permission gates in `references/provider-work-order.md`.

```markdown
Implementation Brief
- Trigger: competing implementation forms / runtime escalation / dependency install / durable writes / permission choice
- Delivery shape: compact-replay / collector
- Real request: scheme + host + port + route | method | content type
- Dynamic fields: name | writer | wire slot | scope | expiry | refresh path
- Evidence and fixed vectors: source/path + keyed fingerprint | expected | observed
- Candidate forms: form | evidence fit | runtime/dependency/authority impact | select/reject reason
- Chosen boundary: Python owns live HTTP/orchestration; helper type and narrow responsibility, or none
- Session contract: issuance | chain | identity/context scope | refresh; no raw secret values
- Acceptance: decisive oracle | negative control | required replay count
- Planned durable paths: only destinations covered by writable mode and inherited allowedPaths
- Permission status: existing authority used | new authority genuinely required
- Residual risk: risk | current evidence | retirement proof
```

## Compact protocol handoff

Use this as the default final summary for `compact-replay` or `collector` after the matching capability gate passes. It summarizes proof; it does not replace that gate. For an `evidence` or `local-proof` result, use it only when a compact protocol summary is useful, label live acceptance and replay count `unproven`, and do not imply runnable delivery.

```markdown
Protocol Handoff
- Capability: compact-replay / collector / explicitly bounded evidence or local-proof
- Real request: scheme + host + port + route | method | content type
- Protocol order: bootstrap/issuance -> refresh -> sign/envelope -> request -> decode -> first downstream consumer, omitting absent stages
- Dynamic fields: name | writer | wire slot | scope | expiry | refresh path
- Evidence: decisive source/path + keyed fingerprint
- Fixed vectors: input/reference | expected | observed | pass/fail
- Python/helper boundary: Python-owned HTTP/orchestration | helper kind, inputs, outputs, and runtime pin, or none
- Session: issuance | required chain | identity/context scope | expiry/refresh | cross-session status
- Acceptance: decisive business oracle | negative control | live/offline replay count
- Saved paths: collector/entrypoint | output | evidence package + SHA-256 | proof manifest + post-write SHA-256
- Browser-free status: yes/no; runtime-free status: yes/no
- Residual risk: remaining dependency or unproved boundary | impact | retirement proof
```

## Final delivery report

Use this expanded form when the compact protocol handoff needs supporting capability or investigation detail.

```markdown
Final Delivery
- Collector path:
- Output path:
- Intake mode:
- Capability snapshot:
- Proof manifest: analysis/proof_manifest.json
- Proof manifest artifact hash: SHA-256 computed after the manifest is written
- Evidence package path and SHA-256:
- First divergence: step / path / kind / or no divergence
- Real endpoint: scheme + host + port + route, without userinfo or raw query values
- Method and content type:
- Final protocol order:
- Real moving parts: name / writer / wire slot / scope / expiry / refresh path
- Transport kind:
- Decode chain:
- Python/helper boundary:
- Session contract:

Verification
- Acceptance oracle:
- Negative control:
- Repeat runs: live / offline
- Pagination confirmed:
- Fixed-input self-checks:
- No browser dependency:

Minimal verifiable facts
- 1.
- 2.
- 3.

Known instability
- 1.
- 2.

Residual risk
- Risk / impact / retirement proof:
```

## Proof manifest

Save `analysis/proof_manifest.json` without live secret values. Include:

```json
{
  "intake_mode": "live-target | artifact-only | continuation",
  "tool_capabilities": {},
  "artifact_hashes": [],
  "evidence_packages": [
    {
      "path": "analysis/evidence.json",
      "sha256": "<64 lowercase hex characters>"
    }
  ],
  "first_divergence": {
    "step_index": 0,
    "path": "<redacted structural path>",
    "kind": "<difference kind>"
  },
  "session_scope": {},
  "helper_versions": {},
  "fixed_vectors": [],
  "live_replay_count": 0,
  "redacted": true
}
```

Report the proof manifest file's own SHA-256 beside its path after writing the
file. Do not place that self-hash inside the manifest, because doing so creates
a recursive value.

## Recommended collector tree

```text
<project-root>/
  analysis/
    deobfuscated.js
    fixed_inputs.md
    key_logic.js
    notes.md
    proof_manifest.json
  collector/
    client.py
    decode.py
    main.py
    pipeline.py
    settings.py
    sign.py
    storage.py
  logs/
  output/
  tests/
    test_smoke.py
  README.md
  requirements.txt
```

## Run path and cache

Document:

- PyCharm entrypoint: `main.py` or `collector/main.py`
- investigation cache: `js_reverse_cache/tasks/<task-id>/`
- delivery proof: `analysis/proof_manifest.json`
