# Troubleshooting Playbook

Use this file when replay logic almost works but still fails.

## Symptom routing

### `403`, `412`, `429`

- compare headers
- compare cookies
- compare pacing
- compare sign freshness
- if failures start only after hooks or breakpoints, suspect observer effect and recapture a clean baseline

### `200` with business error

- compare query and body serialization
- compare timestamp precision
- compare transport wrapper outputs
- compare whether a verifier or cookie refresh step is now missing

### `200` with gibberish or strings

- check decrypt path
- check fonts
- check hint arrays for page-specific header clues

### first request works, replay fails

- check rotating cookies
- check in-memory refresh fields
- check whether bootstrap must run before each request
- prove cookie provenance before blaming the signer

### local helper matches names, not outputs

- move back to fixed-input comparison
- assume helper is patched until proven standard

### clean capture works, hooked capture fails

- suspect observer effect
- remove broad global hooks and debugger pauses
- capture one untouched baseline request and response
- move instrumentation outward toward the request boundary
- prefer initiator stacks and diffs before invasive monkey patches

## Final rule

When stuck, route by symptom. Do not randomly mutate five things at once.
