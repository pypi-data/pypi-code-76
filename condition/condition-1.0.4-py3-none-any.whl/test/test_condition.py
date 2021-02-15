import tempfile

import pandas as pd
import re
import pytest

from condition import *


# def make_df(csv_text: str, index_col: str = 'date') -> pd.DataFrame:
#     df = pd.read_csv(StringIO(cleandoc(csv_text)), parse_dates=[index_col])
#     return df.set_index(index_col)


@pytest.fixture(scope="session")
def my_dataframe():
    df = get_test_df()
    return df


@pytest.fixture(scope="session")
def fl():
    return FieldList("date A B C value".split())


@pytest.fixture(scope="session")
def and1(fl):
    and1 = And(
        [
            fl.date >= pd.to_datetime("20000101"),
            fl.date <= pd.to_datetime("20000131"),
            fl.A == ("a1 a3".split()),
            fl.C != ("c3 c5".split()),
        ]
    )
    return and1


SPACES = re.compile(r"\s+")


def assert_equal_ignore_spaces(s1, s2):
    assert re.sub(SPACES, " ", str(s1).strip()) == re.sub(SPACES, " ", str(s2).strip())


def test_and_operator(fl, and1):
    and2 = (
        (
            (fl.date >= pd.to_datetime("20000101"))
            & (fl.date <= pd.to_datetime("20000131"))
        )
        & (fl.A == "a1 a3".split())
        & (fl.C != "c3 c5".split())
    )
    assert_equal_ignore_spaces(and1, and2)


def test_op(fl):
    with pytest.raises(ValueError):
        fl.A == ([])
    with pytest.raises(ValueError):
        fl.A == ([3, "a"])
    with pytest.raises(ValueError):
        fl.A == [3, "a"]


def test_fieldlist(fl, my_dataframe):
    fl2 = FieldList.from_df(my_dataframe)
    assert fl.fields == fl2.fields


def test_empty_condition(my_dataframe):
    def check_empty(cond):
        df = cond.query(my_dataframe)
        assert df.equals(my_dataframe)
        assert cond.to_pyarrow_filter() is None
        assert_equal_ignore_spaces(cond.to_sql_where_condition(), "1=1")
        assert len(cond._to_sql_dict()) == 0

    check_empty(And())
    check_empty(Or())


def test_and(my_dataframe, and1):
    assert and1.to_df_query() == (
        "((date >= '2000-01-01 00:00:00')&(date <= '2000-01-31 00:00:00')"
        "&(A in ('a1','a3'))&(C not in ('c3','c5')))"
    )
    assert_equal_ignore_spaces(
        and1,
        """
	(date >= '2000-01-01 00:00:00'
	and date <= '2000-01-31 00:00:00'
	and A in ('a1','a3')
	and C not in ('c3','c5'))""",
    )

    assert and1.to_pyarrow_filter() == [
        ("date", ">=", pd.Timestamp("2000-01-01 00:00:00")),
        ("date", "<=", pd.Timestamp("2000-01-31 00:00:00")),
        ("A", "in", {"a1", "a3"}),
        ("C", "not in", {"c3", "c5"}),
    ]

    res = my_dataframe.query(and1.to_df_query())

    assert set(res.index.get_level_values("A").unique()) == set(["a1", "a3"])
    assert set(res.index.get_level_values("C").unique()) ^ set(["c3", "c5"])
    assert res.index.get_level_values("date").min() == pd.to_datetime("20000101")
    assert res.index.get_level_values("date").max() == pd.to_datetime("20000131")

    sql_dict = and1.to_sql_dict()
    assert set(sql_dict.keys()) == {
        "date_LE",
        "A_IN",
        "C_NOT_IN",
        "date_GE",
        "condition",
        "where_condition",
    }
    assert sql_dict["date_GE"] == "'2000-01-01 00:00:00'"
    assert sql_dict["date_LE"] == "'2000-01-31 00:00:00'"


def test_get_all_field_conditions(and1):
    d = and1.get_all_field_conditions()
    assert len(d) == 3
    assert len(d["date"]) == 2


def test_add_date_condition(fl):
    cond = fl.B == ("b3 b5".split())
    cond2 = cond.add_date_condition(fl.date, "20000101", "20000131")
    assert_equal_ignore_spaces(
        cond2,
        """
	(B in ('b3','b5')
	and date >= '2000-01-01 00:00:00'
	and date <= '2000-01-31 00:00:00')
	""",
    )


def test_add_daterange_overlap_condition(fl):
    fl = FieldList(["from_date", "to_date"])
    cond = And()
    cond2 = cond.add_daterange_overlap_condition(
        fl.from_date, fl.to_date, "20000101", "20000131"
    )
    assert_equal_ignore_spaces(
        cond2,
        """
	(to_date >= '2000-01-01 00:00:00'
	and from_date <= '2000-01-31 00:00:00')
    """,
    )


def test_or(fl, my_dataframe, and1):
    and2 = (fl.B == "b3 b5".split()) & (fl.C == "c3 c4".split())

    or1 = Or(
        [
            and1,
            and2,
        ]
    )
    or2 = and1 | and2

    assert str(or1) == str(or2)

    res = my_dataframe.query(or1.to_df_query())
    assert set(res.index.get_level_values("C").unique()) == set(
        ["c1", "c2", "c3", "c4"]
    )
    assert_equal_ignore_spaces(
        or1,
        """
    (
		(date >= '2000-01-01 00:00:00'
		and date <= '2000-01-31 00:00:00'
		and A in ('a1','a3')
		and C not in ('c3','c5'))
	or 
		(B in ('b3','b5')
		and C in ('c3','c4')))""",
    )

    assert set(or1.to_sql_dict().keys()) == {
        "B_IN",
        "date_GE",
        "A_IN",
        "C_IN",
        "date_LE",
        "condition",
        "where_condition",
        "C_NOT_IN",
    }

    assert or1.to_pyarrow_filter() == [
        [
            ("date", ">=", pd.Timestamp("2000-01-01 00:00:00")),
            ("date", "<=", pd.Timestamp("2000-01-31 00:00:00")),
            ("A", "in", {"a3", "a1"}),
            ("C", "not in", {"c3", "c5"}),
        ],
        [("B", "in", {"b3", "b5"}), ("C", "in", {"c3", "c4"})],
    ]


def test_pyarrow_filter(fl):
    cond1 = fl.A >= 300
    assert cond1.to_pyarrow_filter() == [("A", ">=", 300)]
    or1 = cond1 | (fl.B == (["b1", "b2"]))
    assert or1.to_pyarrow_filter() == [[("A", ">=", 300)], [("B", "in", {"b1", "b2"})]]
    or2 = or1 | (fl.B == "b4")
    assert or1.to_pyarrow_filter() == [
        [("A", ">=", 300)],
        [("B", "in", {"b1", "b2"})],
        [("B", "=", "b4")],
    ]
    and1 = cond1 & (fl.B >= "b5") & (fl.C < "c6")
    assert and1.to_pyarrow_filter() == [
        ("A", ">=", 300),
        ("B", ">=", "b5"),
        ("C", "<", "c6"),
    ]

    # normalization
    and2 = (fl.C == "c3") & or1
    filters = and2.to_pyarrow_filter()
    assert filters == [
        [("A", ">=", 300), ("C", "=", "c3")],
        [("B", "in", {"b1", "b2"}), ("C", "=", "c3")],
        [("B", "=", "b4"), ("C", "=", "c3")],
    ]

    or2 = and2 | (fl.A < 400)
    filters = or2.to_pyarrow_filter()
    assert filters == [
        [("A", ">=", 300), ("C", "=", "c3")],
        [("B", "in", {"b1", "b2"}), ("C", "=", "c3")],
        [("B", "=", "b4"), ("C", "=", "c3")],
        [("A", "<", 400)],
    ]


def test_visualize(fl):
    cond1 = And(
        [
            fl.A == "a1",
            Or([fl.B == "b1", fl.C == "c1", And([fl.value >= 3, fl.value <= 5])]),
            Or([fl.B == "b2", fl.C == "c2"]),
        ]
    )
    view = False
    filename = None
    # filename = 'docs/_static/cond1'
    cond1.visualize(filename, view=view)
    # filename = 'docs/_static/cond1-normalized'
    cond1.normalize().visualize(filename, view=view)
    pass


def test_split(fl, and1):
    cond = and1.split(fl)
    assert str(cond) == str(and1)
    cond = and1.split(["notExisted"])
    assert cond is None

    cond1 = And(
        [
            fl.A == "a1",
            Or([fl.B == "b1", fl.C == "c1", And([fl.value >= 3, fl.value <= 5])]),
            Or([fl.B == "b2", fl.C == "c2"]),
        ]
    )
    cond2 = cond1.split("A")
    assert_equal_ignore_spaces(cond2, "A = 'a1'")
    cond2 = cond1.split(["B", "C"])
    assert_equal_ignore_spaces(
        cond2,
        """
        (B = 'b2'
        or C = 'c2')        
        """,
    )


def test_eval():
    paths = [
        "A=a1/B=b1/C=c1",
        "A=a2/B=b1/C=c1",
        "A=a3/B=b1/C=c2",
    ]

    def path2record(path):
        return {p.split("=")[0]: p.split("=")[1] for p in path.split("/")}

    field_list = FieldList("A B C".split())
    cond = And(
        [
            field_list.A == ("a1 a3".split()),
            field_list.C == "c2",
            field_list.B != "b2",
            field_list.B != (["c2"]),
            field_list.B > "a1",
            field_list.B < "c3",
            field_list.B >= "b1",
            field_list.B <= "b8",
        ]
    )
    filtered_path = [
        p for p in paths if cond.eval(path2record(p), type_conversion=True)
    ]
    assert filtered_path == ["A=a3/B=b1/C=c2"]


def test_apply_pyarrow_filter(my_dataframe, and1):
    with tempfile.TemporaryDirectory() as t:
        df = my_dataframe.reset_index()
        df.to_parquet(t, partition_cols=["A", "C"])

        res = pd.read_parquet(t, filters=and1.to_pyarrow_filter())
        assert set(res.A.unique()) == set(["a1", "a3"])
        assert set(res.C.unique()) ^ set(["c3", "c5"])
        res2 = res.query(and1.to_df_query())
        res3 = and1.query(res)
        assert res2.equals(res3)
        assert res2.date.min() == pd.to_datetime("20000101")
        assert res2.date.max() == pd.to_datetime("20000131")


def test_cycle_detection(fl):
    c1 = fl.A == "a1"
    and1 = c1 & (fl.B == "b1")
    or1 = (fl.C == "c1") | (fl.B == "21") | and1 | c1
    and2 = or1 & (fl.B <= "b5")
    or2 = Or([and2])
    # or2.visualize(view = True)
    with pytest.raises(ValueError):
        and1 &= or2
    # and1.visualize(view = True)


if __name__ == "__main__":
    pytest.main([__file__])
