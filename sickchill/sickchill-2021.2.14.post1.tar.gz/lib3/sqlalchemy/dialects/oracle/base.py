# oracle/base.py
# Copyright (C) 2005-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

r"""
.. dialect:: oracle
    :name: Oracle

    Oracle version 8 through current (11g at the time of this writing) are
    supported.


Auto Increment Behavior
-----------------------

SQLAlchemy Table objects which include integer primary keys are usually
assumed to have "autoincrementing" behavior, meaning they can generate their
own primary key values upon INSERT.  Since Oracle has no "autoincrement"
feature, SQLAlchemy relies upon sequences to produce these values.   With the
Oracle dialect, *a sequence must always be explicitly specified to enable
autoincrement*.  This is divergent with the majority of documentation
examples which assume the usage of an autoincrement-capable database.   To
specify sequences, use the sqlalchemy.schema.Sequence object which is passed
to a Column construct::

  t = Table('mytable', metadata,
        Column('id', Integer, Sequence('id_seq'), primary_key=True),
        Column(...), ...
  )

This step is also required when using table reflection, i.e. autoload=True::

  t = Table('mytable', metadata,
        Column('id', Integer, Sequence('id_seq'), primary_key=True),
        autoload=True
  )

Transaction Isolation Level / Autocommit
----------------------------------------

The Oracle database supports "READ COMMITTED" and "SERIALIZABLE" modes
of isolation, however the SQLAlchemy Oracle dialect currently only has
explicit support for "READ COMMITTED".  It is possible to emit a
"SET TRANSACTION" statement on a connection in order to use SERIALIZABLE
isolation, however the SQLAlchemy dialect will remain unaware of this setting,
such as if the :meth:`_engine.Connection.get_isolation_level` method is used;
this method is hardcoded to return "READ COMMITTED" right now.

The AUTOCOMMIT isolation level is also supported by the cx_Oracle dialect.

To set using per-connection execution options::

    connection = engine.connect()
    connection = connection.execution_options(
        isolation_level="AUTOCOMMIT"
    )

Valid values for ``isolation_level`` include:

* ``READ COMMITTED``
* ``AUTOCOMMIT``


.. versionadded:: 1.3.16 added support for AUTOCOMMIT to the cx_oracle dialect
   as well as the notion of a default isolation level, currently hardcoded
   to "READ COMMITTED".

.. seealso::

    :ref:`dbapi_autocommit`

Identifier Casing
-----------------

In Oracle, the data dictionary represents all case insensitive identifier
names using UPPERCASE text.   SQLAlchemy on the other hand considers an
all-lower case identifier name to be case insensitive.   The Oracle dialect
converts all case insensitive identifiers to and from those two formats during
schema level communication, such as reflection of tables and indexes.   Using
an UPPERCASE name on the SQLAlchemy side indicates a case sensitive
identifier, and SQLAlchemy will quote the name - this will cause mismatches
against data dictionary data received from Oracle, so unless identifier names
have been truly created as case sensitive (i.e. using quoted names), all
lowercase names should be used on the SQLAlchemy side.

.. _oracle_max_identifier_lengths:

Max Identifier Lengths
----------------------

Oracle has changed the default max identifier length as of Oracle Server
version 12.2.   Prior to this version, the length was 30, and for 12.2 and
greater it is now 128.   This change impacts SQLAlchemy in the area of
generated SQL label names as well as the generation of constraint names,
particularly in the case where the constraint naming convention feature
described at :ref:`constraint_naming_conventions` is being used.

To assist with this change and others, Oracle includes the concept of a
"compatibility" version, which is a version number that is independent of the
actual server version in order to assist with migration of Oracle databases,
and may be configured within the Oracle server itself. This compatibility
version is retrieved using the query  ``SELECT value FROM v$parameter WHERE
name = 'compatible';``.   The SQLAlchemy Oracle dialect, when tasked with
determining the default max identifier length, will attempt to use this query
upon first connect in order to determine the effective compatibility version of
the server, which determines what the maximum allowed identifier length is for
the server.  If the table is not available, the  server version information is
used instead.

For the duration of the SQLAlchemy 1.3 series, the default max identifier
length will remain at 30, even if compatibility version 12.2 or greater is in
use.  When the newer version is detected, a warning will be emitted upon first
connect, which refers the user to make use of the
:paramref:`_sa.create_engine.max_identifier_length`
parameter in order to assure
forwards compatibility with SQLAlchemy 1.4, which will be changing this value
to 128 when compatibility version 12.2 or greater is detected.

Using :paramref:`_sa.create_engine.max_identifier_length`,
the effective identifier
length used by the SQLAlchemy dialect will be used as given, overriding the
current default value of 30, so that when Oracle 12.2 or greater is used, the
newer identifier length may be taken advantage of::

    engine = create_engine(
        "oracle+cx_oracle://scott:tiger@oracle122",
        max_identifier_length=128)

The maximum identifier length comes into play both when generating anonymized
SQL labels in SELECT statements, but more crucially when generating constraint
names from a naming convention.  It is this area that has created the need for
SQLAlchemy to change this default conservatively.   For example, the following
naming convention produces two very different constraint names based on the
identifier length::

    from sqlalchemy import Column
    from sqlalchemy import Index
    from sqlalchemy import Integer
    from sqlalchemy import MetaData
    from sqlalchemy import Table
    from sqlalchemy.dialects import oracle
    from sqlalchemy.schema import CreateIndex

    m = MetaData(naming_convention={"ix": "ix_%(column_0N_name)s"})

    t = Table(
        "t",
        m,
        Column("some_column_name_1", Integer),
        Column("some_column_name_2", Integer),
        Column("some_column_name_3", Integer),
    )

    ix = Index(
        None,
        t.c.some_column_name_1,
        t.c.some_column_name_2,
        t.c.some_column_name_3,
    )

    oracle_dialect = oracle.dialect(max_identifier_length=30)
    print(CreateIndex(ix).compile(dialect=oracle_dialect))

With an identifier length of 30, the above CREATE INDEX looks like::

    CREATE INDEX ix_some_column_name_1s_70cd ON t
    (some_column_name_1, some_column_name_2, some_column_name_3)

However with length=128, it becomes::

    CREATE INDEX ix_some_column_name_1some_column_name_2some_column_name_3 ON t
    (some_column_name_1, some_column_name_2, some_column_name_3)

The implication here is that by upgrading SQLAlchemy to version 1.4 on
an existing Oracle 12.2 or greater database, the generation of constraint
names will change, which can impact the behavior of database migrations.
A key example is a migration that wishes to "DROP CONSTRAINT" on a name that
was previously generated with the shorter length.  This migration will fail
when the identifier length is changed without the name of the index or
constraint first being adjusted.

Therefore, applications are strongly advised to make use of
:paramref:`_sa.create_engine.max_identifier_length`
in order to maintain control
of the generation of truncated names, and to fully review and test all database
migrations in a staging environment when changing this value to ensure that the
impact of this change has been mitigated.


.. versionadded:: 1.3.9 Added the
   :paramref:`_sa.create_engine.max_identifier_length` parameter; the Oracle
   dialect now detects compatibility version 12.2 or greater and warns
   about upcoming max identitifier length changes in SQLAlchemy 1.4.


LIMIT/OFFSET Support
--------------------

Oracle has no support for the LIMIT or OFFSET keywords.  SQLAlchemy uses
a wrapped subquery approach in conjunction with ROWNUM.  The exact methodology
is taken from
http://www.oracle.com/technetwork/issue-archive/2006/06-sep/o56asktom-086197.html .

There are two options which affect its behavior:

* the "FIRST ROWS()" optimization keyword is not used by default.  To enable
  the usage of this optimization directive, specify ``optimize_limits=True``
  to :func:`_sa.create_engine`.
* the values passed for the limit/offset are sent as bound parameters.   Some
  users have observed that Oracle produces a poor query plan when the values
  are sent as binds and not rendered literally.   To render the limit/offset
  values literally within the SQL statement, specify
  ``use_binds_for_limits=False`` to :func:`_sa.create_engine`.

Some users have reported better performance when the entirely different
approach of a window query is used, i.e. ROW_NUMBER() OVER (ORDER BY), to
provide LIMIT/OFFSET (note that the majority of users don't observe this).
To suit this case the method used for LIMIT/OFFSET can be replaced entirely.
See the recipe at
http://www.sqlalchemy.org/trac/wiki/UsageRecipes/WindowFunctionsByDefault
which installs a select compiler that overrides the generation of limit/offset
with a window function.

.. _oracle_returning:

RETURNING Support
-----------------

The Oracle database supports a limited form of RETURNING, in order to retrieve
result sets of matched rows from INSERT, UPDATE and DELETE statements.
Oracle's RETURNING..INTO syntax only supports one row being returned, as it
relies upon OUT parameters in order to function.  In addition, supported
DBAPIs have further limitations (see :ref:`cx_oracle_returning`).

SQLAlchemy's "implicit returning" feature, which employs RETURNING within an
INSERT and sometimes an UPDATE statement in order to fetch newly generated
primary key values and other SQL defaults and expressions, is normally enabled
on the Oracle backend.  By default, "implicit returning" typically only
fetches the value of a single ``nextval(some_seq)`` expression embedded into
an INSERT in order to increment a sequence within an INSERT statement and get
the value back at the same time. To disable this feature across the board,
specify ``implicit_returning=False`` to :func:`_sa.create_engine`::

    engine = create_engine("oracle://scott:tiger@dsn",
                           implicit_returning=False)

Implicit returning can also be disabled on a table-by-table basis as a table
option::

    # Core Table
    my_table = Table("my_table", metadata, ..., implicit_returning=False)


    # declarative
    class MyClass(Base):
        __tablename__ = 'my_table'
        __table_args__ = {"implicit_returning": False}

.. seealso::

    :ref:`cx_oracle_returning` - additional cx_oracle-specific restrictions on
    implicit returning.

ON UPDATE CASCADE
-----------------

Oracle doesn't have native ON UPDATE CASCADE functionality.  A trigger based
solution is available at
http://asktom.oracle.com/tkyte/update_cascade/index.html .

When using the SQLAlchemy ORM, the ORM has limited ability to manually issue
cascading updates - specify ForeignKey objects using the
"deferrable=True, initially='deferred'" keyword arguments,
and specify "passive_updates=False" on each relationship().

Oracle 8 Compatibility
----------------------

When Oracle 8 is detected, the dialect internally configures itself to the
following behaviors:

* the use_ansi flag is set to False.  This has the effect of converting all
  JOIN phrases into the WHERE clause, and in the case of LEFT OUTER JOIN
  makes use of Oracle's (+) operator.

* the NVARCHAR2 and NCLOB datatypes are no longer generated as DDL when
  the :class:`~sqlalchemy.types.Unicode` is used - VARCHAR2 and CLOB are
  issued instead.   This because these types don't seem to work correctly on
  Oracle 8 even though they are available.  The
  :class:`~sqlalchemy.types.NVARCHAR` and
  :class:`~sqlalchemy.dialects.oracle.NCLOB` types will always generate
  NVARCHAR2 and NCLOB.

* the "native unicode" mode is disabled when using cx_oracle, i.e. SQLAlchemy
  encodes all Python unicode objects to "string" before passing in as bind
  parameters.

Synonym/DBLINK Reflection
-------------------------

When using reflection with Table objects, the dialect can optionally search
for tables indicated by synonyms, either in local or remote schemas or
accessed over DBLINK, by passing the flag ``oracle_resolve_synonyms=True`` as
a keyword argument to the :class:`_schema.Table` construct::

    some_table = Table('some_table', autoload=True,
                                autoload_with=some_engine,
                                oracle_resolve_synonyms=True)

When this flag is set, the given name (such as ``some_table`` above) will
be searched not just in the ``ALL_TABLES`` view, but also within the
``ALL_SYNONYMS`` view to see if this name is actually a synonym to another
name.  If the synonym is located and refers to a DBLINK, the oracle dialect
knows how to locate the table's information using DBLINK syntax(e.g.
``@dblink``).

``oracle_resolve_synonyms`` is accepted wherever reflection arguments are
accepted, including methods such as :meth:`_schema.MetaData.reflect` and
:meth:`_reflection.Inspector.get_columns`.

If synonyms are not in use, this flag should be left disabled.

.. _oracle_constraint_reflection:

Constraint Reflection
---------------------

The Oracle dialect can return information about foreign key, unique, and
CHECK constraints, as well as indexes on tables.

Raw information regarding these constraints can be acquired using
:meth:`_reflection.Inspector.get_foreign_keys`,
:meth:`_reflection.Inspector.get_unique_constraints`,
:meth:`_reflection.Inspector.get_check_constraints`, and
:meth:`_reflection.Inspector.get_indexes`.

.. versionchanged:: 1.2  The Oracle dialect can now reflect UNIQUE and
   CHECK constraints.

When using reflection at the :class:`_schema.Table` level, the
:class:`_schema.Table`
will also include these constraints.

Note the following caveats:

* When using the :meth:`_reflection.Inspector.get_check_constraints` method,
  Oracle
  builds a special "IS NOT NULL" constraint for columns that specify
  "NOT NULL".  This constraint is **not** returned by default; to include
  the "IS NOT NULL" constraints, pass the flag ``include_all=True``::

      from sqlalchemy import create_engine, inspect

      engine = create_engine("oracle+cx_oracle://s:t@dsn")
      inspector = inspect(engine)
      all_check_constraints = inspector.get_check_constraints(
          "some_table", include_all=True)

* in most cases, when reflecting a :class:`_schema.Table`,
  a UNIQUE constraint will
  **not** be available as a :class:`.UniqueConstraint` object, as Oracle
  mirrors unique constraints with a UNIQUE index in most cases (the exception
  seems to be when two or more unique constraints represent the same columns);
  the :class:`_schema.Table` will instead represent these using
  :class:`.Index`
  with the ``unique=True`` flag set.

* Oracle creates an implicit index for the primary key of a table; this index
  is **excluded** from all index results.

* the list of columns reflected for an index will not include column names
  that start with SYS_NC.

Table names with SYSTEM/SYSAUX tablespaces
-------------------------------------------

The :meth:`_reflection.Inspector.get_table_names` and
:meth:`_reflection.Inspector.get_temp_table_names`
methods each return a list of table names for the current engine. These methods
are also part of the reflection which occurs within an operation such as
:meth:`_schema.MetaData.reflect`.  By default,
these operations exclude the ``SYSTEM``
and ``SYSAUX`` tablespaces from the operation.   In order to change this, the
default list of tablespaces excluded can be changed at the engine level using
the ``exclude_tablespaces`` parameter::

    # exclude SYSAUX and SOME_TABLESPACE, but not SYSTEM
    e = create_engine(
      "oracle://scott:tiger@xe",
      exclude_tablespaces=["SYSAUX", "SOME_TABLESPACE"])

.. versionadded:: 1.1

DateTime Compatibility
----------------------

Oracle has no datatype known as ``DATETIME``, it instead has only ``DATE``,
which can actually store a date and time value.  For this reason, the Oracle
dialect provides a type :class:`_oracle.DATE` which is a subclass of
:class:`.DateTime`.   This type has no special behavior, and is only
present as a "marker" for this type; additionally, when a database column
is reflected and the type is reported as ``DATE``, the time-supporting
:class:`_oracle.DATE` type is used.

.. versionchanged:: 0.9.4 Added :class:`_oracle.DATE` to subclass
   :class:`.DateTime`.  This is a change as previous versions
   would reflect a ``DATE`` column as :class:`_types.DATE`, which subclasses
   :class:`.Date`.   The only significance here is for schemes that are
   examining the type of column for use in special Python translations or
   for migrating schemas to other database backends.

.. _oracle_table_options:

Oracle Table Options
-------------------------

The CREATE TABLE phrase supports the following options with Oracle
in conjunction with the :class:`_schema.Table` construct:


* ``ON COMMIT``::

    Table(
        "some_table", metadata, ...,
        prefixes=['GLOBAL TEMPORARY'], oracle_on_commit='PRESERVE ROWS')

.. versionadded:: 1.0.0

* ``COMPRESS``::

    Table('mytable', metadata, Column('data', String(32)),
        oracle_compress=True)

    Table('mytable', metadata, Column('data', String(32)),
        oracle_compress=6)

   The ``oracle_compress`` parameter accepts either an integer compression
   level, or ``True`` to use the default compression level.

.. versionadded:: 1.0.0

.. _oracle_index_options:

Oracle Specific Index Options
-----------------------------

Bitmap Indexes
~~~~~~~~~~~~~~

You can specify the ``oracle_bitmap`` parameter to create a bitmap index
instead of a B-tree index::

    Index('my_index', my_table.c.data, oracle_bitmap=True)

Bitmap indexes cannot be unique and cannot be compressed. SQLAlchemy will not
check for such limitations, only the database will.

.. versionadded:: 1.0.0

Index compression
~~~~~~~~~~~~~~~~~

Oracle has a more efficient storage mode for indexes containing lots of
repeated values. Use the ``oracle_compress`` parameter to turn on key
compression::

    Index('my_index', my_table.c.data, oracle_compress=True)

    Index('my_index', my_table.c.data1, my_table.c.data2, unique=True,
           oracle_compress=1)

The ``oracle_compress`` parameter accepts either an integer specifying the
number of prefix columns to compress, or ``True`` to use the default (all
columns for non-unique indexes, all but the last column for unique indexes).

.. versionadded:: 1.0.0

"""  # noqa

from itertools import groupby
import re

from ... import Computed
from ... import exc
from ... import schema as sa_schema
from ... import sql
from ... import types as sqltypes
from ... import util
from ...engine import default
from ...engine import reflection
from ...sql import compiler
from ...sql import expression
from ...sql import util as sql_util
from ...sql import visitors
from ...types import BLOB
from ...types import CHAR
from ...types import CLOB
from ...types import FLOAT
from ...types import INTEGER
from ...types import NCHAR
from ...types import NVARCHAR
from ...types import TIMESTAMP
from ...types import VARCHAR


RESERVED_WORDS = set(
    "SHARE RAW DROP BETWEEN FROM DESC OPTION PRIOR LONG THEN "
    "DEFAULT ALTER IS INTO MINUS INTEGER NUMBER GRANT IDENTIFIED "
    "ALL TO ORDER ON FLOAT DATE HAVING CLUSTER NOWAIT RESOURCE "
    "ANY TABLE INDEX FOR UPDATE WHERE CHECK SMALLINT WITH DELETE "
    "BY ASC REVOKE LIKE SIZE RENAME NOCOMPRESS NULL GROUP VALUES "
    "AS IN VIEW EXCLUSIVE COMPRESS SYNONYM SELECT INSERT EXISTS "
    "NOT TRIGGER ELSE CREATE INTERSECT PCTFREE DISTINCT USER "
    "CONNECT SET MODE OF UNIQUE VARCHAR2 VARCHAR LOCK OR CHAR "
    "DECIMAL UNION PUBLIC AND START UID COMMENT CURRENT LEVEL".split()
)

NO_ARG_FNS = set(
    "UID CURRENT_DATE SYSDATE USER " "CURRENT_TIME CURRENT_TIMESTAMP".split()
)


class RAW(sqltypes._Binary):
    __visit_name__ = "RAW"


OracleRaw = RAW


class NCLOB(sqltypes.Text):
    __visit_name__ = "NCLOB"


class VARCHAR2(VARCHAR):
    __visit_name__ = "VARCHAR2"


NVARCHAR2 = NVARCHAR


class NUMBER(sqltypes.Numeric, sqltypes.Integer):
    __visit_name__ = "NUMBER"

    def __init__(self, precision=None, scale=None, asdecimal=None):
        if asdecimal is None:
            asdecimal = bool(scale and scale > 0)

        super(NUMBER, self).__init__(
            precision=precision, scale=scale, asdecimal=asdecimal
        )

    def adapt(self, impltype):
        ret = super(NUMBER, self).adapt(impltype)
        # leave a hint for the DBAPI handler
        ret._is_oracle_number = True
        return ret

    @property
    def _type_affinity(self):
        if bool(self.scale and self.scale > 0):
            return sqltypes.Numeric
        else:
            return sqltypes.Integer


class DOUBLE_PRECISION(sqltypes.Float):
    __visit_name__ = "DOUBLE_PRECISION"


class BINARY_DOUBLE(sqltypes.Float):
    __visit_name__ = "BINARY_DOUBLE"


class BINARY_FLOAT(sqltypes.Float):
    __visit_name__ = "BINARY_FLOAT"


class BFILE(sqltypes.LargeBinary):
    __visit_name__ = "BFILE"


class LONG(sqltypes.Text):
    __visit_name__ = "LONG"


class DATE(sqltypes.DateTime):
    """Provide the oracle DATE type.

    This type has no special Python behavior, except that it subclasses
    :class:`_types.DateTime`; this is to suit the fact that the Oracle
    ``DATE`` type supports a time value.

    .. versionadded:: 0.9.4

    """

    __visit_name__ = "DATE"

    def _compare_type_affinity(self, other):
        return other._type_affinity in (sqltypes.DateTime, sqltypes.Date)


class INTERVAL(sqltypes.TypeEngine):
    __visit_name__ = "INTERVAL"

    def __init__(self, day_precision=None, second_precision=None):
        """Construct an INTERVAL.

        Note that only DAY TO SECOND intervals are currently supported.
        This is due to a lack of support for YEAR TO MONTH intervals
        within available DBAPIs (cx_oracle and zxjdbc).

        :param day_precision: the day precision value.  this is the number of
          digits to store for the day field.  Defaults to "2"
        :param second_precision: the second precision value.  this is the
          number of digits to store for the fractional seconds field.
          Defaults to "6".

        """
        self.day_precision = day_precision
        self.second_precision = second_precision

    @classmethod
    def _adapt_from_generic_interval(cls, interval):
        return INTERVAL(
            day_precision=interval.day_precision,
            second_precision=interval.second_precision,
        )

    @property
    def _type_affinity(self):
        return sqltypes.Interval


class ROWID(sqltypes.TypeEngine):
    """Oracle ROWID type.

    When used in a cast() or similar, generates ROWID.

    """

    __visit_name__ = "ROWID"


class _OracleBoolean(sqltypes.Boolean):
    def get_dbapi_type(self, dbapi):
        return dbapi.NUMBER


colspecs = {
    sqltypes.Boolean: _OracleBoolean,
    sqltypes.Interval: INTERVAL,
    sqltypes.DateTime: DATE,
}

ischema_names = {
    "VARCHAR2": VARCHAR,
    "NVARCHAR2": NVARCHAR,
    "CHAR": CHAR,
    "NCHAR": NCHAR,
    "DATE": DATE,
    "NUMBER": NUMBER,
    "BLOB": BLOB,
    "BFILE": BFILE,
    "CLOB": CLOB,
    "NCLOB": NCLOB,
    "TIMESTAMP": TIMESTAMP,
    "TIMESTAMP WITH TIME ZONE": TIMESTAMP,
    "INTERVAL DAY TO SECOND": INTERVAL,
    "RAW": RAW,
    "FLOAT": FLOAT,
    "DOUBLE PRECISION": DOUBLE_PRECISION,
    "LONG": LONG,
    "BINARY_DOUBLE": BINARY_DOUBLE,
    "BINARY_FLOAT": BINARY_FLOAT,
}


class OracleTypeCompiler(compiler.GenericTypeCompiler):
    # Note:
    # Oracle DATE == DATETIME
    # Oracle does not allow milliseconds in DATE
    # Oracle does not support TIME columns

    def visit_datetime(self, type_, **kw):
        return self.visit_DATE(type_, **kw)

    def visit_float(self, type_, **kw):
        return self.visit_FLOAT(type_, **kw)

    def visit_unicode(self, type_, **kw):
        if self.dialect._use_nchar_for_unicode:
            return self.visit_NVARCHAR2(type_, **kw)
        else:
            return self.visit_VARCHAR2(type_, **kw)

    def visit_INTERVAL(self, type_, **kw):
        return "INTERVAL DAY%s TO SECOND%s" % (
            type_.day_precision is not None
            and "(%d)" % type_.day_precision
            or "",
            type_.second_precision is not None
            and "(%d)" % type_.second_precision
            or "",
        )

    def visit_LONG(self, type_, **kw):
        return "LONG"

    def visit_TIMESTAMP(self, type_, **kw):
        if type_.timezone:
            return "TIMESTAMP WITH TIME ZONE"
        else:
            return "TIMESTAMP"

    def visit_DOUBLE_PRECISION(self, type_, **kw):
        return self._generate_numeric(type_, "DOUBLE PRECISION", **kw)

    def visit_BINARY_DOUBLE(self, type_, **kw):
        return self._generate_numeric(type_, "BINARY_DOUBLE", **kw)

    def visit_BINARY_FLOAT(self, type_, **kw):
        return self._generate_numeric(type_, "BINARY_FLOAT", **kw)

    def visit_FLOAT(self, type_, **kw):
        # don't support conversion between decimal/binary
        # precision yet
        kw["no_precision"] = True
        return self._generate_numeric(type_, "FLOAT", **kw)

    def visit_NUMBER(self, type_, **kw):
        return self._generate_numeric(type_, "NUMBER", **kw)

    def _generate_numeric(
        self, type_, name, precision=None, scale=None, no_precision=False, **kw
    ):
        if precision is None:
            precision = type_.precision

        if scale is None:
            scale = getattr(type_, "scale", None)

        if no_precision or precision is None:
            return name
        elif scale is None:
            n = "%(name)s(%(precision)s)"
            return n % {"name": name, "precision": precision}
        else:
            n = "%(name)s(%(precision)s, %(scale)s)"
            return n % {"name": name, "precision": precision, "scale": scale}

    def visit_string(self, type_, **kw):
        return self.visit_VARCHAR2(type_, **kw)

    def visit_VARCHAR2(self, type_, **kw):
        return self._visit_varchar(type_, "", "2")

    def visit_NVARCHAR2(self, type_, **kw):
        return self._visit_varchar(type_, "N", "2")

    visit_NVARCHAR = visit_NVARCHAR2

    def visit_VARCHAR(self, type_, **kw):
        return self._visit_varchar(type_, "", "")

    def _visit_varchar(self, type_, n, num):
        if not type_.length:
            return "%(n)sVARCHAR%(two)s" % {"two": num, "n": n}
        elif not n and self.dialect._supports_char_length:
            varchar = "VARCHAR%(two)s(%(length)s CHAR)"
            return varchar % {"length": type_.length, "two": num}
        else:
            varchar = "%(n)sVARCHAR%(two)s(%(length)s)"
            return varchar % {"length": type_.length, "two": num, "n": n}

    def visit_text(self, type_, **kw):
        return self.visit_CLOB(type_, **kw)

    def visit_unicode_text(self, type_, **kw):
        if self.dialect._use_nchar_for_unicode:
            return self.visit_NCLOB(type_, **kw)
        else:
            return self.visit_CLOB(type_, **kw)

    def visit_large_binary(self, type_, **kw):
        return self.visit_BLOB(type_, **kw)

    def visit_big_integer(self, type_, **kw):
        return self.visit_NUMBER(type_, precision=19, **kw)

    def visit_boolean(self, type_, **kw):
        return self.visit_SMALLINT(type_, **kw)

    def visit_RAW(self, type_, **kw):
        if type_.length:
            return "RAW(%(length)s)" % {"length": type_.length}
        else:
            return "RAW"

    def visit_ROWID(self, type_, **kw):
        return "ROWID"


class OracleCompiler(compiler.SQLCompiler):
    """Oracle compiler modifies the lexical structure of Select
    statements to work under non-ANSI configured Oracle databases, if
    the use_ansi flag is False.
    """

    compound_keywords = util.update_copy(
        compiler.SQLCompiler.compound_keywords,
        {expression.CompoundSelect.EXCEPT: "MINUS"},
    )

    def __init__(self, *args, **kwargs):
        self.__wheres = {}
        self._quoted_bind_names = {}
        super(OracleCompiler, self).__init__(*args, **kwargs)

    def visit_mod_binary(self, binary, operator, **kw):
        return "mod(%s, %s)" % (
            self.process(binary.left, **kw),
            self.process(binary.right, **kw),
        )

    def visit_now_func(self, fn, **kw):
        return "CURRENT_TIMESTAMP"

    def visit_char_length_func(self, fn, **kw):
        return "LENGTH" + self.function_argspec(fn, **kw)

    def visit_match_op_binary(self, binary, operator, **kw):
        return "CONTAINS (%s, %s)" % (
            self.process(binary.left),
            self.process(binary.right),
        )

    def visit_true(self, expr, **kw):
        return "1"

    def visit_false(self, expr, **kw):
        return "0"

    def get_cte_preamble(self, recursive):
        return "WITH"

    def get_select_hint_text(self, byfroms):
        return " ".join("/*+ %s */" % text for table, text in byfroms.items())

    def function_argspec(self, fn, **kw):
        if len(fn.clauses) > 0 or fn.name.upper() not in NO_ARG_FNS:
            return compiler.SQLCompiler.function_argspec(self, fn, **kw)
        else:
            return ""

    def default_from(self):
        """Called when a ``SELECT`` statement has no froms,
        and no ``FROM`` clause is to be appended.

        The Oracle compiler tacks a "FROM DUAL" to the statement.
        """

        return " FROM DUAL"

    def visit_join(self, join, **kwargs):
        if self.dialect.use_ansi:
            return compiler.SQLCompiler.visit_join(self, join, **kwargs)
        else:
            kwargs["asfrom"] = True
            if isinstance(join.right, expression.FromGrouping):
                right = join.right.element
            else:
                right = join.right
            return (
                self.process(join.left, **kwargs)
                + ", "
                + self.process(right, **kwargs)
            )

    def _get_nonansi_join_whereclause(self, froms):
        clauses = []

        def visit_join(join):
            if join.isouter:
                # https://docs.oracle.com/database/121/SQLRF/queries006.htm#SQLRF52354
                # "apply the outer join operator (+) to all columns of B in
                # the join condition in the WHERE clause" - that is,
                # unconditionally regardless of operator or the other side
                def visit_binary(binary):
                    if isinstance(
                        binary.left, expression.ColumnClause
                    ) and join.right.is_derived_from(binary.left.table):
                        binary.left = _OuterJoinColumn(binary.left)
                    elif isinstance(
                        binary.right, expression.ColumnClause
                    ) and join.right.is_derived_from(binary.right.table):
                        binary.right = _OuterJoinColumn(binary.right)

                clauses.append(
                    visitors.cloned_traverse(
                        join.onclause, {}, {"binary": visit_binary}
                    )
                )
            else:
                clauses.append(join.onclause)

            for j in join.left, join.right:
                if isinstance(j, expression.Join):
                    visit_join(j)
                elif isinstance(j, expression.FromGrouping):
                    visit_join(j.element)

        for f in froms:
            if isinstance(f, expression.Join):
                visit_join(f)

        if not clauses:
            return None
        else:
            return sql.and_(*clauses)

    def visit_outer_join_column(self, vc, **kw):
        return self.process(vc.column, **kw) + "(+)"

    def visit_sequence(self, seq, **kw):
        return (
            self.dialect.identifier_preparer.format_sequence(seq) + ".nextval"
        )

    def get_render_as_alias_suffix(self, alias_name_text):
        """Oracle doesn't like ``FROM table AS alias``"""

        return " " + alias_name_text

    def returning_clause(self, stmt, returning_cols):
        columns = []
        binds = []

        for i, column in enumerate(
            expression._select_iterables(returning_cols)
        ):
            if self.isupdate and isinstance(column.server_default, Computed):
                util.warn(
                    "Computed columns don't work with Oracle UPDATE "
                    "statements that use RETURNING; the value of the column "
                    "*before* the UPDATE takes place is returned.   It is "
                    "advised to not use RETURNING with an Oracle computed "
                    "column.  Consider setting implicit_returning to False on "
                    "the Table object in order to avoid implicit RETURNING "
                    "clauses from being generated for this Table."
                )
            if column.type._has_column_expression:
                col_expr = column.type.column_expression(column)
            else:
                col_expr = column

            outparam = sql.outparam("ret_%d" % i, type_=column.type)
            self.binds[outparam.key] = outparam
            binds.append(
                self.bindparam_string(self._truncate_bindparam(outparam))
            )
            columns.append(self.process(col_expr, within_columns_clause=False))

            self._add_to_result_map(
                getattr(col_expr, "name", col_expr.anon_label),
                getattr(col_expr, "name", col_expr.anon_label),
                (
                    column,
                    getattr(column, "name", None),
                    getattr(column, "key", None),
                ),
                column.type,
            )

        return "RETURNING " + ", ".join(columns) + " INTO " + ", ".join(binds)

    def _TODO_visit_compound_select(self, select):
        """Need to determine how to get ``LIMIT``/``OFFSET`` into a
        ``UNION`` for Oracle.
        """
        pass

    def visit_select(self, select, **kwargs):
        """Look for ``LIMIT`` and OFFSET in a select statement, and if
        so tries to wrap it in a subquery with ``rownum`` criterion.
        """

        if not getattr(select, "_oracle_visit", None):
            if not self.dialect.use_ansi:
                froms = self._display_froms_for_select(
                    select, kwargs.get("asfrom", False)
                )
                whereclause = self._get_nonansi_join_whereclause(froms)
                if whereclause is not None:
                    select = select.where(whereclause)
                    select._oracle_visit = True

            limit_clause = select._limit_clause
            offset_clause = select._offset_clause
            if limit_clause is not None or offset_clause is not None:
                # See http://www.oracle.com/technology/oramag/oracle/06-sep/\
                # o56asktom.html
                #
                # Generalized form of an Oracle pagination query:
                #   select ... from (
                #     select /*+ FIRST_ROWS(N) */ ...., rownum as ora_rn from
                #       (  select distinct ... where ... order by ...
                #     ) where ROWNUM <= :limit+:offset
                #   ) where ora_rn > :offset
                # Outer select and "ROWNUM as ora_rn" can be dropped if
                # limit=0

                kwargs["select_wraps_for"] = select
                select = select._generate()
                select._oracle_visit = True

                # Wrap the middle select and add the hint
                limitselect = sql.select([c for c in select.c])
                if (
                    limit_clause is not None
                    and self.dialect.optimize_limits
                    and select._simple_int_limit
                ):
                    limitselect = limitselect.prefix_with(
                        "/*+ FIRST_ROWS(%d) */" % select._limit
                    )

                limitselect._oracle_visit = True
                limitselect._is_wrapper = True

                # add expressions to accommodate FOR UPDATE OF
                for_update = select._for_update_arg
                if for_update is not None and for_update.of:
                    for_update = for_update._clone()
                    for_update._copy_internals()

                    for elem in for_update.of:
                        select.append_column(elem)

                    adapter = sql_util.ClauseAdapter(select)
                    for_update.of = [
                        adapter.traverse(elem) for elem in for_update.of
                    ]

                # If needed, add the limiting clause
                if limit_clause is not None:
                    if not self.dialect.use_binds_for_limits:
                        # use simple int limits, will raise an exception
                        # if the limit isn't specified this way
                        max_row = select._limit

                        if offset_clause is not None:
                            max_row += select._offset
                        max_row = sql.literal_column("%d" % max_row)
                    else:
                        max_row = limit_clause
                        if offset_clause is not None:
                            max_row = max_row + offset_clause
                    limitselect.append_whereclause(
                        sql.literal_column("ROWNUM") <= max_row
                    )

                # If needed, add the ora_rn, and wrap again with offset.
                if offset_clause is None:
                    limitselect._for_update_arg = for_update
                    select = limitselect
                else:
                    limitselect = limitselect.column(
                        sql.literal_column("ROWNUM").label("ora_rn")
                    )
                    limitselect._oracle_visit = True
                    limitselect._is_wrapper = True

                    offsetselect = sql.select(
                        [c for c in limitselect.c if c.key != "ora_rn"]
                    )
                    offsetselect._oracle_visit = True
                    offsetselect._is_wrapper = True

                    if for_update is not None and for_update.of:
                        for elem in for_update.of:
                            if limitselect.corresponding_column(elem) is None:
                                limitselect.append_column(elem)

                    if not self.dialect.use_binds_for_limits:
                        offset_clause = sql.literal_column(
                            "%d" % select._offset
                        )
                    offsetselect.append_whereclause(
                        sql.literal_column("ora_rn") > offset_clause
                    )

                    offsetselect._for_update_arg = for_update
                    select = offsetselect

        return compiler.SQLCompiler.visit_select(self, select, **kwargs)

    def limit_clause(self, select, **kw):
        return ""

    def visit_empty_set_expr(self, type_):
        return "SELECT 1 FROM DUAL WHERE 1!=1"

    def for_update_clause(self, select, **kw):
        if self.is_subquery():
            return ""

        tmp = " FOR UPDATE"

        if select._for_update_arg.of:
            tmp += " OF " + ", ".join(
                self.process(elem, **kw) for elem in select._for_update_arg.of
            )

        if select._for_update_arg.nowait:
            tmp += " NOWAIT"
        if select._for_update_arg.skip_locked:
            tmp += " SKIP LOCKED"

        return tmp

    def visit_is_distinct_from_binary(self, binary, operator, **kw):
        return "DECODE(%s, %s, 0, 1) = 1" % (
            self.process(binary.left),
            self.process(binary.right),
        )

    def visit_isnot_distinct_from_binary(self, binary, operator, **kw):
        return "DECODE(%s, %s, 0, 1) = 0" % (
            self.process(binary.left),
            self.process(binary.right),
        )


class OracleDDLCompiler(compiler.DDLCompiler):
    def define_constraint_cascades(self, constraint):
        text = ""
        if constraint.ondelete is not None:
            text += " ON DELETE %s" % constraint.ondelete

        # oracle has no ON UPDATE CASCADE -
        # its only available via triggers
        # http://asktom.oracle.com/tkyte/update_cascade/index.html
        if constraint.onupdate is not None:
            util.warn(
                "Oracle does not contain native UPDATE CASCADE "
                "functionality - onupdates will not be rendered for foreign "
                "keys.  Consider using deferrable=True, initially='deferred' "
                "or triggers."
            )

        return text

    def visit_drop_table_comment(self, drop):
        return "COMMENT ON TABLE %s IS ''" % self.preparer.format_table(
            drop.element
        )

    def visit_create_index(self, create):
        index = create.element
        self._verify_index_table(index)
        preparer = self.preparer
        text = "CREATE "
        if index.unique:
            text += "UNIQUE "
        if index.dialect_options["oracle"]["bitmap"]:
            text += "BITMAP "
        text += "INDEX %s ON %s (%s)" % (
            self._prepared_index_name(index, include_schema=True),
            preparer.format_table(index.table, use_schema=True),
            ", ".join(
                self.sql_compiler.process(
                    expr, include_table=False, literal_binds=True
                )
                for expr in index.expressions
            ),
        )
        if index.dialect_options["oracle"]["compress"] is not False:
            if index.dialect_options["oracle"]["compress"] is True:
                text += " COMPRESS"
            else:
                text += " COMPRESS %d" % (
                    index.dialect_options["oracle"]["compress"]
                )
        return text

    def post_create_table(self, table):
        table_opts = []
        opts = table.dialect_options["oracle"]

        if opts["on_commit"]:
            on_commit_options = opts["on_commit"].replace("_", " ").upper()
            table_opts.append("\n ON COMMIT %s" % on_commit_options)

        if opts["compress"]:
            if opts["compress"] is True:
                table_opts.append("\n COMPRESS")
            else:
                table_opts.append("\n COMPRESS FOR %s" % (opts["compress"]))

        return "".join(table_opts)

    def visit_computed_column(self, generated):
        text = "GENERATED ALWAYS AS (%s)" % self.sql_compiler.process(
            generated.sqltext, include_table=False, literal_binds=True
        )
        if generated.persisted is True:
            raise exc.CompileError(
                "Oracle computed columns do not support 'stored' persistence; "
                "set the 'persisted' flag to None or False for Oracle support."
            )
        elif generated.persisted is False:
            text += " VIRTUAL"
        return text


class OracleIdentifierPreparer(compiler.IdentifierPreparer):

    reserved_words = {x.lower() for x in RESERVED_WORDS}
    illegal_initial_characters = {str(dig) for dig in range(0, 10)}.union(
        ["_", "$"]
    )

    def _bindparam_requires_quotes(self, value):
        """Return True if the given identifier requires quoting."""
        lc_value = value.lower()
        return (
            lc_value in self.reserved_words
            or value[0] in self.illegal_initial_characters
            or not self.legal_characters.match(util.text_type(value))
        )

    def format_savepoint(self, savepoint):
        name = savepoint.ident.lstrip("_")
        return super(OracleIdentifierPreparer, self).format_savepoint(
            savepoint, name
        )


class OracleExecutionContext(default.DefaultExecutionContext):
    def fire_sequence(self, seq, type_):
        return self._execute_scalar(
            "SELECT "
            + self.dialect.identifier_preparer.format_sequence(seq)
            + ".nextval FROM DUAL",
            type_,
        )


class OracleDialect(default.DefaultDialect):
    name = "oracle"
    supports_alter = True
    supports_unicode_statements = False
    supports_unicode_binds = False
    max_identifier_length = 30

    supports_simple_order_by_label = False
    cte_follows_insert = True

    supports_sequences = True
    sequences_optional = False
    postfetch_lastrowid = False

    default_paramstyle = "named"
    colspecs = colspecs
    ischema_names = ischema_names
    requires_name_normalize = True

    supports_comments = True
    supports_default_values = False
    supports_empty_insert = False

    statement_compiler = OracleCompiler
    ddl_compiler = OracleDDLCompiler
    type_compiler = OracleTypeCompiler
    preparer = OracleIdentifierPreparer
    execution_ctx_cls = OracleExecutionContext

    reflection_options = ("oracle_resolve_synonyms",)

    _use_nchar_for_unicode = False

    construct_arguments = [
        (
            sa_schema.Table,
            {"resolve_synonyms": False, "on_commit": None, "compress": False},
        ),
        (sa_schema.Index, {"bitmap": False, "compress": False}),
    ]

    def __init__(
        self,
        use_ansi=True,
        optimize_limits=False,
        use_binds_for_limits=True,
        use_nchar_for_unicode=False,
        exclude_tablespaces=("SYSTEM", "SYSAUX"),
        **kwargs
    ):
        default.DefaultDialect.__init__(self, **kwargs)
        self._use_nchar_for_unicode = use_nchar_for_unicode
        self.use_ansi = use_ansi
        self.optimize_limits = optimize_limits
        self.use_binds_for_limits = use_binds_for_limits
        self.exclude_tablespaces = exclude_tablespaces

    def initialize(self, connection):
        super(OracleDialect, self).initialize(connection)

        self.implicit_returning = self.__dict__.get(
            "implicit_returning", self.server_version_info > (10,)
        )

        if self._is_oracle_8:
            self.colspecs = self.colspecs.copy()
            self.colspecs.pop(sqltypes.Interval)
            self.use_ansi = False

    def _get_effective_compat_server_version_info(self, connection):
        # dialect does not need compat levels below 12.2, so don't query
        # in those cases

        if self.server_version_info < (12, 2):
            return self.server_version_info
        try:
            compat = connection.execute(
                "SELECT value FROM v$parameter WHERE name = 'compatible'"
            ).scalar()
        except exc.DBAPIError:
            compat = None

        if compat:
            try:
                return tuple(int(x) for x in compat.split("."))
            except:
                return self.server_version_info
        else:
            return self.server_version_info

    @property
    def _is_oracle_8(self):
        return self.server_version_info and self.server_version_info < (9,)

    @property
    def _supports_table_compression(self):
        return self.server_version_info and self.server_version_info >= (10, 1)

    @property
    def _supports_table_compress_for(self):
        return self.server_version_info and self.server_version_info >= (11,)

    @property
    def _supports_char_length(self):
        return not self._is_oracle_8

    def do_release_savepoint(self, connection, name):
        # Oracle does not support RELEASE SAVEPOINT
        pass

    def _check_max_identifier_length(self, connection):
        if self._get_effective_compat_server_version_info(connection) >= (
            12,
            2,
        ):
            util.warn(
                "Oracle version %r is known to have a maximum "
                "identifier length of 128, rather than the historical default "
                "of 30. SQLAlchemy 1.4 will use 128 for this "
                "database; please set max_identifier_length=128 "
                "in create_engine() in order to "
                "test the application with this new length, or set to 30 in "
                "order to assure that 30 continues to be used.  "
                "In particular, pay close attention to the behavior of "
                "database migrations as dynamically generated names may "
                "change. See the section 'Max Identifier Lengths' in the "
                "SQLAlchemy Oracle dialect documentation for background."
                % ((self.server_version_info,))
            )

        # use the default
        return None

    def _check_unicode_returns(self, connection):
        additional_tests = [
            expression.cast(
                expression.literal_column("'test nvarchar2 returns'"),
                sqltypes.NVARCHAR(60),
            )
        ]
        return super(OracleDialect, self)._check_unicode_returns(
            connection, additional_tests
        )

    _isolation_lookup = ["READ COMMITTED"]

    def get_isolation_level(self, connection):
        return "READ COMMITTED"

    def set_isolation_level(self, connection, level):
        # prior to adding AUTOCOMMIT support for cx_Oracle, the Oracle dialect
        # had no notion of setting the isolation level.  As Oracle
        # does not have a straightforward way of getting the isolation level
        # if a server-side transaction is not yet in progress, we currently
        # hardcode to only support "READ COMMITTED" and "AUTOCOMMIT" at the
        # cx_oracle level.  See #5200.
        pass

    def has_table(self, connection, table_name, schema=None):
        if not schema:
            schema = self.default_schema_name
        cursor = connection.execute(
            sql.text(
                "SELECT table_name FROM all_tables "
                "WHERE table_name = :name AND owner = :schema_name"
            ),
            name=self.denormalize_name(table_name),
            schema_name=self.denormalize_name(schema),
        )
        return cursor.first() is not None

    def has_sequence(self, connection, sequence_name, schema=None):
        if not schema:
            schema = self.default_schema_name
        cursor = connection.execute(
            sql.text(
                "SELECT sequence_name FROM all_sequences "
                "WHERE sequence_name = :name AND "
                "sequence_owner = :schema_name"
            ),
            name=self.denormalize_name(sequence_name),
            schema_name=self.denormalize_name(schema),
        )
        return cursor.first() is not None

    def _get_default_schema_name(self, connection):
        return self.normalize_name(
            connection.execute("SELECT USER FROM DUAL").scalar()
        )

    def _resolve_synonym(
        self,
        connection,
        desired_owner=None,
        desired_synonym=None,
        desired_table=None,
    ):
        """search for a local synonym matching the given desired owner/name.

        if desired_owner is None, attempts to locate a distinct owner.

        returns the actual name, owner, dblink name, and synonym name if
        found.
        """

        q = (
            "SELECT owner, table_owner, table_name, db_link, "
            "synonym_name FROM all_synonyms WHERE "
        )
        clauses = []
        params = {}
        if desired_synonym:
            clauses.append("synonym_name = :synonym_name")
            params["synonym_name"] = desired_synonym
        if desired_owner:
            clauses.append("owner = :desired_owner")
            params["desired_owner"] = desired_owner
        if desired_table:
            clauses.append("table_name = :tname")
            params["tname"] = desired_table

        q += " AND ".join(clauses)

        result = connection.execute(sql.text(q), **params)
        if desired_owner:
            row = result.first()
            if row:
                return (
                    row["table_name"],
                    row["table_owner"],
                    row["db_link"],
                    row["synonym_name"],
                )
            else:
                return None, None, None, None
        else:
            rows = result.fetchall()
            if len(rows) > 1:
                raise AssertionError(
                    "There are multiple tables visible to the schema, you "
                    "must specify owner"
                )
            elif len(rows) == 1:
                row = rows[0]
                return (
                    row["table_name"],
                    row["table_owner"],
                    row["db_link"],
                    row["synonym_name"],
                )
            else:
                return None, None, None, None

    @reflection.cache
    def _prepare_reflection_args(
        self,
        connection,
        table_name,
        schema=None,
        resolve_synonyms=False,
        dblink="",
        **kw
    ):

        if resolve_synonyms:
            actual_name, owner, dblink, synonym = self._resolve_synonym(
                connection,
                desired_owner=self.denormalize_name(schema),
                desired_synonym=self.denormalize_name(table_name),
            )
        else:
            actual_name, owner, dblink, synonym = None, None, None, None
        if not actual_name:
            actual_name = self.denormalize_name(table_name)

        if dblink:
            # using user_db_links here since all_db_links appears
            # to have more restricted permissions.
            # http://docs.oracle.com/cd/B28359_01/server.111/b28310/ds_admin005.htm
            # will need to hear from more users if we are doing
            # the right thing here.  See [ticket:2619]
            owner = connection.scalar(
                sql.text(
                    "SELECT username FROM user_db_links " "WHERE db_link=:link"
                ),
                link=dblink,
            )
            dblink = "@" + dblink
        elif not owner:
            owner = self.denormalize_name(schema or self.default_schema_name)

        return (actual_name, owner, dblink or "", synonym)

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        s = "SELECT username FROM all_users ORDER BY username"
        cursor = connection.execute(s)
        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)

        # note that table_names() isn't loading DBLINKed or synonym'ed tables
        if schema is None:
            schema = self.default_schema_name

        sql_str = "SELECT table_name FROM all_tables WHERE "
        if self.exclude_tablespaces:
            sql_str += (
                "nvl(tablespace_name, 'no tablespace') "
                "NOT IN (%s) AND "
                % (", ".join(["'%s'" % ts for ts in self.exclude_tablespaces]))
            )
        sql_str += (
            "OWNER = :owner " "AND IOT_NAME IS NULL " "AND DURATION IS NULL"
        )

        cursor = connection.execute(sql.text(sql_str), owner=schema)
        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_temp_table_names(self, connection, **kw):
        schema = self.denormalize_name(self.default_schema_name)

        sql_str = "SELECT table_name FROM all_tables WHERE "
        if self.exclude_tablespaces:
            sql_str += (
                "nvl(tablespace_name, 'no tablespace') "
                "NOT IN (%s) AND "
                % (", ".join(["'%s'" % ts for ts in self.exclude_tablespaces]))
            )
        sql_str += (
            "OWNER = :owner "
            "AND IOT_NAME IS NULL "
            "AND DURATION IS NOT NULL"
        )

        cursor = connection.execute(sql.text(sql_str), owner=schema)
        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)
        s = sql.text("SELECT view_name FROM all_views WHERE owner = :owner")
        cursor = connection.execute(s, owner=self.denormalize_name(schema))
        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_table_options(self, connection, table_name, schema=None, **kw):
        options = {}

        resolve_synonyms = kw.get("oracle_resolve_synonyms", False)
        dblink = kw.get("dblink", "")
        info_cache = kw.get("info_cache")

        (table_name, schema, dblink, synonym) = self._prepare_reflection_args(
            connection,
            table_name,
            schema,
            resolve_synonyms,
            dblink,
            info_cache=info_cache,
        )

        params = {"table_name": table_name}

        columns = ["table_name"]
        if self._supports_table_compression:
            columns.append("compression")
        if self._supports_table_compress_for:
            columns.append("compress_for")

        text = (
            "SELECT %(columns)s "
            "FROM ALL_TABLES%(dblink)s "
            "WHERE table_name = :table_name"
        )

        if schema is not None:
            params["owner"] = schema
            text += " AND owner = :owner "
        text = text % {"dblink": dblink, "columns": ", ".join(columns)}

        result = connection.execute(sql.text(text), **params)

        enabled = dict(DISABLED=False, ENABLED=True)

        row = result.first()
        if row:
            if "compression" in row and enabled.get(row.compression, False):
                if "compress_for" in row:
                    options["oracle_compress"] = row.compress_for
                else:
                    options["oracle_compress"] = True

        return options

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        """

        kw arguments can be:

            oracle_resolve_synonyms

            dblink

        """

        resolve_synonyms = kw.get("oracle_resolve_synonyms", False)
        dblink = kw.get("dblink", "")
        info_cache = kw.get("info_cache")

        (table_name, schema, dblink, synonym) = self._prepare_reflection_args(
            connection,
            table_name,
            schema,
            resolve_synonyms,
            dblink,
            info_cache=info_cache,
        )
        columns = []
        if self._supports_char_length:
            char_length_col = "char_length"
        else:
            char_length_col = "data_length"

        params = {"table_name": table_name}
        text = """
            SELECT col.column_name, col.data_type, col.%(char_length_col)s,
              col.data_precision, col.data_scale, col.nullable,
              col.data_default, com.comments, col.virtual_column\
            FROM all_tab_cols%(dblink)s col
            LEFT JOIN all_col_comments%(dblink)s com
            ON col.table_name = com.table_name
            AND col.column_name = com.column_name
            AND col.owner = com.owner
            WHERE col.table_name = :table_name
            AND col.hidden_column = 'NO'
        """
        if schema is not None:
            params["owner"] = schema
            text += " AND col.owner = :owner "
        text += " ORDER BY col.column_id"
        text = text % {"dblink": dblink, "char_length_col": char_length_col}

        c = connection.execute(sql.text(text), **params)

        for row in c:
            colname = self.normalize_name(row[0])
            orig_colname = row[0]
            coltype = row[1]
            length = row[2]
            precision = row[3]
            scale = row[4]
            nullable = row[5] == "Y"
            default = row[6]
            comment = row[7]
            generated = row[8]

            if coltype == "NUMBER":
                if precision is None and scale == 0:
                    coltype = INTEGER()
                else:
                    coltype = NUMBER(precision, scale)
            elif coltype == "FLOAT":
                # TODO: support "precision" here as "binary_precision"
                coltype = FLOAT()
            elif coltype in ("VARCHAR2", "NVARCHAR2", "CHAR", "NCHAR"):
                coltype = self.ischema_names.get(coltype)(length)
            elif "WITH TIME ZONE" in coltype:
                coltype = TIMESTAMP(timezone=True)
            else:
                coltype = re.sub(r"\(\d+\)", "", coltype)
                try:
                    coltype = self.ischema_names[coltype]
                except KeyError:
                    util.warn(
                        "Did not recognize type '%s' of column '%s'"
                        % (coltype, colname)
                    )
                    coltype = sqltypes.NULLTYPE

            if generated == "YES":
                computed = dict(sqltext=default)
                default = None
            else:
                computed = None

            cdict = {
                "name": colname,
                "type": coltype,
                "nullable": nullable,
                "default": default,
                "autoincrement": "auto",
                "comment": comment,
            }
            if orig_colname.lower() == orig_colname:
                cdict["quote"] = True
            if computed is not None:
                cdict["computed"] = computed

            columns.append(cdict)
        return columns

    @reflection.cache
    def get_table_comment(
        self,
        connection,
        table_name,
        schema=None,
        resolve_synonyms=False,
        dblink="",
        **kw
    ):

        info_cache = kw.get("info_cache")
        (table_name, schema, dblink, synonym) = self._prepare_reflection_args(
            connection,
            table_name,
            schema,
            resolve_synonyms,
            dblink,
            info_cache=info_cache,
        )

        if not schema:
            schema = self.default_schema_name

        COMMENT_SQL = """
            SELECT comments
            FROM all_tab_comments
            WHERE table_name = :table_name AND owner = :schema_name
        """

        c = connection.execute(
            sql.text(COMMENT_SQL), table_name=table_name, schema_name=schema
        )
        return {"text": c.scalar()}

    @reflection.cache
    def get_indexes(
        self,
        connection,
        table_name,
        schema=None,
        resolve_synonyms=False,
        dblink="",
        **kw
    ):

        info_cache = kw.get("info_cache")
        (table_name, schema, dblink, synonym) = self._prepare_reflection_args(
            connection,
            table_name,
            schema,
            resolve_synonyms,
            dblink,
            info_cache=info_cache,
        )
        indexes = []

        params = {"table_name": table_name}
        text = (
            "SELECT a.index_name, a.column_name, "
            "\nb.index_type, b.uniqueness, b.compression, b.prefix_length "
            "\nFROM ALL_IND_COLUMNS%(dblink)s a, "
            "\nALL_INDEXES%(dblink)s b "
            "\nWHERE "
            "\na.index_name = b.index_name "
            "\nAND a.table_owner = b.table_owner "
            "\nAND a.table_name = b.table_name "
            "\nAND a.table_name = :table_name "
        )

        if schema is not None:
            params["schema"] = schema
            text += "AND a.table_owner = :schema "

        text += "ORDER BY a.index_name, a.column_position"

        text = text % {"dblink": dblink}

        q = sql.text(text)
        rp = connection.execute(q, **params)
        indexes = []
        last_index_name = None
        pk_constraint = self.get_pk_constraint(
            connection,
            table_name,
            schema,
            resolve_synonyms=resolve_synonyms,
            dblink=dblink,
            info_cache=kw.get("info_cache"),
        )

        uniqueness = dict(NONUNIQUE=False, UNIQUE=True)
        enabled = dict(DISABLED=False, ENABLED=True)

        oracle_sys_col = re.compile(r"SYS_NC\d+\$", re.IGNORECASE)

        index = None
        for rset in rp:
            index_name_normalized = self.normalize_name(rset.index_name)

            # skip primary key index.  This is refined as of
            # [ticket:5421].  Note that ALL_INDEXES.GENERATED will by "Y"
            # if the name of this index was generated by Oracle, however
            # if a named primary key constraint was created then this flag
            # is false.
            if (
                pk_constraint
                and index_name_normalized == pk_constraint["name"]
            ):
                continue

            if rset.index_name != last_index_name:
                index = dict(
                    name=index_name_normalized,
                    column_names=[],
                    dialect_options={},
                )
                indexes.append(index)
            index["unique"] = uniqueness.get(rset.uniqueness, False)

            if rset.index_type in ("BITMAP", "FUNCTION-BASED BITMAP"):
                index["dialect_options"]["oracle_bitmap"] = True
            if enabled.get(rset.compression, False):
                index["dialect_options"][
                    "oracle_compress"
                ] = rset.prefix_length

            # filter out Oracle SYS_NC names.  could also do an outer join
            # to the all_tab_columns table and check for real col names there.
            if not oracle_sys_col.match(rset.column_name):
                index["column_names"].append(
                    self.normalize_name(rset.column_name)
                )
            last_index_name = rset.index_name

        return indexes

    @reflection.cache
    def _get_constraint_data(
        self, connection, table_name, schema=None, dblink="", **kw
    ):

        params = {"table_name": table_name}

        text = (
            "SELECT"
            "\nac.constraint_name,"  # 0
            "\nac.constraint_type,"  # 1
            "\nloc.column_name AS local_column,"  # 2
            "\nrem.table_name AS remote_table,"  # 3
            "\nrem.column_name AS remote_column,"  # 4
            "\nrem.owner AS remote_owner,"  # 5
            "\nloc.position as loc_pos,"  # 6
            "\nrem.position as rem_pos,"  # 7
            "\nac.search_condition,"  # 8
            "\nac.delete_rule"  # 9
            "\nFROM all_constraints%(dblink)s ac,"
            "\nall_cons_columns%(dblink)s loc,"
            "\nall_cons_columns%(dblink)s rem"
            "\nWHERE ac.table_name = :table_name"
            "\nAND ac.constraint_type IN ('R','P', 'U', 'C')"
        )

        if schema is not None:
            params["owner"] = schema
            text += "\nAND ac.owner = :owner"

        text += (
            "\nAND ac.owner = loc.owner"
            "\nAND ac.constraint_name = loc.constraint_name"
            "\nAND ac.r_owner = rem.owner(+)"
            "\nAND ac.r_constraint_name = rem.constraint_name(+)"
            "\nAND (rem.position IS NULL or loc.position=rem.position)"
            "\nORDER BY ac.constraint_name, loc.position"
        )

        text = text % {"dblink": dblink}
        rp = connection.execute(sql.text(text), **params)
        constraint_data = rp.fetchall()
        return constraint_data

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        resolve_synonyms = kw.get("oracle_resolve_synonyms", False)
        dblink = kw.get("dblink", "")
        info_cache = kw.get("info_cache")

        (table_name, schema, dblink, synonym) = self._prepare_reflection_args(
            connection,
            table_name,
            schema,
            resolve_synonyms,
            dblink,
            info_cache=info_cache,
        )
        pkeys = []
        constraint_name = None
        constraint_data = self._get_constraint_data(
            connection,
            table_name,
            schema,
            dblink,
            info_cache=kw.get("info_cache"),
        )

        for row in constraint_data:
            (
                cons_name,
                cons_type,
                local_column,
                remote_table,
                remote_column,
                remote_owner,
            ) = row[0:2] + tuple([self.normalize_name(x) for x in row[2:6]])
            if cons_type == "P":
                if constraint_name is None:
                    constraint_name = self.normalize_name(cons_name)
                pkeys.append(local_column)
        return {"constrained_columns": pkeys, "name": constraint_name}

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        """

        kw arguments can be:

            oracle_resolve_synonyms

            dblink

        """
        requested_schema = schema  # to check later on
        resolve_synonyms = kw.get("oracle_resolve_synonyms", False)
        dblink = kw.get("dblink", "")
        info_cache = kw.get("info_cache")

        (table_name, schema, dblink, synonym) = self._prepare_reflection_args(
            connection,
            table_name,
            schema,
            resolve_synonyms,
            dblink,
            info_cache=info_cache,
        )

        constraint_data = self._get_constraint_data(
            connection,
            table_name,
            schema,
            dblink,
            info_cache=kw.get("info_cache"),
        )

        def fkey_rec():
            return {
                "name": None,
                "constrained_columns": [],
                "referred_schema": None,
                "referred_table": None,
                "referred_columns": [],
                "options": {},
            }

        fkeys = util.defaultdict(fkey_rec)

        for row in constraint_data:
            (
                cons_name,
                cons_type,
                local_column,
                remote_table,
                remote_column,
                remote_owner,
            ) = row[0:2] + tuple([self.normalize_name(x) for x in row[2:6]])

            cons_name = self.normalize_name(cons_name)

            if cons_type == "R":
                if remote_table is None:
                    # ticket 363
                    util.warn(
                        (
                            "Got 'None' querying 'table_name' from "
                            "all_cons_columns%(dblink)s - does the user have "
                            "proper rights to the table?"
                        )
                        % {"dblink": dblink}
                    )
                    continue

                rec = fkeys[cons_name]
                rec["name"] = cons_name
                local_cols, remote_cols = (
                    rec["constrained_columns"],
                    rec["referred_columns"],
                )

                if not rec["referred_table"]:
                    if resolve_synonyms:
                        (
                            ref_remote_name,
                            ref_remote_owner,
                            ref_dblink,
                            ref_synonym,
                        ) = self._resolve_synonym(
                            connection,
                            desired_owner=self.denormalize_name(remote_owner),
                            desired_table=self.denormalize_name(remote_table),
                        )
                        if ref_synonym:
                            remote_table = self.normalize_name(ref_synonym)
                            remote_owner = self.normalize_name(
                                ref_remote_owner
                            )

                    rec["referred_table"] = remote_table

                    if (
                        requested_schema is not None
                        or self.denormalize_name(remote_owner) != schema
                    ):
                        rec["referred_schema"] = remote_owner

                    if row[9] != "NO ACTION":
                        rec["options"]["ondelete"] = row[9]

                local_cols.append(local_column)
                remote_cols.append(remote_column)

        return list(fkeys.values())

    @reflection.cache
    def get_unique_constraints(
        self, connection, table_name, schema=None, **kw
    ):
        resolve_synonyms = kw.get("oracle_resolve_synonyms", False)
        dblink = kw.get("dblink", "")
        info_cache = kw.get("info_cache")

        (table_name, schema, dblink, synonym) = self._prepare_reflection_args(
            connection,
            table_name,
            schema,
            resolve_synonyms,
            dblink,
            info_cache=info_cache,
        )

        constraint_data = self._get_constraint_data(
            connection,
            table_name,
            schema,
            dblink,
            info_cache=kw.get("info_cache"),
        )

        unique_keys = filter(lambda x: x[1] == "U", constraint_data)
        uniques_group = groupby(unique_keys, lambda x: x[0])

        index_names = {
            ix["name"]
            for ix in self.get_indexes(connection, table_name, schema=schema)
        }
        return [
            {
                "name": name,
                "column_names": cols,
                "duplicates_index": name if name in index_names else None,
            }
            for name, cols in [
                [
                    self.normalize_name(i[0]),
                    [self.normalize_name(x[2]) for x in i[1]],
                ]
                for i in uniques_group
            ]
        ]

    @reflection.cache
    def get_view_definition(
        self,
        connection,
        view_name,
        schema=None,
        resolve_synonyms=False,
        dblink="",
        **kw
    ):
        info_cache = kw.get("info_cache")
        (view_name, schema, dblink, synonym) = self._prepare_reflection_args(
            connection,
            view_name,
            schema,
            resolve_synonyms,
            dblink,
            info_cache=info_cache,
        )

        params = {"view_name": view_name}
        text = "SELECT text FROM all_views WHERE view_name=:view_name"

        if schema is not None:
            text += " AND owner = :schema"
            params["schema"] = schema

        rp = connection.execute(sql.text(text), **params).scalar()
        if rp:
            if util.py2k:
                rp = rp.decode(self.encoding)
            return rp
        else:
            return None

    @reflection.cache
    def get_check_constraints(
        self, connection, table_name, schema=None, include_all=False, **kw
    ):
        resolve_synonyms = kw.get("oracle_resolve_synonyms", False)
        dblink = kw.get("dblink", "")
        info_cache = kw.get("info_cache")

        (table_name, schema, dblink, synonym) = self._prepare_reflection_args(
            connection,
            table_name,
            schema,
            resolve_synonyms,
            dblink,
            info_cache=info_cache,
        )

        constraint_data = self._get_constraint_data(
            connection,
            table_name,
            schema,
            dblink,
            info_cache=kw.get("info_cache"),
        )

        check_constraints = filter(lambda x: x[1] == "C", constraint_data)

        return [
            {"name": self.normalize_name(cons[0]), "sqltext": cons[8]}
            for cons in check_constraints
            if include_all or not re.match(r"..+?. IS NOT NULL$", cons[8])
        ]


class _OuterJoinColumn(sql.ClauseElement):
    __visit_name__ = "outer_join_column"

    def __init__(self, column):
        self.column = column
