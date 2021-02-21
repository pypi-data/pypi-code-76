class System(object):
    """This class represents a System Dynamics system/model.

    It maintains a list of system elements (:py:attr:`~_system_elements`).
    """

    def __init__(self, name):
        """Constructor method.

        :param name: The name of the system.
        :type name: str, optional
        """
        self.name = name
        self._system_elements = []
        """ A list of system elements.
        
        :type: list
        """


    def show_system_elements(self):
        """Creates a string with information about the system elements.

        This includes the properties :py:attr:`~.SystemElement.name` and 
        :py:attr:`~.SystemElement.var_name`. Depending on the system element
        :py:attr:`~.Stock.calc_rule` and :py:attr:`~.Stock.input_elements`
        are given as additional information. :py:attr:`~.Stock.input_elements`
        only shows the name of all direct input elements to prevent recursion.
        The string is printed to the console.
        """
        s = ""
        s += "==== " + self.name + " ====\n"
        for element in self._system_elements:
            s += "{ name: " + element.name
            if hasattr(element, "value"):
                s += ", value: " + str(element.value)
            s += ", var_name: " + str(element.var_name)
            if hasattr(element, "input_elements"):
                s += ", input_elements: ["
                for idx, input_element in enumerate(element.input_elements):
                    if idx < len(element.input_elements)-1:
                        s += "{ name: " + input_element.name + "}, "
                    else:
                        s += "{ name: " + input_element.name + "}"
                s += "]"
            s += "}\n"
        print(s)


    @property
    def name(self):
        """see :py:meth:`~__init__`
        """
        return self._name


    @name.setter
    def name(self, value):
        if len(value):
            self._name = value
        else:
            raise ValueError("name can not be empty")