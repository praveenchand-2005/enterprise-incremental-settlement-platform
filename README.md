# Enterprise Incremental Settlement Platform

A change-driven Spark + Apache Hudi lakehouse architecture for mutable trip/order settlement, late-arriving events, custom record merging, checkpointed processing, data quality, and incremental computation.

## Client problem

A high-volume transaction platform receives refunds, tips, disputes, and adjustments long after the original transaction. Historical-window recomputation is expensive and can still miss events older than the configured lookback.

## Solution

**Hudi commit → incremental latest_state → affected entities → custom merge → typed Trip/Order state → rule engine → final Hudi state.**

The project includes deterministic correctness tests, an adversarial late-event case, Spark/Hudi Docker runtime definitions, CI integration, benchmarks, runbooks, and a freelance case study.

## Validation

The deterministic suite contains 24+ tests covering late updates, duplicate delivery, merge idempotence/associativity, data quality, replay, and checkpoint semantics.

The distributed Spark/Hudi benchmark is intentionally not claimed as executed unless it runs in a Docker/Maven-capable environment.

## Reference

The architecture is independently inspired by the publicly documented Uber/Hudi incremental collection problem; it contains no proprietary Uber source code or data.
