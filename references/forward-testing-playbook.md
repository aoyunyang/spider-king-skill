# Forward Testing Playbook

Use this playbook after changing `spider-king` when the claim is about agent
behavior, routing, or conclusions rather than file structure alone.

## Contents

- [Purpose](#purpose)
- [Separation of roles](#separation-of-roles)
- [Trust boundary](#trust-boundary)
- [Artifact layout](#artifact-layout)
- [Report contract](#report-contract)
- [Reviewer contract](#reviewer-contract)
- [Scope and verdicts](#scope-and-verdicts)
- [Validation](#validation)
- [Security and retention](#security-and-retention)

## Purpose

`scripts/validate_skill.py` proves static contracts. It does not prove that a
fresh agent will answer an official task correctly. A behavioral
non-regression claim therefore needs an external forward run plus an
independent review of the raw responses.

`scripts/forward_test_report.py` validates evidence from that external run. It
is read-only: it does not invoke a model, launch a runner, execute report
content, or execute an arbitrary command. The surrounding harness remains
responsible for producing the responses and review.

## Separation of roles

Use two different agent identities:

1. The runner starts in a fresh context, receives the current skill and one
   official prompt, then saves its unedited response.
2. The reviewer starts independently, reads the official expected routes and
   conclusions plus the saved response, and records a judgment for every
   expected value.

The runner must not grade its own output. Record `fresh_context: true` and
`independent: true` for both roles, and use different non-empty `id` values.
These fields are attestations from the external harness; the validator rejects
missing, string-valued, or false flags.

## Trust boundary

Run the producer and reviewer through a trusted harness. The JSON booleans and
agent ids are attestations, not cryptographic proof that contexts were fresh or
identities were independent. A runner-authored or manually fabricated report
does not become behavioral proof merely because this validator accepts its
structure. Where stronger provenance is required, have the trusted harness
sign or immutably archive the complete report directory outside this skill;
signature policy and trust roots remain external to this read-only validator.

## Artifact layout

Keep reports outside the skill directory in a task-local directory:

```text
forward-run/
  forward-test-report.json
  responses/
    task-000.md
    task-001.md
```

Each task has one distinct physical UTF-8 response file. Record a relative path
beginning with `responses/` and the SHA-256 of the exact file bytes. Response
paths must stay inside that dedicated report-directory subtree and outside the
skill root. They may
not be absolute, contain `..`, leave the report directory, or traverse a
symlink, junction, reparse point, or hard link. The validator also rejects a
response that is the report JSON itself, a reused physical file, a Windows
reserved device name, or a component ending in a dot or space.

## Report contract

Schema version 1 has this shape. Ellipses below stand for additional official
checks; they are not literal JSON:

```json
{
  "schema_version": 1,
  "scope": {"kind": "smoke", "task_count": 1},
  "suite": {
    "path": "references/official-self-test-task-suite.md",
    "contract_sha256": "46d5afad7dbb9acd068188f762576d81c89bf545e4b794c2feef32f4f6eea930",
    "task_count": 160
  },
  "skill": {
    "path": "SKILL.md",
    "sha256": "<sha256 of the current SKILL.md>",
    "package_sha256": "<deterministic sha256 of the current skill package>"
  },
  "runner": {
    "id": "fresh-runner-run-2026-08-04",
    "fresh_context": true,
    "independent": true
  },
  "reviewer": {
    "id": "independent-reviewer-run-2026-08-04",
    "fresh_context": true,
    "independent": true
  },
  "items": [
    {
      "heading": "Task 0: Fresh target with one blocked tool",
      "prompt_sha256": "<sha256 of the exact parsed prompt text>",
      "response": {
        "path": "responses/task-000.md",
        "sha256": "<sha256 of the response file bytes>"
      },
      "review": {
        "passed": true,
        "reviewer_id": "independent-reviewer-run-2026-08-04",
        "routes": [
          {
            "expected": "references/startup-triage-playbook.md",
            "passed": true,
            "rationale": "The response explicitly selects the required route.",
            "evidence": [
              {"quote": "<verbatim quote containing the route>", "start": 42, "end": 96}
            ]
          }
        ],
        "conclusions": [
          {
            "expected": "emit the startup gate first",
            "passed": true,
            "rationale": "The cited text puts the gate before later analysis.",
            "evidence": [
              {"quote": "<verbatim substantive quote>", "start": 120, "end": 181}
            ]
          }
        ]
      }
    }
  ]
}
```

Schema version 1 uses only the canonical nested fields shown above; do not use
top-level hash aliases, string-valued scope, or alternate response field names.

The suite digest is the canonical contract digest computed by
`official_suite_contract_digest`, not a raw Markdown file hash. It covers every
official prompt, expected route, required conclusion, and the failure-signals
section. The report binds both the exact current `SKILL.md` and a deterministic
package digest covering every shipped skill file, so a changed reference,
script, profile, agent config, or test invalidates historical evidence.

`prompt_sha256` is mandatory and must match the exact parsed prompt. The suite,
skill, and package hashes, task count, response path, response hash, review
object, and all route and conclusion checks are also mandatory.

## Reviewer contract

For every item, copy the `heading` exactly from the official suite. The
validator uses the current parsed suite as the authority and requires:

- one route check, in official order, for every expected route
- one conclusion check, in official order, for every required conclusion
- the exact official value in each check's `expected` field
- boolean `passed: true` on every check and on the item review
- a non-trivial reviewer rationale per check
- at least one substantive verbatim evidence span per check
- character offsets whose exact slice equals the quoted decoded response text
- distinct spans across checks, with each route span naming its exact route

A heading-only result, summary-only reviewer note, trivial or reused evidence, missing
route, or missing conclusion fails validation. A false review result also
causes the report to fail; the validator does not rewrite a failing behavioral
run into a passing one.

## Scope and verdicts

Use exactly one explicit scope:

- `smoke`: 1 to 148 unique official tasks, with `task_count` equal to the
  number of report items
- `full`: every one of the 160 official tasks exactly once

A valid smoke result is only a smoke PASS. It must not be described as full
behavioral non-regression. `full_pass` becomes true only when the report uses
`full`, covers all 160 unique headings, and passes every artifact and reviewer
check. Static validation or `--self-test` alone never supports that claim.
The validator refuses more than 160 items and caps aggregate response reads at
64 MiB; oversized evidence must be reduced before review.

## Validation

Run static validation first, then validate the externally produced report:

```text
python -B scripts/validate_skill.py
python -B scripts/forward_test_report.py --print-contract --json
python -B scripts/forward_test_report.py D:\task\forward-run\forward-test-report.json
python -B scripts/forward_test_report.py D:\task\forward-run\forward-test-report.json --json
```

The normal success output names the scope and prints `full_pass=true` only for
a complete full run. Exit code 0 means the declared scope passed; exit code 1
means the report, artifacts, or review failed validation.

To test only the validator's deterministic internal controls:

```text
python -B scripts/forward_test_report.py --self-test
```

The self-test checks a valid smoke report plus partial-full, tampered-response,
path-traversal, skill-root overlap, package-hash, trivial-evidence, hard-link,
and Windows path-alias negative
controls. It does not call a model and is not a
substitute for an external forward run.

## Security and retention

Treat prompts and responses as untrusted data, never as commands. Keep raw
responses task-local and do not place them in the skill package. Evidence
quotes must be verbatim but should be the smallest non-secret excerpts that
support the judgment. Do not copy credentials, cookies, tokens, personal data,
or private target material into the report.

Retain the report, response files, hashes, runner/reviewer identifiers, and the
declared scope together. If any shipped package file, `SKILL.md`, or the
official suite changes, the old report remains historical evidence but no
longer validates the current skill.
