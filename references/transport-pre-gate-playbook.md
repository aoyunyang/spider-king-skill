# Transport Pre-Gate Playbook

Use this playbook when the clean baseline dies before meaningful application semantics are visible.

## Contents

- [Route here when](#route-here-when)
- [Core idea](#core-idea)
- [Identity coherence](#identity-coherence)
- [Fast execution path](#fast-execution-path)
- [Minimal admission matrix](#minimal-admission-matrix)
- [Native escalation checkpoint](#native-escalation-checkpoint)
- [High-value checks](#high-value-checks)
- [Common traps](#common-traps)
- [Delivery guidance](#delivery-guidance)
- [Minimal handoff notes](#minimal-handoff-notes)

## Route here when

- standard HTTP clients fail at H2 reset, TLS EOF, handshake timeout, or early disconnect
- the same route behaves differently across UA families, HTTP versions, ALPN, or client stacks
- a stdlib client still fails after copying browser headers and cookies, while a browser-like transport reaches a different branch
- impersonated transport or mobile or app UA passes while default desktop or stdlib traffic fails
- one challenged landing route fails, but a sibling auth, identity, or business route still works
- a stdlib client returns HTTP 403 JSON forbidden after copying a live-admitted token or cookie, while installed curl impersonate returns business 200 on those same bytes
- the same implementation alternates between success and access denial by proxy exit or network path

## Core idea

Transport admission is a separate contract from signer, cookie, or payload logic.
That contract can be decided before normal HTTP semantics even exist.

Treat the admission profile as a whole:

- TLS ClientHello family
- ALPN and negotiated HTTP version
- HTTP/2 SETTINGS, pseudo-header order, and early request ordering when H2 is in play
- declared identity such as UA family
- Client Hints, language, timezone, runtime navigator identity, and proxy exit when they are reflected in verifier or telemetry payloads

Do not reverse the application layer until one request is admitted cleanly enough to observe real semantics.
JA3 and JA4 are summary indicators, not the protocol itself; the authoritative evidence is the underlying transport profile that produced them.

## Identity coherence

Keep the declared identity internally consistent across layers:

```text
transport impersonation family
HTTP version and ALPN
User-Agent major
Client Hints brands and versions
runtime navigator.userAgent / platform
language, timezone, screen, and device class when collected
proxy exit and session cadence
```

Do not combine a transport profile from one browser family, headers from a
second, and runtime fingerprint data from a third unless live captures prove the
target tolerates that mixture. A root page can pass with an incoherent tuple
while a route, sidecar, or business request fails later.

Lock replay identity to the installed curl impersonate chrome major from
`scripts/check_reverse_env.py`. Evidence-host major should match that
impersonate. Do not copy a newer live Chrome major into User-Agent or Client
Hints while TLS/H2 stays on a lower impersonate. That mismatch is
`transport-admission` / profile-drift: repair the capsule, do not restart
application-layer risk-control reverse and do not add extra APIs.

## Fast execution path

1. Freeze a small admission matrix.
   Record:
   - route
   - method
   - client stack
   - UA family
   - HTTP version
   - ALPN and transport fingerprint family when visible
   - result class such as pass, H2 reset, timeout, redirect loop, or challenged HTML

2. Compare packet-level transport before giant bundle work.
   If a pcap, packet trace, or handshake capture is available, diff:
   - cipher-suite set and order
   - extension set and order
   - GREASE behavior
   - supported groups, key shares, and signature algorithms
   - ALPN offerings
   - HTTP/2 SETTINGS and pseudo-header order
   - first-request ordering when the transport immediately pipelines follow-up traffic

3. Test narrow transport variations before giant bundle work.
   Common variations:
   - stdlib client vs impersonated TLS client
   - the same live-admitted token or cookie bytes on stdlib versus impersonate, especially when sibling routes already return 200 on stdlib
   - HTTP/2 vs HTTP/1.1
   - desktop browser UA vs mobile or app UA
   - challenged landing route vs sibling auth or data route
   - plain client stack versus browser-like impersonation when the returned challenge family itself changes
   - closest browser-family transport backend versus a distant default stack that would need hand patching

4. Keep the exception narrow.
   If only one route family needs a special transport profile, scope it there instead of polluting the whole collector.

5. Separate admission from later gates.
   After one route is admitted, continue normal triage for signer, verifier, decode, or session logic.

6. Prefer route bypass over unnecessary challenge work.
   If a sibling identity, auth, or data route cleanly avoids the challenged landing path, use that evidence before spending hours on the wrong gate.

7. Separate egress reputation from implementation failure.
   When a previously accepted protocol chain suddenly returns access-denied
   bodies, hard resets, or abuse pages, test the same route with the same exit
   in a real browser or closest available browser-like baseline before changing
   signer, form, or verifier logic. If the browser fails on that exit too, label
   the state `egress-gated`, change the exit or cooldown, and rerun the whole
   chain. If the browser succeeds but the protocol client fails, then inspect
   transport coherence, sidecar count, cookie transition, and serialization.

## Minimal admission matrix

Before changing signer, cookie, or payload code, freeze a small same-input
matrix. Hold the route, method, business parameters, session chain, referer,
and pacing constant while varying only the transport surface under test:

```text
same route + same business input + same session
  -> plain client / HTTP version A
  -> closest admitted client / HTTP version B
  -> compare protocol result, response family, and business oracle
```

Record at least the client profile, negotiated HTTP version, ALPN when known,
status class, response family, parseable business anchor, and whether the
connection was new or reused. A transport failure is only a pre-gate finding;
the admitted row must reach the real downstream business oracle before the
application layer is considered understood.

Use one intentional negative control, such as replacing the admitted
transport with the plain-client profile. If that control does not fail for the
expected transport reason, do not promote the transport-gated hypothesis.
Conversely, if the differential disappears when cookies, session state,
signer fields, or permissions are held correctly, return to the relevant
request or session playbook instead of widening the transport profile.

HTTP/2, a particular ALPN value, or a browser-like client is not a universal
recipe. Keep the accepted profile route-local until an independent target
repeats the same invariant, and preserve connection reuse or H2 settings only
when live evidence shows they matter.

## Native escalation checkpoint

Do not build a custom TLS backend merely because an impersonated client still
fails. Escalate only after repeated browser and candidate captures prove a
decisive transport mismatch that the closest maintained backend cannot express.

Before escalating, freeze:

- the exact browser build, operating system, route, network path, and capture hashes
- at least three browser cold-connection samples so stable fields are separated from GREASE or proved ordering variability
- one negative-control capture from the failing client and one capture from the closest candidate backend
- the exact unexpressible field across ClientHello, ALPN, H2 settings, pseudo-header order, or connection behavior
- whether the proxy tunnels end-to-end TLS or terminates and replaces the client fingerprint

Then read `references/native-transport-profile-playbook.md`. Prefer a Python
collector with a small route-local native package, expose enough diagnostics to
prove the backend and connection state, and keep deterministic proof separate
from any research randomizer. Use `scripts/transport_profile_diff.py` to compare
structured browser and candidate profiles; do not promote one browser version's
raw values into universal defaults.

## High-value checks

- whether the failure happens before headers, after TLS, or only after body bytes start flowing
- whether HTTP headers look browser-like but the pre-HTTP ClientHello family is still obviously different
- whether redirects or alternate hosts change the policy
- whether JA3, JA4, or another summary fingerprint is only acting as a hint while the real mismatch sits in raw extension order, GREASE behavior, ALPN, or H2 settings
- whether the target browser family naturally randomizes extension order or GREASE, making one frozen JA3 hash a bad success target
- whether mobile or app UA changes the returned HTML shape, not just the pass or fail status
- whether ALPN, HTTP version, and H2 settings match the branch you are trying to replay
- whether UA, Client Hints, runtime navigator identity, and collected profile fields describe one coherent client generation
- whether two client stacks are reaching different challenge families on the same route rather than the same family with different success rates
- whether the route requires the same transport profile as neighboring routes or is an isolated exception
- whether the browser-success sample is really application success or only a different transport admission path
- whether browser-like impersonation is required first to observe the same bootstrap chain the browser sees before any application-layer reverse is honest
- whether changing only the exit restores a known-good implementation, indicating residual egress risk rather than an algorithm regression

## Common traps

- blaming cookies or signatures for traffic that never cleared transport admission
- treating stdlib 403 JSON forbidden of a live-admitted token as a bad signer because sibling routes still return 200 on stdlib
- restarting canvas, audio, or WebGL reverse after impersonate plus the current helper already returns business 200
- changing only `User-Agent` or HTTP headers when the gate is decided by ClientHello or H2 profile before the request semantics exist
- treating JA3 or JA4 equality as the only goal instead of matching the underlying transport behavior that the route actually checks
- hard-freezing one browser fingerprint hash even though that browser family randomizes extension order or GREASE between requests
- hardcoding one magical UA across the whole collector when only one route needed it
- copying a newer live Chrome major onto a lower curl impersonate and treating the new challenge family as a fresh signer problem
- treating impersonated TLS as final victory instead of the start of application-layer reversal
- reversing the wrong verifier or challenge page because a weaker client stack was silently diverted into a different gate family
- patching a distant default TLS stack piece by piece before testing a closer transport family or narrow route-local adapter
- assuming the challenged landing page is the only entry route worth testing

## Delivery guidance

Preferred shape:

1. Python collector with route-local transport policy
2. narrow transport adapter or closer client backend only where stdlib transport is insufficient
3. application-layer reversal done only after admission is proven
4. no browser dependency in the final path

## Minimal handoff notes

Report these items explicitly:

- which route family was transport-gated
- which transport surfaces actually mattered: ClientHello family, ALPN, HTTP version, H2 settings, pseudo-header order, or early request ordering
- whether summary fingerprints such as JA3 or JA4 were only hints or an actual acceptance condition proven by evidence
- which narrow client profile admitted the baseline
- whether the exception is route-local or global
- whether a sibling route bypassed the gate
- whether stdlib 403 versus impersonate 200 on the same admitted bytes decided transport versus signer
- which later family triage won after admission
