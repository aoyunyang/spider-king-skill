# Report Templates

Use these headings to keep progress crisp and comparable across investigations.

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
  - Key headers:
  - Key cookies:
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
- Raw payload sample:

What changed on the wire
- Query:
- Body:
- Headers:
- Cookies:

Conclusion
- Verified helper or protocol rule:
- Verified decode or parser rule:
- Remaining unknowns:
```

## Implementation decision report

```markdown
Implementation Decision
- Delivery shape: Python / Python + JS helper / Python + WASM helper / Python + bootstrap helper
- Why this shape:
  1.
  2.
  3.

Protocol contract
- Required session state:
- Required headers:
- Required cookies:
- Required helper outputs:
- Required transport envelope:
- Required decode chain:

Known risks
- 1.
- 2.
```

## Final delivery report

```markdown
Final Delivery
- Collector path:
- Output path:
- Real endpoint:
- Real moving parts:
- Transport kind:
- Decode chain:

Verification
- Repeat runs:
- Pagination confirmed:
- Fixed-input self-checks:
- No browser dependency:

Known instability
- 1.
- 2.
```

## Recommended collector tree

```text
<project-root>/
  analysis/
    deobfuscated.js
    fixed_inputs.md
    key_logic.js
    notes.md
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
