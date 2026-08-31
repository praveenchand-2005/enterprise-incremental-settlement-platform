#!/usr/bin/env bash
set -euo pipefail

docker compose -f docker-compose.real-hudi.yml build spark
docker compose -f docker-compose.real-hudi.yml run --rm spark \
  spark-submit --master local[2] \
  --jars /opt/hudi/hudi-spark-bundle.jar \
  --conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
  --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.hudi.catalog.HoodieCatalog \
  --conf spark.sql.extensions=org.apache.spark.sql.hudi.HoodieSparkSessionExtension \
  --conf spark.kryo.registrator=org.apache.spark.HoodieSparkKryoRegistrar \
  /opt/commerce/integration/hudi_real_validation.py
