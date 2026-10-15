# Specialist Handoff Contract

Use this contract when one focused route or installed specialist should take ownership of a proved blocker. The handoff narrows work; it does not broaden target scope, permissions, request budget, runtime access, or delivery requirements.

When the active work order authorizes this exact path, store request and result in one envelope at:

```text
<project>/js_reverse_cache/tasks/<task-id>/handoff.json
```

Use `{"request": {...}, "result": null}` initially, then replace only the `result` member after return. Never append a second top-level JSON object or overwrite the request. Under `writeMode: no-write` or an empty `allowedPaths`, return the same request/result fields in memory or in the user response and do not create `handoff.json`.

## Contents

- [Before Handoff](#before-handoff)
- [Request Shape](#request-shape)
- [Return Shape](#return-shape)
- [Acceptance](#acceptance)

## Before Handoff

1. Pass `references/evidence-corroboration-gate.md`: the blocker type or ownership claim has at least two independent evidence surfaces. One status code, one cookie/token name, one old note, or one plausible helper output is not enough.
2. Confirm the intended specialist exists in the current capability snapshot.
3. Name an executable Spider fallback when it does not exist. If the user explicitly required the missing specialist/runtime, present the fallback for acceptance; do not silently treat it as equivalent. Never invent a family-specific shortcut inside Spider when the specialist is missing.
4. Park or release the current same-target owner before the next owner becomes `TARGET_ACTIVE`.
5. Preserve unique unreplayable state as `RETAINED_EXCEPTION`; do not destroy it just to make cleanup look complete.
6. Reference secrets by task-local path plus hash only. Never embed raw Cookie, Authorization, token, key, IV, account, or private payload values.

## Request Shape

Copy scope, permissions, budget, and `allowedPaths` from the active provider work order, then narrow them for the specialist. The values below are conservative defaults for a handoff with no upstream authorization. A handoff may change `no-write` to a writable mode only when the upstream work order already authorized that mode and every writable path remains in the inherited allowlist.

The envelope's `request` member is:

```json
{
  "schemaVersion": 1,
  "taskId": "non-secret task identifier",
  "intakeMode": "live-target | artifact-only | continuation",
  "fromRoute": "current Spider route",
  "requestedOwner": "installed specialist or focused Spider route",
  "fallbackRoute": "executable Spider route",
  "reason": "one proved blocker",
  "scope": {
    "scheme": null,
    "host": null,
    "port": null,
    "routePrefix": "/proved-prefix",
    "allowedArtifacts": []
  },
  "permissions": {
    "browserRecon": false,
    "liveReplay": false,
    "accountOrSessionUse": "none",
    "targetCodeExecution": "blocked",
    "dependencyInstall": "blocked",
    "writeMode": "no-write"
  },
  "budget": {
    "requestsRemaining": 0,
    "retriesRemaining": 0,
    "websocketFramesRemaining": 0,
    "minDelayMs": 0,
    "concurrency": 1
  },
  "allowedPaths": [],
  "provenFacts": [],
  "evidence": [
    {
      "path": "task-relative path",
      "sha256": "64 lowercase hex characters",
      "proves": "one bounded claim",
      "capturedAt": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ],
  "unknowns": [],
  "requestedOutput": "evidence | local-proof | code | blocker",
  "acceptanceTest": "one objective proof",
  "cleanupState": "PARKED | RELEASED | RETAINED_EXCEPTION"
}
```

Unknown or omitted permissions mean blocked. Every boolean, enum, counter, delay, scope field, and path must be equal to or narrower than the upstream work order. The specialist may consume only the recorded budget and may write only the recorded `allowedPaths`; `task-cache-only` without a non-empty inherited allowlist grants no write. A live-target specialist must follow the same serial browser ownership and paired evidence rules as Spider King.

## Return Shape

The owner returns this object and, only when authorized, stores it as the envelope's `result` member:

```json
{
  "status": "evidence | local-proof | code | blocked",
  "owner": "actual capability owner",
  "result": "bounded result or named blocker",
  "claims": [
    {
      "claim": "one conclusion",
      "evidenceSha256": ["supporting artifact hashes"],
      "verifiedAt": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ],
  "artifacts": [],
  "fixedVector": "passed | failed | not-applicable",
  "liveReplay": "passed | failed | blocked | not-authorized",
  "budgetConsumed": {},
  "runtimeCleanupState": "RELEASED | PARKED | RETAINED_EXCEPTION",
  "residualRisks": [],
  "recommendedNextOwner": "Spider route or none"
}
```

## Acceptance

Spider King remains responsible for accepting the return against the recorded test and final delivery gate. Specialist completion is not protocol completion. Reject or send back a result when it:

- hardens a family or gate claim from only one evidence surface; downgrade that claim to hypothesis and continue the generic Spider loop
- cites no artifact hash for a technical claim
- substitutes helper load, output shape, or HTTP status for the requested oracle
- relies on a browser, browser profile, page-context fetch, or manual state in final delivery
- widens scope or permissions silently
- leaves a task-owned hook, browser, worker, profiler, lease, or runtime active without an explicit retained exception
- copies task secrets into reports, fixtures, code, or the skill directory
