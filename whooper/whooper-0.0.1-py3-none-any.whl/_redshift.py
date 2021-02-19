# standard library imports
import os
from typing import Dict, Union

# third party imports
import pg8000


def redshift_get_conn(env_var: str) -> pg8000.Connection:
    """Creates a Redshift connection object

    Parameters
    ----------
    env_var : str
        name of the environment variable containing the credentials str
        creds_str should have the below format where the user has inserted their values:
        'host=my_hostname database=my_database user=my_user password=my_password port=1234'

    Returns
    -------
    database connection object

    Example use
    -----------
    conn = redshift_get_conn(env_var='REDSHIFT_CREDS')
    """
    _env_var_validator(env_var=env_var)
    cred_str = os.environ[env_var]
    creds_dict = _create_creds_dict(cred_str)
    conn = pg8000.dbapi.connect(ssl_context=True, **creds_dict)
    return conn


def read_sql(sql_filename: str) -> str:
    """Ingests a SQL file and returns a str containing the contents of the file

    Parameters
    ----------
    sql_filename : str
        path to and name of SQL file to be ingested

    Returns
    -------
    str
        contents of the SQL file ingested

    Example use
    -----------
    sql = read_sql(sql_filename='../sql/my_script.sql')
    """
    if not isinstance(sql_filename, str):
        raise TypeError("sql_filename must be of str type")
    with open(sql_filename, "r") as f:
        sql_str = " ".join(f.readlines())
    return sql_str


def redshift_execute_sql(
    sql: str,
    env_var: str,
    return_data: bool = False,
    return_dict: bool = False,
):
    """Ingests a SQL query as a string and executes it (potentially returning data)

    Parameters
    ----------
    sql : str
        SQL query to be executed
    env_var : str
        name of the environment variable containing the credentials str
        creds_str should have the below format where the user has inserted their values:
        'host=my_hostname database=my_database user=my_user password=my_password port=1234'
    return_data : bool
        whether or not the query should return data
    return_dict : bool
        whether or not to return data as a dict (for easy ingestion into pandas)

    Returns
    -------
    None or list of str and list of tuples or dict
        if not return_data then None
        if return_data and not return_dict then list of str (column names) and list of tuples (data)
        if return_data and return_dict then dict with keys 'columns' and 'data' with values from above

    Example use
    -----------
    # Statement that does not return data (creating/dropping tables or copying/unloading data, etc)
    redshift_execute_sql(
        sql=sql,
        env_var='REDSHIFT_CREDS',
        return_data=False,
        return_dict=False)

    # Return data as a list of tuples and the columns as a list of str
    data, columns = redshift_execute_sql(
        sql=sql,
        env_var='REDSHIFT_CREDS',
        return_data=True,
        return_dict=False)

    # Return data for direct ingestion into pandas
    import pandas as pd
    df = pd.DataFrame(**redshift_execute_sql(
        sql=sql,
        env_var='REDSHIFT_CREDS',
        return_data=True,
        return_dict=True))
    """
    _redshift_execute_sql_arg_validator(
        sql=sql, env_var=env_var, return_data=return_data, return_dict=return_dict
    )
    with redshift_get_conn(env_var=env_var) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        if return_data:
            columns = [desc[0] for desc in cursor.description]
            data = [row for row in cursor]
            conn.commit()
            if return_dict:
                return {"data": data, "columns": columns}
            else:
                return data, columns
        else:
            conn.commit()
            return


def _create_creds_dict(creds_str: str) -> Dict[str, Union[str, int]]:
    """Takes the credentials str and converts it to a dict

    Parameters
    ----------
    creds_str : str
        credentials string with the below format where the user has inserted their values:
        'host=my_hostname database=my_database user=my_user password=my_password port=1234'

    Returns
    -------
    dict
        credentials in dict form
    """
    creds_dict = {}
    for param in creds_str.split(" "):
        split_param = param.split("=")
        if split_param[0] == "port":
            split_param[1] = int(split_param[1])
        creds_dict[split_param[0]] = split_param[1]
    return creds_dict


def _env_var_validator(env_var: str) -> None:
    """Validates that the user is providing the an environment variable name, rather than the credentials string

    Parameters
    ----------
    env_var : str
        the name of the environment variable referencing the Redshift credential string

    Returns
    -------
    None
    """
    creds_str_keys = ["host", "database", "user", "password", "port"]
    if all(key in env_var for key in creds_str_keys):
        raise ValueError(
            "This field should contain the name of an env variable, not the credentials string."
        )
    elif env_var not in os.environ:
        raise KeyError("Redshift credentials env variable not found.")
    return


def _redshift_execute_sql_arg_validator(
    sql: str,
    env_var: str,
    return_data: bool,
    return_dict: bool,
) -> None:
    """Validates the redshift_execute_sql arguments and raises clear errors

    Parameters
    ----------
    sql : str
        SQL query to be executed
    env_var : str
        name of the environment variable containing the credentials str
    return_data : bool
        whether or not the query should return data
    return_dict : bool
        whether or not to return data as a dict (for easy ingestion into pandas)

    Returns
    -------
    None
    """
    for arg in [sql, env_var]:
        if not isinstance(arg, str):
            raise TypeError("sql and env_var must be of str type")
    for arg in [return_data, return_dict]:
        if not isinstance(arg, bool):
            raise TypeError("return_data and return_dict must be of bool type")
    return
