## Kafka Datagen
This example generates data using `datagen` connector and insert to the Kafka.

```shell
$ flink run -py ./jobs/kafka-datagen/main.py \
    -m localhost:30000 \
    --dep "file://$(pwd)/libs/flink-sql-connector-kafka-1.15.4.jar;file://$(pwd)/libs/flink-json-1.15.4.jar" \
    --detach
```