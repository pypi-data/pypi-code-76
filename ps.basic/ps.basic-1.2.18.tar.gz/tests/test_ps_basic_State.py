"""Test State Module."""

import os
import pprint

from ps.basic.State import State, StateError

import pytest


os.environ["IS_TESTING"] = "YES"


def f(state: State, context: dict) -> str:
    """[summary]

    transition_func.
    :param state: [description]
    :type state: State
    :param context: [description]
    :type context: dict
    :return: [description]
    :rtype: str
    """
    context[state.name] = "visited"
    #    print(state.name)
    d = {}
    d[state.name] = state.name
    print(pprint.pformat(context))
    if state.name == "START":
        return "input"
    if state.name == "STAGE1":
        return "input2"
    if state.name == "FIN":
        return "ii"


def test_attributes_are_set():
    """[summary]

    test_attributes_are_set.
    """
    global f
    final = State("FINAL", f, final=True)
    assert final.name == "FINAL"
    assert final.compute_function == f
    assert not final.error  # ==> False
    assert not final.initial  # ==> False
    assert final.final  # ==> True
    assert final.default_transition is None


def test_default_transition_is_set():
    """[summary]

    test_default_transition_is_set.
    """
    global f
    final = State("FINAL", f, final=True)
    initial = State("INITIAL", f, initial=True, default=final)
    assert initial.default_transition == final


def test_strings_for_input_alphabet_could_be_set():
    """[summary]

    test_strings_for_input_alphabet_could_be_set.
    """
    global f
    final = State("FINAL", f, final=True)
    intermediate = State("INTERMEDIATE", f)
    intermediate["input2"] = final
    assert intermediate["input2"] == final


def test_wrong_result_state_on_input_raise_error():
    """[summary]

    test_wrong_result_state_on_input_raise_error.
    """
    with pytest.raises(StateError):
        intermediate = State("INTERMEDIATE", f)
        intermediate["input2"] = "xx"


def test_repr_works():
    """[summary]

    test_repr_works.
    """
    global f
    final = State("FINAL", f, final=True)
    x = repr(final)
    assert "FINAL" in x
    assert "State" in x
