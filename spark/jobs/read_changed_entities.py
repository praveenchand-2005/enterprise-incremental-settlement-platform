def incremental_options(begin_commit, end_commit=None):
    opts = {
        "hoodie.datasource.query.type": "incremental",
        "hoodie.datasource.query.incremental.format": "latest_state",
        "hoodie.datasource.read.begin.instanttime": begin_commit,
    }
    if end_commit is not None:
        opts["hoodie.datasource.read.end.instanttime"] = end_commit
    return opts

def read_changed_entities(spark, table_path, begin_commit, end_commit=None):
    return (spark.read.format("hudi")
            .options(**incremental_options(begin_commit, end_commit))
            .load(table_path)
            .select("entity_id").distinct())
