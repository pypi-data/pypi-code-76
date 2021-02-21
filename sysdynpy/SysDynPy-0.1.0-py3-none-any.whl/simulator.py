import time
import copy
import numbers

class Simulator(object):
    """Can be used to run simulations for a given system.
    """

    VALID_TIME_UNITS = ("milliseconds", "seconds", "minutes",
        "hours", "days", "weeks", "months", "years")
    """Possible values for the property :py:attr:`~time_unit`.
    """

    def __init__(self, simulation_steps = 10, time_unit = "days", dt=0.05):
        """Constructor method.

        :param simulation_steps: The number of steps to simulate
            when run_simulation() is called, defaults to 10
        :type simulation_steps: int
        :param time_unit: Defines the time period of one simulation step.
            The value must be one of the values defines in :py:attr:`~VALID_TIME_UNITS`
            , defaults to "days"
        :type time_unit: str
        :param dt: The interval between calculations. Must be a number between
            zero and one. The reciprocal of this argument is the number of 
            calculation steps per simulation step. One means that the system 
            element values are calculated once per simulation step. Smaller 
            numbers result in higher accuracy but longer calculation times while 
            greater numbers lead to faster calculations but lower accuracy.
            Defaults to 0.05.

            |  Example: 
            |  0.05 means the reciprocal is 1 / 0.05 = 20. So by default
               20 calculations are done per simulation step.
        :type dt: float
        """
        self.simulation_steps = simulation_steps
        self.time_unit = time_unit
        self.dt = dt
        self._system_states = []
        """ Stores the system state after each simulation step.
        
        :type: list
        """


    def run_simulation(self, system):
        """Runs a simulation for the given system.

        Once the simulation is finished, results are available by calling
        :py:meth:`~get_simulation_results`

        :param system: The system to run a simulation for.
        :type system: System
        """

        print("Simulation started")

        """
        In the initial iteration values for dynamic variables and
        flows are calculated, but nothing else changes. So we need one iteration
        more to get the required number of steps
        """
        
        for i in range(int(self.simulation_steps / self.dt)+1):
            
            # make a deep copy of the current system state
            system_backup = copy.deepcopy(system)

            # iterate all system elements
            for idx, elem in enumerate(system_backup._system_elements):
                # for flows and dynamic variables
                if "Flow" in str(type(elem)) or "DynamicVariable" in str(type(elem)):
                    # set the calculated value directly
                    system._system_elements[idx].value = \
                        self._calculate_value(elem)
                else:
                    pass # for parameters and stocks

            if i == 0:
                # in the first iteration only store the initial system state
                system_backup = copy.deepcopy(system)
                self._system_states.append(system_backup)
                continue

            # for stocks 
            for idx, elem in enumerate(system_backup._system_elements):
                if  "Stock" in str(type(elem)):
                    current_stock_value = system._system_elements[idx].value
                    change = self._calculate_stock_change(elem)
                    system._system_elements[idx].value = current_stock_value + change * self.dt

            # store copy of system state every 1 / dt iterations
            # example: dt = 0.05 --> every 20 iterations
            if int(i % (1 / self.dt)) == 0:
                self._system_states.append(system_backup)

        print("Simulation finished")

        

    def get_simulation_results(self):
        """Provides the trajectories of all system elements during the
        simulation. Must be called after the simulation.

        :return: 
            A dictionary where each key corresponds to the name of a
            system element. The values are lists. For each simulation step
            a list contains the value of the system element (key) at that
            simulation step.

            Example:

            .. code-block:: python

                {
                    someStockName: [10, 7.5, 5, 3.5, 2.5, 3, 3],
                    someFlowName: [0, -2.5, -2, -1.5, -1, 0, 0],
                    someParameterName: [3, 3, 3, 3, 3, 3, 3]
                }
        :rtype: None or dict
        """
        if not self._system_states: # empty
            return None
        else:
            result = {}
            # create dict from list of system states
            # for each state
            for state in self._system_states:
                # iterate system elements
                for element in state._system_elements:
                    if element.name not in result:
                        result[element.name] = [element.value]
                    else:
                        result[element.name].append(element.value)
        return result


    def _calculate_value(self, element):
        """Calculates the value for a given element based on the calculation rule.

        This is a recursive function to calculate the value of a flow or
        dynamic variable. The values of flows or dynamic variables can always be
        deduced from parameters or stocks. But it can not be assumed that a dynamic
        variable or flow **directly** depends on only parameters or stocks.

        :param element: The element to calculate a value for.
        :type element: Flow or DynamicVariable
        :return: The calculated value
        :rtype: float
        """
        calc_rule = element.calc_rule

        temp_dict = {}
        # store var_name of input elements as keys in temp_dict.
        # dict values are the values of input_elements
        for inp_elem in element.input_elements:
            if "Stock" in str(type(inp_elem)) or "Parameter" in str(type(inp_elem)):
                temp_dict[inp_elem.var_name] = inp_elem.value
            else:
                temp_dict[inp_elem.var_name] = self._calculate_value(inp_elem)
        
        # replace the reference to the classes in the scope of the lambda expression
        # with the values. __globals__ is a dict, so we can update it.
        for key in temp_dict:
            calc_rule.__globals__[key] = temp_dict[key]

        return calc_rule()


    def _calculate_stock_change(self, stock):
        """Calculates the change for a given stock based on the calculation rule.

        This method only checks the input- and output flows of the stock. It presumes
        that values for these flows have already been calculated for the current
        simulation step.

        :param stock: The stock to calculate the change for.
        :type stock: Stock
        :return: The calculated value
        :rtype: float
        """
        calc_rule = stock.calc_rule

        temp_dict = {}
        for inp_elem in stock.input_elements:
                temp_dict[inp_elem.var_name] = inp_elem.value
        
        for key in temp_dict:
            calc_rule.__globals__[key] = temp_dict[key]

        return calc_rule()


    @property
    def simulation_steps(self):
        """see :py:meth:`~__init__`
        """
        return self._simulation_steps


    @property
    def time_unit(self):
        """see :py:meth:`~__init__`
        """
        return self._time_unit
    

    @property
    def dt(self):
        """see :py:meth:`~__init__`
        """
        return self._dt
    

    @simulation_steps.setter
    def simulation_steps(self, value):
        if value > 0:
            self._simulation_steps = value
        else:
            raise ValueError("simulation_steps must be positive.")


    @time_unit.setter
    def time_unit(self, value):
        if value.strip().lower() in Simulator.VALID_TIME_UNITS:
            self._time_unit = value.strip().lower()
        else:
            raise ValueError("Given time unit " + value + " is not allowed. " \
                + "Allowed values are: " + str(Simulator.VALID_TIME_UNITS))
    

    @dt.setter
    def dt(self, value):
        if 0 < value and value <= 1:
            self._dt = value

