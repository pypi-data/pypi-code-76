from enum import unique
from pathlib import Path
import numpy as np
import re
import itertools
from typing import Generator, List, Optional, Sequence, Set, Tuple, Dict, Iterator, Union
import xarray
import pandas as pd
from xarray.core.utils import V
from collections.abc import MutableMapping
from itertools import product, combinations
from glob import iglob
from collections import defaultdict
from datetime import datetime
from parse import parse, extract_format
from functools import cmp_to_key


def is_singular(value):
    """Whether a value is singular or has multiple options.
    """
    if isinstance(value, str):
        return True
    try:
        iter(value)
        return False
    except TypeError:
        return True

class Placeholders(MutableMapping):
    """Dictionary-like object containing the placeholder values.

    It understands about sub-trees (i.e., if "<sub_tree>/<placeholder>" does not exist it will return "<placeholder>" instead).
    """
    def __init__(self, *args, **kwargs):
        self.mapping = {}
        self.linkages = {}
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key: str):
        actual_key = self.find_key(key)
        if actual_key is None:
            raise KeyError(f"No parameter value available for {key}")
        if actual_key in self.linkages:
            return self.mapping[self.linkages[actual_key]][actual_key]
        return self.mapping[actual_key]

    def __delitem__(self, key):
        if isinstance(key, tuple):
            key = frozenset(key)
        del self.mapping[key]
        if isinstance(key, frozenset):
            for k in key:
                del self.linkages[k]

    def __setitem__(self, key, value):
        if isinstance(key, tuple):  # create linked placeholders
            if len(key) != len(value):
                raise ValueError(f"Attempting to set linked placeholders for {key}, but {value} has a different number of elements than {key}")
            if any([len(value[0]) != len(v) for v in value]):
                raise ValueError(f"Attempting to set linked placeholders for {key}, but not all elements in {value} have the same length")
            value = {k: v for k, v in zip(key, value)}
            key = frozenset(key)
        if isinstance(key, frozenset):
            for k in list(key):
                if k in self.linkages:
                    unmatched_keys = [unmatched for unmatched in self.linkages[k] if unmatched not in key]
                    if len(unmatched_keys) > 0:
                        raise ValueError(f"Attempting to set linked placeholders for {key}, but {k} is already linked to {unmatched_keys}")
            self.mapping[key] = value
            for k in list(key):
                self.linkages[k] = key
                if k in self.mapping:
                    del self.mapping[k]
        elif key in self.linkages:
            raise ValueError(f"Can not overwrite placeholder {key} as it is linked to: {self.linkages[key]}")
        else:
            self.mapping[key] = value

    def __iter__(self):
        for key in self.mapping:
            if self.mapping[key] is not None:
                yield key

    def __len__(self):
        return len(self.mapping)

    def __repr__(self):
        return f"Placeholders({self.mapping})"

    def find_key(self, key: str) -> Optional[str]:
        """Finds the actual key containing the value

        Will look for:

            - not None value for the key itself
            - not None value for any parent (i.e, for key "A/B", will look for "B" as well)
            - otherwise will return None

        Args:
            key (str): placeholder name

        Returns:
            Optional[str]: None if no value for the key is available, otherwise the key used to index the value
        """
        if isinstance(key, tuple):
            key = frozenset(key)
        if key in self.linkages:
            return key
        if self.mapping.get(key, None) is not None:
            return key
        elif '/' in key:
            *sub_trees, _, actual_key = key.split('/')
            new_key = '/'.join([*sub_trees, actual_key])
            return self.find_key(new_key)
        else:
            return None

    def split(self) -> Tuple["Placeholders", "Placeholders"]:
        """Splits all placeholders into those with a single value or those with multiple values

        Placeholders are considered to have multiple values if they are equivalent to 1D-arrays (lists, tuples, 1D ndarray, etc.). 
        Anything else is considered a single value (string, int, float, etc.)

        Args:
            placeholders (Dict): all mappings from placeholder names to values

        Returns:
            Tuple[Dict, Dict]: Returns tuples with two dictionaries (first those with single values, then those with the multiple values)
        """
        single_placeholders = Placeholders()
        multi_placeholders = Placeholders()
        for name, value in self.mapping.items():
            if isinstance(name, frozenset) or not is_singular(value):
                multi_placeholders[name] = value
            else:
                single_placeholders[name] = value
        return single_placeholders, multi_placeholders

    def iter_over(self, keys) -> Generator["Placeholders", None, None]:
        """Iterate over the placeholder placeholder names

        Args:
            keys (Sequence[str]): sequence of placeholder names to iterate over

        Returns:
            Generator[FileTree]: yields Placeholders object, where each of the listed keys only has a single possible value
        """
        actual_keys = [self.linkages.get(self.find_key(key), key) for key in keys]
        unfilled = {orig for orig, key in zip(keys, actual_keys) if key is None}
        if len(unfilled) > 0:
            raise KeyError(f"Can not iterate over undefined placeholders: {unfilled}")

        unique_keys = []
        iter_values = {}
        for key in actual_keys:
            if key not in unique_keys:
                if isinstance(key, frozenset):  # linked placeholder
                    unique_keys.append(key)
                    iter_values[key] = ({k: self[k][idx] for k in key} for idx in range(len(self[list(key)[0]])))
                elif not is_singular(self[key]):  # iterable placeholder
                    unique_keys.append(key)
                    iter_values[key] = self[key]

        for values in product(*[iter_values[k] for k in unique_keys]):
            new_vars = Placeholders(self)
            for key, value in zip(unique_keys, values):
                if isinstance(key, frozenset):
                    del new_vars[key]  # break the placeholders link
                    new_vars.update(value)
                else:
                    new_vars[key] = value
            yield new_vars

    def link(self, *keys):
        """
        Link the placeholders represented by `keys`.

        When iterating over linked placeholders the i-th tree will contain the i-th element from all linked placeholders,
        instead of the tree containing all possible combinations of placeholder values.

        This can be thought of using `zip` for linked variables and `itertools.product` for unlinked ones.
        """
        self[keys] = [self[key] for key in keys]

    def unlink(self, *keys):
        """
        Unlink the placeholders represented by `keys`.

        See :meth:`link` for how linking affects the iteration through placeholders with multiple values.

        Raises a ValueError if the placeholders are not actually linked.
        """
        if keys not in self:
            raise ValueError(f"{keys} were not linked, so cannot unlink them")
        new_vars = {k: self[k] for k in keys}
        del self[keys]
        self.update(new_vars)
        

class Template:
    def __init__(self, parent: "Template", unique_part: str):
        self.parent = parent
        self.unique_part = unique_part

    @property
    def as_path(self, ) -> Path:
        """The full path with no placeholders filled in
        """
        if self.parent is None:
            return Path(self.unique_part)
        return self.parent.as_path.joinpath(self.unique_part)

    def __str__(self, ):
        return f"Template({str(self.as_path)})"

    def children(self, templates: Sequence["Template"]) -> List["Template"]:
        """From a sequence of templates find the children

        Returns:
            List[Template]: list of children templates
        """
        return [t for t in templates if t.parent is self]

    def as_string(self, other_templates: Dict[str, "Template"], indentation=4) -> str:
        """Generates a string describing this and child templates as 

        Args:
            other_templates (Dict[str, Template]): templates including all the child templates and itself
            indentiation (int, optional): number of spaces to use as indentation. Defaults to 4

        Returns:
            str: multi-line string that can be processed by :meth:`file_tree.FileTree.read`
        """
        result = self._as_string_helper(other_templates, indentation)

        is_top_level = other_templates[""] is self
        if not is_top_level and self.parent is None:
            return '!' + result
        else:
            return result

    def _as_string_helper(self, other_templates: Dict[str, "Template"], indentation=4, _current_indentation=0) -> str:
        leaves = []
        branches = []
        for t in sorted(self.children(other_templates.values()), key=lambda t: t.unique_part):
            if len(t.children(other_templates.values())) == 0:
                leaves.append(t)
            else:
                branches.append(t)

        is_top_level = other_templates[""] is self
        if is_top_level:
            base_line = '.'
            assert _current_indentation == 0 and self.parent is None
            _current_indentation = -indentation
        else:
            base_line = _current_indentation * ' ' + self.unique_part

        all_keys = []
        for key, value in other_templates.items():
            if value is not self:
                continue
            if is_top_level and key == "":
                continue
            all_keys.append(key)
        if is_top_level and len(all_keys) == 0:
            lines = []
        elif len(all_keys) == 1 and all_keys[0] == self.guess_key():
            lines = [base_line]
        else:
            assert len(all_keys) > 0
            lines = [base_line + f' ({",".join(all_keys)})']

        already_done = set()
        for t in leaves + branches:
            if t not in already_done:
                lines.append(t._as_string_helper(other_templates, indentation, indentation + _current_indentation))
                already_done.add(t)
        return '\n'.join(lines)

    @property
    def _parts(self, ):
        return TemplateParts.parse(str(self.as_path))

    def placeholders(self, ) -> List[str]:
        """Returns a list of the placeholder names

        Returns:
            List[str]: placeholder names in order that they appear in the template
        """
        return self._parts.ordered_placeholders()

    def format_single(self, placeholders: Placeholders, check=True) -> Path:
        """Formats the template with the placeholders filled in

        Only placeholders with a single value are considered.

        Args:
            placeholders (Placeholders): values to fill into the placeholder
            check (bool): skip check for missing placeholders if set to True

        Raises:
            KeyError: if any placeholder is missing

        Returns:
            Path: filled in template
        """
        single_placeholders, _ = placeholders.split()
        res = self._parts.resolve(single_placeholders)
        if res.ndim > 0:
            raise KeyError(f"Multiple placeholder values provided for {res.coords}")
        template: TemplateParts = res.data[()]
        if check:
            unfilled = template.required_placeholders()
            if len(unfilled) > 0:
                raise KeyError(f"Missing placeholder values for {unfilled}")
        return Path(str(template))

    def format_mult(self, placeholders: Placeholders, check=False) -> xarray.DataArray:
        """Replaces placeholder with the provided placeholders

        Args:
            placeholders (Placeholders): mapping from placeholder names to single or multiple vaalues
            check (bool): skip check for missing placeholders if set to True

        Raises:
            KeyError: if any placeholder is missing

        Returns:
            xarray.DataArray: array with possible resolved paths
        """
        resolved = self._parts.resolve(placeholders)
        if check:
            for template in resolved.data.flatten():
                unfilled = template.required_placeholders()
                if len(unfilled) > 0:
                    raise KeyError(f"Missing placeholder values for {unfilled}")
        paths = xarray.apply_ufunc(lambda t: Path(str(t)), resolved, vectorize=True)
        return paths

    def optional_placeholders(self, ) -> Set[str]:
        """Finds all placeholders that are only within optional blocks (i.e., they do not require a value)

        Returns:
            Set[str]: names of optional placeholders
        """
        return self._parts.optional_placeholders()

    def required_placeholders(self, ) -> Set[str]:
        """Finds all placeholders that are outside of optional blocks (i.e., they do require a value)

        Returns:
            Set[str]: names of required placeholders
        """
        return self._parts.required_placeholders()

    def guess_key(self, ) -> str:
        """Proposes a short name for the template

        The proposed short name is created by:

            - taking the basename (i.e., last component) of the path
            - removing the first '.' and everything beyond (to remove the extension)

        .. warning::

            If there are multiple dots within the path's basename, this might remove far more than just the extension.

        Returns:
            str: proposed short name for this template (used if user does not provide one)
        """
        parts = self.as_path.parts
        if len(parts) == 0:
            return ""
        else:
            return parts[-1].split('.')[0]

    def add_precursor(self, text) -> "Template":
        """Returns a new Template with any placeholder names in the unique part now preceded by `text`

        Used for adding sub-trees
        """
        parts = TemplateParts.parse(self.unique_part).parts
        updated = ''.join([str(p.add_precursor(text)) for p in parts])
        return Template(self.parent, updated)

    def get_all_placeholders(self, placeholders: Placeholders) -> Placeholders:
        """Fill placeholders with possible values based on what is available on disk

        Args:
            placeholders (Placeholders): New values for undefined placeholders in template
        """
        single_vars, multi_vars = placeholders.split()
        filled_template: TemplateParts = self._parts.fill_known(single_vars).data[()]
        optionals = self.optional_placeholders()
        undefined = defaultdict(set)
        get_type = defaultdict(str)
        for to_glob, templates in filled_template.all_optionals().items():
            for fn in iglob(to_glob):
                for t in templates:
                    try:
                        vars = t.parse_filename(fn)
                    except ValueError:
                        continue
                    for var_name in optionals:
                        if var_name not in vars:
                            vars[var_name] = None
                    if not all(name not in multi_vars or value in multi_vars[name] for name, value in vars.items()):
                        continue
                    for name, value in vars.items():
                        if name not in placeholders:
                            undefined[name].add(value)
                            if value is not None:
                                get_type[name] = type(value)

        def cmp(item1, item2):
            if item1 is None:
                return -1
            if item2 is None:
                return 1
            if item1 < item2:
                return -1
            if item1 > item2:
                return 1
            return 0

        return Placeholders({k: sorted(v, key=cmp_to_key(cmp)) for k, v in undefined.items()})


def extract_placeholders(template, filename, known_vars=None):
    """
    Extracts the placeholder values from the filename

    :param template: template matching the given filename
    :param filename: filename
    :param known_vars: already known placeholders
    :return: dictionary from placeholder names to string representations (unused placeholders set to None)
    """
    return TemplateParts.parse(template).extract_placeholders(filename, known_vars)



class Part:
    """
    Individual part of a template

    3 subclasses are defined:

    - :class:`Literal`: piece of text
    - :class:`Required`: required placeholder to fill in (between curly brackets)
    - :class:`OptionalPart`: part of text containing optional placeholders (between square brackets)
    """
    def fill_single_placeholders(self, placeholders: Placeholders, ignore_type=False) -> Sequence["Part"]:
        """
        Fills in the given placeholders
        """
        return [self]

    def optional_placeholders(self, ) -> Set["Part"]:
        """
        Returns all placeholders in optional parts
        """
        return set()

    def required_placeholders(self, ) -> Set["Part"]:
        """
        Returns all required placeholders
        """
        return set()

    def contains_optionals(self, placeholders: Set["Part"]=None):
        """
        Returns True if this part contains the optional placeholders
        """
        return False

    def append_placeholders(self, placeholders: List[str]):
        """
        Appends the placeholders in this part to the provided list in order
        """
        pass

    def add_precursor(self, text: str) -> "Part":
        """Prepends any placeholder names by `text`.
        """
        return self

    def for_defined(self, placeholder_names: Set[str]) -> "Part":
        """Returns the template string assuming the placeholders in `placeholder_names` are defined

        Removes any optional parts, whose placeholders are not in `placeholder_names`.
        """
        return [self]

    def remove_precursors(self, ):
        return self

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

        Required placeholder part of template is defined by placeholder name and its format

        :param var_name: name of placeholder
        :param var_formatting: how to format the placeholder
        """
        self.var_name = var_name
        self.var_formatting = var_formatting

    def __str__(self):
        """
        Returns this part of the template as a string
        """
        if self.var_formatting is None or len(self.var_formatting) == 0:
            return '{' + self.var_name + '}'
        else:
            return '{' + self.var_name + ':' + self.var_formatting + '}'

    def fill_single_placeholders(self, placeholders: Placeholders, ignore_type=False):
        value = placeholders.get(self.var_name, None)
        if value is None:
            return [self]
        else:
            if not ignore_type and len(self.var_formatting) > 0:
                format_type = extract_format(self.var_formatting, [])["type"]
                if format_type in list(r"dnbox"):
                    value = int(value)
                elif format_type in list(r"f%eg"):
                    value = float(value)
                elif format_type in ['t' + ft for ft in 'iegachs']:
                    value = datetime(value)
            as_string = ('{' + self.var_name + '}') if ignore_type else str(self)
            return TemplateParts.parse(as_string.format(**{self.var_name: value})).parts

    def required_placeholders(self, ):
        return {self.var_name}

    def append_placeholders(self, placeholders):
        placeholders.append(self.var_name)

    def add_precursor(self, text: str) -> "Required":
        """Prepends any placeholder names by `text`.
        """
        return Required(text + self.var_name, self.var_formatting)

    def remove_precursors(self, ):
        return Required(self.var_name.split('/')[-1], self.var_formatting)

class OptionalPart(Part):
    def __init__(self, sub_template: "TemplateParts"):
        """
        Optional part of template (between square brackets)

        Optional part can contain literal and required parts

        :param sub_template: part of the template within square brackets
        """
        self.sub_template = sub_template

    def __str__(self):
        return '[' + str(self.sub_template) + ']'

    def fill_single_placeholders(self, placeholders: Placeholders, ignore_type=False):
        new_opt = self.sub_template.fill_single_placeholders(placeholders, ignore_type=ignore_type)
        if len(new_opt.required_placeholders()) == 0:
            return TemplateParts.parse(str(new_opt)).parts
        return [OptionalPart(new_opt)]

    def optional_placeholders(self, ):
        return self.sub_template.required_placeholders()

    def contains_optionals(self, placeholders=None):
        if placeholders is None and len(self.optional_placeholders()) > 0:
            return True
        return len(self.optional_placeholders().intersection(placeholders)) > 0

    def append_placeholders(self, placeholders):
        placeholders.extend(self.sub_template.ordered_placeholders())

    def add_precursor(self, text: str) -> "OptionalPart":
        return OptionalPart(TemplateParts([p.add_precursor(text) for p in self.sub_template.parts]))

    def for_defined(self, placeholder_names: Set[str]) -> "Part":
        """Returns the template string assuming the placeholders in `placeholder_names` are defined

        Removes any optional parts, whose placeholders are not in `placeholder_names`.
        """
        if len(self.optional_placeholders().difference(placeholder_names)) > 0:
            return []
        return self.sub_template.parts

    def remove_precursors(self):
        return OptionalPart(self.sub_template.remove_precursors())


class TemplateParts:
    """
    The parts of a larger template
    """
    def __init__(self, parts: Sequence[Part]):
        if isinstance(parts, str):
            raise ValueError("Input to Template should be a sequence of parts; " +
                             "did you mean to call `TemplateParts.parse` instead?")
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
                parts.append(OptionalPart(TemplateParts.parse(optional_parts[1:-1])))
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
        return str(Path(''.join([str(p) for p in self.parts])))

    def optional_placeholders(self, ) -> Set[str]:
        """Set of optional placeholders
        """
        if len(self.parts) == 0:
            return set()
        optionals = set.union(*[p.optional_placeholders() for p in self.parts])
        return optionals.difference(self.required_placeholders())

    def required_placeholders(self, ) -> Set[str]:
        """Set of required placeholders
        """
        if len(self.parts) == 0:
            return set()
        return set.union(*[p.required_placeholders() for p in self.parts])

    def ordered_placeholders(self, ) -> Tuple[str]:
        """Sequence of all placeholders in order (can contain duplicates)
        """
        ordered_vars = []
        for p in self.parts:
            p.append_placeholders(ordered_vars)
        return ordered_vars

    def fill_known(self, placeholders: Placeholders, ignore_type=False) -> xarray.DataArray:
        """Fill in the known placeholders

        Any optional parts, where all placeholders have been filled will be automatically replaced
        """
        single, multi = placeholders.split()
        new_template = self.fill_single_placeholders(single, ignore_type=ignore_type)
        for name in new_template.ordered_placeholders():
            if name in multi:
                values = list(multi[name])
                use_name = multi.find_key(name)
                assert use_name is not None
                templates = [new_template.fill_known(Placeholders({**placeholders, **{name: value}}), ignore_type=ignore_type) for value in values]
                return xarray.concat(templates, pd.Index(values, name=use_name))
        return xarray.DataArray(new_template)

    def fill_single_placeholders(self, placeholders: Placeholders, ignore_type=False):
        """
        Helper method for :meth:`fill_known`
        """
        current = self
        prev = ''
        while str(current) != prev:
            prev = str(current)
            res = []
            for p in current.parts:
                res.extend(p.fill_single_placeholders(placeholders, ignore_type=ignore_type))
            current = TemplateParts(res)
        return current

    def remove_optionals(self, optionals=None) -> "TemplateParts":
        """
        Removes any optionals containing the provided placeholders (default: remove all)
        """
        return TemplateParts([p for p in self.parts if not p.contains_optionals(optionals)])

    def all_optionals(self, ) -> Dict[str, List["TemplateParts"]]:
        """Yields all possible templates depending on which optional placeholders are defined

        None of the resulting templates will have optional placeholders (i.e., square brackets)
        """
        required = self.required_placeholders()
        optional = self.optional_placeholders()
        to_glob = defaultdict(list)
        for defined_optionals in [c for n in range(len(optional) + 1) for c in combinations(optional, n)]:
            new_glob = str(self.resolve(Placeholders({req: '*' for req in required}, **{opt: '*' for opt in defined_optionals}), ignore_type=True).data[()])
            while '**' in new_glob:
                new_glob = new_glob.replace('**', '*')
            res = []
            vars = required.union(defined_optionals)
            for p in self.parts:
                res.extend(p.for_defined(vars))
            to_glob[new_glob].append(TemplateParts(res))
        return to_glob

    def resolve(self, placeholders, ignore_type=False) -> str:
        """
        Resolves the template given a set of placeholders

        :param placeholders: mapping of placeholder names to values
        :param ignore_type: if True, ignore the type formatting when filling in placeholders
        :return: cleaned string
        """
        return xarray.apply_ufunc(lambda t: t.remove_optionals(), self.fill_known(placeholders, ignore_type=ignore_type), vectorize=True)

    def optional_subsets(self, ) -> Iterator["TemplateParts"]:
        """
        Yields template sub-sets with every combination optional placeholders
        """
        optionals = self.optional_placeholders()
        for n_optional in range(len(optionals) + 1):
            for exclude_optional in itertools.combinations(optionals, n_optional):
                yield self.remove_optionals(exclude_optional)

    def extract_placeholders(self, filename, known_vars=None):
        """
        Extracts the placeholder values from the filename

        :param filename: filename
        :param known_vars: already known placeholders
        :return: dictionary from placeholder names to string representations (unused placeholders set to None)
        """
        if known_vars is not None:
            template = self.fill_known(known_vars)
        else:
            template = self
        while '//' in filename:
            filename = filename.replace('//', '/')

        required = template.required_placeholders()
        optional = template.optional_placeholders()
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
            ordered_vars = to_fill.ordered_placeholders()
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
            for name in template.optional_placeholders():
                if name not in extracted_value:
                    extracted_value[name] = None
            if known_vars is not None:
                extracted_value.update(known_vars)
            results.append(extracted_value)
        if len(results) == 0:
            raise ValueError("{} did not match {}".format(filename, template))

        def score(placeholders):
            """
            The highest score is given to the set of placeholders that:

            1. has used the largest amount of optional placeholders
            2. has the shortest text within the placeholders (only used if equal at 1
            """
            number_used = len([v for v in placeholders.values() if v is not None])
            length_hint = sum([len(v) for v in placeholders.values() if v is not None])
            return number_used * 1000 - length_hint

        best = max(results, key=score)
        for var in results:
            if best != var and score(best) == score(var):
                raise KeyError("Multiple equivalent ways found to parse {} using {}".format(filename, template))
        return best

    def parse_filename(self, filename):
        if any(isinstance(p, OptionalPart) for p in self.parts):
            raise ValueError("Can not parse filename when there are optional parts in the template")
        result = parse(str(self.remove_precursors()), filename, case_sensitive=True)
        if result is None:
            raise ValueError(f"template string ({str(self)}) does not mach filename ({filename})")
        named = result.named
        if any(isinstance(value, str) and '/' in value for value in named.values()):
            raise ValueError("Placeholder can not span directories")
        return named

    def remove_precursors(self, ):
        return TemplateParts([p.remove_precursors() for p in self.parts])
