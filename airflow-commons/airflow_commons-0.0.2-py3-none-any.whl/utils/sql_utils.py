from google.cloud import bigquery

from airflow_commons.utils.bigquery_utils import query_information_schema

COMMA = ", "
EQUALS_SIGN = "="
DESCENDING = "DESC"
AND = "AND"
WHITE_SPACE = " "
SOURCE_PREFIX = "S."
TARGET_PREFIX = "T."


def get_column_list_and_update_statements(
    client: bigquery.Client, project_id: str, dataset_id: str, table_id: str
):
    """
    Gets column list from information schema and prepares column list and update statements for further queries

    :param client: Client needed for API request
    :param project_id: Bigquery project id
    :param dataset_id: dataset id
    :param table_id: table id
    :return: columns, update_statements strings
    """
    columns_list = query_information_schema(
        client=client,
        requested_column_name="column_name",
        project_id=project_id,
        dataset_id=dataset_id,
        table_name=table_id,
    )
    columns = COMMA.join(columns_list)
    update_statements = COMMA.join(
        [i + EQUALS_SIGN + SOURCE_PREFIX + i for i in columns_list]
    )
    return columns, update_statements


def get_primary_key_statements(primary_keys):
    """
    Gets group by clause and merge keys based on given primary key list, for further usage on queries

    :param primary_keys: list of primary key columns
    :return: sql group by and merge keys
    """
    group_by_clause = COMMA.join(primary_keys)
    merge_keys = (AND + WHITE_SPACE).join(
        [
            TARGET_PREFIX + i + EQUALS_SIGN + SOURCE_PREFIX + i + WHITE_SPACE
            for i in primary_keys
        ]
    )
    return group_by_clause, merge_keys


def get_order_by_statement(time_columns):
    """
    Gets order by statement based on given datetime columns, for further usage on queries

    :param time_columns: list of datetime columns
    :return: sql order by values, ordering rows descending by given columns
    """
    return COMMA.join([i + WHITE_SPACE + DESCENDING for i in time_columns])
