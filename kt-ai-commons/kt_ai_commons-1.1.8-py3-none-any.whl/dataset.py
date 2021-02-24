import psycopg2
import pandas.io.sql as sqlio
import os
import json

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# secret_file = os.path.join(BASE_DIR, 'secrets.json')

# with open(secret_file) as f:
#     secrets = json.loads(f.read())

# def get_secret(setting, secrets=secrets):
#     return secrets[setting]


# def get_connection():
#     return psycopg2.connect(host=get_secret("ip_address"),
#                             dbname=get_secret("db_name"),
#                             user=get_secret("user"),
#                             password=get_secret("PASSWORD"),
#                             port=get_secret("port"))

def get_connection():
    return psycopg2.connect(host="211.253.10.76",
                            dbname="postgres",
                            user="readonly",
                            password="yourpassword",
                            port=5432)


def close_connection(connection):
    if not connection.closed:
        connection.close()


def _check_connection(connection):
    if not connection or connection == 1:
        raise ValueError("connection is not opened.")
    return


def query_onenavi_train(connection):
    _check_connection(connection)

    sql = """
        SELECT *
        FROM onenavi_train
        ;
        """
    return sqlio.read_sql_query(sql, connection)


def query_onenavi_evaluation(connection):
    _check_connection(connection)

    sql = """
        SELECT *
        FROM onenavi_evaluation
        ;
        """
    return sqlio.read_sql_query(sql, connection)


def query_onenavi_pnu(connection):
    _check_connection(connection)

    sql = """
        SELECT *
        FROM onenavi_pnu
        ;
        """
    return sqlio.read_sql_query(sql, connection)


def query_onenavi_signal(connection):
    _check_connection(connection)

    sql = """
        SELECT *
        FROM onenavi_signal
        ;
        """
    return sqlio.read_sql_query(sql, connection)


def query_onenavi_weather(connection):
    _check_connection(connection)

    sql = """
        SELECT *
        FROM onenavi_weather
        ;
        """
    return sqlio.read_sql_query(sql, connection)
