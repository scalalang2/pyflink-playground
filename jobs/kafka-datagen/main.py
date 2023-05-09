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
        transaction_id INT,
        from_account_id INT,
        to_account_id INT,
        amount INT,
        created_at TIMESTAMP_LTZ
    ) WITH (
        'connector' = 'datagen',
        'rows-per-second' = '10',
        'fields.amount.min' = '1',
        'fields.amount.max' = '1000',
        'fields.from_account_id.min' = '1',
        'fields.from_account_id.max' = '100000',
        'fields.to_account_id.min' = '1',
        'fields.to_account_id.max' = '100000',
        'fields.created_at.max-past' = '1000'
    )
""")

# define sink table with kafka connector
t_env.execute_sql("""
    CREATE TABLE bank_transfers_sink(
        transaction_id INT,
        from_account_id INT,
        to_account_id INT,
        amount INT,
        created_at TIMESTAMP_LTZ
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'bank_transfers',
        'properties.bootstrap.servers' = 'play-kafka-headless:9092',
        'format' = 'json'
    )
""")

t_env.sql_query("SELECT * FROM bank_transfers") \
        .execute_insert("bank_transfers_sink").wait()