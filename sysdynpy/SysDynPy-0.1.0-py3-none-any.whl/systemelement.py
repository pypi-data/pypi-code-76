from abc import ABC, abstractmethod
import re
from sysdynpy.system import System
from abc import ABC, ABCMeta, abstractmethod

class SubclassOnlyABC(object):
    """Helper class to prevent instantiation.
    The class SystemElement is declared as abstract and should not be instantiated.
    However, if there are no abstract methods present, it could be
    instantiated.
    
    By deriving SystemElement from this class we ensure that no instances can be
    created. This is done by overriding the __new__ method.
    """
    __metaclass__ = ABCMeta
    def __new__(cls, *args, **kwargs):
        if cls.__bases__ == (SubclassOnlyABC,):
            msg = 'Abstract class {} cannot be instantiated'.format(cls.__name__)
            raise TypeError(msg)
        return super(SubclassOnlyABC, cls).__new__(cls)


class SystemElement(SubclassOnlyABC):
    """An **abstract** class for generic system elements. Concrete system elements
    like stacks or flows are derived from this class.
    """

    def __init__(self, name, system, var_name):
        """Constructor method.

        As this is an abstract class this constructor **can not be called** directly.
        But it provides a way to bundle code that needs to run when a subclass
        instance is created.

        :param name: The element name. Can not be empty. Must be unique within the system.
        :type name: str
        :param system: The system that this element shall be part of.
        :type system: System
        :param var_name: The name of the variable this element will be assigned to,
            once it is constructed. This is needed because the variable name has to
            be known in other modules to execute the lambda expression that defines
            the calculation rule.
        :type var_name: str
        """
        self.name = name
        self.system = system
        self.var_name = var_name
        # add to list of elements in system class
        system._system_elements.append(self)


    @property
    def name(self):
        """see :py:meth:`~__init__`
        """
        return self._name


    @property
    def value(self):
        """The numeric value that is used in calculations.

        :type: int or float
        """
        return self._value


    @property
    def var_name(self):
        """see :py:meth:`~__init__`
        """
        return self._var_name


    @property
    def system(self):
        """see :py:meth:`~__init__`
        """
        return self._system


    @name.setter
    def name(self, value):
        if len(value):
            self._name = value
        else:
            raise ValueError("name can not be empty")


    @value.setter
    def value(self, value):
        self._value = value


    @system.setter
    def system(self, value):
        self._system = value

    @var_name.setter
    def var_name(self, value):
        # check if value is a valid python variable name
        pattern = re.compile("[a-zA-Z_][a-zA-Z\d_]*")
        if pattern.match(value):
            self._var_name = value
        else:
            raise ValueError("Given name " + value + " is no valid name for a " \
                + "python variable")