from pathlib import Path
import numpy as np
import re
import itertools
import glob
from typing import List, Sequence, Set, Tuple, Dict, Iterator
import xarray
import pandas as pd


class Template(object):
    def __init__(self, parent: "Template", unique_part: str):
        self.parent = parent
        self.unique_part = unique_part

    @property
    def as_path(self, ) -> Path:
        """The full path with no placeholders filled in
        """
        return self.parent.as_path().joinpath(self.unique_part)

    def __str__(self, ):
        return f"Template({str(self.as_path())})"

    @property
    def _parts(self, ):
        return TemplateParts.parse(str(self.as_path))

    def placeholders(self, ) -> List[str]:
        """Returns a list of the placeholder names

        Returns:
            List[str]: placeholder names in order that they appear in the template
        """
        return self._parts.ordered_variables()

    def format(self, variables: Dict[str, str]) -> xarray.DataArray:
        """Replaces placeholder with the provided variables

        Args:
            variables (Dict[str, str]): mapping from placeholder names to actual values

        Returns:
            xarray.DataArray: array with possible resolved paths
        """
        return self._parts.resolve(variables)

    def optional_placeholders(self, ) -> Set[str]:
        """Finds all placeholders that are only within optional blocks (i.e., they do not require a value)

        Returns:
            Set[str]: names of optional placeholders
        """
        return self._parts.optional_variables()

    def required_placeholders(self, ) -> Set[str]:
        """Finds all placeholders that are outside of optional blocks (i.e., they do require a value)

        Returns:
            Set[str]: names of required placeholders
        """
        return self._parts.required_variables()


def extract_variables(template, filename, known_vars=None):
    """
    Extracts the variable values from the filename

    :param template: template matching the given filename
    :param filename: filename
    :param known_vars: already known variables
    :return: dictionary from variable names to string representations (unused variables set to None)
    """
    return Template.parse(template).extract_variables(filename, known_vars)



class Part:
    """
    Individual part of a template

    3 subclasses are defined:

    - :class:`Literal`: piece of text
    - :class:`Required`: required variable to fill in (between curly brackets)
    - :class:`Optional`: part of text containing optional variables (between square brackets)
    """
    def fill_known(self, variables) -> Sequence["Part"]:
        """
        Fills in the given variables
        """
        return [self]

    def optional_variables(self, ) -> Set["Part"]:
        """
        Returns all variables in optional parts
        """
        return set()

    def required_variables(self, ) -> Set["Part"]:
        """
        Returns all required variables
        """
        return set()

    def contains_optionals(self, variables: Set["Part"]=None):
        """
        Returns True if this part contains the optional variables
        """
        return False

    def append_variables(self, variables: List[str]):
        """
        Appends the variables in this part to the provided list in order
        """
        pass


class Literal(Part):
    def __init__(self, text: str):
        """
        Literal part is defined purely by the text it contains

        :param text: part of the template
        """
        self.text = text

    def __str__(self):
        """
        Returns this part of the template as a string
        """
        return self.text


class Required(Part):
    def __init__(self, var_name, var_formatting=None):
        """
        Required part of template (between curly brackets)

        Required variable part of template is defined by variable name and its format

        :param var_name: name of variable
        :param var_formatting: how to format the variable
        """
        self.var_name = var_name
        self.var_formatting = var_formatting

    def __str__(self):
        """
        Returns this part of the template as a string
        """
        if self.var_formatting is None:
            return '{' + self.var_name + '}'
        else:
            return '{' + self.var_name + ':' + self.var_formatting + '}'

    def fill_known(self, variables):
        value = variables.get(self.var_name, None)
        if value is None:
            return [self]
        else:
            value = variables[self.var_name]
            return Template.parse(str(self).format(**variables)).parts

    def required_variables(self, ):
        return {self.var_name}

    def append_variables(self, variables):
        variables.append(self.var_name)


class Optional(Part):
    def __init__(self, sub_template: "Template"):
        """
        Optional part of template (between square brackets)

        Optional part can contain literal and required parts

        :param sub_template: part of the template within square brackets
        """
        self.sub_template = sub_template

    def __str__(self):
        return '[' + str(self.sub_template) + ']'

    def fill_known(self, variables):
        new_opt = self.sub_template.fill_known(variables)
        if len(new_opt.required_variables()) == 0:
            return Template.parse(str(new_opt)).parts
        return [Optional(new_opt)]

    def optional_variables(self, ):
        return self.sub_template.required_variables()

    def contains_optionals(self, variables=None):
        if variables is None and len(self.optional_variables()) > 0:
            return True
        return len(self.optional_variables().intersection(variables)) > 0

    def append_variables(self, variables):
        variables.extend(self.sub_template.ordered_variables())


class TemplateParts:
    """
    The parts of a larger template
    """
    def __init__(self, parts: Sequence[Part]):
        if isinstance(parts, str):
            raise ValueError("Input to Template should be a sequence of parts; " +
                             "did you mean to call `Template.parse` instead?")
        self.parts = tuple(parts)

    @classmethod
    def parse(cls, text: str) -> "TemplateParts":
        """Parses a template string into its constituent parts

        Raises:
            ValueError: raised if a parsing error is

        Returns:
            TemplateParts: object that contains the parts of the template
        """

        parts = []
        for optional_parts in re.split(r'(\[.*?\])', text):
            if len(optional_parts) > 0 and optional_parts[0] == '[' and optional_parts[-1] == ']':
                if '[' in optional_parts[1:-1] or ']' in optional_parts[1:-1]:
                    raise ValueError(f'Can not parse {text}, because unmatching square brackets were found')
                parts.append(Optional(Template.parse(optional_parts[1:-1])))
            else:
                for required_parts in re.split(r'(\{.*?\})', optional_parts):
                    if len(required_parts) > 0 and required_parts[0] == '{' and required_parts[-1] == '}':
                        if ':' in required_parts:
                            var_name, var_type = required_parts[1:-1].split(':')
                        else:
                            var_name, var_type = required_parts[1:-1], ''
                        parts.append(Required(var_name, var_type))
                    else:
                        parts.append(Literal(required_parts))
        return TemplateParts(parts)

    def __str__(self):
        """
        Returns the template as a string
        """
        return ''.join([str(p) for p in self.parts])

    def optional_variables(self, ) -> Set[str]:
        """Set of optional variables
        """
        if len(self.parts) == 0:
            return set()
        optionals = set.union(*[p.optional_variables() for p in self.parts])
        return optionals.difference(self.required_variables())

    def required_variables(self, ) -> Set[str]:
        """Set of required variables
        """
        if len(self.parts) == 0:
            return set()
        return set.union(*[p.required_variables() for p in self.parts])

    def ordered_variables(self, ) -> Tuple[str]:
        """Sequence of all variables in order (can contain duplicates)
        """
        ordered_vars = []
        for p in self.parts:
            p.append_variables(ordered_vars)
        return ordered_vars

    def fill_known(self, variables) -> xarray.DataArray:
        """Fill in the known variables

        Any optional parts, where all variables have been filled will be automatically replaced
        """
        single, multi = split_variables(variables)
        new_template = self._fill_single_variables(single)
        for name in new_template.ordered_variables:
            if name in multi:
                values = np.asanyarray(multi[name])
                templates = [new_template.fill_known({**variables, **{name: value}}) for value in values]
                return xarray.concat(templates, pd.Index(values, name=name))
        return xarray.DataArray(new_template)

    def _fill_single_variables(self, variables):
        """
        Helper method for :meth:`_fill_known`
        """
        res = []
        for p in self.parts:
            res.extend(p.fill_known(variables))
        return TemplateParts(res)


    def remove_optionals(self, optionals=None) -> "TemplateParts":
        """
        Removes any optionals containing the provided variables (default: remove all)
        """
        return TemplateParts([p for p in self.parts if not p.contains_optionals(optionals)])

    def resolve(self, variables) -> str:
        """
        Resolves the template given a set of variables

        :param variables: mapping of variable names to values
        :return: cleaned string
        """
        clean_template = self.fill_known(variables).remove_optionals()
        if len(clean_template.required_variables()) > 0:
            raise KeyError("Variables %s not defined" % clean_template.required_variables())
        return str(clean_template)

    def get_all(self, variables, glob_vars=()) -> Tuple[Dict[str, str]]:
        """
        Gets all variables for files on disk matching the templates

        :param variables: (incomplete) mapping of variable names to values
        :param glob_vars: sequence of undefined variables that can take any possible values when looking for matches on the disk
        """
        filled = self.fill_known(variables)
        if glob_vars == 'all':
            glob_vars = set.union(self.required_variables(), self.optional_variables())
        if len(filled.required_variables().difference(glob_vars)) > 0:
            raise KeyError("Required variables {} were not defined".format(
                filled.required_variables().difference(glob_vars)
            ))
        cleaned = filled.remove_optionals(filled.optional_variables().difference(glob_vars))
        return cleaned._get_all_helper(glob_vars)

    def _get_all_helper(self, glob_vars):
        params = set()
        optionals = self.optional_variables()
        for to_fill in self.optional_subsets():
            pattern = str(to_fill.fill_known({var: '*' for var in glob_vars}))
            while '//' in pattern:
                pattern = pattern.replace('//', '/')

            for filename in sorted(glob.glob(pattern)):
                try:
                    extracted_vars = to_fill.extract_variables(filename)
                    for name in optionals:
                        if name not in extracted_vars:
                            extracted_vars[name] = None
                    params.add(tuple(sorted(extracted_vars.items(), key=lambda item: item[0])))
                except ValueError:
                    pass
        return tuple([dict(p) for p in params])

    def optional_subsets(self, ) -> Iterator["TemplateParts"]:
        """
        Yields template sub-sets with every combination optional variables
        """
        optionals = self.optional_variables()
        for n_optional in range(len(optionals) + 1):
            for exclude_optional in itertools.combinations(optionals, n_optional):
                yield self.remove_optionals(exclude_optional)

    def extract_variables(self, filename, known_vars=None):
        """
        Extracts the variable values from the filename

        :param filename: filename
        :param known_vars: already known variables
        :return: dictionary from variable names to string representations (unused variables set to None)
        """
        if known_vars is not None:
            template = self.fill_known(known_vars)
        else:
            template = self
        while '//' in filename:
            filename = filename.replace('//', '/')

        required = template.required_variables()
        optional = template.optional_variables()
        results = []
        for to_fill in template.optional_subsets():
            sub_re = str(to_fill.fill_known(
                {var: r'(\S+)' for var in required.union(optional)},
            ))
            while '//' in sub_re:
                sub_re = sub_re.replace('//', '/')
            sub_re = sub_re.replace('.', r'\.')
            match = re.match(sub_re, filename)
            if match is None:
                continue

            extracted_value = {}
            ordered_vars = to_fill.ordered_variables()
            assert len(ordered_vars) == len(match.groups())

            failed = False
            for var, value in zip(ordered_vars, match.groups()):
                if var in extracted_value:
                    if value != extracted_value[var]:
                        failed = True
                        break
                else:
                    extracted_value[var] = value
            if failed or any('/' in value for value in extracted_value.values()):
                continue
            for name in template.optional_variables():
                if name not in extracted_value:
                    extracted_value[name] = None
            if known_vars is not None:
                extracted_value.update(known_vars)
            results.append(extracted_value)
        if len(results) == 0:
            raise ValueError("{} did not match {}".format(filename, template))

        def score(variables):
            """
            The highest score is given to the set of variables that:

            1. has used the largest amount of optional variables
            2. has the shortest text within the variables (only used if equal at 1
            """
            number_used = len([v for v in variables.values() if v is not None])
            length_hint = sum([len(v) for v in variables.values() if v is not None])
            return number_used * 1000 - length_hint

        best = max(results, key=score)
        for var in results:
            if best != var and score(best) == score(var):
                raise KeyError("Multiple equivalent ways found to parse {} using {}".format(filename, template))
        return best


def split_variables(variables: Dict) -> Tuple[Dict, Dict]:
    """Splits all variables into those with a single value or those with multiple values

    Variables are considered to have multiple values if they are equivalent to 1D-arrays (lists, tuples, 1D ndarray, etc.). 
    Anything else is considered a single value (string, int, float, etc.)

    Args:
        variables (Dict): all mappings from placeholder names to values

    Returns:
        Tuple[Dict, Dict]: Returns tuples with two dictionaries (first those with single values, then those with the multiple values)
    """
    single_variables = {}
    multi_variables = {}
    for name, value in variables.items():
        if np.asanyarray(value).ndim == 1:
            multi_variables[name] = value
        else:
            single_variables[name] = value
    return single_variables, multi_variables