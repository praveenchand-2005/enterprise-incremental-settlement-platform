import argparse
import shutil
from pathlib import Path
from pyspark.sql import SparkSession

def spark_session():
    return (SparkSession.builder.appName("enterprise-commerce-hudi-validation")
            .master("local[2]")
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.hudi.catalog.HoodieCatalog")
            .config("spark.sql.extensions", "org.apache.spark.sql.hudi.HoodieSparkSessionExtension")
            .config("spark.kryo.registrator", "org.apache.spark.HoodieSparkKryoRegistrar")
            .getOrCreate())

def run(base_path):
    spark = spark_session()
    base = Path(base_path)
    if base.exists(): shutil.rmtree(base)
    base.mkdir(parents=True)
    options = {
        "hoodie.table.name": "trip_intermediate",
        "hoodie.datasource.write.recordkey.field": "entity_id",
        "hoodie.datasource.write.precombine.field": "event_version",
        "hoodie.datasource.write.operation": "upsert",
        "hoodie.record.merge.mode": "EVENT_TIME_ORDERING",
        "hoodie.table.ordering.fields": "event_version",
    }
    initial = spark.createDataFrame([
        ("trip-1", "trip_completed", "100", 1),
        ("trip-2", "trip_completed", "50", 1)],
        ["entity_id", "event_type", "amount", "event_version"])
    initial.write.format("hudi").options(**options).mode("append").save(str(base))
    first_commit = (spark.read.format("hudi").load(str(base))
                    .select("_hoodie_commit_time").distinct().orderBy("_hoodie_commit_time").collect()[-1][0])
    update = spark.createDataFrame([("trip-1", "refund", "-25", 2)],
                                   ["entity_id", "event_type", "amount", "event_version"])
    update.write.format("hudi").options(**options).mode("append").save(str(base))
    second_commit = (spark.read.format("hudi").load(str(base))
                     .select("_hoodie_commit_time").distinct().orderBy("_hoodie_commit_time").collect()[-1][0])
    incremental = (spark.read.format("hudi")
                   .option("hoodie.datasource.query.type", "incremental")
                   .option("hoodie.datasource.query.incremental.format", "latest_state")
                   .option("hoodie.datasource.read.begin.instanttime", first_commit)
                   .option("hoodie.datasource.read.end.instanttime", second_commit)
                   .load(str(base)))
    print(f"FIRST_COMMIT={first_commit}")
    print(f"SECOND_COMMIT={second_commit}")
    incremental.select("entity_id", "event_type", "amount", "event_version").show(truncate=False)
    assert incremental.filter("entity_id = 'trip-1'").count() == 1
    spark.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="/tmp/enterprise-hudi-validation")
    run(parser.parse_args().path)
