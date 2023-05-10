"""
Streaming Kafka To S3 sink 
"""
import os
import sys
import argparse

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(stream_execution_environment=env)

parser = argparse.ArgumentParser()
parser.add_argument(
    '--dep',
    dest='dep',
    required=True)

argv = sys.argv[1:]
known_args, _ = parser.parse_known_args(argv)
t_env.get_config().set("pipeline.jars", known_args.dep)

t_env.get_config().get_configuration().set_string(
    "execution.checkpointing.mode", "EXACTLY_ONCE"
)
t_env.get_config().get_configuration().set_string(
    "execution.checkpointing.interval", "1min"
)

def create_source_table(table_name, broker):
    return """ CREATE TABLE {0} (
        transaction_id INT,
        from_account_id INT,
        to_account_id INT,
        amount INT,
        created_at TIMESTAMP_LTZ
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'bank_transfers',
        'properties.group.id' = 'test_group',
        'properties.bootstrap.servers' = '{1}',
        'scan.startup.mode' = 'earliest-offset',
        'format' = 'json'
    )""".format(table_name, broker)

def create_sink_table(table_name, bucket_name):
    return """ CREATE TABLE {0} (
        transaction_id INT,
        from_account_id INT,
        to_account_id INT,
        amount INT,
        created_at TIMESTAMP_LTZ
    ) WITH (
        'connector' = 'filesystem',
        'path' = 's3://{1}/',
        'format' = 'json',
        'sink.partition-commit.policy.kind' = 'success-file',
        'sink.partition-commit.delay' = '1 min'
    )""".format(table_name, bucket_name)
    

def main():
    source = create_source_table("kafka_source", "play-kafka-headless:9092")
    sink = create_sink_table("sink_s3", "test")

    t_env.execute_sql(source)
    t_env.execute_sql(sink)

    t_env.execute_sql("INSERT INTO {0} SELECT * FROM {1}"
                        .format("sink_s3", "kafka_source"))

if __name__ == "__main__":
    main()