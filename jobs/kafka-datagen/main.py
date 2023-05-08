import sys
import argparse

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

parser = argparse.ArgumentParser()
parser.add_argument(
    '--dep',
    dest='dep',
    required=True)

argv = sys.argv[1:]
known_args, _ = parser.parse_known_args(argv)

env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(stream_execution_environment=env)

t_env.get_config().set('pipeline.jars', known_args.dep)
t_env.get_config().set('pipeline.classpaths', known_args.dep)

# define source table with datagen
t_env.execute_sql("""
    CREATE TABLE bank_transfers(
        transaction_id BIGINT,
        from_account_id BIGINT,
        to_account_id BIGINT,
        amount DECIMAL(32, 2)
    ) WITH (
        'connector' = 'datagen'
    )
""")

# define sink table with kafka connector
t_env.execute_sql("""
    CREATE TABLE bank_transfers_sink(
        transaction_id BIGINT,
        from_account_id BIGINT,
        to_account_id BIGINT,
        amount DECIMAL(32, 2)
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'bank_transfers',
        'properties.bootstrap.servers' = 'play-kafka-headless:9092',
        'format' = 'json'
    )
""")

t_env.sql_query("SELECT * FROM bank_transfers") \
        .execute_insert("bank_transfers_sink").wait()