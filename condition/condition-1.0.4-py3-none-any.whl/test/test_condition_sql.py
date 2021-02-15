import os

import pandas as pd
import pytest
from jinja2 import UndefinedError

from .test_condition import assert_equal_ignore_spaces
from condition import *
from condition.sql import render_sql


@pytest.fixture(scope="session")
def and1():
    os.environ["USER"] = "wyzhao"
    fl = FieldList("A B C date value".split())

    and1 = (
        (fl.date >= pd.to_datetime("20000101"))
        & (fl.date <= pd.to_datetime("20010131"))
        & (fl.A == "a1 a3".split())
        & (fl.C != "c3 c5".split())
    )

    return and1


def test_sql_basic(and1):
    sql = """
        select *
        from my_table
        where {{where_condition}}
    """
    assert_equal_ignore_spaces(
        render_sql(sql, and1),
        """
        select *
        from my_table
        where 
		(date >= '2000-01-01 00:00:00'
		and date <= '2001-01-31 00:00:00'
		and A in ('a1','a3')
		and C not in ('c3','c5'))
    """,
    )


def test_sql_with_db_mapping(and1):
    sql = """
        select *
        from my_table t1, my_table2 t2
        where
        t1.id = t2.id
        and {{where_condition}}
    """
    assert_equal_ignore_spaces(
        render_sql(sql, and1, {"A": "t1.col1", "C": "t2.col2"}),
        """
        select *
        from my_table t1, my_table2 t2
        where
        t1.id = t2.id
        and 
		(date >= '2000-01-01 00:00:00'
		and date <= '2001-01-31 00:00:00'
		and t1.col1 in ('a1','a3')
		and t2.col2 not in ('c3','c5'))
            """,
    )


def test_sql_with_individual_clause(and1):
    # test And predicate with separate param values
    sql = """
        select *
        from my_table
        where
        date_col>={{date_GE}}
        and date_col<={{date_LE}}
        and sector in {{A_IN}}
        and C not in {{C_NOT_IN}}
        and user = '{{env['USER']}}'
    """
    assert_equal_ignore_spaces(
        render_sql(sql, and1),
        """
        select *
        from my_table
        where
        date_col>='2000-01-01 00:00:00'
        and date_col<='2001-01-31 00:00:00'
        and sector in ('a1','a3')
        and C not in ('c3','c5')
        and user = 'wyzhao'
        """,
    )


def test_sql_with_param(and1):
    # test And predicate with adhoc sql params and db field mapping
    and1.set_param("use_join_clause", True)

    sql = """
        select *
        from my_table as t1
        {% if use_join_clause -%}
        join my_table2 t2 on t1.fpe=t2.date 
        {%- endif %}
        where {{where_condition}}
        """
    assert_equal_ignore_spaces(
        render_sql(sql, and1),
        """
        select *
        from my_table as t1
        join my_table2 t2 on t1.fpe=t2.date
        where 
		(date >= '2000-01-01 00:00:00'
		and date <= '2001-01-31 00:00:00'
		and A in ('a1','a3')
		and C not in ('c3','c5'))
        """,
    )

    and1.set_param("use_join_clause", False)
    assert_equal_ignore_spaces(
        render_sql(sql, and1),
        """
        select *
        from my_table as t1
        
        where 
		(date >= '2000-01-01 00:00:00'
		and date <= '2001-01-31 00:00:00'
		and A in ('a1','a3')
		and C not in ('c3','c5'))
		""",
    )
    pass


def test_sql_with_like():
    # work around with 'like' in sql
    and1 = And()
    and1.set_param("col_a_like", "Par%s")

    sql = """
        select *
        from my_table as t1
        where col_a like '{{col_a_like}}'
        """
    assert_equal_ignore_spaces(
        render_sql(sql, and1),
        """
        select *
        from my_table as t1
        where col_a like 'Par%s'
        """,
    )
    pass


def test_error(and1):
    with pytest.raises(UndefinedError, match=r".*non_existent_key.*"):
        sql = """
            select *
            from my_table as t1
            where col_a like '{{non_existent_key}}'
            """
        render_sql(sql, and1)
