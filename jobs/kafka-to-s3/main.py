"""
Streaming Kafka To S3 sink 
"""
import logging
import os
import sys
import argparse

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment
from pyflink.table.window import Tumble

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

def create_source_table(table_name, topic, broker):
    return """ CREATE TABLE {0} (
        transaction_id INT,
        from_account_id INT,
        to_account_id INT,
        amount INT,
        created_at TIMESTAMP(0),
        WATERMARK FOR created_at AS created_at - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = '{1}',
        'properties.group.id' = 'test_group_id',
        'properties.bootstrap.servers' = '{2}',
        'scan.startup.mode' = 'earliest-offset',
        'format' = 'json'
    )""".format(table_name, topic, broker)

def create_sink_table(table_name, bucket_name):
    return """ CREATE TABLE {0} (
        transaction_id INT,
        from_account_id INT,
        to_account_id INT,
        amount INT,
        created_at TIMESTAMP(0),
        dt STRING,
        `hour` STRING,
        `minute` STRING
    ) PARTITIONED BY (dt, `hour`)
    WITH (
        'connector' = 'filesystem',
        'path' = 's3://{1}/',
        'format' = 'json',
        'sink.partition-commit.policy.kind' = 'success-file',
        'sink.partition-commit.delay' = '5 min'
    )""".format(table_name, bucket_name)
    

def main():
    input_table_name = "kafka_input"
    output_table_name = "s3_output"
    bucket_name = "analyticlogs"
    kafka_brokers = "play-kafka-headless:9092"
    kafka_topic = "test_topic"

    source = create_source_table(input_table_name, kafka_topic, kafka_brokers)
    sink = create_sink_table(output_table_name, bucket_name)

    # 1. Create tables
    t_env.execute_sql(source)
    t_env.execute_sql(sink)

    # 2. Set windows
    t_env.execute_sql("""
        INSERT INTO {0} 
        SELECT 
            transaction_id,
            from_account_id,
            to_account_id,
            amount,
            created_at,
            DATE_FORMAT(created_at, 'yyyy-MM-dd'),
            DATE_FORMAT(created_at, 'HH')
        FROM {1}
    """.format(output_table_name, input_table_name))

if __name__ == "__main__":
    main()