#!/usr/bin/env python3

import argparse
import shlex

class ParserError(Exception):
    pass

class ArgumentParserFix(argparse.ArgumentParser):
    def _get_action_from_name(self, name):
        """Given a name, get the Action instance registered with this parser.
        If only it were made available in the ArgumentError object. It is
        passed as it's first arg...
        """
        container = self._actions
        if name is None:
            return None
        for action in container:
            if '/'.join(action.option_strings) == name:
                return action
            elif action.metavar == name:
                return action
            elif action.dest == name:
                return action

    def error(self, message):
        raise ParserError(message)



if __name__ == "__main__":
    for args in ['a', 'bno055 -p', 'esp -p lib', "a b", "-p a b", "pack -p x -p y"]:
        print("\nARGS", args)
        parser = ArgumentParserFix(description='Install package from PyPi.org')
        parser.add_argument('package')
        parser.add_argument('-p', '--project', default='root', help="sub-folder in ~/mcu")
        try:
            a = parser.parse_args(shlex.split(args))
            print(f"    {args}  -->  {a.package}  in  {a.project}")
        except ParserError as pe:
            print("    PE", pe)
