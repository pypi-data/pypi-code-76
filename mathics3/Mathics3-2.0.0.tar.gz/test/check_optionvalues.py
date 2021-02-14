import time
from mathics.core.parser import parse, MathicsSingleLineFeeder
from mathics.core.definitions import Definitions
from mathics.core.evaluation import Evaluation
from mathics.session import MathicsSession

session = MathicsSession(add_builtin=True, catch_interrupt=False)

def check_evaluation(str_expr: str, str_expected: str, message=""):
    """Helper function to test that a WL expression against
    its results"""
    result = session.evaluate(str_expr)
    expected = session.evaluate(str_expected)

    print(time.asctime())
    print(str_expected)
    print(str_expr)
    if message:
        assert result == expected, message
    else:
        assert result == expected

def test_optionvalues():
    session.evaluate("ClearAll[q];ClearAll[a];ClearAll[s];")
    for str_expr, str_expected in (
        (
            """
            Options[f1]:={q->12};
            f1[x_,OptionsPattern[]]:=x^OptionValue[q]; f1[y]
            """,
            "y ^ 12",
        ),
        # (
        #     """Options[f2]:={s->12}; f2[x_,opt:OptionsPattern[]]:=x^OptionValue[s];
        #     f2[y]""",
        #     "y ^ 12",
        # ),
        (
            """Options[f3]:={a->12};
               f3[x_,opt:OptionsPattern[{a:>4}]]:=x^OptionValue[a];
               f3[y]
            """,
            "y ^ 4",
        ),
        (
            """
            Options[f4]:={a->12};
            f4[x_,OptionsPattern[{a:>4}]]:=x^OptionValue[a];
            f4[y]
            """,
            "y ^ 4",
        ),
        (
            """Options[F]:={a->89,b->37};
               OptionValue[F, a]""",
            "89",
        ),
        (
            """OptionValue[F, {a,b}]""",
            "{89, 37}",
        ),
        # (
        #     "OptionValue[F, {a,b, l}]"
        #     "{89, 37, OptionValue[l]}",
        #     "OptionValue::optnf: Option name l not found.",
        # ),
        ("OptionValue[F, {l->77}, {a,b, l}]", "{89, 37, 77}"),
    ):
        check_evaluation(str_expr, str_expected)

test_optionvalues()
