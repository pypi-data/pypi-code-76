import sqlite3


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


def execute_query(conn, query, commit=1):
    cur = conn.cursor()
    cur.execute(query)
    if(commit):
        conn.commit()


def execute_query_for_results(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    # for row in rows:
    #    print(row)
    return rows


def truncate_table(conn, table_name):
    query = "DELETE FROM {}".format(table_name)
    execute_query(conn, query, 1)


def escape_field(str):
    str = str.replace("'", "''")
    return str


def check_if_table_exists(conn, table_name):
    query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}';".format(table_name)
    cur = conn.cursor()
    cur.execute(query)

    if cur.fetchone()[0] == 1 :
        return True
    else:
        return False
