from pathlib import Path
from datetime import datetime
from data_engineering_extract_metadata.utils import write_json, prepare_folder


def get_table_list(
    connection,
    save_folder,
    title,
    schema,
    filter_function=None,
):
    """Extract, filter and save of a list of tables.

    Parameters
    ----------
    connection (cx_Oracle connection):
        A premade connection to a database

    save_folder (str):
        Folder to save the table list into - probably the database name

    title (str):
        What to call this metadata - will become the file name of the table list

    schema (str):
        Name of the database schema to get tables from

    filter_function (function or None):
        If you want to filter the list of tables after extracting it, pass a function
        here. The function should take a single argument: a list of tuples in the form
        (table name, tablespace). It should return a list of table names (not tuples).
    """
    # Get list of tables, with tablespaces
    table_list = get_names_and_spaces(schema, connection, True)

    # Filter if needed - otherwise just get the table names out of the tuples
    if filter_function:
        filtered = filter_function(table_list)
    else:
        filtered = [table[0] for table in table_list]

    # Identify blob columns in those tables
    blobs = find_blob_columns(filtered, schema, connection)

    # Save the list
    save_tables(title, save_folder, filtered, blobs)


def get_names_and_spaces(database: str, connection, include_tablespace=False) -> list:
    """Gets names of tables in the database

    You can save the output into a file, or pass it directly to create_table_json

    Parameters
    ----------
    database (str):
        The name of the database/schema - for example DELIUS_ANALYTICS_PLATFORM

    connection (database connection object):
        The database connection to query - for example a cx_Oracle.connect() object

    include_tablespace (bool):
        If False, return list of table names.
        If true, return list of tuples of table name and tablespace

    Returns
    -------
    List of table names as strings.
    If including tablespaces, returns list of tuples of table names and tablespaces
    """
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT table_name, tablespace_name FROM all_tables WHERE OWNER = '{database}'"
    )
    result = cursor.fetchall()
    cursor.close()

    if include_tablespace:
        return [(r[0], r[1]) for r in result]
    else:
        return [r[0] for r in result]


def find_blob_columns(tables: list, database: str, connection) -> list:
    """Return a list of blob columns that in a specified schema and list of tables.

    Parameters
    ----------
    tables (list):
        List of tables to search for blobs.

    database (str):
        The name of the database/schema - for example DELIUS_ANALYTICS_PLATFORM.

    connection (database connection object):
        The database connection to query - for example a cx_Oracle.connect() object.
    """
    # Format the table list to put it in the SQL query
    tables_string = ", ".join([f"'{t}'" for t in tables])

    cursor = connection.cursor()
    cursor.execute(
        f"SELECT table_name, column_name "
        f"FROM all_tab_columns "
        f"WHERE owner = '{database}' "
        f"AND table_name IN ({tables_string}) "
        f"AND data_type = 'BLOB' "
        f"ORDER BY table_name, column_name"
    )
    blobs = cursor.fetchall()
    cursor.close()

    return blobs


def save_tables(title: str, folder: str, tables: list, blobs: list = []):
    """Saves the tables to json with a timestamp.

    Parameters
    ----------

    title (str):
        Name for the table list - used in the json and for the filename

    folder (str):
        Subfolder to save the json to

    tables (list[str]):
        List of table names
    """
    prepare_folder(folder, clear_content=False)

    output = {
        "tables_from": title,
        "extraction_date": datetime.now().isoformat(),
        "tables": sorted(tables),
        "blobs": blobs,
    }
    write_json(output, Path(folder) / f"{title.lower()}.json")
    print(f"Saved list of {len(output['tables'])} tables")
