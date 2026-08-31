# Architecture

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

The defining characteristic is change-driven processing: stages consume and emit changes rather than repeatedly recomputing the full historical dataset.

The architecture is independently inspired by the publicly documented Uber/Hudi engineering problem and contains no proprietary source code or data.
