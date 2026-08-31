# Freelance Data Engineering Case Study

## Challenge
A transaction/settlement pipeline receives late updates to historical transactions. A fixed historical lookback creates unnecessary reads and can miss events older than the configured window.

## Solution
I designed an incremental Spark + Apache Hudi lakehouse pipeline that consolidates mutable trip/order state, merges updates by deterministic event identity, and evaluates settlement through independently testable rules.

## Engineering decisions
1. Hudi incremental latest-state reads.
2. Record-key based mutable state instead of repeated historical self-joins.
3. Custom merge boundary for nested state.
4. Typed settlement rules.
5. Idempotent source event IDs.
6. Publish-then-checkpoint semantics.
7. Automated correctness tests for late data, duplicates, replay, and merge algebra.

## Client value
Processing follows changed entities rather than repeatedly materializing an entire historical window, while preserving correctness for old transactions receiving new updates.

## Evidence
The repository contains the source implementation, tests, Docker/Spark/Hudi runtime, CI workflow, benchmark methodology, runbook, and architecture documentation.

## Honesty
Local correctness results and reference-company production metrics are kept separate. Only measured runtime results should be reported as project performance.
