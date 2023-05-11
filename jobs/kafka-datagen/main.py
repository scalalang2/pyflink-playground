import sys
import argparse

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

parser = argparse.ArgumentParser()
parser.add_argument(
    '--dep',
    dest='dep',
    required=True)

parser.add_argument(
    '--topic',
    dest='topic',
    default='test_topic')

argv = sys.argv[1:]
known_args, _ = parser.parse_known_args(argv)

env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(stream_execution_environment=env)

t_env.get_config().set('pipeline.jars', known_args.dep)
t_env.get_config().set('pipeline.classpaths', known_args.dep)

def source_table(table_name):
    return """
        CREATE TABLE {0} (
            transaction_id INT,
            from_account_id INT,
            to_account_id INT,
            amount INT,
            created_at TIMESTAMP_LTZ(0)
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
    """.format(table_name)

def sink_table(table_name, brokers, topic):
    return """
        CREATE TABLE {0} (
            transaction_id INT,
            from_account_id INT,
            to_account_id INT,
            amount INT,
            created_at TIMESTAMP_LTZ(0)
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = '{1}',
            'topic' = '{2}',
            'format' = 'json'
        )
    """.format(table_name, brokers, topic)


def main():
    topic = known_args.topic
    input_table_name = "bank_transfer_datagen"
    output_table_name = "bank_transfer_sink"
    brokers = "play-kafka-headless:9092"

    source_ddl = source_table(input_table_name)
    sink_ddl = sink_table(output_table_name, brokers, topic)

    t_env.execute_sql(source_ddl)
    t_env.execute_sql(sink_ddl)

    t_env.sql_query("SELECT * FROM {0}".format(input_table_name)) \
        .execute_insert(output_table_name).wait()

if __name__ == '__main__':
    main()