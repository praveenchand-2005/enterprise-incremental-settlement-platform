package com.example.commerce.hudi;

import java.io.IOException;
import org.apache.avro.Schema;
import org.apache.hudi.common.config.TypedProperties;
import org.apache.hudi.common.engine.RecordContext;
import org.apache.hudi.common.model.HoodieRecord.HoodieRecordType;
import org.apache.hudi.common.model.HoodieRecordMerger;
import org.apache.hudi.common.table.read.BufferedRecord;

/**
 * Hudi 1.1.1 custom merger adapter.
 *
 * The domain merge contract lives in the Python reference implementation.
 * This adapter is deliberately minimal until the Spark engine-specific
 * RecordContext serialization contract is wired to the domain representation.
 */
public final class TripCollectionMerger implements HoodieRecordMerger {
    public static final String STRATEGY_ID = "2b3d0e4c-6d75-4c6e-8f2a-7f3a4d6e9c11";

    @Override
    public <T> BufferedRecord<T> merge(
            BufferedRecord<T> older,
            BufferedRecord<T> newer,
            RecordContext<T> context,
            TypedProperties props) throws IOException {
        return newer;
    }

    @Override
    public <T> BufferedRecord<T> partialMerge(
            BufferedRecord<T> older,
            BufferedRecord<T> newer,
            Schema readerSchema,
            RecordContext<T> context,
            TypedProperties props) throws IOException {
        return newer;
    }

    @Override
    public HoodieRecordType getRecordType() {
        return HoodieRecordType.SPARK;
    }

    @Override
    public String getMergingStrategy() {
        return STRATEGY_ID;
    }
}
