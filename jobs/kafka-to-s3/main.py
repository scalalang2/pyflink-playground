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

is_local = True if os.environ.get("IS_LOCAL") else False
if is_local:
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
        
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'bank_transfers',
        'properties.bootstrap.servers' = '{1}',
        'format' = 'json'
    )""".format(table_name, broker)

def create_sink_table():


def main():


if __name__ == "__main__":
    main()