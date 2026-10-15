# Project Artifact Contract

Use this before the first save, before promoting code out of cache, and whenever a route wants to reuse or overwrite an existing artifact.

## Contents

- [Core Rule](#core-rule)
- [Before First Write](#before-first-write)
- [Success and failure path hygiene](#success-and-failure-path-hygiene)
- [Volatile Evidence](#volatile-evidence)
- [Stable Delivery](#stable-delivery)
- [Proof Manifest](#proof-manifest)
- [Promotion Checklist](#promotion-checklist)

## Core Rule

Spider King keeps volatile reverse evidence separate from stable delivery code.

Task captures and probes go under:

```text
<project>/js_reverse_cache/tasks/<task-id>/
```

Stable proof and handoff metadata go under:

```text
<project>/analysis/proof_manifest.json
```

Runnable `compact-replay` and `collector` delivery remains a PyCharm right-click entrypoint, normally:

```text
<project>/main.py
<project>/collector/main.py
```

`evidence` and `local-proof` do not require either entrypoint unless executable packaging was requested. A `no-write` conversational result does not create this layout. Do not replace the layout with another skill's project tree during routine work.

## Before First Write

Bind one project root. If the user gave a folder, use it. If not, ask once whether to use the current workspace or a custom folder.

Bind every prospective write to a non-empty `allowedPaths` entry before resolving the destination. The resolved destination must remain equal to or below both the bound project and an allowed path.

Reject task-owned writes when:

- the destination is the skill directory
- the destination is OS temp, `%TEMP%`, `%TMP%`, `AppData/Local/Temp`, or an agent temp root
- the path escapes the chosen project
- the path is a symlink, junction, mount-point reparse path, or hard-link target
- the write would overwrite an existing stable file without explicit path approval


## Success and failure path hygiene

- give each runner invocation a unique task-local run id or directory
- never let a failed diagnosis overwrite the last accepted success package
- store accepted fixtures and reports under a success-stable name; write failure dumps beside them, not on top of them
- regenerate volatile helper inputs under run-scoped temp names when concurrent stages exist

## Volatile Evidence

Use `js_reverse_cache/tasks/<task-id>/` for:

- `task.json`
- `network.jsonl`
- `runtime-evidence.jsonl`
- `silent_value/` when low-observer boundary capture is used (`capture_plan.json`, `sign_boundary.jsonl`, `vm_public_io.jsonl`, `wasm_boundary.jsonl`, `state_writes.jsonl`, `wire_correlations.jsonl`, `source_index.json`)
- `handoff.json`
- `experience-candidate.json`
- `fixtures/`
- `report.md`
- downloaded JS, WASM, HTML, fonts, images, protobuf samples, HAR extracts, screenshots, net logs, and decoded scratch files

Create folders on demand. Do not pre-create empty evidence trees.

Silent-value cards follow schema `spider-king.silent_value/v1` in `references/silent-value-capture-playbook.md`. Keep raw proprietary capture dumps task-local; index them from `source_index.json` by path, size, and hash when needed. Do not promote capture backends into stable delivery code.

Raw account state, cookies, tokens, Authorization values, personal data, and full private responses must stay local, redacted from chat, and excluded from version control. Prefer hashes, lengths, field names, provenance, and structural samples in reports.

## Stable Delivery

Promote a file out of cache only when:

1. Its inputs are known.
2. Its import has no network, browser, profile, or file side effects.
3. Fixed vectors or named checkpoints pass.
4. The live path, if requested, is Python-owned.
5. The file is listed in the proof manifest or final report.

Use `main.py` or `collector/main.py` for the right-click entrypoint. Move only proven reusable responsibilities into helpers such as:

- `collector/client.py`
- `collector/sign.py`
- `collector/bootstrap.py`
- `collector/decode.py`
- `collector/storage.py`
- `utils/*`

Keep dynamic cookies, timestamps, current browser exports, and run-specific challenge bodies out of stable code.

### Dual-runtime helper packaging

When Python owns HTTP and a tiny Node or WASM helper remains:

- keep helper files next to the collector, not in the skill directory
- ship `package.json` or equivalent and install instructions; do not rely on copying `node_modules`
- ship secret-free structural baselines such as field-slot masks, sparse index maps, or fixed-vector fixtures
- keep live tokens, cookies, account state, and raw success grants task-local
- document whether delivery is browser-free only or also free of any non-Python runtime
- proof manifest records helper version or asset hash, not secret values
- before the helper runs, bind the project with `scripts/check_reverse_env.py --project-root <project>` and fingerprint only explicitly selected public lockfiles with `--helper-lockfile`; record relative paths, byte lengths, and SHA-256 values without copying lockfile contents

Suggested stable layout:

```text
collector/
  main.py
  requirements.txt
  helpers/
    package.json
    encrypt_or_vm_helper.js
  artifacts/
    baseline_field_mask.json
    sparse_slots.json
    fixed_vectors.json
  README_install.md
analysis/
  proof_manifest.json
```

## Proof Manifest

Manifest content is capability-specific. Record only facts that the producing
tool can prove; do not fill unknown session, helper, or replay fields with
guessed defaults.

For a standalone `evidence` delivery, run
`scripts/evidence_normalizer.py` with `--proof-manifest`; it emits evidence
proof-manifest schema v2:

```json
{
  "proof_manifest_version": 2,
  "source": {
    "format": "har | transcript",
    "hmac_sha256": "keyed source-artifact fingerprint"
  },
  "evidence_package": {
    "schema_version": 2,
    "sha256": "hash of the already-redacted evidence package"
  },
  "redaction": {
    "scheme": "hmac-sha256",
    "scope": "known-sensitive-fields-and-recognizable-values",
    "publication_review_required": true,
    "raw_hashes_included": false
  }
}
```

This evidence manifest does not claim live replay, session compatibility, or a
helper boundary. If a broader delivery manifest already exists, write the
evidence manifest to a distinct approved path and reference its post-write hash
from the broader manifest or final report; never overwrite the broader manifest.

For persisted `local-proof`, `compact-replay`, or `collector` delivery, record
enough to audit the claimed capability without storing secrets:

```json
{
  "capability": "collector | compact-replay | local-proof",
  "targetScope": "redacted exact scope",
  "artifactFingerprints": [],
  "sessionScope": "anonymous | account-bound | retained-exception | none",
  "helperBoundary": "pure-python | local-js | wasm | local-bootstrap | iv8-local-runtime",
  "runtimeEvidence": {
    "pythonVersion": "resolved version",
    "nodeVersion": "resolved version | missing | not-required",
    "npmVersion": "resolved version | missing | not-required",
    "projectVenv": "active | advisory-mismatch | required-mismatch | not-required",
    "helperLockfiles": [
      {"path": "relative/public-lockfile", "bytes": 0, "sha256": "..."}
    ]
  },
  "fixedVectorProof": "passed | failed | not-run",
  "liveReplayProof": "passed | blocked | not-requested",
  "browserFree": true,
  "runtimeFree": false,
  "residualRisks": []
}
```

Use unkeyed SHA-256 only for public, high-entropy code, already-public assets,
or an explicitly local analysis artifact. Use keyed HMAC fingerprints for
captures or bodies that can contain secrets or personal data. The normalizer's
`--include-raw-hashes` flag is local-only and must not be used for a publication
manifest. Hash the already-redacted evidence package for artifact auditing,
require publication review, and never claim that arbitrary input is universally
secret-free. A manifest cannot contain its own stable hash, so record its path
and post-write SHA-256 in the final report or its parent delivery manifest.
Never copy raw secrets into the proof manifest.

## Promotion Checklist

Before final delivery, answer:

- Does deleting OS temp leave the project reproducible?
- Does removing the browser profile leave the collector runnable?
- Are fixed samples separated from live-generation code?
- Is every rotating state regenerated, refreshed, or clearly declared as a retained exception?
- Is one lucky response prevented from becoming scale?

If any answer is no, keep the artifact in cache and return a precise blocker.
