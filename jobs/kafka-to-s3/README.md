## Kafka To S3
This example gather kafka messages hourly and store those to the persistent storage (Amazon S3)

```shell
$ flink run -py ./jobs/kafka-to-s3/main.py \
    -m localhost:30000 \
    --dep "file://$(pwd)/libs/flink-sql-connector-kafka-1.15.4.jar" \
    --detach
```