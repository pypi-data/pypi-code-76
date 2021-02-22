# PyBase – Manager for NoSQL and SQL databases.
#==============================================#
# PyBase is distributed under MIT License.     #

# dependencies (packages/modules)
import datetime
import itertools
import os
import pathlib
import sqlite3
import traceback
from threading import Thread
from time import sleep

from .utils import Utils
from .version import __version__


class PySQL:
    """
    PyBase SQL Class

    ...

    Attributes
    ----------

    Methods
    -------
    delete(table: str, objects: dict = None)
        Delete a table or a element from a column (if it was declared) from the database established in PySQL init.
    create(objects: dict)
        Create a table with columns inside the database established in PySQL init.
    insert(table: str, objects: dict)
        Insert objects into the columns of the given table
    get(table: str, objects: dict = None)
        Get data from the database.
    """
    def __init__(self,
                 database: str = None,
                 db_path: str = str(pathlib.Path().absolute()) + '/db'):
        """
        Define the SQLite3 database to use and create it if it doesn't exist.

        ...

        Parameters
        ----------
        database : str, optional
            The name of the database without extension.
            Note: If you don't put a name for the db, it will be created directly in memory without consuming disk.
        db_path : str, optional
            The path where the database is located (default is dir called db in the current working directory).
            Example: /home/bloodbath/Desktop/PyBase
            Note: If the name of a db isn't specified in the db parameter, this path will not be used.

        Raises
        ------
        TypeError
            If database isn't a String (if it's declared).
            If debug isn't a Boolean.
        FileNotFoundError
            If the given path wasn't found.
        """

        self._path = db_path

        # Search for config file
        Utils().search_config()

        # Search for old logs files and delete them
        if Utils().logs_enabled:

            def search_old_logs():
                Utils().delete_old_logs()
                sleep(Utils().time_to_seconds(Utils().logs_life_cycle))

            delete_old_logs = Thread(target=search_old_logs)
            delete_old_logs.daemon = True
            delete_old_logs.start()

        # If database isn't equal to None or isn't a String, then raise TypeError.
        if not isinstance(database, str) and database is None:
            raise TypeError('database must be a String.')
        elif os.path.exists(db_path) is True:
            raise FileNotFoundError(
                f'The path ({self._path}) wasn\'t found. Please check that the path exists.'
            )
        else:
            if Utils().debug:
                print(f"[DEBUG] Using PyBase v{__version__}")

            if database is None:
                try:
                    self._conn = sqlite3.connect(':memory:')
                    self._cursor = self._conn.cursor()
                    if Utils().debug:
                        print('[DEBUG] Using a database stored in memory.')
                        sleep(1)
                except Exception as err:
                    print("[ERROR] Something went wrong ...")
                    traceback.print_exc()
                    if Utils().logs_enabled:
                        with open(f"{Utils().current_logs()}",
                                  mode="a") as log_file:
                            log_file.write(
                                f"\033[1m{datetime.datetime.utcnow().strftime('%c')}\033[0m\n"
                                + "========================\n" +
                                f"\033[0;31mAn error has occurred.\n{err}\033[0m\n\n"
                            )
            else:
                self._DB = (f'{self._path}/{database}.db')
                try:
                    self._conn = sqlite3.connect(self._DB)
                    self._cursor = self._conn.cursor()
                    if Utils().debug:
                        print(
                            f'[DEBUG] using a database stored in disk ({self._DB}).'
                        )
                        sleep(1)
                except Exception as err:
                    print("[ERROR] Something went wrong ...")
                    traceback.print_exc()
                    if Utils().logs_enabled:
                        with open(f"{Utils().current_logs()}",
                                  mode="a") as log_file:
                            log_file.write(
                                f"\033[1m{datetime.datetime.utcnow().strftime('%c')}\033[0m\n"
                                + "========================\n" +
                                f"\033[0;31mAn error has occurred.\n{err}\033[0m\n\n"
                            )

            if Utils().debug:
                print(f'[DEBUG] Using SQLite3 version v{sqlite3.version}')
                sleep(1)
        if Utils().stats_enabled:
            try:
                Utils().interval(
                    Utils().send_stats,
                    Utils().time_to_seconds(Utils().stats_interval))
            except Exception as err:
                print("[ERROR] Something went wrong ...")
                traceback.print_exc()
                if Utils().logs_enabled:
                    with open(f"{Utils().current_logs()}",
                              mode="a") as log_file:
                        log_file.write(
                            f"\033[1m{datetime.datetime.utcnow().strftime('%c')}\033[0m\n"
                            + "========================\n" +
                            f"\033[0;31mAn error has occurred.\n{err}\033[0m\n\n"
                        )

    def delete(self, table: str, objects: dict = None):
        """
        Delete a table or element inside of the given table from the database established in PySQL init.

        ...

        Parameters
        ----------
        table : str
            The table which will be deleted from the database.
            Note: If the value parameter isn't None, the table will not be deleted, if not, the element inside it.
        objects : dict, optional
            The column and value to be deleted from the table.
            Example:
                {
                    "column": "username",
                    "value": "bloodbath"
                }

        Raises
        ------
        ValueError
            If table isn't a String or isn't declared or is equal to None.
        KeyError
            If objects doesn't have a value key.
        sqlite3.OperationalError
            If the given table isn't found.
            If the given table doesn't have the given value.
            If the given table doesn't have the given column.
        """

        if not isinstance(table, str):
            # If a table isn't a String or isn't declared or is equal to None, then raise ValueError.
            raise ValueError('table must be a String.')
        elif objects is None or len(objects) == 0:
            # If a element isn't declared, then delete the entire table.
            # Search if the given table exists inside the database.
            self._cursor.execute(
                f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"""
            )
            rows = self._cursor.fetchone()
            if rows is None:
                raise KeyError("The given table doesn't exists.")
            else:
                self._cursor.execute(f"""DROP TABLE {table}""")
                if Utils().debug:
                    sleep(0.5)
                    print(f"[DEBUG] Deleting the table {table}...")
                    sleep(1.5)
                self._conn.commit()
                sleep(0.5)
                print(f"[LOG]: The table {table} has been deleted.")
        else:
            # If there's no value key in objects, then raise error.
            if "value" not in objects:
                raise KeyError("[ERROR]: objects must have a value key.")
            else:
                # If a element is declared, then delete it from the table.
                # Search the given element in the given column and if it doesn't exists, raise error
                self._cursor.execute(
                    f"""SELECT {objects['column']} FROM {table} WHERE {objects['column']} = '{objects['value']}'"""
                )
                rows = self._cursor.fetchall()
                if len(rows) == 0:
                    raise ValueError(
                        "The given element doesn't exists in the given column."
                    )
                else:
                    try:
                        self._cursor.execute(
                            f"""DELETE FROM {table} WHERE {objects['column']} = '{objects['value']}'"""
                        )
                        if Utils().debug:
                            sleep(0.5)
                            print(
                                f"[DEBUG] Deleting the value {objects['value']} from the column {objects['column']} in table {table}..."
                            )
                            sleep(1)
                        self._conn.commit()
                        sleep(0.5)
                        print(
                            f"[LOG]: The element {objects['value']} has been deleted from {objects['column']} in {table}."
                        )
                    except sqlite3.OperationalError as err:
                        print("[ERROR] Something went wrong ...")
                        traceback.print_exc()
                        if Utils().logs_enabled:
                            with open(f"{Utils().current_logs()}",
                                      mode="a") as log_file:
                                log_file.write(
                                    f"\033[1m{datetime.datetime.utcnow().strftime('%c')}\033[0m\n"
                                    + "========================\n" +
                                    f"\033[0;31mAn error has occurred.\n{err}\033[0m\n\n"
                                )

    def create(self, objects: dict):
        """
        Create a table if not exists and its elements.

        ...

        Parameters
        ----------
        objects : dict
            The dictionary that contains the table and its elements.
            Example:
                {
                    "table": {
                        "name": "example",
                        "columns": {
                            "test": {
                                "type": "integer",
                                "value": 12345 # or [12345, 67890]
                            }
                        }
                    }
                }

        Raises
        ------
        ValueError
            If objects isn't a dict or is empty (equal to zero).
            If table name isn't a String.
            If columns key is empty (is equal to Zero).
            If columns key type isn't text or integer.
        KeyError
            If objects doesn't have a key called name or columns.
            If columns keys doesn't have type.
        """

        # Collect each column name and save them inside a list.
        each_column = []
        # Collect each column type and save them inside a list.
        each_type = []
        # Collect each column value and save them inside a list.
        each_value = []

        # If objects isn't a dict or is equal to zero
        if not isinstance(objects, dict) or len(objects) == 0:
            raise ValueError('objects must be a dict and cannot be empty.')
        elif "name" not in objects["table"]:
            raise KeyError(
                'object dict must have a name key inside the table key.')
        # If table name value isn't a String.
        elif not isinstance(objects["table"]["name"], str):
            raise ValueError('table name must be a String.')
        # If table doesn't have a columns key.
        elif "columns" not in objects["table"]:
            raise KeyError(
                'object dict must have a columns key inside the table key.')
        else:
            if len(objects["table"]["columns"]) == 0:
                raise ValueError('columns key cannot be empty.')
            else:
                columns = objects["table"]["columns"]
                # Search in all the columns keys for type and value
                for column in columns:
                    # If type isn't a key inside the column, raise KeyError
                    if "type" in columns[column] is False:
                        raise KeyError(f'{column} must have a type key')
                    # If type value isn't integer or text, raise ValueError
                    elif columns[column]["type"] not in ["text", "integer"]:
                        raise ValueError(
                            f'{column} type must be integer or text')
                    # If value isn't a key inside the element, raise KeyError
                    elif "value" in columns[column] is False:
                        raise KeyError(f'{column} must have a value key')
                    else:
                        # If all is good, then insert each element with
                        # their types and values inside different lists.
                        each_column.append(column)
                        each_type.append(columns[column]["type"])
                        each_value.append(columns[column]["value"])
                # Check if table doesn't exists.
                self._cursor.execute(
                    f"""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{objects['table']['name']}'"""
                )
                if not self._cursor.fetchone()[0] == 1:

                    try:
                        # Initializing the table creation.
                        create_table = f"""CREATE TABLE IF NOT EXISTS {objects["table"]["name"]} (\n"""
                        for c in range(len(each_column)):
                            create_table += f"""    {'{} {},'.format(each_column[c], each_type[c]) if (c + 1) != len(each_column) else '{} {}'.format(each_column[c], each_type[c])}\n"""
                        create_table += """);"""

                        if Utils().debug:
                            print(
                                f"[DEBUG] Creating table {objects['table']['name']}..."
                            )
                            sleep(0.5)
                            print("[DEBUG]", create_table)
                            sleep(1.5)
                        self._cursor.execute(create_table)
                        sleep(0.5)
                        print(
                            f"[LOG]: The table {objects['table']['name']} has been created successfully."
                        )
                    except Exception as err:
                        print("[ERROR] Something went wrong ...")
                        traceback.print_exc()
                        if Utils().logs_enabled:
                            with open(f"{Utils().current_logs()}",
                                      mode="a") as log_file:
                                log_file.write(
                                    f"\033[1m{datetime.datetime.utcnow().strftime('%c')}\033[0m\n"
                                    + "========================\n" +
                                    f"\033[0;31mAn error has occurred.\n{err}\033[0m\n\n"
                                )

                # Initializing the insertion
                try:
                    insert_data = f"""INSERT INTO {objects['table']['name']} ("""
                    for c in range(len(each_column)):
                        insert_data += f"""{'{}, '.format(each_column[c]) if (c + 1) != len(each_column) else '{}'.format(each_column[c])}"""
                    insert_data += """) SELECT """
                    for c in range(len(each_column)):
                        insert_data += f"""'{"{}".format(each_value[c]) if isinstance(each_value[c], list) == False else "{}".format(each_value[c][0])}'""" + f"""{", " if (c + 1) != len(each_column) else " "}"""
                    insert_data += f"""WHERE NOT EXISTS (SELECT 1 FROM {objects['table']['name']} WHERE """
                    for c in range(len(each_column)):
                        insert_data += f"""{each_column[c]} = '{"{}".format(each_value[c]) if isinstance(each_value[c], list) == False else "{}".format(each_value[c][0])}'"""
                        insert_data += f"""{ " AND " if (c + 1) != len(each_column) else ''}"""
                    insert_data += """);"""

                    self._cursor.execute(insert_data)
                    self._conn.commit()

                    if Utils().debug:
                        if any(
                                isinstance(value, list)
                                for value in each_value):
                            print(
                                "[DEBUG] Inserting the data only with the first arrays value..."
                            )
                            print("[DEBUG]", insert_data)
                        else:
                            print(
                                f"[DEBUG] Inserting the data inside the table {objects['table']['name']}..."
                            )
                            print("[DEBUG]", insert_data)

                    # Insert the rest of the array data inside the column
                    self.columns = []
                    self.all_values = []
                    self.values = []

                    for c in range(len(each_column)):
                        if isinstance(each_value[c], list):
                            self.columns.append(each_column[c])
                            self.all_values.append(each_value[c])
                    all_values_length = 0
                    values_length = 0

                    insert_data = ""
                    while 0 <= all_values_length < len(self.all_values):
                        for i, name in enumerate(
                                self.all_values[all_values_length]):
                            if 0 < i:
                                if i == 1:
                                    self.values.append([])
                                    self.values[values_length].append(name)
                                else:
                                    self.values[values_length].append(name)
                        values_length += 1
                        all_values_length += 1

                    self.values = list(zip(*self.values))

                    row = 0
                    values_length = 0
                    while 0 <= values_length < len(
                            self.columns) and 0 <= row <= (len(self.values) -
                                                           1):
                        insert_data += f"""INSERT INTO {objects['table']['name']} ("""
                        for c in range(len(self.columns)):
                            insert_data += f"""{'{}, '.format(self.columns[c]) if (c + 1) != len(self.columns) else '{}'.format(self.columns[c])}"""
                        insert_data += """) SELECT """
                        for i in range(len(self.values[row])):
                            insert_data += f"""'{"{}".format(self.values[row][i])}'""" + f"""{", " if (i + 1) != len(self.values[row]) else " "}"""
                        print(self.values[row])
                        insert_data += f"""WHERE NOT EXISTS (SELECT 1 FROM {objects['table']['name']} WHERE """
                        for c, i in itertools.zip_longest(
                                range(len(self.columns)),
                                range(len(self.values[row])),
                                fillvalue=None):
                            insert_data += f"""{self.columns[c]} = '{"{}".format(self.values[row][i])}'"""
                            insert_data += f"""{ " AND " if (c + 1) != len(self.columns) else ''}"""
                        insert_data += """);\n\n"""
                        row += 1
                        values_length += 1

                    self._cursor.executescript(insert_data)
                    self._conn.commit()

                    if Utils().debug:
                        if any(
                                isinstance(value, list)
                                for value in each_value):
                            print(
                                f"[DEBUG] Inserting the rest of the data arrays values inside the table {objects['table']['name']}..."
                            )
                            sleep(0.5)
                            print("[DEBUG]", insert_data)
                            sleep(1)

                    sleep(0.5)
                    print(
                        f"[LOG]: The data has been inserted successfully inside the table {objects['table']['name']}."
                    )
                except Exception as err:
                    print("[ERROR] Something went wrong ...")
                    traceback.print_exc()
                    if Utils().logs_enabled:
                        with open(f"{Utils().current_logs()}",
                                  mode="a") as log_file:
                            log_file.write(
                                f"\033[1m{datetime.datetime.utcnow().strftime('%c')}\033[0m\n"
                                + "========================\n" +
                                f"\033[0;31mAn error has occurred.\n{err}\033[0m\n\n"
                            )

    def get(self, table: str, objects: dict = None):
        """
        Get data from the database.

        ...

        Parameters
        ----------
        table : str
            The table where the data will be searched.
        objects : dict, optional
            The column and value that will be searched.
            Note: If the value is not specified, the entire column will be obtained.
            Example: {
                "column": "languages",
                "value": "Python"
            }

        Raises
        ------
        ValueError
            If table isn't a String.
            If objects isn't a dict.
        KeyError
            If the given column doesn't have the given value.
        sqlite3.OperationalError
            If the given table doesn't have the given column.

        Returns
        -------
        list
            A list with tuples that returns all the found values.
        """

        if not isinstance(table, str):
            raise ValueError('table must be a String.')
        if not isinstance(objects, dict):
            raise ValueError('objects must be a dict.')
        else:
            if "column" not in objects:
                try:
                    # Get all the table
                    self._cursor.execute(f"""SELECT * FROM {table}""")
                    rows = self._cursor.fetchall()
                except sqlite3.OperationalError as err:
                    print("[ERROR] Something went wrong ...")
                    traceback.print_exc()
                    if Utils().logs_enabled:
                        with open(f"{Utils().current_logs()}",
                                  mode="a") as log_file:
                            log_file.write(
                                f"\033[1m{datetime.datetime.utcnow().strftime('%c')}\033[0m\n"
                                + "========================\n" +
                                f"\033[0;31mAn error has occurred.\n{err}\033[0m\n\n"
                            )

                if Utils().debug:
                    sleep(0.5)
                    print(f"[DEBUG] Getting the table {table}...")
                    sleep(0.5)
                    print(
                        f"[DEBUG] The table {table} was obtained successfully and saved in rows attribute."
                    )
                    sleep(0.5)
                    print("[DEBUG]", rows)

                return rows
            else:
                if "value" not in objects:
                    try:
                        # Get all the column
                        self._cursor.execute(
                            f"""SELECT {objects['column']} FROM {table}""")
                        rows = self._cursor.fetchall()
                    except sqlite3.OperationalError as err:
                        print("[ERROR] Something went wrong ...")
                        traceback.print_exc()
                        if Utils().logs_enabled:
                            with open(f"{Utils().current_logs()}",
                                      mode="a") as log_file:
                                log_file.write(
                                    f"\033[1m{datetime.datetime.utcnow().strftime('%c')}\033[0m\n"
                                    + "========================\n" +
                                    f"\033[0;31mAn error has occurred.\n{err}\033[0m\n\n"
                                )

                    if Utils().debug:
                        sleep(0.5)
                        print(
                            f"[DEBUG] Getting the column {objects['column']} from {table} table..."
                        )
                        sleep(0.5)
                        print(
                            f"[DEBUG] The column {objects['column']} was obtained successfully and saved in rows attribute."
                        )
                        sleep(0.5)
                        print("[DEBUG]", rows)

                    return rows
                else:
                    try:
                        # Get the value in the column
                        self._cursor.execute(
                            f"""SELECT {objects['column']} FROM {table} WHERE {objects['column']} = '{objects['value']}'"""
                        )
                        rows = self._cursor.fetchone()[0]
                    except sqlite3.OperationalError as err:
                        print("[ERROR] Something went wrong ...")
                        traceback.print_exc()
                        if Utils().logs_enabled:
                            with open(f"{Utils().current_logs()}",
                                      mode="a") as log_file:
                                log_file.write(
                                    f"\033[1m{datetime.datetime.utcnow().strftime('%c')}\033[0m\n"
                                    + "========================\n" +
                                    f"\033[0;31mAn error has occurred.\n{err}\033[0m\n\n"
                                )

                    if Utils().debug:
                        sleep(0.5)
                        print(
                            f"[DEBUG] Getting the value {objects['value']} from column {objects['column']} in {table} table..."
                        )
                        sleep(0.5)
                        print(
                            f"[DEBUG] The value {objects['value']} was obtained successfully and saved in rows attribute."
                        )
                        sleep(0.5)
                        print("[DEBUG]", rows)

                    return rows
