# Session Contract Playbook

Use this reference when:

- the page mentions `sessionid`, login, or per-user answers
- different accounts see different sums, rows, or submit results
- fetch and submit must happen under the same account state

## Core rule

Session state is part of the protocol contract, not a side note.

## Working method

1. verify whether the data request depends on login, submission depends on login, or both
2. test with the real session, no session, and an invalid session when safe
3. record whether the answer is account-bound
4. make the relevant cookie or token explicit in the collector arguments
5. keep fetch and submit under the same account when required

## Common traps

- assuming login is irrelevant because one endpoint works once without it
- collecting with one account and submitting with another
- treating per-account answers as signer bugs

## Delivery rule

The collector should expose the required session inputs and document whether the result is account-bound.
