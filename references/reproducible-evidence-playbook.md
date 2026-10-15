# Reproducible Evidence Playbook

Use this playbook when a lesson should survive the current target, when a
successful and failing session chain look identical at the final request, or
when real captures must be deposited without publishing reusable secrets.

## Contents

- [Core rule](#core-rule)
- [Normalize evidence first](#normalize-evidence-first)
- [Find the first divergence](#find-the-first-divergence)
- [Minimal patch unit](#minimal-patch-unit)
- [Exercise the local practice lab](#exercise-the-local-practice-lab)
- [Deposit an experience card](#deposit-an-experience-card)
- [Evidence freshness](#evidence-freshness)
- [Completion gate](#completion-gate)

## Core rule

Do not promote a practical lesson from prose alone.

A reusable lesson needs:

- one minimal artifact or deterministic generator
- one expected success oracle
- one decisive negative control
- one explicit failure boundary
- no live credentials, cookies, tokens, or account data

## Normalize evidence first

Run `scripts/evidence_normalizer.py` on HAR or transcript JSON before comparing,
reporting, or publishing it. Use the same private HMAC key for samples that must
remain correlatable.

The normalized package must preserve:

- ordered session-chain steps
- request method and URL shape
- ordered and duplicate request and response headers
- body byte length and keyed HMAC-SHA-256 fingerprint
- redirects and response status
- state writes and their surfaces
- a keyed source-artifact fingerprint

The public-default package keeps structural field names, scopes, order,
lengths, and stable HMAC fingerprints. It omits raw bodies and unkeyed source
or body hashes because low-entropy passwords, PINs, and OTPs can be tested
against a public SHA-256. Known sensitive fields and recognizable sensitive
values are pseudonymized, but the manifest deliberately requires publication
review instead of claiming that arbitrary input is universally secret-free.
Keep exact raw captures only in the task-local ignored secret store.

Example:

```text
python scripts/evidence_normalizer.py capture.har evidence.json \
  --hmac-key-env SPIDER_EVIDENCE_HMAC_KEY \
  --proof-manifest analysis/proof_manifest.json
```

Use a high-entropy task-local key. Prefer `--hmac-key-env` or
`--hmac-key-file`; a literal `--hmac-key` is visible in process arguments and
is intended only for disposable tests.

Only a local analysis that explicitly needs raw source/body equality may add
`--include-raw-hashes`. That flag writes unkeyed SHA-256 values and therefore
must not be used for a public package or publication manifest. The evidence
package SHA-256 remains suitable for auditing the already-redacted package.

With `--proof-manifest`, the normalizer writes evidence proof-manifest schema
v2: a keyed source-artifact fingerprint, the normalized package schema version
and SHA-256, and redaction/publication-review flags. It deliberately does not
invent session scope, helper boundaries, or live-replay proof. Use a distinct
approved evidence-manifest path when a broader replay or collector manifest
already exists. Record the emitted package path and SHA-256 plus the manifest
path and its post-write SHA-256; the CLI prints all four values after a
successful write.

## Find the first divergence

When the final request matches but acceptance differs, compare whole ordered
chains with `scripts/transcript_diff.py`:

```text
python scripts/transcript_diff.py success.json failure.json --json
```

Start at the reported first divergence. Check the writer and first downstream
consumer before tuning later signers, bodies, or verifier fields. Do not sort
header lists or collapse duplicate headers into mappings just to make the diff
smaller.

The CLI reports fingerprints rather than raw changed values. A difference in an
earlier `Set-Cookie`, redirect, sidecar response, counter, or storage write can
explain failure even when the final body hash is identical.

### Minimal patch unit

`first_divergence` is the earliest proven difference between browser truth and local output.
Patch only the smallest causal unit that explains it: one value, one function shell, one returned object contract, or one inseparable serializer step.

Each patch iteration records:

1. triggering evidence id or transcript step
2. browser expected value or behavior
3. local actual value or behavior
4. why this unit is the smallest honest fix
5. whether the divergence moved later or disappeared

Loading without errors, fewer logs, plausible output length, or one HTTP `200` does not prove the divergence moved. If the first divergence stays at the same path, the patch did not earn escalation.

When live success exists and many layers are still open, isolate the layer first with `references/positive-sample-ablation-playbook.md`, then apply this minimal-unit rule inside that layer.

## Exercise the local practice lab

Use `scripts/practice_lab.py` to verify that an implementation can distinguish
protocol truth from plausible shortcuts:

This loopback service is a deterministic skill fixture, not a fresh live
target. Use a direct HTTP client and do not start either browser tool merely to
exercise it.

```text
python scripts/practice_lab.py describe
python scripts/practice_lab.py --self-test
python scripts/practice_lab.py serve --port 8765
```

The four offline cases cover:

1. exact body bytes, duplicate header order, and correct field slot
2. same-session challenge and bootstrap state
3. ordered prefix, Base64, zlib, and JSON response decode
4. pagination that pivots to a different route family

Each case includes a positive oracle and a negative control. Passing only the
positive path is insufficient because a weak validator can make broken logic
look correct.

## Deposit an experience card

Use `references/experience-card-schema.md` as the canonical machine-readable contract. During an investigation, this compact block may remain in `report.md` as human notes:

```text
Symptom:
Initial wrong hypothesis:
Decisive evidence:
One-variable experiment:
First divergent state transition:
Positive oracle:
Negative control:
Final invariant:
Failure boundary:
Fixture or generator path and hash:
```

The note is not a promoted card. Keep a one-off finding in task-local
`experience-candidate.json`; promote it only after two independent jobs and all
schema gates pass. Add a general playbook or deterministic script only after the
same operation remains useful across repeated cases.



## Evidence freshness

On continuation or after a live miss against previously good artifacts:

1. recheck script/source fingerprints, request/response shape, cookie/storage transitions, and the challenge state the current test consumes
2. if consistent, continue and record that the package was revalidated
3. if changed, mark the old package stale, capture a new immutable package, and resume from the earliest dependent stage
4. do not mix old dynamic state into the new session chain
5. keep historical replay against an old package separate from live acceptance against the current package

## Completion gate

Do not call the lesson deposited until the fixture is secret-free, the negative
control fails for the intended reason, the positive oracle passes from a clean
run, and the relevant skill validator executes the check automatically.
