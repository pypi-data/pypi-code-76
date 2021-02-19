"""Tests for the ps.basic.fsm."""
import os
import pprint

import pytest

# Import of the fsm modules has to be done after initialisation of the
# Config Module as that needs the logger (Config.logger) to be set up.
from ps.basic import Config  # noqa:  I100

os.environ["IS_TESTING"] = "YES"
os.environ["DEV_STAGE"] = "TESTING"
Config.Basic("TEST_SERVICE_NAME")

from ps.basic.State import State, StateError  # noqa: E402 I202
from ps.basic.fsm import FiniteStateMachine, TransitionError  # noqa: E402
from ps.basic.get_graph import get_graph  # noqa: E402


# from t_utils import TEST_SERVICE_NAME, reset_singleton


def f(state: State, context: dict) -> str:
    """[summary]

    test_no_initial_stage_raise_Attribute_error.
    :param state: [description]
    :type state: State
    :param context: [description]
    :type context: dict
    :return: [description]
    :rtype: str
    """
    context[state.name] = "visited"
    print(state.name)
    context[state.name] = state.name
    print(pprint.pformat(context))
    if state.name == "START":
        return "input"
    if state.name == "STAGE1":
        return "input2"
    if state.name == "FIN":
        return "ii"


def test_no_initial_stage_raise_attribute_error():
    """[summary]

    test_no_initial_stage_raise_Attribute_error.
    """
    stage1 = State("STAGE1", f)
    fsm = FiniteStateMachine("TheMachine")
    fsm.add_state([stage1])
    with pytest.raises(AttributeError):
        fsm.run({})


def test_input_not_in_alphabet_raises_transition_error():
    """[summary]

    test_no_initial_stage_raise_Attribute_error.
    """
    stage1 = State("STAGE1", f)
    fsm = FiniteStateMachine("TheMachine")
    fsm.add_state([stage1])
    with pytest.raises(TypeError):
        fsm.process(["a"])


def test_multiple_initial_stages_raise_transition_error():
    """[summary]

    test_no_initial_stage_raise_Attribute_error.
    """
    start = State(
        "START",
        f,
        initial=True,
    )
    stage1 = State(
        "STAGE1",
        f,
        initial=True,
    )
    fsm = FiniteStateMachine("TheMachine")
    with pytest.raises(TransitionError):
        fsm.add_state([start, stage1])


def test_attributes_are_set():
    """[summary]

    test_no_initial_stage_raise_Attribute_error.
    """
    #    #reset_singleton()
    #    #Config.Basic(TEST_SERVICE_NAME)
    final = State("FINAL", f, final=True)
    error = State(
        "ERROR",
        f,
        error=True,
        mail_addr='[{"A":"error_handler@mail.company"}]',
        default=final,
    )
    start = State("START", f, initial=True, default=error)
    stage1 = State("STAGE1", f, default=error)

    start["input"] = stage1
    stage1["input2"] = final
    error["go_back_to_start"] = start
    error["go_back_to_stage1"] = stage1
    kk = start["input"]
    print(kk)

    print(start)
    # start.compute_function(start,d)
    # stage1.compute_function(stage1,d)
    # error.compute_function(error,d)
    # final.compute_function(final,d)
    #

    fsm = FiniteStateMachine("TheMachine")
    fsm.add_state([start, stage1, error, final])
    fsm.run({})
    # assert False

    graph = get_graph(fsm)
    graph.draw("x.png", prog="dot")
    graph.draw("x.svg", prog="dot")


#
# Graph Printing
#
def test_get_graph_without_initi_state_raises_stateerror():
    """[summary]

    test_no_initial_stage_raise_Attribute_error.
    """
    final = State("FINAL", f, final=True)
    fsm = FiniteStateMachine("TheMachine")
    fsm.add_state([final])
    with pytest.raises(StateError):
        get_graph(fsm)
