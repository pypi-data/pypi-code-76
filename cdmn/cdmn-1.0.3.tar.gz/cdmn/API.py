"""
    Copyright 2020 Simon Vandevelde, Joost Vennekens
    This code is licensed under GNU GPLv3 license (see LICENSE) for more
    information.
    This file is part of the cDMN solver.
"""
from cdmn.parse_xml import XMLparser
from cdmn.glossary import Glossary
from cdmn.interpret import VariableInterpreter
from cdmn.idply import Parser
from cdmn.table_operations import (fill_in_merged, identify_tables,
                                   find_glossary, find_execute_method,
                                   replace_with_error_check,
                                   create_voc, create_main, create_struct,
                                   create_theory, find_auxiliary_variables,
                                   create_display, create_dependency_graph,
                                   get_dependencies)
from idp_solver import idpparser
import sys
from io import StringIO
import copy
from typing import Dict, List


class DMNError(Exception):
    """ Base class for all DMN-related exceptions """
    pass


class NotSatisfiableError(DMNError):
    """ Error thrown when unsat """


class Variable():
    """
    Class representing (c)DMN variables.
    On top of variable name, type, logical type and value, we also gather what
    dependencies (both upstream and downstream) a variable has.

    :param name: the name of the variable
    :type name: str
    :param type: if the variable is a constant, the type can be string,
        integer, float. If the variable is a boolean, the type is None.
    :type type: str
    :param logical_type: the variable type from a logical viewpoint.
        This can be boolean, constant, predicate or function.
    :type logical_type: str
    :param value: the value that a symbol has.
    :type value: str, int
    :param possible_values: a list containing possible values.
        This list is only relevant for symbols with type string.
    :type value: List[str]
    :param dependent_on: a Dict of symbols on which this variable depends,
        together with their 'dependency level'
    :type dependent_on: List[str]
    :param dependency_of: a Dict of symbols that depend on this variable,
        together with their 'dependency level'
    :type dependency_of: List[str]
    """
    def __init__(self, name: str, var_type: str, logical_type: str,
                 possible_values: List, dependent_on: Dict,
                 dependency_of: Dict):
        self.name = name
        self.type = var_type
        self.logical_type = logical_type
        self._value = None
        self.possible_values = possible_values
        self.dependent_on = dependent_on
        self.dependency_of = dependency_of

    def __str__(self):
        return f"{self.name} {self.logical_type}, with value {self.value}"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if (self.possible_values and new_value and
                new_value not in self.possible_values):
            raise DMNError(f'Value {new_value} not in possible values for'
                           f' {self.name}.\n Possible values:'
                           f' {self.possible_values}'
        self._value = new_value

    def is_input(self):
        if len(self.dependent_on) == 0:
            return True
        else:
            return False

    def is_output(self):
        if len(self.dependency_of) == 0:
            return True
        else:
            return False


class DMN():
    """
    A class representing DMN objects.

    :param _specification: the xml specification
    :type _specification: str
    :param variables: a dict containing all the variables found in the
        specification
    :type variables: Dict[str]: :class:`cdmn.API.Variable`
    :param prop_variables: a dict containing the values of propagated
        variables
    :param dependency_tree: a dictionary containing for every variable what
        other variables define it
    :type dependency_tree: Dict[str]: List[str]
    :param _idp: a dictionary containing the IDP blocks
    :type _idp: Dict[str]: str
    """
    def __init__(self, path: str = None, xml: str = None,
                 auto_propagate: bool = False):
        """
        Initializes the DMN object.
        There are two ways to input the DMN:
            * Using `path` by supplying a path to the DMN file.
            * Using `xml` by supplying the XML directly.

        By setting the specification, we also invoke _update_variables().

        :param path: the path to a .dmn file
        :type path: str, optional
        :param xml: xml representing a DMN model
        :type xml: str, optional
        """
        self._specification = ''
        self.variables: Dict[str, Variable] = {}
        self.prop_variables: Dict[str, Variable] = {}
        self.dependency_tree = ''
        self.auto_propagate = auto_propagate
        self._idp = {'voc': '', 'struct': '', 'theory': '', 'main': ''}

        if path and not xml:
            with open(path, 'r') as fp:
                self.specification = fp.read()
        elif xml and not path:
            self.specification = xml
        elif xml and path:
            raise DMNError('Cannot init DMN with both path and xml.')

    def __str__(self):
        msg = "Values of DMN specification: \n"
        for name, val in self.get_all_values().items():
            msg += f"{name} = {val}\n"
        return msg

    @property
    def specification(self):
        """Getter for specification.

        :returns: the specification
        :rtype: str
        """
        return self._specification

    @specification.setter
    def specification(self, spec: str):
        """
        Setter method to set the specification.
        Additionally, this invokes the _update_variables() method.

        :param spec: the DMN specification in XML
        :type spec: str
        :returns: None
        """
        self._specification = spec
        self._update_variables()

    @property
    def idp(self):
        """Getter for idp.

        :returns: the idp code
        :rtype: str
        """
        return "".join(self._idp.values())

    def _update_variables(self):
        """ Method to update the list of variables and meta-info.

        This method sets the following attributes:
            * _idp
            * variables

        It first parses the XML, then parses the resulting cDMN, after which it
        creates a variable for every symbol in the glossary.

        :returns: None
        """
        # Parse XML, parse cDMN.
        xml_parser = XMLparser(self._specification)
        tables = xml_parser.get_tables()
        glossary = Glossary(find_glossary(tables))
        i = VariableInterpreter(glossary)
        cdmn_parser = Parser(i, 'idpz3')
        dep_graph = create_dependency_graph(tables, cdmn_parser)

        for symb in glossary.predicates:
            # Create new variable.
            if symb.zero_arity:
                logical_type = 'constant'
            else:
                logical_type = 'boolean'
            var_type = symb.super_type if symb.super_type is not None else None

            if symb.super_type is not None and symb.super_type.possible_values:
                possible_values = symb.super_type.possible_values
            else:
                possible_values = None

            up_deps = get_dependencies(symb.name, dep_graph, downstream=False)
            down_deps = get_dependencies(symb.name, dep_graph, downstream=True)

            var = Variable(symb.name, var_type.name, logical_type, possible_values,
                           up_deps, down_deps)

            self.variables[symb.name] = var

        # We don't set the main, as it depends on the inference method used.
        self._idp['voc'] = create_voc(glossary, target_lang='idpz3')
        self._idp['theory'] = create_theory(tables, cdmn_parser, False,
                                            target_lang='idpz3')

        self.prop_variables = self.variables
        if self.auto_propagate:
            self.propagate()

    def set_value(self, variable: str, value):
        """ Set a variable's value.

        :param variable: the name of the variable
        :type variable: str
        :param value: the value for the variable
        :type value: str or int
        """
        self.variables[variable].value = value
        if self.auto_propagate:
            self.propagate()
        pass

    def update_structure(self):
        """ Method to generate the structure.
        If a variable has been assigned a value, it should be included in the
        structure.

        This method also updates the struct value in _idp.

        :returns: the structure
        :rtype: str
        """
        struct = "structure S: V{\n"
        for name, var in self.variables.items():
            # If a value has been set, add it to the structure.
            if var.value:
                struct += f"{name} = {{{var.value}}}\n"

        struct += "}\n"
        self._idp['struct'] = struct

    def model_expand(self):
        """ Method to model expand the current system """
        self.update_structure()
        idp = ''.join(self._idp.values())
        idp += 'procedure main() {\n\t print(model_expand(T, S))}'
        idp = idpparser.model_from_str(idp)

        # We need to capture the idp output, which has the terminal as default
        # stdout.
        old_stdout = sys.stdout
        sys.stdout = idp_out = StringIO()
        idp.execute()
        sys.stdout = old_stdout  # Reset stdout.

        if "No models" in idp_out.getvalue():
            raise NotSatisfiableError('DMN model has no models.')
        return idp_out

    def propagate(self):
        """ Method to propagate.

        :returns: None
        :rtype: None
        :throws NotSatisfiableError: thrown when model resulted in unsat
        """
        self.update_structure()
        idp = ''.join(self._idp.values())
        idp += 'procedure main() {\n\t print(model_propagate(T, S))}'
        idp = idpparser.model_from_str(idp)

        # We need to capture the idp output, which has the terminal as default
        # stdout.
        old_stdout = sys.stdout
        sys.stdout = idp_out = StringIO()
        idp.execute()
        sys.stdout = old_stdout  # Reset stdout back to before.

        if "Not satisfiable" in idp_out.getvalue():
            raise NotSatisfiableError('DMN model not satisfiable')

        # Now that we have propagated, we check if any propagations happened.
        self.prop_variables = copy.deepcopy(self.variables)
        props = idp_out.getvalue().split('\n')
        for prop in props:
            if '->' in prop:
                variable, value = prop.split(' -> ')
                self.prop_variables[variable].value = value

    def dependencies_of(self, var: str):
        """
        Returns the list of dependencies of a variable.

        :param var: the name of the variable
        :type var: str
        :returns: list of variable dependencies
        :rtype: List[str]
        """
        return self.variables[var].dependent_on

    def type_of(self, var: str):
        return self.variables[var].type

    def possible_values_of(self, var: str) -> List:
        """
        Returns the possible values of a variable.
        Only strings have a set of possible values in DMN.

        :param var: the variable
        :type var: Variable
        :returns: list of possible values
        :rtype: List[str]
        """
        return self.variables[var].possible_values

    def value_of(self, var: str, prop: bool = True):
        if prop:
            return self.prop_variables[var].value
        else:
            return self.variables[var].value

    def is_certain(self, var: str):
        """
        Method to check if a variable is certain.
        A variable is certain if it has been given a value using `set_value`,
        or if it has been propagated a value (i.e. all of the symbols it
        depends on are also certain)

        :param var: the variable
        :type var: str
        :returns: whether the variable's value is certain
        :rtype: bool
        """
        if self.prop_variables[var].value is None:
            return False
        else:
            return True

    def get_inputs(self):
        """
        Get a list of the input variables.

        :returns: the list of inputs
        :rtype: List[str]
        """
        variables = [x for x, y in self.variables.items() if y.is_input()]
        return variables

    def get_outputs(self):
        """
        Get a list of the output variables.

        :returns: list of the output variables
        :rtype: List[str]
        """
        return [x for x, y in self.variables.items() if y.is_output()]

    def get_intermediary(self):
        """
        Get a list of intermediary variables.
        An intermediary variable is a variable that is not

        :returns: list of intermediary variables
        :rtype: List[str]
        """
        return [x for x, y in self.variables.items() if
                not y.is_input() and not y.is_output()]

    def get_unknown_variables(self):
        """
        Get a list of all variables with unknown values

        :returns: the list of variables that are still missing
        :rtype: List[str]
        """
        return [x for x, y in self.prop_variables.items() if
                not y.value]

    def get_certain_variables(self):
        """
        Get a list of all the variables for which the value is known.

        :returns: list of variables for which the value is known
        :rtype: List[str]
        """
        return [x for x, y in self.prop_variables.items() if
                y.value]

    def missing_for(self, variable: str, ):
        """
        Get a list of dependencies of varuable without known value.

        :param variable:
        :type variable: str
        :returns: list of variables needed that are still unknown
        :rtype: List[str]
        """
        return [x for x in self.prop_variables[variable].dependent_on
                if self.prop_variables[x].value is None]

    def get_all_values(self, propagated: bool = True):
        """
        Get a dictionary mapping every variable on their value.
        If the value is not known, it is None.
        If propagated is True, then we also include the values of propagated
        variables. Else, we exclude them, and set them as None.

        :param propagated: True if propagated variables are included.
        :type propagated: bool
        :returns: dict mapping variables on their (propagated) values.
        :rtype: Dict[str, str]
        """
        values = {}
        if propagated:
            values = {x: y.value for x, y in self.prop_variables.items()}
        else:
            values = {x: y.value for x, y in self.variables.items()}

        return values

    def get_variable_names(self) -> List:
        """
        Get all variable names.

        :returns: a list containing all variable names.
        :rtype: List[str]
        """
        return list(self.variables.keys())

    def clear(self):
        """
        Reset all variables' values back to None.

        :returns: None
        :rtype: Nono
        """
        for var in self.variables.keys():
            self.variables[var].value = None
        self.prop_variables = copy.deepcopy(self.variables)
