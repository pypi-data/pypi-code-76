"""
Implement the ps Finite State Machine.

 >>> import os
"""


import ps.basic.Config
from ps.basic import __version__ as version
from ps.basic import get_html_string
from ps.basic.State import State


class TransitionError(Exception):
    """[summary]

    State Exception.

    :param Exception: [description]
    :type Exception: [type]
    """

    def __init__(self, message):
        """[summary]

        :param message: [description]
        :type message: [type]
        """
        self.message = message


class FiniteStateMachine(object):
    """[summary]

         :param object: [description]
         :type object: [type]

         Import ...

         >>> from ps.basic.State import State, StateError
         >>> from ps.basic.fsm import FiniteStateMachine, TransitionError

         Define  handler functions.

         The __doc__ variables text of a handler function lateron will
         be displayed within the generated documentations tooltip.

         >>> def init_state_handler(state: State, context_p: dict) -> str:
         ...   __doc__="This is the documentation of init_state_handler"
         ...   context_p[state.name] = "visited"
         ...   if True:
         ...       return "INIT_OK"
         ...   else:
         ...       return "DIRECT"
         >>> def state1_handler(state: State, context_p: dict) -> str:
         ...   __doc__="This is the documentation of state1_state_handler"
         ...   context_p[state.name] = "visited"
         ...   return "STATE1_OK"
         >>> def error_state_handler(state: State, context_p: dict) -> str:
         ...   __doc__="This is the documentation of error_state_handler"
         ...   context_p[state.name] = "visited"
         ...   return "ERROR_STATE_OK"
         >>> def fin_state_handler(state: State, context_p: dict) -> str:
         ...   __doc__="This is the documentation of fin_state_handler"
         ...   context_p[state.name] = "visited"
         ...   return "FIN_STATE_OK"

        Given the defined handler_functions, we are able to define State
        variables using those handler functions.

        First a final state is defined - the fsm terminates if it enters
        a final state.

         >>> final = State("FINAL", fin_state_handler, final=True)

        Next we define an error state - entering the error state may result
        in sending an email to some recipients - defined in the mail_addr list.

         >>> error = State( "ERROR",error_state_handler, error=True,
         ...     mail_addr='[{"A":"ror_handler@mail.company"}]',
         ...     default=final,)

        Now we define state handling functions - the default parameter
        tells the state, that in case  the states compute_function
        returns a string not definied
        im the state's transition strings, that state will be entered.

         >>> start = State("START", init_state_handler,
         ...                initial=True, default=error)
         >>> state1 = State("STATE1", state1_handler, default=error)


         Currently we have 4 State Instances named final, error,
         start and state1.

         A State instance  (inherited from dict)  defines a
         key/value pair where:

             - key is a string (the string returned by a
               states computing function)
             - value is the reference to the state to be
               visited  if the states
               computing function returns that string.

         - if in state start  and start.computing_function alia
           init_state_handler() returns "INIT_OK" we switch
           to state state1

         >>> start["INIT_OK"] = state1
         >>> start["DIRECT"] = final

             - if in state state1 and  state1.computing_function()
               alia state1_state_handler() returns "STATE1_OK"
               we switch to state final

         >>> state1["STATE1_OK"] = final

             - if in state error  and error.computing_function()
               alia error_state_handler() returns
               "ERROR_STATE_OK" we switch to state final

         >>> error["ERROR_STATE_OK"] = final

         Creating an instance of the Finite State machine

         >>> fsm = FiniteStateMachine("ThedoctestMachine")

         Add the before defined states and state exhchanges
         to the FiniteStateMachine instance *fsm*

         >>> fsm.add_state([start, state1, error, final])

         Define an empty context

         >>> context = {}

         Run the finite State machine.

         >>> from ps.basic import Config
         >>> import os
         >>> os.environ["DEV_STAGE"] = "TESTING"
         >>> from ps.basic.Config import reset_singleton  
         >>> reset_singleton()
         >>> singleton=Config.Basic("fsm_test")
         >>> fsm.run(context)

         As the (for all states) used handler_function  puts its
         state name to the context we get an context as assumed.

         >>> context
         {'START': 'visited', 'STATE1': 'visited', 'FINAL': 'visited'}

        To Check the behaviour of the fsm we can inspect the trace of
        the last run - it is remebered in fsm.inputs:

        >>> fsm.inputs
        ['INIT_OK', 'STATE1_OK', 'FIN_STATE_OK']

        For the next run we are able to  Reset the fsms state, the
        inputs will be empty.

        >>> fsm.reset()
        >>> fsm.inputs
        []

        To check  the transitions defined  inside the fsm:

        >>> fsm.all_transitions # doctest:+ELLIPSIS
        [(<'START' State @ 0x...>, 'INIT_OK', <'STATE1' State @ 0x...>)]

    ..    [(<'START' State @ 0x...>, 'INIT_OK', <'STATE1' State @ 0x...>),
          (<'STATE1' State @ 0x...>, 'STATE1_OK', <'FINAL' State @ 0x...>),
          (<'ERROR' State @ 0x...>, 'ERROR_STATE_OK', <'FINAL' State @ 0x...>)]


        Generate an image of the fsm - based on it's implementation ...

        >>> from ps.basic.get_graph import get_graph
        >>> graph = get_graph(fsm)
        >>> graph.draw(f"{fsm.name}.svg", prog="dot")

    .. Comment  Copy the file to the documentation environment
       >>> assert os.path.isfile(f"{fsm.name}.svg")
       >>> from shutil import copyfile
       >>> assert os.path.isdir("../docs/source")
       >>> copyfile(f"{fsm.name}.svg", f"../docs/source/{fsm.name}.svg")
       '../docs/source/ThedoctestMachine.svg'

    It serves as a good documentation for the implementatons behaviour.

        .. image:: ThedoctestMachine.svg

    """

    def __init__(self, name: str):
        """[summary]

        Construct a FSM.

        :param name: [description]
        :type name: str
        """
        self.name = name
        self.current_state, self.init_state = None, None
        self.inputs, self.states, = (
            [],
            [],
        )
        self.final_states = []
        self.error_states = []

    def add_state(self, states: [State]) -> None:
        """[summary]

        Add State(s) to the fsm.

        :param states: [description]
        :type states: [type]
        :raises TransitionError: [description]
        """
        for state in states:
            if state.error:
                self.error_states.append(state)
            if state.final:
                self.final_states.append(state)
            if state.initial:
                if self.init_state is None:
                    self.init_state = state
                else:
                    raise TransitionError("Only One initial State allowed.")
            self.states.append(state)

    @property
    def all_transitions(self):
        """[summary]

        Get transitions from the states of the fsm.

        :return: [ (source state, input, destination state) ]
        :rtype: [type]
        """
        transitions = list()
        for src_state in self.states:
            for input_value, dst_state in src_state.items():
                transitions.append((src_state, input_value, dst_state))
        return transitions

    def transition(self, input_value: str):
        """[summary]

        Transition to the next state.

        :param input_value: [description]
        :type input_value: str
        """
        current = self.current_state
        destination_state = current[input_value]
        self.current_state = destination_state

    def reset(self):
        """[summary]

        Enter the Finite State Machine.
        """
        self.current_state = self.init_state
        del self.inputs
        self.inputs = list()

    def process(self, input_data: str):
        """[summary]

        Process input data.

        :param input_data: [description]
        :type input_data: str
        """
        self.reset()
        for item in input_data:
            self.transition(item)

    def run(self, context: dict):
        """[summary]

        Process input data.

        :param context: [description]
        :type context: dict
        """
        self.reset()
        current_state = self.init_state
        ps.basic.Config.logger.debug(
            "FSM: " + self.name + " started in State " + str(current_state),
            extra={"package_version": version},
        )
        while True:
            my_current_state = self.current_state
            rval = my_current_state.compute_function(my_current_state, context)
            s = f"{my_current_state.name}-compute_function ret {str(rval)}"
            # print(s)
            ps.basic.Config.logger.debug(
                s,
                extra={"package_version": version},
            )
            s = f"{self.name}.run new step: {my_current_state.name} compute"
            s += f" function left context as {get_html_string(context)}"
            ps.basic.Config.logger.debug(
                s,
                extra={"package_version": version},
            )
            self.inputs.append(rval)
            if my_current_state.final is True:
                ps.basic.Config.logger.debug(
                    f"""Leave run, as
                     {self.current_state.name}
                      is a final state """,
                    extra={"package_version": version},
                )
                break
            else:
                self.transition(rval)
                ps.basic.Config.logger.debug(
                    f"""TRANSITION: from State
                    {my_current_state.name}
                    <br> ONInput:
                    {str(rval)}
                    <br>To State:
                    {self.current_state.name}""",
                    extra={"package_version": version},
                )
