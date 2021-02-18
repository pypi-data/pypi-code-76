from typing import Any, Type


def assert_type(var: Any, varname: str, type_: Type, noneable=False) -> None:
    assert noneable or var, f"{varname} is None"
    assert isinstance(var, type_),\
        f"Invalid type {varname}. Desire {type_} but given {type(var)}"
