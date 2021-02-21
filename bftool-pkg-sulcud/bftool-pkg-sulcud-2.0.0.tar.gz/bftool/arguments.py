import collections
import inspect

from .bftool_types import SpecialGenerator, ExpandableTuple
from .bruteforce import bruteforce_wordlist
from .file_reading import read_file_lines

__all__ = ["Arguments", "merge_iterables"]


def _expand_product_result(product_: tuple) -> list:
    result = []
    for value in product_:
        if isinstance(value, ExpandableTuple):
            result += _expand_product_result(value)
        elif isinstance(value, tuple):
            if len(value) == 1:  # If the tuple is just one argument
                result.append(value[0])
            else:
                result.append(value)
        else:
            result.append(value)
    return result


def _merged_generator(a: collections.abc.Iterable, b: collections.abc.Iterable):
    yield from a
    yield from b


def merge_iterables(a: collections.abc.Iterable, b: collections.abc.Iterable) -> SpecialGenerator:
    return SpecialGenerator(_merged_generator, a, b)


def _combine_wordlists(iterables_: list, master=True):
    number_of_iterables = len(iterables_)
    if isinstance(iterables_[0], SpecialGenerator):
        cycle_iterable = iterables_[0]()
    else:
        cycle_iterable = iterables_[0]
    if number_of_iterables == 1:
        for value in cycle_iterable:
            yield value,
    elif number_of_iterables > 1:
        for value in cycle_iterable:
            for second_value in _combine_wordlists(iterables_[1:], False):
                second_value = ExpandableTuple(second_value)
                if master:
                    # When is the master function (the one that the user called), normalize it's values
                    yield _expand_product_result((value, second_value))
                else:
                    yield value, second_value
    else:
        raise IndexError("Invalid number of arguments")


# This class prepare all the arguments that the Runner is going to use
class Arguments(object):
    """Class that handles all the configuration of the the arguments that are going to be passed
    to `bftool.Runner`"""

    def __init__(self,
                 function_: collections.abc.Callable,
                 iterables: dict = None,
                 bruteforce_rules: dict = None,
                 files: dict = None
                 ):
        self.__function_args_spec = inspect.getfullargspec(function_)
        # - Wordlist Setup
        # This is the argument that will replace replace Wordlist.wordlist
        self.__wordlists = [None] * len(self.__function_args_spec.args)

        self._arguments_from_iterables(iterables)
        self._arguments_from_bruteforce_rules(bruteforce_rules)
        self._arguments_from_files(files)

        self.__arguments = SpecialGenerator(_combine_wordlists, self.__wordlists)
        if not self.is_valid():
            raise IndexError("Wrong number of arguments provided for the targeted function")

    def __iter__(self):
        yield from self.__arguments

    def _arguments_from_iterables(self, iterables_wordlists: dict):
        # If the user provide raw iterables like list, sets, tuples, dicts...
        # To handle generators please check bftool.Types.SpecialGenerator
        if iterables_wordlists:
            for key, value in iterables_wordlists.items():
                if isinstance(key, str):
                    key = self.__function_args_spec.args.index(key)
                if not isinstance(key, int):
                    raise TypeError("key must be the index of the argument or it's name")
                if self.__wordlists[key] is not None:
                    self.__wordlists[key] = merge_iterables(self.__wordlists[key], value)
                else:
                    self.__wordlists[key] = value

    def _arguments_from_bruteforce_rules(self, bruteforce_rules_wordlists: dict):
        # If the user provides wordlist generation rules
        if bruteforce_rules_wordlists:
            for key, value in bruteforce_rules_wordlists.items():
                if isinstance(key, str):
                    key = self.__function_args_spec.args.index(key)
                if not isinstance(key, int):
                    raise TypeError("key must be the index of the argument or it's name")
                if self.__wordlists[key] is not None:
                    self.__wordlists[key] = merge_iterables(self.__wordlists[key], bruteforce_wordlist(value))
                else:
                    self.__wordlists[key] = bruteforce_wordlist(value)

    def _arguments_from_files(self, files_wordlists: dict):
        # If the user provide a file as a wordlist (it always read each line as an argument)
        if files_wordlists:
            for key, value in files_wordlists.items():
                if isinstance(key, str):
                    key = self.__function_args_spec.args.index(key)
                if not isinstance(key, int):
                    raise TypeError("key must be the index of the argument or it's name")
                if self.__wordlists[key] is not None:
                    self.__wordlists[key] = merge_iterables(self.__wordlists[key], read_file_lines(value))
                else:
                    self.__wordlists[key] = read_file_lines(value)

    def is_valid(self):
        if not self.__wordlists:
            raise ValueError("No wordlist input provided")

        if any(value is None for value in self.__wordlists):
            raise IndexError(f"Invalid number of wordlists provided ({len(self.__wordlists)})"
                             f" for a function of {len(self.__function_args_spec.args)} arguments")
        return True
