# Enterprise Incremental Settlement Platform

A change-driven Spark + Apache Hudi lakehouse architecture for mutable trip/order settlement, late-arriving events, custom record merging, checkpointed processing, data quality, and incremental computation.

## Client problem

A high-volume transaction platform receives refunds, tips, disputes, and adjustments long after the original transaction. Historical-window recomputation is expensive and can still miss events older than the configured lookback.

## Solution

**Hudi commit → incremental latest_state → affected entities → custom merge → typed Trip/Order state → rule engine → final Hudi state.**

## Core implementation

- Typed trip/order domain model
- Deterministic nested-state merge contract
- Idempotent event identity
- Composable settlement rules
- Durable publish-then-checkpoint semantics
- Hudi `latest_state` incremental reader boundary
- Hudi `CUSTOM` merge configuration and `HoodieRecordMerger` adapter
- Spark/Hudi Docker runtime
- GitHub Actions deterministic and real-runtime workflows
- Adversarial late-event benchmark
- Freelance case study and architecture documentation

## Validation

The local release contains **24+ deterministic tests** covering late updates, duplicate delivery, merge idempotence/associativity, data quality, replay, and checkpoint semantics.

The distributed Spark/Hudi benchmark is intentionally **not claimed as executed** unless it runs in a Docker/Maven-capable environment.

## Architecture

```text
Operational sources / CDC / events
              |
              v
        Apache Hudi state
              |
       incremental latest_state
              |
              v
       affected entities
              |
       custom merge boundary
              |
              v
      typed Trip / Order state
              |
              v
        settlement rules
              |
              v
      final Hudi settlement
              |
          BI / SQL / API
```

See `docs/architecture.md`, `portfolio/bid-case-study.md`, and `integration/` for the runtime acceptance path.

## Real runtime

```bash
docker compose -f docker-compose.real-hudi.yml build spark
bash integration/run-real-hudi.sh
```

## Reference

The architecture is independently inspired by the publicly documented Uber/Hudi incremental collection problem; it contains no proprietary Uber source code or data. Reference-company production metrics are not presented as this project's results.
