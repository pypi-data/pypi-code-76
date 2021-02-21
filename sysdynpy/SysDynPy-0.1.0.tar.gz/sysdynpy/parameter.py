from sysdynpy.systemelement import SystemElement


class Parameter(SystemElement):
    """Stores fixed values.

    Parameters don't have input elements. That means, the value of a parameter,
    once set, will not change during the simulation.
    """

    def __init__(self, name, value, system, var_name):
        """Constructor method.

        :param name: The element name. Can not be empty. Must be unique within the system.
        :type name: str
        :param value: The numeric value that is used in calculations.
        :type value: int or float
        :param system: The system that this element shall be part of.
        :type system: System
        :param var_name: The name of the variable this element will be assigned to,
            once it is constructed. This is needed because the variable name has to
            be known in other modules to execute the lambda expression that defines
            the calculation rule.
        :type var_name: str
        """
        super().__init__(name, system, var_name)
        self.value = value


    def __str__(self):
        s = ""
        s += "{ name: " + self.name \
            + ", value: " + str(self.value) \
            + ", system: " + str(self.system.name) \
            + ", var_name: " + self.var_name \
            + " }"
        return s