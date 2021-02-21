import argparse
import collections
import json
import random
import string
import sys
import types

import bftool


# Default argument capture for the main function
def _get_arguments() -> argparse.Namespace:
    """Default function to prepare the arguments for the `Runner` during it's execution in a terminal

    Returns:
        - bftool.Arguments with all  the configurations provided by the user
    """
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-mt", "--max-threads",
                                 help="Maximum number of threads per process", default=1, type=int)
    argument_parser.add_argument("-mp", "--max-processes",
                                 help="Maximum number of process to have active at the same time",
                                 default=1, type=int)
    argument_parser.add_argument("-w", "--wordlist", help="File wordlist to use"
                                                          " based on \"{'argument_1': FILE_PATH, ...}\"",
                                 default="{}")
    argument_parser.add_argument("-b", "--bruteforce",
                                 help="Generate a virtual wordlist based on \
                                 rules \"{'argument_1': {'elements': [element_1, ...], 'minlength': INT, 'maxlength': "
                                      "INT, 'string-join': BOOL}, ...}\"",
                                 default="{}")
    argument_parser.add_argument("-sf", "--success-function",
                                 help="Function to pass the success result to (default is custom 'print')",
                                 default="lambda output: print(f\"[+] {output}\\n\", end='')")
    argument_parser.add_argument("-cf", "--check-function",
                                 help="Function useful to check the output (default is 'lambda output: output')",
                                 default="lambda output: output")
    argument_parser.add_argument("-sp", "--script_path", help="Python script to import", default=None, type=str)
    argument_parser.add_argument("expression", help="expression that will result in a callable")
    return argument_parser.parse_args()


def random_name():
    return "".join(random.choice(string.ascii_lowercase) for _ in range(32))


def import_function(expression: str, path: str = None) -> collections.abc.Callable:
    func_name = random_name()
    if path is not None:
        module = bftool.import_module_from_path(path)
        exec(f"{func_name} = {expression}", module.__dict__, module.__dict__)
        return module.__getattribute__(func_name)
    definitions = types.ModuleType("definitions")
    exec(f"{func_name} = {expression}", definitions.__dict__, definitions.__dict__)
    return definitions.__getattribute__(func_name)


if __name__ == "__main__":
    sys.argv[0] = "bftool"
    parsed_arguments = _get_arguments()
    function_ = import_function(parsed_arguments.expression, parsed_arguments.script_path)
    success_function = import_function(parsed_arguments.success_function, parsed_arguments.script_path)
    check_function = import_function(parsed_arguments.check_function, parsed_arguments.script_path)
    function_arguments = bftool.Arguments(
        function_=function_,
        files=json.loads(parsed_arguments.wordlist),
        bruteforce_rules=json.loads(parsed_arguments.bruteforce),
    )
    bftool.Pool(
        function_,
        function_arguments=function_arguments,
        check_function=check_function,
        success_function=success_function,
        max_processes=parsed_arguments.max_processes,
        max_threads=parsed_arguments.max_threads
    ).run()
