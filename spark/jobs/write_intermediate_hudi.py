MERGER_CLASS = "com.example.commerce.hudi.TripCollectionMerger"
MERGE_STRATEGY_ID = "2b3d0e4c-6d75-4c6e-8f2a-7f3a4d6e9c11"

def hudi_options():
    return {
        "hoodie.table.name": "trip_intermediate",
        "hoodie.datasource.write.recordkey.field": "entity_id",
        "hoodie.datasource.write.partitionpath.field": "event_date",
        "hoodie.table.ordering.fields": "event_version",
        "hoodie.record.merge.mode": "CUSTOM",
        "hoodie.record.merge.strategy.id": MERGE_STRATEGY_ID,
        "hoodie.write.record.merge.custom.implementation.classes": MERGER_CLASS,
        "hoodie.datasource.write.operation": "upsert",
    }
