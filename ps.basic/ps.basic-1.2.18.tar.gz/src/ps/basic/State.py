from typing import Any, Callable


class StateError(Exception):
    """[summary]

    Error in setting a destination state based on a string.

    :param Exception: [description]
    :type Exception: [type]
    """

    def __init__(self, message):
        """[summary]

        :param message: [description]
        :type message: [type]
        """
        self.message = message


class State(dict):
    """[summary]

        :raises StateError: [description]
        :return: [description]
        :rtype: [type]

    State class.

    A State instance is a dictionary:
         - its keys are the strings identified for state_changes of the
           fsm the states are used within
         - the value correlated to the key defines a state instance
           (the next state) if the state computing function returns that value

    We first define a state_enter_function *f* ...

    >>> def f(state: State, context_p: dict) -> str:
    ...     context_p["fin_visited"] = True
    ...     return "FIN"

    In the next step we define a State. The creation of the State
    indicates, that the function
    *f* will be executed if we enter the state.
    Furthermore we indicate, (final=True) that the state is a final state.

    >>> final = State("FINAL", f, final=True)

    We define a dictionary named context. That dictionary is a required
    parameter to any  states computing function.

    >>> context={}

    If we call the states computing function it will return the string "FIN"

    >>> final.compute_function(final,context)
    'FIN'

    It will modify the context

    >>> context["fin_visited"]
    True

    Let us create other states

    >>> other_state = State("other_state", f)
    >>> other_state2 = State("other_state2", f)

    and set it's behaviour so, that if its compute fuction returns
    'Go_To_Fi_State' it will change its state to the final state.

    >>> other_state["Go_To_Fi_State"] = final
    >>> other_state["Go_To_Other_State2"] = other_state2

    To show the state_change list we issue:

    >>> other_state.keys()
    dict_keys(['Go_To_Fi_State', 'Go_To_Other_State2'])

    To find out, to which state we change if the states compute function
    returns a value we check:

    >>> other_state['Go_To_Fi_State']  #doctest: +ELLIPSIS
    <'FINAL' State ...>
    >>> other_state['Go_To_Other_State2']  #doctest: +ELLIPSIS
    <'other_state2' State ...>

    """

    def __init__(
        self,
        name: str,
        compute_function: Callable[[Any, dict], str],
        initial: bool = False,
        final: bool = False,
        error: bool = False,
        mail_addr: str = "",
        default: Any = None,
    ):
        """[summary]

        Construct a state.
        :param name: [description]
        :type name: str
        :param compute_function: [description]
        :type compute_function: Callable[[Any, dict], str]
        :param initial: [description], defaults to False
        :type initial: bool, optional
        :param final: [description], defaults to False
        :type final: bool, optional
        :param error: [description], defaults to False
        :type error: bool, optional
        :param mail_addr: [description], defaults to ""
        :type mail_addr: str, optional
        :param default: [description], defaults to None
        :type default: Any, optional
        """
        self.name = name
        self.compute_function = compute_function
        self.final = final
        self.error = error
        self.initial = initial
        self.mail_addr = mail_addr
        self.default_transition = default
        self.tooltip = "None"

    def __getitem__(self, input_value):
        """[summary]

        Make a transition to the next state.
        :param input_value: [description]
        :type input_value: [type]
        :return: [description]
        :rtype: [type]
        """
        return dict.__getitem__(self, input_value)

    def __setitem__(self, input_value, next_state):
        """[summary]

        Set a transition to a new state.
        :param input_value: [description]
        :type input_value: [type]
        :param next_state: [description]
        :type next_state: [type]
        :raises StateError: [description]
        """
        if not isinstance(next_state, State):
            raise StateError(
                "A state must transition to another state,"
                " got %r instead." % next_state
            )
        dict.__setitem__(self, input_value, next_state)

    def __repr__(self):
        """[summary]

        Represent the object in a string.
        :return: [description]
        :rtype: [type]
        """
        return "<%r %s @ 0x%x>" % (
            self.name,
            self.__class__.__name__,
            id(self),
        )
