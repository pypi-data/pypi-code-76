from pathlib import Path
from data_engineering_extract_metadata.table_list import get_table_list
from data_engineering_extract_metadata.utils import (
    write_json,
    read_json,
    prepare_folder,
)


def create_all_metadata(
    connection,
    save_folder,
    title,
    description,
    schema,
    source_bucket,
    source_folder,
    include_op_column=True,
    include_timestamp_column=True,
    include_scn_column=True,
    include_derived_columns=True,
    include_objects=False,
    filter_function=None,
):
    """Perform the whole process: get table list, filter it and create metadata folder

    Just runs get_table_list and create_metadata_folder - no extra processing

    Parameters
    ----------
    connection (cx_Oracle connection):
        A premade connection to a database.

    save_folder (str or Path):
        Location for the table list and metadata subfolder.

    title (str):
        Title for the table list file and metadata subfolder.

    description (str):
        How to describe the database in the Glue catalogue.

    schema (str):
        Name of the database schema to get tables from.

    source_bucket (str):
        The name of the S3 bucket the source data will be stored in.

    source_folder (str):
        Folder/prefix within the S3 bucket for the relevant source data.

    filter_function (function or None):
        If you want to filter the list of tables after extracting it, pass a function
        here. The function should take a single argument: a list of tuples in the form
        (table name, tablespace). It should return a list of table names (not tuples).

    include_op_column (boolean):
        If True, adds a column called 'Op' for operation type - I, U or D
        This data is automatically added by AWS DMS ongoing replication tasks.

    include_timestamp_column (string):
        If True, adds a column called 'extraction_timestamp'.
        This data is added by DMS if the source extra connection attribute is set.

    include_scn_column (boolean):
        If True, adds a column called 'scn'.
        This data is added by DMS after being extracted from the source Oracle table.

    include_derived_columns (boolean):
        If True, adds three columns: mojap_current_record, mojap_start_datetime,
        mojap_end_datetime.

    include_objects (boolean):
        If True, will include metadata for DB_TYPE_OBJECT columns as array<character>.
        Leave False to ignore these columns - AWS DMS doesn't extract them.
    """
    get_table_list(connection, save_folder, title, schema, filter_function)
    create_metadata_folder(
        connection,
        save_folder,
        title,
        description,
        schema,
        source_bucket,
        source_folder,
        include_op_column,
        include_timestamp_column,
        include_scn_column,
        include_derived_columns,
        include_objects,
    )


def create_metadata_folder(
    connection,
    save_folder,
    title,
    description,
    schema,
    source_bucket,
    source_folder,
    include_op_column=True,
    include_timestamp_column=True,
    include_scn_column=True,
    include_derived_columns=False,
    include_objects=False,
):
    """
    Creates a folder of metadata readable by etl_manager's read_database_folder.

    You must already have prepared a list of tables using get_table_list.

    Parameters
    ----------
    connection (cx_Oracle connection):
        A premade connection to a database.

    save_folder (str or Path):
        Location of the table_list. Metadata will be saved into a subfolder of this.

    title (str):
        Title for this collection of metadata - files will be saved into a subfolder
        with this name. This should also be the name of the table list file.

    description (str):
        How to describe the database in the Glue catalogue.

    schema (str):
        Name of the database schema to get tables from.

    source_bucket (str):
        The name of the S3 bucket the source data will be stored in.

    source_folder (str):
        Folder/prefix within the S3 bucket for the relevant source data.

    include_op_column (boolean):
        If True, adds a column called 'Op' for operation type - I, U or D
        This data is automatically added by AWS DMS ongoing replication tasks.

    include_timestamp_column (string):
        If True, adds a column called 'extraction_timestamp'.
        This data is added by DMS if the source extra connection attribute is set.

    include_scn_column (boolean):
        If True, adds a column called 'scn'.
        This data is added by DMS after being extracted from the source Oracle table.

    include_derived_columns (boolean):
        If True, adds three columns: mojap_current_record, mojap_start_datetime,
        mojap_end_datetime.

    include_objects (boolean):
        If True, will include metadata for DB_TYPE_OBJECT columns as array<character>.
        Leave False to ignore these columns - AWS DMS doesn't extract them.
    """
    # Create destination folder if it doesn't already exist
    destination = Path(save_folder) / title

    # Create database.json file
    create_json_for_database(
        description=description,
        name=title,
        bucket=source_bucket,
        base_folder=source_folder,
        location=destination,
    )

    # Get pre-saved table list
    tables = read_json(title, save_folder)
    table_list = tables["tables"]

    # Connect to database and get the table metadata
    create_json_for_tables(
        tables=table_list,
        schema=schema,
        location=destination,
        include_op_column=include_op_column,
        include_timestamp_column=include_timestamp_column,
        include_scn_column=include_scn_column,
        include_derived_columns=include_derived_columns,
        include_objects=include_objects,
        connection=connection,
    )


def create_json_for_database(
    description: str,
    name: str,
    bucket: str,
    base_folder: str,
    location="./meta_data",
):
    """Creates a database.json file suitable for reading with read_database_folder()

    Parameters
    ----------
    description (str):
        Text saying where the data comes from.

    name (str):
        What you want the database to be called in Glue and Athena. Use underscores.

    bucket (str):
        The S3 bucket where the actual data will end up.

    base_folder (str):
        The folder/prefix within the S3 bucket for the data you want
        Use capitals if the S3 location includes capitals
        Don't go down to the table level - it should be the level above
        For example "hmpps/delius/DELIUS_ANALYTICS_PLATFORM".

    location (str):
        Folder where you'd like to create the json metadata.

    Returns
    -------
    None, but creates a json file in the specified location.
    """
    prepare_folder(location)

    db = {
        "description": description,
        "name": name,
        "bucket": bucket,
        "base_folder": base_folder,
    }
    write_json(db, Path(location) / "database.json")


def create_json_for_tables(
    tables: list,
    schema: str,
    location="./meta_data",
    include_op_column=True,
    include_timestamp_column=True,
    include_scn_column=True,
    include_derived_columns=False,
    include_objects=False,
    connection=None,
):
    """
    Creates a json file of metadata for each table that's named in tables and has rows
    These json files are suitable for reading with read_database_folder().

    Parameters
    ----------
    tables (list):
        A list of table names from the source database.

    schema (str):
        The name of the Oracle schema to get metadata from.

    location (string):
        Folder where you want to save the metadata.

    include_op_column (boolean):
        If True, adds a column called 'Op' for operation type - I, U or D
        This data is automatically added by AWS DMS ongoing replication tasks.

    include_timestamp_column (string):
        If True, adds a column called 'extraction_timestamp'.
        This data is added by DMS if the source extra connection attribute is set.

    include_scn_column (boolean):
        If True, adds a column called 'scn'.
        This data is added by DMS after being extracted from the source Oracle table.

    include_derived_columns (boolean):
        If True, adds three columns: mojap_current_record, mojap_start_datetime,
        mojap_end_datetime.

    include_objects (boolean):
        If True, will include metadata for DB_TYPE_OBJECT columns as array<character>.
        Leave False to ignore these columns - AWS DMS doesn't extract them.

    connection (database connection object):
        The database connection to query - for example a cx_Oracle.connect() object.

    Returns
    -------
    None
        But creates a json file for each table in the database.
    """
    cursor = connection.cursor()

    # Get all the non-nullable columns
    not_nullable = find_not_nullable(cursor, schema)

    problems = {}
    for table in tables:
        try:
            # Get a row to see the columns and check the table has data
            # 'WHERE ROWNUM <= 1' is Oracle for 'LIMIT 1'
            # fetchone() to see the first row of the query executed
            cursor.execute(f"SELECT * FROM {schema}.{table} WHERE ROWNUM <= 1")
            cursor.fetchone()
            # For Delius purposes we want all tables including those without rows
            # This might not be the case for all metadata
            metadata = get_table_meta(
                cursor,
                table,
                schema,
                not_nullable.get(table.lower(), []),
                include_op_column,
                include_timestamp_column,
                include_scn_column,
                include_derived_columns,
                include_objects,
            )
            write_json(metadata, Path(location) / f"{table.lower()}.json")

        except Exception as e:
            # Likely errors are that the table has been deleted, marked
            # for deletion, or relies on an external reference you can't access
            print(f"Problem reading {table} in {schema}")
            problems[table] = e.args[0].message  # this attribute may be Oracle-only
            continue

    # Print the error messages at the end
    if problems:
        print()
        print("ERRORS RAISED")
        for p, e in problems.items():
            print(f"Error in table {p}: {e}")

    cursor.close()


def get_table_meta(
    cursor,
    table: str,
    schema: str,
    not_nullable: list,
    include_op_column: bool = True,
    include_timestamp_column: bool = True,
    include_scn_column: bool = True,
    include_derived_columns: bool = False,
    include_objects: bool = False,
) -> list:
    """
    Lists a table's columns, plus any primary key fields and partitions

    Parameters
    ----------
    cursor:
        A cursor where .execute has already been run - usually querying
        "SELECT * FROM {database}.{table} WHERE ROWNUM <= 1".
        This will give the cursor a .description attribute with column info.

    table (str):
        Name of the table.

    not_nullable (list):
        List of column names in this table that aren't nullable.

    include_op_column (boolean):
        If True, adds a column called 'Op' for operation type - I, U or D
        This data is automatically added by AWS DMS ongoing replication tasks.

    include_timestamp_column (boolean):
        If True, adds a column called 'extraction_timestamp'
        This data is added by AWS DMS, when configured as an extra connection attribute.

    include_scn_column (boolean):
        If True, adds a column called 'scn'
        This data is added by DMS after being extracted from the source Oracle table.

    include_derived_columns (boolean):
        If True, adds three columns: mojap_current_record, mojap_start_datetime,
        mojap_end_datetime.

    include_objects (boolean):
        If True, will include metadata for DB_TYPE_OBJECT columns as array<character>.
        Leave False to ignore these columns - AWS DMS doesn't extract them.

    Returns
    -------
    List of dicts
        Contains data for all the columns in the table, ready to write to json.
    """
    # This lookup is specific to Oracle data types
    # Likely to need separate dictionaries for other data sources
    # Numbers aren't covered here - they're handled further down as they're more complex
    type_lookup = {
        "DB_TYPE_DATE": "datetime",
        "DB_TYPE_TIMESTAMP": "datetime",
        "DB_TYPE_TIMESTAMP_TZ": "datetime",
        "DB_TYPE_CHAR": "character",
        "DB_TYPE_CLOB": "character",
        "DB_TYPE_VARCHAR": "character",
        "DB_TYPE_LONG": "character",
        "DB_TYPE_RAW": "binary",
        "DB_TYPE_OBJECT": "array<character>",
    }
    columns = []

    if include_op_column:
        columns.append(
            {
                "name": "op",
                "type": "character",
                "description": "Type of change, for rows added by ongoing replication.",
                "nullable": True,
                "enum": ["I", "U", "D"],
            }
        )

    if include_timestamp_column:
        columns.append(
            {
                "name": "extraction_timestamp",
                "type": "datetime",
                "description": "DMS extraction timestamp",
                "nullable": False,
            }
        )

    if include_scn_column:
        columns.append(
            {
                "name": "scn",
                "type": "character",
                "description": "Oracle system change number",
                "nullable": True,
            }
        )

    # Data types to skip. This list is specific to working with
    # Amazon Database Migration Service and an Oracle database.
    # These are the Oracle datatypes that DMS can't copy
    # Plus blob columns, which we're intentionally excluding
    skip = ["REF", "ANYDATA", "DB_TYPE_ROWID", "DB_TYPE_BFILE", "DB_TYPE_BLOB"]

    if not include_objects:
        skip.append("DB_TYPE_OBJECT")

    # Main column info - cursor.description has 7 set columns:
    # name, type, display_size, internal_size, precision, scale, null_ok
    # Usually type is just a lookup, but decimal types need scale and precision too
    # null_ok isn't accurate in Delius, so nullable uses an external dict
    for col in cursor.description:
        if col[1].name not in skip:
            if col[1].name == "DB_TYPE_NUMBER":
                if col[4] == 0 and col[5] == -127:
                    column_type = "decimal(38,10)"
                else:
                    column_type = f"decimal({col[4]},{col[5]})"
            else:
                column_type = type_lookup[col[1].name]
            columns.append(
                {
                    "name": col[0].lower(),
                    "type": column_type,
                    "description": "",
                    "nullable": bool(col[0].lower() not in not_nullable),
                }
            )

    derived_columns = [
        {
            "name": "mojap_current_record",
            "type": "boolean",
            "description": "If the record is current",
            "nullable": False,
        },
        {
            "name": "mojap_start_datetime",
            "type": "datetime",
            "description": "When the record became current",
            "nullable": False,
        },
        {
            "name": "mojap_end_datetime",
            "type": "datetime",
            "description": "When the record ceased to be current",
            "nullable": False,
        },
    ]

    if include_derived_columns:
        columns += derived_columns

    primary_keys = get_primary_keys(table=table, cursor=cursor)
    partition_keys = get_partition_keys(table=table, schema=schema, cursor=cursor)

    metadata = {
        "$schema": (
            "https://moj-analytical-services.github.io/metadata_schema/table/"
            "v1.4.0.json"
        ),
        "name": table.lower(),
        "description": "",
        "data_format": "parquet",
        "columns": columns,
        "location": f"{table}/",
        "partitions": partition_keys,
        "primary_key": primary_keys,
    }
    return metadata


def get_primary_keys(table, cursor):
    """Looks through constraints for primary keys, and checks they match colums
    Run as part of get_curated_metadata
    """
    statement = (
        "SELECT cols.column_name "
        "FROM all_constraints cons, all_cons_columns cols "
        "WHERE cons.constraint_type = 'P' "
        "AND cons.constraint_name = cols.constraint_name "
        "AND cons.owner = cols.owner "
        "AND cons.status = 'ENABLED' "
        "AND cons.table_name = :table_name "
        "ORDER BY cols.table_name, cols.position"
    )
    cursor.execute(statement, table_name=table)
    result = cursor.fetchall()
    if result == []:
        print(f"No primary key fields found for table {table.lower()}")
        primary_keys = None
    else:
        primary_keys = [item[0].lower() for item in result]
    return primary_keys


def get_partition_keys(schema: str, table: str, cursor) -> list:
    """Returns a list the partitioning key columns for the given table.

    Parameters
    ----------
    schema : str
        Also referred to as "owner" in Oracle databases.
    table : str
        The table to get partitioning keys for.
    cursor :
        A database Cursor object ready to execute queries with.
    """
    statement = (
        "SELECT * "
        "FROM SYS.all_part_key_columns "
        "WHERE OWNER = :schema "
        "AND name = :table_name"
    )
    cursor.execute(statement, [schema, table])
    result = cursor.fetchall()
    if not result:
        print(f"No partition keys found for table {table.lower()}")
        return None
    else:
        partition_keys = [item[3].lower() for item in result]
    return partition_keys


def find_not_nullable(cursor, schema):
    """Returns a dictionary of tables, each with a list of their non-nullable columns.

    Can't use table descriptions for this as the null_ok field is inaccurate in Delius.

    Parameters
    ----------
    cursor:
        A database Cursor object ready to execute queries with.

    schema (str):
        Name of the database schema you want to get data from.
        This is schema in the Oracle sense of a section of the database.
    """
    # SQL to get all primary key (P) and check (C) constraints from the selected schema
    cursor.execute(
        f"""
        SELECT
            cons.table_name,
            cols.column_name,
            cons.constraint_type,
            cons.search_condition
        FROM all_constraints cons, all_cons_columns cols
        WHERE cons.constraint_name = cols.constraint_name
        AND cons.owner = '{schema}'
        AND (cons.constraint_type = 'C' OR cons.constraint_type = 'P')
        """
    )
    constraints = cursor.fetchall()
    not_nullable = {}
    for con in constraints:
        # For 'C' constraints, only want the 'IS NOT NULL' ones
        # Can't put this check in the SQL query because can't use LIKE on LONG datatype
        if con[2] == "P" or con[3].endswith("IS NOT NULL"):
            not_nullable.setdefault(con[0].lower(), []).append(con[1].lower())
    return not_nullable
