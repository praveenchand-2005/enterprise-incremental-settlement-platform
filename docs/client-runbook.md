# Client Runbook — Incremental Settlement

## Normal run
1. Read the durable Hudi checkpoint.
2. Incrementally read `latest_state` from the last checkpoint to the current completion instant.
3. Extract affected `entity_id` values.
4. Reconstruct/merge only affected trip/order state.
5. Execute the typed collection rule engine.
6. Upsert final settlement state.
7. Persist the new checkpoint only after successful publication.
8. Emit metrics.

## Late event
A late refund/tip/dispute enters as a new Hudi commit, appears in the incremental query, marks its entity as affected, and causes that entity's state to be re-evaluated.

## Failure
If final publication fails, do not advance the checkpoint. Replay the same commit range and rely on event identity/idempotent merge.

## Correctness invariant
Replaying the same source events in any arrival order produces the same final settlement state.
