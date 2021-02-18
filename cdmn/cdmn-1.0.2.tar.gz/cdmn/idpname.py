"""
    Copyright 2020 Simon Vandevelde, Bram Aerts, Joost Vennekens
    This code is licensed under GNU GPLv3 license (see LICENSE) for more
    information.
    This file is part of the cDMN solver.
"""


def idp_name(string: str):
    """
    Formats a string to be compatible for the IDP system.
    This means that it changes some characters to others.

    :arg string: the string to change.
    :returns str: the IDP compatible string.
    """
    string = str(string)
    try:
        return str(int(string))
    except ValueError:
        pass
    try:
        return str(float(string))
    except ValueError:
        pass

    return f'{string}'\
           .replace(' ', '_')\
           .replace('“', '"')\
           .replace('”', '"')
