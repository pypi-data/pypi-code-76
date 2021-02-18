"""
    Copyright 2020 Simon Vandevelde, Bram Aerts, Joost Vennekens
    This code is licensed under GNU GPLv3 license (see LICENSE) for more
    information.
    This file is part of the cDMN solver.
"""

import xml.etree.ElementTree as ET
import re
import numpy as np
import collections


class XMLparser:
    """
    The parser class responsible for parsing the xml file, and turning it into
    cDMN tables.
    This means a conversion from XML into the Type and Constant glossary, and
    into standard Decision Tables.
    """
    def __init__(self, xml_str: str):
        """
        Initializes the class.

        :arg xml_str: the xml file, as one big string.
        """
        # Initialize all the variables.
        self.__root = None
        self.__table_nodes = {}
        self.__tables = []
        self.__var_types = collections.defaultdict(lambda: 'Key not found')
        self.__predefined_values = {}
        self.__possible_values = {}
        self.__type_glos = {}
        self.__constant_glos = {}
        self.__bool_glos = {}
        self.__types = {}
        self.__dependency_graph = {}

        # Parse the xml, grab the root.
        self.root = ET.fromstring(xml_str)

        # Look for all the XML tables nodes.
        self.__table_nodes = self.__find_table_nodes()

        # Convert the XML table nodes into numpy tables, as if they are cDMN
        # decision tables.
        self.__tables, self.__var_types, self.__predefined_values = \
            self.__convert_to_numpy()

        # Find the constants, possible values and types by looking through the
        # numpy tables.
        self.__constants, self.__possible_values, self.__types, \
            self.__booleans = self.__find_constants_booleans()

        # Now we create the glossary, based on the values we find.
        # After this, we have converted DMN into a full cDMN model.
        self.__type_glos = self.__create_type_glos()
        self.__constant_glos = self.__create_constant_glos()
        self.__bool_glos = self.__create_boolean_glos()

        self.get_goal_variables()

    def __find_namespace(self, elem):
        """
        Method to find the namespace of the XML we're parsing.

        :returns namespace:
        """
        if elem.tag[0] == "{":
            ns, ignore, tag = elem.tag[1:].partition("}")
        else:
            ns = None
        return ns

    def __find_table_nodes(self):
        """
        Iterates through the XML, and search for the "decisionTable" elements.
        We keep a dictionary which maps every table id on their contents.

        :returns nodes: a dict containing XML decisionTable nodes.
        """
        ns = {'dmn': self.__find_namespace(self.root)}
        decisions = self.root.findall('dmn:decision', ns)
        nodes = {}
        for decision in decisions:
            table_id = decision.attrib['id']
            if table_id in nodes.keys():
                raise ValueError("Duplicate table ids!")

            # Find the table element and add it to the dict.
            table = decision.find('dmn:decisionTable', ns)
            nodes[table_id] = table

        return nodes

    def __cDMN_type(self, var_type) -> str:
        """
        Help function which converts a DMN variable type into a cDMN one.
        cDMN only knows 4 types: string, int, float and real (these last two
        are the same).

        :param var_type: the DMN variable type to convert.

        :returns str: the cDMN variable type.
        :raises ValueError: in case an unknown DMN variable type is given.
        """
        if var_type == "string":
            return "string"
        elif var_type == "integer" or var_type == "feel:number":
            return "Int"
        elif var_type == "long" or var_type == "double":
            return "Real"
        elif var_type == "boolean":
            return "bool"
        else:
            raise ValueError(f"Unknown variable type: {var_type}")

    def __convert_to_numpy(self):
        """
        Convert every decisionTable XML node into a numpy table, conform to the
        cDMN format.

        :returns tables: an array of np.arrays, each representing a decision
            table.
        :returns var_types: a dictionary mapping each variable on their type.
        :returns predefined_val: a dictionary mapping each variable on a
            string of predefined values, if it is present.
        """
        # Set the namespace of the XML.
        ns = {'dmn': self.__find_namespace(self.root)}

        tables = []
        predefined_val = {}
        # We use a default dict to prevent errors later for unknown variables.
        var_types = collections.defaultdict(lambda: "Key not found")
        for i, (table_name, table_node) in \
                enumerate(self.__table_nodes.items()):
            inputs = []
            outputs = []
            rules = []
            hit_policy = table_node.get("hitPolicy")
            name = table_name

            if name is None:
                name = f"table{i}"

            # Find all input columns.
            inputs = table_node.findall('dmn:input', ns)
            for child in inputs:

                # Set the variable's type, in cDMN format.
                try:
                    input_expr = child.find('dmn:inputExpression', ns)
                    type_name = input_expr.find('dmn:text', ns).text
                    var_type = input_expr.attrib['typeRef']
                    var_types[type_name] = self.__cDMN_type(var_type)
                except KeyError:
                    pass
                except IndexError:
                    raise IndexError(f"Input index out of range. Did you"
                                     f" forget to set the Input Expression"
                                     f" for column {child.attrib['label']}"
                                     f" in table {table_name}?")

                # Check if there are predefined values set.
                input_vals = child.find('dmn:inputValues', ns)
                if input_vals is not None:
                    text = input_vals.find('dmn:text', ns).text
                    predefined_val[type_name] = text
                continue

            # Find all output columns.
            outputs = table_node.findall('dmn:output', ns)
            for child in outputs:

                # Set the variable's type, in cDMN format.
                try:
                    type_name = child.attrib['name']
                    var_type = child.attrib['typeRef']
                    var_types[type_name] = self.__cDMN_type(var_type)
                except KeyError:
                    pass

                # Check if there are predefined values set.
                output_vals = child.find('dmn:outputValues', ns)
                if output_vals is not None:
                    text = output_vals.find('dmn:text', ns).text
                    predefined_val[type_name] = text
                continue

            rules = table_node.findall('dmn:rule', ns)

            # Table dimensions: #inputs+#outputs + 1 x #rules + 2
            table_width = len(inputs) + len(outputs) + 1
            table_height = len(rules) + 2

            # Create an empty table and set its name.
            table = np.full((table_height, table_width), None)
            table[0][0:len(inputs)+1] = name

            # Set the hit policy.
            if hit_policy is None or hit_policy == "UNIQUE":
                table[1][0] = "U"
            elif hit_policy == "ANY":
                table[1][0] = "A"
            elif hit_policy == "FIRST":
                table[1][0] = "F"
            elif hit_policy == "COLLECT":
                aggr = table_node.get("aggregation")
                if aggr is None:
                    table[1][0] = "A"
                elif aggr == "SUM":
                    table[1][0] = "C+"
                else:
                    raise IOError(f"Unsupported aggregate {aggr}")
            else:
                raise IOError(f"Unsupported hit policy: {hit_policy}")

            # Fill in the table input headers.
            for i, input_node in enumerate(inputs):
                header = (input_node.find('dmn:inputExpression', ns)
                                    .find('dmn:text', ns).text)
                table[1][i+1] = header

            # Fill in the table output headers.
            for i, output_node in enumerate(outputs):
                table[1][len(inputs)+1+i] = output_node.get("name")

            # Fill in the table rules.
            for i, rule_node in enumerate(rules):
                table[i+2][0] = i + 1
                j = 1
                # Find all entry nodes, i.e. input and output nodes.
                entry_node = rule_node.findall('dmn:inputEntry', ns)
                entry_node += rule_node.findall('dmn:outputEntry', ns)
                for child in entry_node:
                    try:
                        value = (child.find('dmn:text', ns).text
                                                           .replace('"', ''))
                        # Replace the spaces in strings.
                        if not re.search(r"(\[|\]|>|<|=|\(|\))", value):
                            value = value.replace(" + ", "+")
                        # Uppercase any occurence of true or false.
                        if re.match("true", value, re.IGNORECASE):
                            value = "Yes"
                        elif re.match("false", value, re.IGNORECASE):
                            value = "No"
                    except AttributeError:
                        value = "-"
                    table[i+2][j] = value
                    j += 1
            tables.append(table)
        return tables, var_types, predefined_val

    def __find_constants_booleans(self):
        """
        Iterates over all input and output columns and do the following:
            * Store all constants, found in column headers, in a set.
            * Store all booleans, found in column headers, in a set.
            * Store all possible value for all constants, in a dict.
            * Store the type of every constant, in a dict.

        :returns constants: a set containing all constants in the tables.
        :returns possible_values: a dict containing all possible values for the
            constants.
        :returns types: a dict containing the type for each constant.
        :returns booleans: a set containing all boolean objects.
        """
        constants = set()
        booleans = set()
        possible_values = {}
        types = self.__var_types

        for table in self.__tables:
            for column in table[1:].T[1:]:
                # The atom's name is defined in the header.
                var = column[0]

                # If the var has no posvars set, make one.
                if var not in possible_values.keys():
                    possible_values[var] = set()

                # Check if we already know the var's type.
                if self.__var_types[var] == "Int" or \
                        self.__var_types[var] == "Real":
                    # For ints or real, no values need to be added.
                    constants.add(var)

                elif self.__var_types[var] == "bool":
                    # Booleans also do need predefined values.
                    booleans.add(var)

                elif self.__var_types[var] == "string":
                    constants.add(var)
                    # If given, use the list of predefined values.
                    if var in self.__predefined_values.keys():
                        possible_values[var] = set()
                        posvals = self.__predefined_values[var]
                        posvals.replace('"', '')
                        for val in posvals.split(','):
                            possible_values[var].add(val)
                    # If no predefined values were given, we iterate over every
                    # value in the column and we add them to the set of
                    # possible values.
                    else:
                        for value in column[1:]:
                            if value == "-" or value is None or value == "":
                                continue
                            elif "not(" in value:
                                continue
                            elif "," in value:
                                for val in value.split(","):
                                    val = val.strip()
                                    possible_values[var].add(val)
                            else:
                                possible_values[var].add(value)

                # If we do not know its type, we need to find out.
                else:
                    for value in column[1:]:
                        if re.search(r"(\[|\]|>|<|=|\(|\))", value):
                            # If we find one of these symbols, it is always a
                            # constant real.
                            types[var] = "Real"
                            constants.add(var)
                        else:
                            # If a "-" is used, we don't need to add it.
                            if value == "-" or value is None or value == "":
                                continue
                            try:
                                # If the value is a number, it is always a
                                # constant. We set its type as real.
                                # No possible value needs to be added.
                                float(value)
                                types[var] = "Real"
                                constants.add(var)
                            except ValueError:
                                # Check if true or false appear. If so, it's a
                                # bool.
                                if re.match("Yes$", value, re.IGNORECASE):
                                    booleans.add(var)
                                    continue
                                elif re.match("No$", value, re.IGNORECASE):
                                    booleans.add(var)
                                    continue

                                # If it's not a bool, add it to the list of
                                # constants.
                                constants.add(var)
                                types[var] = "string"
                                possible_values[var].add(value)

        return constants, possible_values, types, booleans

    def __create_type_glos(self):
        """
        Creates the type glossary.

        :returns type_glos: a np.array containing the type glossary.
        """

        # Count the amount of types, create an empty Type table.
        str_amount = list(self.__types.values()).count('string')
        type_glos = np.full((2+str_amount, 3), None)

        # Fill the header with the names.
        type_glos[0] = "Type"
        type_glos[1][0] = "Name"
        type_glos[1][1] = "DataType"
        type_glos[1][2] = "Possible Values"

        # Now create a type for each string constant!
        i = 2
        for constant in self.__constants:
            # We only need to create entries for the string.
            if self.__types[constant] != 'string':
                continue
            type_glos[i][0] = constant + "t"
            type_glos[i][1] = self.__types[constant]
            posvals = ", ".join(self.__possible_values[constant])
            type_glos[i][2] = posvals.replace('"', '')
            i += 1

        return type_glos

    def __create_constant_glos(self):
        """
        Creates the constant glossary.

        :returns constant_glos: a np.array containing the constant glossary.
        """

        # Create an empty Constant table.
        constant_glos = np.full((2+len(self.__constants), 2), None)

        # Fill in the header with the names.
        constant_glos[0] = "Constant"
        constant_glos[1][0] = "Name"
        constant_glos[1][1] = "DataType"

        # Fill in every constant.
        for i, constant in enumerate(self.__constants):
            constant_glos[i+2][0] = constant
            if self.__types[constant] == 'string':
                constant_glos[i+2][1] = constant + "t"
            else:
                constant_glos[i+2][1] = self.__types[constant]
        return constant_glos

    def __create_boolean_glos(self):
        """
        Creates the boolean glossary.

        :returns bool_glos: a np.array containing the boolean glossary.
        """

        # Create an empty Boolean table.
        bool_glos = np.full((2+len(self.__booleans), 1), None)

        # Fill in the header with the names.
        bool_glos[0] = "Boolean"
        bool_glos[1] = "Name"

        # Fill in every boolean.
        for i, boolean in enumerate(self.__booleans):
            bool_glos[i+2] = boolean

        return bool_glos

    def get_tables(self):
        """
        Method to return all the tables as one big array.
        This is the internal cDMN representation.

        :returns tables: a list containing all decision and glossary tables.
        """
        tables = self.__tables
        tables.append(self.__constant_glos)
        tables.append(self.__type_glos)
        tables.append(self.__bool_glos)
        return tables

    def __generate_dependency_graph(self):
        """
        Iterates through the XML, and tries to create a dependency graph which
        is stored in the form of a dict.

        The leaves of the graph are the table ids with empty dependency lists
        (i.e. have no dependencies themselves) and the root of the graph is the
        table on which no other table depends. To be compliant to the
        specifications, there can only be one root. In practice however,
        who knows right? Better safe than sorry.

        :returns dependencies: a dict representing the dependency graph.
        """
        ns = {'dmn': self.__find_namespace(self.root)}
        decisions = self.root.findall('dmn:decision', ns)
        dep_graph = {}
        for decision in decisions:
            table_id = decision.attrib['id']
            dependencies = []

            for req in decision.findall('dmn:informationRequirement', ns):
                dep = req.find('dmn:requiredDecision', ns)
                if dep is not None:
                    dep_id = dep.attrib['href'][1:]  # Strip the preceding '#'
                    dependencies.append(dep_id)

            dep_graph[table_id] = dependencies
        return dep_graph

    def get_goal_variables(self):
        """
        Find the variables which are defined by the last decision table.
        This decision table always contains the "final decision" of the
        specification, and thus, its outputs contain the goals.

        :returns goal_variables: list containing the names of the goal var.
        """
        if len(self.__dependency_graph) == 0:
            self.__dependency_graph = self.__generate_dependency_graph()

        # Get list of the goal table ids.
        table_ids = list(self.__table_nodes.keys())
        goal_ids = []
        for table_id in table_ids:
            # If the table_id does not appear as any dependency, it is a/the
            # root.
            is_dependency = False
            for dep_ids in self.__dependency_graph.values():
                if table_id in dep_ids or is_dependency:
                    is_dependency = True
                    continue
            if is_dependency:
                continue
            goal_ids.append(table_id)

        # Get output variable(s) of the goal table ids.
        ns = {'dmn': self.__find_namespace(self.root)}
        goal_variables = []
        for table_id in goal_ids:
            outputs = self.__table_nodes[table_id].findall('dmn:output', ns)
            for output in outputs:
                goal_variables.append(output.attrib['name'])
        return goal_variables

    def get_table_dependencies(self, table_name, dependencies=[]):
        """
        Returns a list of all the tables which depend on the table with
        `table_name`.
        This includes indirect dependencies as well.

        :returns dependencies: list of all dependencies.
        """
        # dep_graph should be cached, too lazy rn.
        dep_graph = self.__generate_dependency_graph()

        for table in dep_graph[table_name]:
            dependencies.append(table)
            dependencies = self.get_table_dependencies(table, dependencies)

        return dependencies
