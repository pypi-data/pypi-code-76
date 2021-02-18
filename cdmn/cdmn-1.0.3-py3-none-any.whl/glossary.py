"""
    Copyright 2020 Simon Vandevelde, Bram Aerts, Joost Vennekens
    This code is licensed under GNU GPLv3 license (see LICENSE) for more
    information.
    This file is part of the cDMN solver.
"""

import re
from typing import List
from cdmn.idpname import idp_name

"""
The glossary object contains the entire cDMN glossary table.
It interprets each line, and creates a Type or Predicate/Function object.
"""


class Glossary:
    """
    The Glossary object contains all types, functions and predicates.
    During initialisation, it reads and interprets all the types, functions,
    constants, relations and booleans it can find and it reports any errors.
    Once the Glossary is created and initialized without errors, it's
    possible to print out the predicates in their IDP version.
    """
    def __init__(self, glossary_dict: dict):
        """
        Initialise the glossary.
        Create 4 default types, create an empty list of predicates, and
        interpret all 5 different glossaries.

        :arg dict: glossary_dict, the dictionary containing for each glossary
            type their tables.
        """
        self.types = [Type('String', None),
                      Type('Int', None),
                      Type('Float', None),
                      Type('Real', None)]
        self.predicates: List[Predicate] = []
        self.__read_types(glossary_dict["Type"], 0, 1, 2)
        self.__read_predicates(glossary_dict["Function"], "Function")
        self.__read_predicates(glossary_dict["Constant"], "Constant",
                               zero_arity=True)
        self.__read_predicates(glossary_dict["Relation"], "Relation")
        self.__read_predicates(glossary_dict["Boolean"], "Boolean",
                               zero_arity=True)

    def __str__(self):
        """
        Magic method to convert the Glossary to string.
        Prints out all the types, predicates and functions it contains.
        """
        retstr = "Glossary containing:\n"
        for typ in self.types:
            retstr += f"\t{str(typ)}\n"
        for pred in self.predicates:
            retstr += f"\t{str(pred)}\n"
        return retstr

    def contains(self, typestr):
        """
        Checks whether or not a type was already added to the glossary.

        :returns bool: True if the type has been added already.
        """
        for typ in self.types:
            if typestr == typ.name:
                return True
        return False

    def find_type(self, t):
        """
        Looks for types in the glossary.

        :returns List<Type>: the types found.
        """
        types = []
        for typ in self.types:
            if typ.match(t):
                types.append(typ)
        return next(filter(lambda x: x.match(t), self.types))

    def __read_types(self, array, ix_name=0, ix_type=1, ix_posvals=2):
        """
        Read and interpret all the types listed in the Type glossary.
        When it finds the keyword, it tries to interpret the other columns on
        that row.

        :arg np.array: the numpy array containing the Type glossary.
        :arg int: ix_name, the index for the name column.
        :arg int: ix_type, the index for the type column.
        :arg int: ix_posvals, the type for the posvals column.
        :returns None:
        """
        error_message = ""
        rows, cols = array.shape
        # Skip the first 2 rows, as these are headers.
        for row in array[2:]:
            # Loop over all the rows.
            name = row[ix_name]
            name = name.strip()

            # Get, and try to decypher the type.
            # If we're not able to find the type, raise error.
            typ = row[ix_type]
            try:
                typ = self.find_type(typ)
            except StopIteration:
                error_message = (f"DataType \"{typ}\" should be either a"
                                 f" (String, Int, Float) or a"
                                 f" user-defined type")
                raise ValueError(error_message)

            # Check for possible values.
            posvals = row[ix_posvals]
            try:
                # Match for the int range type, for instance [1, 10].
                int_reg = r'(\[|\()(-?\d+)\s*(?:\.\.|,)\s*(-?\d+)\s*(\]|\))'
                match = re.match(int_reg, posvals)

            except Exception:  # TODO: find errortype to except and fix except.
                match = None

            # Interpret range of int, if a match was found.
            if match:
                match = list(match.groups())
                if match[0] == '(':
                    match[1] += 1
                if match[-1] == ')':
                    match[2] -= 1
                posvals = '..'.join(match[1:-1])
            elif posvals is not None:
                posvals = ', '.join([idp_name(x) for x in
                                    re.split(r'\s*,\s*', posvals)])

            # Create the type and append it to the list.
            self.types.append(Type(name, typ, posvals))

    def __read_predicates(self, array, glosname, ix_name=0,
                          ix_type=1, zero_arity=False):
        """
        Method to read and interpret predicates.
        Loops over an array containing only predicates or functions,
        and filters them into subcategories.

        The possible entries are: Relation, Function, partial Function,
            boolean, and relation..

        :arg array: a glossary table
        :arg glosname: the name of the glossary, i.e. Function, Relation,
            Constant or Boolean
        :arg ix_name: the column index of the name column. By default this is
            always the first column.
        :arg ix_type: the column index of the type column. By default this is
            always the second column.
        :arg zero_arity: bool which should be True when the predicate is a
            0-arity predicate (constants and booleans).

        :returns None:
        """
        # It's possible that there's no glossary defined.
        if array is None:
            return

        for row in array[2:]:
            full_name = row[ix_name].strip()
            partial = False
            typ = None
            predicate = None

            # Check if it's a (partial) function/constant or a
            # relation/boolean.
            if re.match('(partial )?Function|Constant', glosname):
                predicate = False
                typ = row[ix_type]
                if typ:
                    typ = typ.strip()

                # Check if it's a partial function
                partial = bool(re.match('(?i)partial', full_name))
                full_name = full_name.replace('partial ', '')
                try:
                    typ = self.find_type(typ)
                except TypeError:
                    raise ValueError(f'DataType of Function "{full_name}" is'
                                     f' empty')
                except StopIteration:
                    raise ValueError(f'DataType "{typ}" of "{full_name}" is'
                                     f' not an existing Type')

            # The predicate is a relation.
            else:
                predicate = True

            # Create the predicate.
            p = Predicate.from_string(full_name, predicate, typ, self,
                                      partial, zero_arity)

            # Append the new predicate to the list.
            self.predicates.append(p)

    def lookup(self, string: str):
        """
        TODO
        REWORK ENTIRE METHOD.
        """
        return list(filter(lambda x: x,
                           map(lambda x: x.lookup(string), self.predicates)))

    def read_datatables(self, datatables, parser):
        """
        Reads and interprets the datatables.
        Also checks if the values in the datatables appear in the possible
        values column of the glossary.

        Firstly it checks which columns are input, and which are output.
        A column is an inputcolumn if it contains the table title in the first
        cell, and an output if it contains `None` in the first cell.

        Iterates over every outputcolumn, deciphers which predicate the
        outputcolumn represents, and sets its "struct_args" to a combination
        of the input arguments and the output column's arguments.
        The predicate uses this struct_args to format its struct string.

        :arg List<np.array>: datatables, containing all the datatables.
        :arg parser:
        :returns None:
        """
        # return
        if len(datatables) == 0:
            return
        for table in datatables:
            inputs = []
            outputs = []
            tablename = table[0][0]
            # First, we find the input and outputcolumns.
            for column in table.T[1:]:
                # If a column contains the table title, it's an inputcolumn.
                if column[0] is not None:
                    # We also want to find out the input variables.
                    inputs.append(column[1:])
                else:
                    outputs.append(column[1:])
            # Second, we check if the inputcolumns contain the right values.
            # This also adds those values to the "constructed from" if needed.
            for i, inputarr in enumerate(inputs):
                header = inputarr[0]
                # The header can be just the Type name, or "Type called ..".
                typename = header.split(" ")[0]

                # Look for the type name in the glossary.
                for typ in self.types:
                    if typename == typ.name:
                        typ.check_values(inputarr[1:], tablename)

            # Third, we check if the outputcolumns contain the right values.
            # This also adds those values to the "constructed from" if needed.
            for i, outputarr in enumerate(outputs):
                header = outputarr[0]
                # The header can be a function like "Department of Person".
                # Or it can be a relation. If it's a relation, we skip.
                typename = header.split(" ")[0]
                pred = parser.interpreter.interpret_value(header).pred
                if pred.is_relation():
                    continue
                typename = pred.super_type.name

                # Look for the type name in the glossary, and check its values.
                for typ in self.types:
                    if typename == typ.name:
                        typ.check_values(outputarr[1:], tablename)

            # Then we iterate over the outputcolumns.
            for i, output in enumerate(outputs):
                header = output[0]
                # Format the args.
                args = {}
                # Iterate over each row of the outputcolumn.
                # Skip the first cell because it's always None.
                for j, value in enumerate(output[1:]):
                    # Find the inputvalues for the same row, in order to create
                    # the `args` dictionary. This contains the output values
                    # for every predicate in a data table.
                    inputvals = []
                    for inputcol in inputs:
                        inputval = str(inputcol[j+1])
                        inputvals.append(inputval)
                    inputval = "|".join(inputvals)

                    args[inputval] = value

                header = parser.interpreter.interpret_value(header).pred.name

                # Look for the predicate name.
                success = False
                for pred in self.predicates:
                    if pred.full_name == header or pred.name == header:
                        pred.struct_args = args
                        success = True
                        break
                if not success:
                    raise ValueError(f"Predicate \"{header}\" in datatable but"
                                     f" not in glossary")

    def to_idp_voc(self, target_lang: str = 'idp'):
        """
        Function which turns every object in a glossary into their vocabulary
        definitions.

        :arg target_lang: the format for the output. Either `idp` or `idpz3`.
        :returns voc: string
        """
        voc = ''.join(map(lambda x: x.to_idp_voc(target_lang),
                          self.types+self.predicates))
        # Add error specific concepts.
        return voc

    def to_json_dicts(self):
        """
        Creates a dict entry for every predicate and function, which is later
        turned into json.

        :returns dict:
        """
        json_dicts = []
        for pred in self.predicates:
            json_dicts.append(pred.to_json_dict())
        return json_dicts

    def add_aux_var(self, aux):
        """
        Some variables need to use auxiliary variables, for instance those
        found in the outputcolumns of C# tables.
        This method allows the creation of those variables.
        No aux var are created when makin an IDP file for the autoconfig
        interfaces.

         :arg List<str> a list containing strings of the variables.
         """
        for var in aux:
            # Split of the predicate name.
            p_name = var.split('(')[0]
            p_name = p_name.replace('_', ' ')
            for p in self.predicates:
                if p_name == p.name:
                    new_name = f"_{p.name}"
                    new_p = Predicate(new_name, p.args, p.super_type,
                                      partial=p.partial)
                    self.predicates.append(new_p)


class Type:
    """
    TODO
    """
    def __init__(self, name: str, super_type, posvals="-"):
        """
        :arg str: the name of the type.
        :arg Type: the super type of the type.
        :arg str: posvals, the possible values of the type.
        """
        self.name = name
        if name != "Int" and name != "Float" and name != "Real" \
                and name != "String":
            self.display_name = self.name + "_t"
        else:
            self.display_name = self.name
        self.super_type = super_type
        self.possible_values = posvals

        self.struct_args = []
        self.knows_values = True
        self.source_datatable = ""

        # Check the input.
        if posvals is None:
            raise ValueError(f"Values column for type {self.name} is empty."
                             f" Did you forget a '-'?")

        # Toggle knows_values if the values are known.
        if posvals == "_" or posvals == "-" or posvals == "−":
            self.knows_values = False
            self.possible_values = ""

        if re.search("(?i)see_Data_Table|see_DataTable", posvals):
            self.knows_values = False
            self.possible_values = ""
            m = re.search(r"(?i)(?<=see_Data_Table_)(.*?)(?=\Z)"
                          r"|(?<=see_DataTable_)(.*?)(?=\Z)",
                          posvals)
            self.source_datatable = m[0]

    def __str__(self):
        """
        Magic method to turn the type into a string.

        :returns str: the typename.
        """
        return f"Type: {self.name}"

    def to_theory(self):
        """
        TODO
        """
        return self.display_name

    def match(self, value):
        if self.basetype == self:  # When comparing with string, int, float,...
            return re.match(f'^{self.name}$', value, re.IGNORECASE)
        else:
            return re.match(f'^{self.name}$', value)

    @property
    def basetype(self):
        """
        The basetype represents one of the ancestor types, such as int or str.

        :returns type: the basetype.
        """
        try:
            return self.super_type.basetype
        except AttributeError:
            return self

    def check_values(self, values, tablename):
        """
        Method to check if the values listed in a datatable match with the
        values listed in the possible values column(if a datatable was used).

        If the possible values column is left empty, then it assumes all the
        values are correct and it fills the possible values automatically.
        This is needed so that the type can input these values into constructed
        from.

        If the possible values column contains values, then every value used in
        a datatable needs to match a value in the possible values.

        :returns boolean: True if all the values match.
        :throws ValueError: if a value appears in the datatable but not in
            posvals.
        """

        # We only check the data if the tablename (see datatable ...) is
        # explicitly given or a wildcard (-) was used in the glossary.
        if self.source_datatable not in tablename:
            return

        if self.basetype.name == "String":
            # If no possible values were listed, read the datatable values and
            # add them to the possible values.
            if not self.knows_values:
                if self.possible_values is None:
                    self.possible_values = ""

                # Check for each value if it exists already, add it if not.
                for value in values:
                    subvalues = str(value).split(',')
                    for subvalue in subvalues:
                        subvalue = subvalue.strip()
                        subvalue = idp_name(subvalue)
                        regex = r"(?<!\w){}(?!\w)".format(idp_name(subvalue))
                        if not re.search(regex, self.possible_values):
                            if not self.possible_values == "":
                                self.possible_values += ","
                            self.possible_values += f" {subvalue}"
                return

            # If possible values were listed in the glossary, we check for
            # typos in the data table.
            for value in values:
                subvalues = str(value).split(',')
                for subvalue in subvalues:
                    subvalue = subvalue.strip()
                    subvalue = idp_name(subvalue)
                    regex = r"(?<!\w){}(?!\w)".format(subvalue)
                    if not re.search(regex, self.possible_values):
                        raise ValueError(f"Error: value {subvalue} in data"
                                         f"table but not in possible values.")

        elif self.basetype.name == "Int":
            # For integers we only check if they're in the right range.
            # We don't add them if the possible values is empty, because there
            # is no clear way of defining a range.
            if not self.knows_values:
                raise ValueError(f"The values column for integer type"
                                 f" {self.name} was left empty")

            # A range should be declared in the possible values. We need to
            # check if our value is within that range.
            leftbound, rightbound = None, None
            possible_values = None
            if ".." in self.possible_values:
                # E.g. "[0..30]"
                leftbound, rightbound = self.possible_values.split("..")
            elif '[' in self.possible_values and \
                    self.possible_values.count(",") == 1:
                # E.g. "[0, 30]"
                leftbound, rightbound = self.possible_values.split(",")
            else:
                # E.g. "0, 1, 2, 3, 4"
                possible_values = [int(x) for x in
                                   self.possible_values.split(",")]

            for value in values:
                subvalues = str(value).split(',')
                for subvalue in subvalues:
                    subvalue = int(subvalue.strip())
                    # If we know boundaries, the value should be within them.
                    if rightbound and (int(rightbound) < subvalue or
                                       subvalue < int(leftbound)):
                        raise ValueError(f"Error: value \"{subvalue}\" for"
                                         f" type {self.name} in"
                                         f" datatable but not in"
                                         f" range of possible values")
                    # If we know a list of values, the value should be in it.
                    if possible_values and subvalue not in possible_values:
                        raise ValueError(f"Error: value \"{subvalue}\" for"
                                         f" type {self.name} in"
                                         f" datatable but not in"
                                         f" list of possible values")

    def to_idp_voc(self, target_lang: str = 'idp'):
        """
        Converts all the information of the Type into a string for the IDP
        vocabulary.

        :arg target_lang: the format for the output. Either `idp` or `idpz3`.
        :returns str: the vocabulary form of the type.
        """
        # Check for 'string', 'int', and other default types which don't need
        # to explicitly be declared.
        if self.name == self.basetype.name:
            return ''

        typename = idp_name(self.display_name)
        # If it's a string, use :=.
        if self.basetype.name == 'String':
            constr_from = 'constructed from' if target_lang == 'idp' else ':='
        # Else, we use "=" and semicolons instead of commas.
        else:
            constr_from = '=' if target_lang == 'idp' else ':='
            if target_lang == 'idp':
                self.possible_values = self.possible_values.replace(',', ';')
        if self.possible_values is None:
            return f'type {typename}\n'

        if self.basetype.name == 'String' or target_lang != 'idp':
            isa = ''
        else:
            isa = f'isa {self.basetype.name.lower()}'

        if self.basetype.name == 'Int' and target_lang == 'idp':
            vals = self.possible_values.replace(',', ';')
        else:
            vals = self.possible_values

        voc = (f'\ttype {typename} {constr_from} {{ {vals} }} {isa}\n')

        return voc

    def to_idp_struct(self, target_lang: str = 'idp'):
        """
        Converts all the information of the Type into a string for the IDP
        structure.
        Normal types don't need a structure, as their possible values are
        listed as "constructed from" in the voc.
        This is here for future's sake.

        :returns str: the string for the structure.
        """
        return ""


class Predicate:
    """
    Class which represents both predicates and functions.
    This double meaning is a relic of the past, and is to be fixed.
    In the future, a separate Function class should be created.
    """
    def __init__(self, name: str, args: List[Type], super_type: Type,
                 partial=False, full_name=None, zero_arity=False):
        """
        Initialises a predicate.
        :arg zero_arity: bool which should be True when the predicate is a
            0-arity predicate (constants and booleans).
        """
        self.name = name
        self.args = args
        self.super_type = super_type
        self.partial = partial
        self.repr = self.interpret_name()
        self.full_name = full_name
        self.struct_args = {}
        self.zero_arity = zero_arity

        if not self.args and self.is_function and not zero_arity:
            print(f'WARNING: "{self.name}" has been interpreted as single'
                  f' value instead of a function. Functions should be defined'
                  f' as FunctionName of Type and Type ...')
        elif not self.args and self.is_relation and not zero_arity:
            print(f'WARNING: "{self.name}" has been interpreted as a boolean'
                  f' value instead of a relation. Relations should be defined'
                  f' as Type and Type ... is RelationName')

    def __str__(self):
        """
        TODO
        """
        retstr = f"Predicate: {self.name}"
        return retstr

    @staticmethod
    def from_string(full_name: str, predicate: bool, super_type: Type,
                    glossary: Glossary, partial=False,
                    zero_arity=False):
        """
        Static method to create a predicate from string.

        :arg str: full_name, the full name.
        :arg bool: predicate, true if predicate, false if function.
        :arg Type: super_type, the super type of the predicate.
        :arg Glossary: glossary, the glossary.
        :arg bool: partial, whether or not it's a partial function.
        :arg zero_arity: bool which should be True when the predicate is a
            0-arity predicate (constants and booleans).
        :returns Predicate:
        """
        if not predicate:  # Check if it's a function.
            regex = (r'^(?P<name>.*)$')
            # regex = (r"^(?P<name>.*) of (?P<args>(?:{0})(?: and (?:{0}))*)$"
            #          .format('|'.join([x.name for x in glossary.types])))
        else:
            regex = (r'^(?P<name>.*)$')
        #    regex = ('^(?P<args>(?:{0})(?: and (?:{0}))*) is (?P<name>.*)$'
        #             .format('|'.join([x.name for x in glossary.types])))
        try:
            name = re.match(regex, full_name).group('name')
        except AttributeError:
            name = full_name
        try:
            # args = re.match(regex, full_name).group('args').split(' and ')
            raise IndexError
        except (AttributeError, IndexError):
            if zero_arity:
                return Predicate(full_name, [], super_type, partial,
                                 zero_arity=zero_arity)
            else:  # We need to find the relation's types.
                # We simply loop over all words and look for full matches.
                # TODO This should be done better. Types could be multiple
                # words.
                args = []
                name_elements = full_name.split(" ")

                for element in name_elements:
                    for t in glossary.types:
                        if re.fullmatch(element, t.name):
                            args.append(t)
                            break
                return Predicate(name, args,
                                 super_type, partial,
                                 full_name, zero_arity)

        return Predicate(name, [glossary.find_type(t) for t in args],
                         super_type, partial, full_name, zero_arity)

    def is_function(self):
        """
        Method to check whether the predicate is a function.
        Since only functions have super types, we use that as a check.
        Note that constants are a special case of functions.

        :returns boolean:
        """
        if self.super_type is None:
            return False
        else:
            return True

    def is_relation(self):
        """
        Method to check whether the predicate is a relation.
        A predicate is either a relation or a function, so we use that as a
        check. Note that booleans are a special case of relations.

        :returns boolean:
        """
        return not self.is_function()

    def interpret_name(self):
        """
        Method to interpret the name.
        This method forms a generic name representation, by replacing the
        arguments by dummies.
        In this way, it creates a skeleton structure for the name.

        Thus, it returns the name, without the arguments.
        For instance, `Country borders Country` becomes
        `(?P<arg0>.+) borders (?P<arg1>.+)`.
        This way, arg0 and arg1 can be found easily later on.
        """
        if not self.args:
            return self.name
        elif self.args:
            name_elements = self.name.split(" ")
            new_alias = ""
            arg_index = 0
            arglist = [arg.name for arg in self.args]
            for element in name_elements:
                if element in arglist:
                    new_alias += f"(?P<arg{arg_index}>.+) "
                    arg_index += 1
                    continue
                else:
                    new_alias += f"{element} "
            return new_alias[:-1]  # We drop the last space.
        else:
            raise ValueError("No idea what went wrong.")

    def lookup(self, string: str):
        """
        Method to compare a string to this predicate, to see if the predicate
        appears in the string in any form.
        TODO: make this more clear.
        """
        d = re.match(self.repr, string)
        if d:
            d = d.groupdict()
            return self, [v for k, v in sorted(d.items(),
                                               key=(lambda x: int(x[0][3:])))]

    def to_idp_voc(self, target_lang: str):
        """
        Convert the predicate/function to a string for the IDP vocabulary.

        :arg target_lang: the format for the output. Either `idp` or `idpz3`.
        :returns str: the predicate/function in vocabulary format.
        """
        if target_lang == 'idp':
            voc = '\tpartial ' if self.partial else '\t'
            voc += f'{idp_name(self.name)}'
            if self.args:
                voc += '({})'.format(', '.join(map(lambda t:
                                                   idp_name(t.display_name),
                                                   self.args)))
            if self.is_function():
                voc += f': {idp_name(self.super_type.display_name)}'
        elif target_lang == 'idpz3':
            voc = f'\t{idp_name(self.name)}: '
            if self.args:
                arg_str = ' ⨯ '.join(map(lambda t: idp_name(t.display_name),
                                     self.args))
                voc += f'{arg_str}'
            if self.is_function():
                voc += f' → {idp_name(self.super_type.display_name)}'
            else:
                voc += ' → Bool'
        return voc + "\n"

    def to_idp_struct(self, target_lang: str = 'idp'):
        """
        If a function or predicate receives a value in a datatable, we need to
        set it's values in the structure.
        When parsing the datatable in "read_datatables", we set the
        "struct_args" of the predicates/functions that get a value.
        struct_args could look like: {key1|key2:value}. However, it's possible
        to input multiple keys per cell to save space.

        For instance:
        "Jim|Skydiving, Soccer" needs to be formatted as
        "Jim, Skydiving; Jim, Soccer".
        The same goes for functions.

        To achieve this, we split the keys on their seperator, and then we
        split each key on a comma. This way, we have an array of keys in which
        each item is an array of subkeys. We need to form every possible
        combination of these keys, and to do this we use itertools.product.

        :arg target_lang: the target language format. Either `idp` or `idpz3`.
        :returns: str
        """
        import itertools
        if len(self.struct_args) == 0:
            return None
        assign = "=" if target_lang == "idp" else ":="
        struct = f'\t{idp_name(self.name)} {assign} {{'
        # If the pred is a function, the IDP format is "arg,.. -> arg;".
        # The IDP-Z3 format is "(arg, ...) -> arg,"
        if self.is_function():
            default_val = None
            for key, arg in self.struct_args.items():
                # Here be dragons.
                default_val = arg  # TODO: actual default arg!
                keys = key.split('|')
                keys = [x.split(',') for x in keys]
                keys_product = itertools.product(*keys)
                for combination in list(keys_product):
                    idp_combination = [idp_name(x.strip())
                                       for x in combination]
                    if target_lang == 'idp':
                        struct += (f"{','.join(idp_combination)} ->"
                                   f" {idp_name(arg)}; ")
                    else:
                        struct += (f"({','.join(idp_combination)})"
                                   f" → {idp_name(arg)}, ")
            if target_lang == 'idpz3':
                # Remove the final ", ".
                struct = struct[:-2]
                struct += "}\n"  # } else {} \n".format(default_val)
            else:
                struct += "}\n"

        else:
            for key, arg in self.struct_args.items():
                # Check if the relation is a boolean (booleans have no keys).
                if key == "":
                    if re.match("(?i)yes", arg):
                        struct = f"\t{idp_name(self.name)} {assign} true\n"
                        return struct
                    if re.match("(?i)no", arg):
                        struct = f"\t{idp_name(self.name)} {assign} false\n"
                        return struct
                # Only add a relation if the value of the argument is yes.
                if not re.match("(?i)yes", arg):
                    continue
                # The key can consist of multiple values.
                keys = key.split('|')
                keys = [x.split(',') for x in keys]
                keys_product = itertools.product(*keys)
                for combination in list(keys_product):
                    idp_combination = [idp_name(x.strip())
                                       for x in combination]
                    if target_lang == "idp":
                        struct += ",".join(idp_combination) + ";"
                    else:
                        struct += f"({','.join(idp_combination)}), "
            if target_lang == 'idpz3' and struct[-2] == ',':
                # Remove the ', ' at the end.
                struct = struct[:-2]
            struct += '}\n'

        return struct

    def to_json_dict(self):
        json_dict = {}
        json_dict['idpname'] = idp_name(self.name)
        # json_dict['expandArgs'] = 1
        if self.is_function():
            json_dict['type'] = "function"
            if self.zero_arity:
                basetype = self.super_type.basetype.name
                if basetype == "Int" or basetype == "Float":
                    json_dict['showOptimize'] = "true"
        else:
            if self.zero_arity:
                json_dict['type'] = "proposition"
            else:
                json_dict['type'] = "predicate"
        return json_dict
