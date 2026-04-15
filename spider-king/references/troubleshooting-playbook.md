# Troubleshooting Playbook

Use this file when replay logic almost works but still fails.

## Symptom routing

### `403`, `412`, `429`

- compare headers
- compare cookies
- compare pacing
- compare sign freshness

### `200` with business error

- compare query and body serialization
- compare timestamp precision
- compare transport wrapper outputs

### `200` with gibberish or strings

- check decrypt path
- check fonts
- check hint arrays for page-specific header clues

### first request works, replay fails

- check rotating cookies
- check in-memory refresh fields
- check whether bootstrap must run before each request

### local helper matches names, not outputs

- move back to fixed-input comparison
- assume helper is patched until proven standard

## Final rule

When stuck, route by symptom. Do not randomly mutate five things at once.
