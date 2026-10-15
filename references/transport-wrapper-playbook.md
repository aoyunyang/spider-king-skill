# Transport Wrapper Playbook

Use this reference when:

- business code builds one param but the wire sends another
- `token`, `sign`, `m`, `f`, or payload fields are rewritten before send
- `$.ajaxSetup`, interceptors, fetch wrappers, or request middleware mutate headers or bodies

## Core rule

The canonical mutation point is where the wire payload changes, not where the business code first creates placeholders.
An empty or no-op wrapper is not a mutation point.

## Recognition signals

- UI code builds `token`, but the network sends `m`
- query params or body fields appear only after wrapper execution
- headers are injected in `beforeSend` or fetch middleware
- request serialization differs from the visible input object
- the candidate blob looks right, but replay only works after moving it to a different header, cookie echo, query param, or wrapper-owned field
- an interceptor rewrites the URL, skips original send, and rebuilds a different form
- an empty or no-op `beforeSend` / IIFE is present but the captured body still equals the visible business fields

## Working method

1. diff business-layer params against the final network payload
2. inspect wrappers before digging deeper into business code
3. record exactly which fields the wrapper adds, rewrites, deletes, or relocates
4. if the wrapper is empty or a no-op IIFE and the captured body equals the visible fields, skip signer reverse
5. prove the final transport slot of each decisive artifact, not just its value shape
6. rebuild the wrapper logic locally
7. verify the final serialized payload, not just the intermediate object

## Common traps

- reversing a decoy param that never reaches the wire
- signing decoded values when the site signs URL-encoded values
- assuming visible JSON is the final signed payload
- treating a plausible blob as correct while leaving it in the wrong transport slot
- replaying the VM-native body against the live sibling endpoint after the interceptor reshaped the form
- treating an empty ajax `beforeSend` IIFE as a missing token writer when the captured body already equals the visible fields

## Delivery rule

Reproduce the transport-layer mutation locally and keep the decoy field out of the final collector.
