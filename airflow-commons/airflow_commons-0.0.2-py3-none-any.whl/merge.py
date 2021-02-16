from airflow_commons.utils.bigquery_utils import *
from airflow_commons.logger import LOGGER
from airflow_commons.utils.sql_utils import (
    get_column_list_and_update_statements,
    get_primary_key_statements,
    get_order_by_statement,
)
from airflow_commons.utils.file_utils import read_sql
from airflow_commons.utils.time_utils import get_buffered_timestamp

here = os.path.abspath(os.path.dirname(__file__))

DEDUPLICATION_SQL_FILE = os.path.join(here, "sql/deduplication.sql")
GET_OLDEST_PARTITION_FIELD_SQL_FILE = os.path.join(
    here, "sql/get_oldest_partition_field.sql"
)
DEFAULT_PRIMARY_KEYS = ["id"]
DEFAULT_TIME_COLUMNS = ["last_updated_at", "processed_at"]


def get_oldest_partition_field(
    client: bigquery.Client,
    dataset_id: str,
    table_id: str,
    target_partition_field: str,
    source_partition_field: str,
    start_date: str,
    end_date: str,
):
    """
    Queries source table and returns the oldest value target table's partition column

    :param client: Client needed for API request
    :param dataset_id: dataset id of source table
    :param table_id: table id of source table
    :param target_partition_field: time partitioning column of target table
    :param source_partition_field: time partitioning column of source table
    :param start_date: query start date
    :param end_date: query end date
    :return:
    """
    sql = read_sql(
        GET_OLDEST_PARTITION_FIELD_SQL_FILE,
        dataset_id=dataset_id,
        table_id=table_id,
        target_partition_field=target_partition_field,
        source_partition_field=source_partition_field,
        start_date=start_date,
        end_date=end_date,
    )
    return single_value_select(
        client=client,
        sql=sql,
    )


def get_time_partition_field(client: bigquery.Client, dataset_id: str, table_id: str):
    """
    Makes an API call to get time partitioning of a table, then gets time partitioning column name from response

    :param client: Client needed for API request
    :param dataset_id: dataset id
    :param table_id: table id
    :return:
    """
    return get_table_time_partitioning_info(client, dataset_id, table_id).field


def get_deduplication_sql(
    client: bigquery.Client,
    sql_file: str,
    start_date: str,
    end_date: str,
    project_id: str,
    source_dataset: str,
    source_table: str,
    target_dataset: str,
    target_table: str,
    primary_keys: list,
    time_columns: list,
):
    """
    Prepares deduplication sql that will be run on deduplication process

    :param client: Client needed for API request
    :param sql_file: relative location of sql file
    :param start_date: deduplication time interval start
    :param end_date: deduplication time interval end
    :param project_id: Bigquery project id
    :param source_dataset: source dataset id
    :param source_table: source table id
    :param target_dataset: target dataset id
    :param target_table: target table id
    :param primary_keys: primary key column list
    :param time_columns: time columns list to order rows
    :return: deduplication query or None
    """
    buffered_start_date = get_buffered_timestamp(start_date)
    source_partition_field = get_time_partition_field(
        client, source_dataset, source_table
    )
    target_partition_field = get_time_partition_field(
        client, target_dataset, target_table
    )
    oldest_target_partition = get_oldest_partition_field(
        client,
        source_dataset,
        source_table,
        target_partition_field,
        source_partition_field,
        buffered_start_date,
        end_date,
    )

    if oldest_target_partition:
        (columns, update_statements,) = get_column_list_and_update_statements(
            client, project_id, source_dataset, source_table
        )
        group_by_clause, merge_keys = get_primary_key_statements(primary_keys)
        order_by_clause = get_order_by_statement(time_columns)
        return read_sql(
            sql_file=sql_file,
            target_dataset=target_dataset,
            target_table=target_table,
            order_by_clause=order_by_clause,
            source_dataset=source_dataset,
            source_table=source_table,
            source_partition_field=source_partition_field,
            start_date=buffered_start_date,
            end_date=end_date,
            target_partition_field=target_partition_field,
            oldest_target_partition=oldest_target_partition,
            group_by_clause=group_by_clause,
            merge_keys=merge_keys,
            update_statements=update_statements,
            columns=columns,
        )
    else:
        LOGGER(
            "There is no data: - {source_dataset}.{source_table} - between [{start_date} - {end_date}] .".format(
                source_dataset=source_dataset,
                source_table=source_table,
                start_date=buffered_start_date,
                end_date=end_date,
            )
        )
        return None


def deduplicate(
    service_account_file: str,
    start_date: str,
    end_date: str,
    project_id: str,
    source_dataset: str,
    source_table: str,
    target_dataset: str,
    target_table: str,
    primary_keys=None,
    time_columns=None,
    sql_file=DEDUPLICATION_SQL_FILE,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
):
    """
    Runs a merge query to deduplicate rows in historic table, and write to target snapshot table

    :param service_account_file: relative location of service account json
    :param start_date: deduplication interval start
    :param end_date: deduplication interval end
    :param project_id: Bigquery project id
    :param source_dataset: source dataset id
    :param source_table: source table id
    :param target_dataset: target dataset id
    :param target_table: target table id
    :param primary_keys: primary key columns of the source and target tables
    :param time_columns: time columns list to order rows
    :param sql_file: relative location of unformatted sql file
    :param timeout: query timeout duration parameter
    :param location: query location parameter
    :return:
    """
    client = connect(service_account_file)
    if primary_keys is None:
        primary_keys = DEFAULT_PRIMARY_KEYS
    if time_columns is None:
        time_columns = DEFAULT_TIME_COLUMNS
    sql = get_deduplication_sql(
        client,
        sql_file,
        start_date,
        end_date,
        project_id,
        source_dataset,
        source_table,
        target_dataset,
        target_table,
        primary_keys,
        time_columns,
    )
    if sql:
        query(
            client=client,
            job_config=bigquery.QueryJobConfig(),
            sql=sql,
            timeout=timeout,
            location=location,
        )
