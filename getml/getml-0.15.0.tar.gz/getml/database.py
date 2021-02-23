# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""This module provides communication routines to access various databases.

The :func:`~getml.database.connect_greenplum`,
:func:`~getml.database.connect_mariadb`,
:func:`~getml.database.connect_mysql`,
:func:`~getml.database.connect_postgres`, and
:func:`~getml.database.connect_sqlite3` functions establish a
connection between a database and the getML engine. During the data
import using either the :meth:`~getml.data.DataFrame.read_db` or
:meth:`~getml.data.DataFrame.read_query` methods of a
:class:`~getml.data.DataFrame` instance or the corresponding
:func:`~getml.data.DataFrame.from_db` class method all data will be
directly loaded from the database into the engine without ever passing
the Python interpreter.

In addition, several auxiliary functions that might be handy during
the analysis and interaction with the database are provided.
"""

import json
import os

import pandas as pd

import getml.communication as comm
import getml.constants as constants
from getml.helpers import _str

# -----------------------------------------------------------------------------


class Connection:
    """
    A handle to a database connection on the getML engine.

    Args:
        conn_id (str, optional): The name you want to use to reference the connection.
            You can call it
            anything you want to. If a database
            connection with the same conn_id already exists, that connection
            will be removed automatically and the new connection will take its place.
            The default conn_id is "default", which refers to the default connection. If you
            do not explicitly pass a connection handle to any function that relates to a
            database, the default connection will be used automatically.
    """

    def __init__(self, conn_id="default"):
        self.conn_id = conn_id

    def __repr__(self):
        return str(self)

    def __str__(self):

        cmd = dict()

        cmd["name_"] = self.conn_id
        cmd["type_"] = "Database.describe_connection"

        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Success!":
            comm.engine_exception_handler(msg)

        description = comm.recv_string(sock)

        sock.close()

        json_obj = json.loads(description)

        json_obj["type"] = "Connection"

        return _str(json_obj)


# -----------------------------------------------------------------------------


def connect_greenplum(
    dbname,
    user,
    password,
    host,
    hostaddr,
    port=5432,
    time_formats=None,
    conn_id="default",
):
    """Creates a new Greenplum database connection.

    But first, make sure your database is running and you can reach it
    from via your command line.

    Args:
        dbname (str): The name of the database to which you want to connect.
        user (str): User name with which to log into the Greenplum database.
        password (str): Password with which to log into the Greenplum database.
        host (str): Host of the Greenplum database.
        hostaddr (str): IP address of the Greenplum database.
        port(int, optional): Port of the Greenplum database.

            The default port used by Greenplum is 5432.

            If you do not know, which port to use, type the following into your
            Greenplum client:

            .. code-block:: sql

                SELECT setting FROM pg_settings WHERE name = 'port';

        time_formats (List[str], optional):

            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

        conn_id (str, optional): The name to be used to reference the connection.
            If you do not pass anything, this will create a new default connection.

    Note:

        Please note that this feature is **not supported on
        Windows**. Please use :func:`~getml.database.connect_odbc`
        instead.

        By selecting an existing table of your database in
        :func:`~getml.data.DataFrame.from_db` function, you can create
        a new :class:`~getml.data.DataFrame` containing all its data.
        Alternatively you can use the
        :meth:`~.getml.data.DataFrame.read_db` and
        :meth:`~.getml.data.DataFrame.read_query` methods to replace
        the content of the current :class:`~getml.data.DataFrame`
        instance or append further rows based on either a table or a
        specific query.

        You can also write your results back into the Greenplum
        database. By passing the name for the destination table to
        :meth:`getml.pipeline.Pipeline.transform`, the features
        generated from your raw data will be written back. Passing
        them into :meth:`getml.pipeline.Pipeline.predict`, instead,
        makes predictions of the target variables to new, unseen data
        and stores the result into the corresponding table.

    """
    # -------------------------------------------

    time_formats = time_formats or constants.TIME_FORMATS

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Database.new"
    cmd["db_"] = "greenplum"

    cmd["host_"] = host
    cmd["hostaddr_"] = hostaddr
    cmd["port_"] = port
    cmd["dbname_"] = dbname
    cmd["user_"] = user
    cmd["time_formats_"] = time_formats
    cmd["conn_id_"] = conn_id

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # The password is sent separately, so it doesn't
    # end up in the logs.

    comm.send_string(sock, password)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    return Connection(conn_id=conn_id)


# -----------------------------------------------------------------------------


def connect_mariadb(
    dbname,
    user,
    password,
    host,
    port=3306,
    unix_socket="/var/run/mysqld/mysqld.sock",
    time_formats=None,
    conn_id="default",
):
    """
    Creates a new MariaDB database connection.

    But first, make sure your database is running and you can reach it
    from via your command line.

    Args:
        dbname (str): The name of the database to which you want to connect.

        user (str): User name with which to log into the MariaDB database.

        password (str): Password with which to log into the MariaDB database.

        host (str): Host of the MariaDB database.

        port (int, optional): Port of the MariaDB database.

            The default port for MariaDB is 3306.

            If you do not know which port to use, type

            .. code-block:: sql

                SELECT @@port;

            into your MariaDB client.

        unix_socket (str, optional): The UNIX socket used to connect to the MariaDB database.

            If you do not know which UNIX socket to use, type

            .. code-block:: sql

                SELECT @@socket;

            into your MariaDB client.

        time_formats (List[str], optional):

            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

        conn_id (str, optional): The name to be used to reference the connection.
            If you do not pass anything, this will create a new default connection.
    Note:

        By selecting an existing table of your database in
        :func:`~getml.data.DataFrame.from_db` function, you can create
        a new :class:`~getml.data.DataFrame` containing all its data.
        Alternatively you can use the
        :meth:`~.getml.data.DataFrame.read_db` and
        :meth:`~.getml.data.DataFrame.read_query` methods to replace
        the content of the current :class:`~getml.data.DataFrame`
        instance or append further rows based on either a table or a
        specific query.

        You can also write your results back into the MariaDB
        database. By passing the name for the destination table to
        :meth:`getml.pipeline.Pipeline.transform`, the features
        generated from your raw data will be written back. Passing
        them into :meth:`getml.pipeline.Pipeline.predict`, instead,
        makes predictions
        of the target variables to new, unseen data and stores the result into
        the corresponding table.

    """
    # -------------------------------------------

    time_formats = time_formats or constants.TIME_FORMATS

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Database.new"
    cmd["db_"] = "mariadb"

    cmd["host_"] = host
    cmd["port_"] = port
    cmd["dbname_"] = dbname
    cmd["user_"] = user
    cmd["unix_socket_"] = unix_socket
    cmd["time_formats_"] = time_formats
    cmd["conn_id_"] = conn_id

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # The password is sent separately, so it doesn't
    # end up in the logs.

    comm.send_string(sock, password)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    return Connection(conn_id=conn_id)


# -----------------------------------------------------------------------------


def connect_mysql(
    dbname,
    user,
    password,
    host,
    port=3306,
    unix_socket="/var/run/mysqld/mysqld.sock",
    time_formats=None,
    conn_id="default",
):
    """
    Creates a new MySQL database connection.

    But first, make sure your database is running and you can reach it
    from via your command line.

    Args:
        dbname (str): The name of the database to which you want to connect.

        user (str): User name with which to log into the MySQL database.

        password (str): Password with which to log into the MySQL database.

        host (str): Host of the MySQL database.

        port (int, optional): Port of the MySQL database.

            The default port for MySQL is 3306.

            If you do not know which port to use, type

            .. code-block:: sql

                SELECT @@port;

            into your mysql client.

        unix_socket (str, optional): The UNIX socket used to connect to the MySQL database.

            If you do not know which UNIX socket to use, type

            .. code-block:: sql

                SELECT @@socket;

            into your mysql client.

        time_formats (List[str], optional):

            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

        conn_id (str, optional): The name to be used to reference the connection.
            If you do not pass anything, this will create a new default connection.
    Note:

        By selecting an existing table of your database in
        :func:`~getml.data.DataFrame.from_db` function, you can create
        a new :class:`~getml.data.DataFrame` containing all its data.
        Alternatively you can use the
        :meth:`~.getml.data.DataFrame.read_db` and
        :meth:`~.getml.data.DataFrame.read_query` methods to replace
        the content of the current :class:`~getml.data.DataFrame`
        instance or append further rows based on either a table or a
        specific query.

        You can also write your results back into the MySQL
        database. By passing the name for the destination table to
        :meth:`getml.pipeline.Pipeline.transform`, the features
        generated from your raw data will be written back. Passing
        them into :meth:`getml.pipeline.Pipeline.predict`, instead,
        makes predictions of the target variables to new, unseen data
        and stores the result into the corresponding table.

    """
    # -------------------------------------------

    time_formats = time_formats or constants.TIME_FORMATS

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Database.new"
    cmd["db_"] = "mysql"

    cmd["host_"] = host
    cmd["port_"] = port
    cmd["dbname_"] = dbname
    cmd["user_"] = user
    cmd["unix_socket_"] = unix_socket
    cmd["time_formats_"] = time_formats
    cmd["conn_id_"] = conn_id

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # The password is sent separately, so it doesn't
    # end up in the logs.

    comm.send_string(sock, password)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    return Connection(conn_id=conn_id)


# -----------------------------------------------------------------------------


def connect_odbc(
    server_name,
    user="",
    password="",
    escape_chars='"',
    double_precision="DOUBLE PRECISION",
    integer="INTEGER",
    text="TEXT",
    time_formats=None,
    conn_id="default",
):
    """
    Creates a new ODBC database connection.

    ODBC is standardized format that can be used to connect to almost any
    database.

    Before you use the ODBC connector, make sure the database is up and
    running and that the appropriate ODBC drivers are installed.

    Args:
        server_name (str): The server name, as referenced in your .obdc.ini file.

        user (str, optional): User name with which to log into the database.
            You do not need to pass this, if it is already contained in your
            .odbc.ini.

        password (str, optional): Password with which to log into the database.
            You do not need to pass this, if it is already contained in your
            .odbc.ini.

        escape_chars (str, optional): ODBC drivers are supposed to support
            escaping table and column names using '"' characters irrespective of the
            syntax in the target database. Unfortunately, not ODBC drivers
            follow this standard. This is why some
            tuning might be necessary.

            The escape_chars value behaves as follows:

            * If you pass an empty string, schema, table and column names will not
              be escaped at all. This is not a problem unless some table
              or column names are identical to SQL keywords.

            * If you pass a single character, schema, table and column names will
              be enveloped in that character: "TABLE_NAME"."COLUMN_NAME" (standard SQL)
              or `TABLE_NAME`.`COLUMN_NAME` (MySQL/MariaDB style).

            * If you pass two characters, table, column and schema names will be enveloped
              between these to characters. For instance, if you pass "[]", the produced
              queries look as follows: [TABLE_NAME].[COLUMN_NAME] (MS SQL Server style).

            * If you pass more than two characters, the engine will throw an exception.

        double_precision (str, optional): The keyword used for double precision columns.

        integer (str, optional): The keyword used for integer columns.

        text (str, optional): The keyword used for text columns.

        time_formats (List[str], optional):

            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

        conn_id (str, optional): The name to be used to reference the connection.
            If you do not pass anything, this will create a new default connection.

    Note:
        By selecting an existing table of your database in
        :func:`~getml.data.DataFrame.from_db` function, you can create
        a new :class:`~getml.data.DataFrame` containing all its data.
        Alternatively you can use the
        :meth:`~.getml.data.DataFrame.read_db` and
        :meth:`~.getml.data.DataFrame.read_query` methods to replace
        the content of the current :class:`~getml.data.DataFrame`
        instance or append further rows based on either a table or a
        specific query.

        You can also write your results back into the
        database. By passing the name for the destination table to
        :meth:`getml.pipeline.Pipeline.transform`, the features
        generated from your raw data will be written back. Passing
        them into :meth:`getml.pipeline.Pipeline.predict`, instead,
        makes predictions of the target variables to new, unseen data
        and stores the result into the corresponding table.
    """
    # -------------------------------------------

    time_formats = time_formats or constants.TIME_FORMATS

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Database.new"
    cmd["db_"] = "odbc"

    cmd["server_name_"] = server_name
    cmd["user_"] = user
    cmd["escape_chars_"] = escape_chars
    cmd["double_precision_"] = double_precision
    cmd["integer_"] = integer
    cmd["text_"] = text
    cmd["time_formats_"] = time_formats
    cmd["conn_id_"] = conn_id

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # The password is sent separately, so it doesn't
    # end up in the logs.

    comm.send_string(sock, password)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    return Connection(conn_id=conn_id)


# -----------------------------------------------------------------------------


def connect_postgres(
    dbname,
    user,
    password,
    host,
    hostaddr,
    port=5432,
    time_formats=None,
    conn_id="default",
):
    """
    Creates a new PostgreSQL database connection.

    But first, make sure your database is running and you can reach it
    from via your command line.

    Args:
        dbname (str): The name of the database to which you want to connect.
        user (str): User name with which to log into the PostgreSQL database.
        password (str): Password with which to log into the PostgreSQL database.
        host (str): Host of the PostgreSQL database.
        hostaddr (str): IP address of the PostgreSQL database.
        port(int, optional): Port of the PostgreSQL database.

            The default port used by PostgreSQL is 5432.

            If you do not know, which port to use, type the following into your
            PostgreSQL client

            .. code-block:: sql

                SELECT setting FROM pg_settings WHERE name = 'port';

        time_formats (List[str], optional):

            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

        conn_id (str, optional): The name to be used to reference the connection.
            If you do not pass anything, this will create a new default connection.

    Note:

        Please note that this feature is **not supported on
        Windows**. Please use :func:`~getml.database.connect_odbc`
        instead.

        By selecting an existing table of your database in
        :func:`~getml.data.DataFrame.from_db` function, you can create
        a new :class:`~getml.data.DataFrame` containing all its data.
        Alternatively you can use the
        :meth:`~.getml.data.DataFrame.read_db` and
        :meth:`~.getml.data.DataFrame.read_query` methods to replace
        the content of the current :class:`~getml.data.DataFrame`
        instance or append further rows based on either a table or a
        specific query.

        You can also write your results back into the PostgreSQL
        database. By passing the name for the destination table to
        :meth:`getml.pipeline.Pipeline.transform`, the features
        generated from your raw data will be written back. Passing
        them into :meth:`getml.pipeline.Pipeline.predict`, instead,
        makes predictions of the target variables to new, unseen data
        and stores the result into the corresponding table.
    """
    # -------------------------------------------

    time_formats = time_formats or constants.TIME_FORMATS

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Database.new"
    cmd["db_"] = "postgres"

    cmd["host_"] = host
    cmd["hostaddr_"] = hostaddr
    cmd["port_"] = port
    cmd["dbname_"] = dbname
    cmd["user_"] = user
    cmd["time_formats_"] = time_formats
    cmd["conn_id_"] = conn_id

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # The password is sent separately, so it doesn't
    # end up in the logs.

    comm.send_string(sock, password)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    return Connection(conn_id=conn_id)


# -----------------------------------------------------------------------------


def connect_sqlite3(name=":memory:", time_formats=None, conn_id="default"):
    """Creates a new SQLite3 database connection.

    SQLite3 is a popular in-memory database. It is faster than
    distributed databases, like PostgreSQL, but less stable under massive
    parallel access, consumes more memory and requires all contained
    data sets to be loaded into memory, which might fill up too much
    of your RAM, especially for large data set.

    Args:
        name (str, optional): Name of the sqlite3 file.  If the file does not exist, it
            will be created. Set to ":memory:" for a purely in-memory SQLite3
            database.

        time_formats (List[str], optional):

            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

        conn_id (str, optional): The name to be used to reference the connection.
            If you do not pass anything, this will create a new default connection.
    Note:

        By selecting an existing table of your database in
        :func:`~getml.data.DataFrame.from_db` function, you can create
        a new :class:`~getml.data.DataFrame` containing all its data.
        Alternatively you can use the
        :meth:`~.getml.data.DataFrame.read_db` and
        :meth:`~.getml.data.DataFrame.read_query` methods to replace
        the content of the current :class:`~getml.data.DataFrame`
        instance or append further rows based on either a table or a
        specific query.

        You can also write your results back into the SQLite3
        database. By passing the name for the destination table to
        :meth:`getml.pipeline.Pipeline.transform`, the features
        generated from your raw data will be written back. Passing
        them into :meth:`getml.pipeline.Pipeline.predict`, instead,
        makes predictions of the target variables to new, unseen data
        and stores the result into the corresponding table.

    """
    # -------------------------------------------

    time_formats = time_formats or constants.TIME_FORMATS

    # -------------------------------------------
    # We want to use the absolute path, unless it is a pure
    # in-memory version.

    name_ = name

    if name_ != ":memory":
        os.path.abspath(name)

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = name_
    cmd["type_"] = "Database.new"

    cmd["db_"] = "sqlite3"
    cmd["time_formats_"] = time_formats
    cmd["conn_id_"] = conn_id

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # The password is sent separately, so it doesn't
    # end up in the logs. However, Sqlite3 does not
    # need a password, so we just send a dummy.

    comm.send_string(sock, "none")

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    return Connection(conn_id=conn_id)


# -----------------------------------------------------------------------------


def copy_table(source_conn, target_conn, source_table, target_table=None):
    """
    Copies a table from one database connection to another.

    Args:
        source_conn (:class:`~getml.database.Connection`): The database
            connection to be copied from.

        target_conn (:class:`~getml.database.Connection`): The database
            connection to be copied to.

        source_table (str): The name of the table in the source connection.

        target_table (str, optional): The name of the table in the target
            connection. If you do not explicitly pass a target_table, the
            name will be identical to the source_table.

    Example:
        A frequent use case for this function is to copy data from a data source into
        sqlite. This is a good idea, because sqlite is faster than most standard,
        ACID-compliant databases and also you want to avoid messing up a productive
        environment.

        It is important to explicitly pass conn_id, otherwise the source connection
        will be closed
        when you create the target connection. What you pass as conn_id is entirely
        up to you,
        as long as the conn_id of the source and the target are different. It can
        be any name you see fit.

        >>> source_conn = getml.database.connect_odbc("MY-SERVER-NAME", conn_id="MY-SOURCE")
        >>>
        >>> target_conn = getml.database.connect_sqlite3("MY-SQLITE.db", conn_id="MY-TARGET")
        >>>
        >>> data.database.copy_table(
        ...         source_conn=source_conn,
        ...         target_conn=target_conn,
        ...         source_table="MY-TABLE"
        ... )
    """

    # -------------------------------------------

    target_table = target_table or source_table

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Database.copy_table"

    cmd["source_conn_id_"] = source_conn.conn_id
    cmd["target_conn_id_"] = target_conn.conn_id
    cmd["source_table_"] = source_table
    cmd["target_table_"] = target_table

    # -------------------------------------------
    # Send JSON command to engine.

    comm.send(cmd)


# -----------------------------------------------------------------------------


def drop_table(name, conn=None):
    """
    Drops a table from the database.

    Args:
        name (str): The table to be dropped.

        conn (:class:`~getml.database.Connection`, optional): The database connection to be used.
            If you don't explicitly pass a connection, the engine will use the default connection.
    """

    # -------------------------------------------

    conn = conn or Connection()

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = name
    cmd["type_"] = "Database.drop_table"
    cmd["conn_id_"] = conn.conn_id

    # -------------------------------------------
    # Send JSON command to engine.

    comm.send(cmd)


# -----------------------------------------------------------------------------


def get(query, conn=None):
    """
    Executes an SQL query on the database and returns the result as
    a pandas dataframe.

    Args:
        query (str): The SQL query to be executed.

        conn (:class:`~getml.database.Connection`, optional): The database connection to be used.
            If you don't explicitly pass a connection, the engine will use the default connection.
    """

    # -------------------------------------------

    conn = conn or Connection()

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = conn.conn_id
    cmd["type_"] = "Database.get"

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # Send the actual query.

    comm.send_string(sock, query)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # -------------------------------------------
    # Return results as pd.DataFrame.

    json_str = comm.recv_string(sock)

    sock.close()

    return pd.read_json(json_str)


# -----------------------------------------------------------------------------


def execute(query, conn=None):
    """
    Executes an SQL query on the database.
    Please note that this is not meant to return results. If you want to
    get results, use database.get(...) instead.

    Args:
        query (str): The SQL query to be executed.

        conn (:class:`~getml.database.Connection`, optional): The database connection to be used.
            If you don't explicitly pass a connection, the engine will use the default connection.
    """

    # -------------------------------------------

    conn = conn or Connection()

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = conn.conn_id
    cmd["type_"] = "Database.execute"

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # Send the actual query.

    comm.send_string(sock, query)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    sock.close()

    if msg != "Success!":
        comm.engine_exception_handler(msg)


# -----------------------------------------------------------------------------


def get_colnames(name, conn=None):
    """
    Lists the colnames of a table held in the database.

    Args:
        name (str): The name of the table in the database.

        conn (:class:`~getml.database.Connection`, optional): The database connection to be used.
            If you don't explicitly pass a connection, the engine will use the default connection.
    """
    # -------------------------------------------

    conn = conn or Connection()

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = name
    cmd["type_"] = "Database.get_colnames"
    cmd["conn_id_"] = conn.conn_id

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        sock.close()
        comm.engine_exception_handler(msg)

    # -------------------------------------------
    # Parse result as list.

    arr = json.loads(comm.recv_string(sock))

    sock.close()

    return arr


# -----------------------------------------------------------------------------


def list_connections():
    """
    Returns a list handles to all connections that are currently active on the
    engine.
    """

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Database.list_connections"

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        sock.close()
        comm.engine_exception_handler(msg)

    # -------------------------------------------
    # Parse result as list.

    arr = json.loads(comm.recv_string(sock))

    sock.close()

    return [Connection(elem) for elem in arr]


# -----------------------------------------------------------------------------


def list_tables(conn=None):
    """
    Lists all tables and views currently held in the database.

    Args:
        conn (:class:`~getml.database.Connection`, optional): The database connection to be used.
            If you don't explicitly pass a connection, the engine will use the default connection.
    """

    # -------------------------------------------

    conn = conn or Connection()

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = conn.conn_id
    cmd["type_"] = "Database.list_tables"

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        sock.close()
        comm.engine_exception_handler(msg)

    # -------------------------------------------
    # Parse result as list.

    arr = json.loads(comm.recv_string(sock))

    sock.close()

    return arr


# -----------------------------------------------------------------------------


def read_csv(
    name,
    fnames,
    quotechar='"',
    sep=",",
    num_lines_read=0,
    skip=0,
    colnames=None,
    conn=None,
):
    """
    Reads a CSV file into the database.

    Args:
        name (str): Name of the table in which the data is to be inserted.

        fnames (List[str]): The list of CSV file names to be read.

        quotechar (str, optional): The character used to wrap strings. Default:`"`

        sep (str, optional): The separator used for separating fields. Default:`,`

        num_lines_read (int, optional): Number of lines read from each file.
            Set to 0 to read in the entire file.

        skip (int, optional): Number of lines to skip at the beginning of each
            file (Default: 0).

        colnames(List[str] or None, optional): The first line of a CSV file
            usually contains the column names. When this is not the case, you need to
            explicitly pass them.

        conn (:class:`~getml.database.Connection`, optional): The database connection to be used.
            If you don't explicitly pass a connection, the engine will use the default connection.

    Example:
        Let's assume you have two CSV files - *file1.csv* and
        *file2.csv* . You can import their data into the database
        using the following commands:

        >>> stmt = data.database.sniff_csv(
        ...         fnames=["file1.csv", "file2.csv"],
        ...         name="MY_TABLE",
        ...         sep=';'
        ... )
        >>>
        >>> getml.database.execute(stmt)
        >>>
        >>> stmt = data.database.read_csv(
        ...         fnames=["file1.csv", "file2.csv"],
        ...         name="MY_TABLE",
        ...         sep=';'
        ... )
    """
    # -------------------------------------------

    conn = conn or Connection()

    # -------------------------------------------
    # Transform paths

    if not isinstance(fnames, list):
        fnames = [fnames]

    fnames_ = [os.path.abspath(fname) for fname in fnames]

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = name
    cmd["type_"] = "Database.read_csv"

    cmd["fnames_"] = fnames_
    cmd["quotechar_"] = quotechar
    cmd["sep_"] = sep
    cmd["skip_"] = skip
    cmd["num_lines_read_"] = num_lines_read
    cmd["conn_id_"] = conn.conn_id

    if colnames is not None:
        cmd["colnames_"] = colnames

    # -------------------------------------------
    # Send JSON command to engine.

    comm.send(cmd)


# -----------------------------------------------------------------------------


def read_s3(
    name,
    bucket,
    keys,
    region,
    sep=",",
    num_lines_read=0,
    skip=0,
    colnames=None,
    conn=None,
):
    """
    Reads a list of CSV files located in an S3 bucket.

    Args:
        name (str): Name of the table in which the data is to be inserted.

        bucket (str):
            The bucket from which to read the files.

        keys (List[str]): The list of keys (files in the bucket) to be read.

        region (str):
            The region in which the bucket is located.

        sep (str, optional): The separator used for separating fields. Default:`,`

        num_lines_read (int, optional): Number of lines read from each file.
            Set to 0 to read in the entire file.

        skip (int, optional): Number of lines to skip at the beginning of each
            file (Default: 0).

        colnames(List[str] or None, optional): The first line of a CSV file
            usually contains the column names. When this is not the case, you need to
            explicitly pass them.

        conn (:class:`~getml.database.Connection`, optional): The database connection to be used.
            If you don't explicitly pass a connection, the engine will use the default connection.

    Example:
        Let's assume you have two CSV files - *file1.csv* and
        *file2.csv* - in the bucket. You can
        import their data into the getML engine using the following
        commands:

        >>> getml.engine.set_s3_access_key_id("YOUR-ACCESS-KEY-ID")
        >>>
        >>> getml.engine.set_s3_secret_access_key("YOUR-SECRET-ACCESS-KEY")
        >>>
        >>> stmt = data.database.sniff_s3(
        ...         bucket="your-bucket-name",
        ...         keys=["file1.csv", "file2.csv"],
        ...         region="us-east-2",
        ...         name="MY_TABLE",
        ...         sep=';'
        ... )
        >>>
        >>> getml.database.execute(stmt)
        >>>
        >>> stmt = data.database.read_s3(
        ...         bucket="your-bucket-name",
        ...         keys=["file1.csv", "file2.csv"],
        ...         region="us-east-2",
        ...         name="MY_TABLE",
        ...         sep=';'
        ... )

        You can also set the access credential as environment variables
        before you launch the getML engine.
    """
    # -------------------------------------------

    conn = conn or Connection()

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = name
    cmd["type_"] = "Database.read_s3"

    cmd["bucket_"] = bucket
    cmd["keys_"] = keys
    cmd["num_lines_read_"] = num_lines_read
    cmd["region_"] = region
    cmd["sep_"] = sep
    cmd["skip_"] = skip
    cmd["conn_id_"] = conn.conn_id

    if colnames is not None:
        cmd["colnames_"] = colnames

    # -------------------------------------------
    # Send JSON command to engine.

    comm.send(cmd)


# -----------------------------------------------------------------------------


def sniff_csv(
    name,
    fnames,
    num_lines_sniffed=1000,
    quotechar='"',
    sep=",",
    skip=0,
    colnames=None,
    conn=None,
):
    """
    Sniffs a list of CSV files.

    Args:
        name (str): Name of the table in which the data is to be inserted.

        fnames (List[str]): The list of CSV file names to be read.

        num_lines_sniffed (int, optional):
            Number of lines analyzed by the sniffer.

        quotechar (str, optional): The character used to wrap strings. Default:`"`

        sep (str, optional): The separator used for separating fields. Default:`,`

        skip (int, optional): Number of lines to skip at the beginning of each
            file (Default: 0).

        colnames(List[str] or None, optional): The first line of a CSV file
            usually contains the column names. When this is not the case, you need to
            explicitly pass them.

        conn (:class:`~getml.database.Connection`, optional): The database connection to be used.
            If you don't explicitly pass a connection, the engine will use the default connection.

    Returns:
        str: Appropriate `CREATE TABLE` statement.
    """
    # -------------------------------------------

    conn = conn or Connection()

    # -------------------------------------------
    # Transform paths
    if not isinstance(fnames, list):
        fnames = [fnames]

    fnames_ = [os.path.abspath(fname) for fname in fnames]

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = name
    cmd["type_"] = "Database.sniff_csv"

    cmd["fnames_"] = fnames_
    cmd["num_lines_sniffed_"] = num_lines_sniffed
    cmd["quotechar_"] = quotechar
    cmd["sep_"] = sep
    cmd["skip_"] = skip
    cmd["conn_id_"] = conn.conn_id

    if colnames is not None:
        cmd["colnames_"] = colnames

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        sock.close()
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    stmt = comm.recv_string(sock)

    sock.close()

    return stmt


# -----------------------------------------------------------------------------


def sniff_s3(
    name,
    bucket,
    keys,
    region,
    num_lines_sniffed=1000,
    sep=",",
    skip=0,
    colnames=None,
    conn=None,
):
    """
    Sniffs a list of CSV files located in an S3 bucket.

    Args:
        name (str): Name of the table in which the data is to be inserted.

        bucket (str):
            The bucket from which to read the files.

        keys (List[str]): The list of keys (files in the bucket) to be read.

        region (str):
            The region in which the bucket is located.

        num_lines_sniffed (int, optional):
            Number of lines analysed by the sniffer.

        sep (str, optional):
            The character used for separating fields.

        skip (int, optional):
            Number of lines to skip at the beginning of each file.

        colnames(List[str] or None, optional): The first line of a CSV file
            usually contains the column names. When this is not the case, you need to
            explicitly pass them.

        conn (:class:`~getml.database.Connection`, optional): The database connection to be used.
            If you don't explicitly pass a connection, the engine will use the default connection.

    Returns:
        str: Appropriate `CREATE TABLE` statement.

    Example:
        Let's assume you have two CSV files - *file1.csv* and
        *file2.csv* - in the bucket. You can
        import their data into the getML engine using the following
        commands:

        >>> getml.engine.set_s3_access_key_id("YOUR-ACCESS-KEY-ID")
        >>>
        >>> getml.engine.set_s3_secret_access_key("YOUR-SECRET-ACCESS-KEY")
        >>>
        >>> stmt = data.database.sniff_s3(
        ...         bucket="your-bucket-name",
        ...         keys=["file1.csv", "file2.csv"],
        ...         region="us-east-2",
        ...         name="MY_TABLE",
        ...         sep=';'
        ... )

        You can also set the access credential as environment variables
        before you launch the getML engine.
    """
    # -------------------------------------------

    conn = conn or Connection()

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = name
    cmd["type_"] = "Database.sniff_s3"

    cmd["bucket_"] = bucket
    cmd["keys_"] = keys
    cmd["num_lines_sniffed_"] = num_lines_sniffed
    cmd["region_"] = region
    cmd["sep_"] = sep
    cmd["skip_"] = skip
    cmd["conn_id_"] = conn.conn_id

    if colnames is not None:
        cmd["colnames_"] = colnames

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_receive_socket(cmd)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        sock.close()
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    stmt = comm.recv_string(sock)

    sock.close()

    return stmt


# -----------------------------------------------------------------------------
