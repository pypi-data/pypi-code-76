"""
    Copyright 2019 Simon Vandevelde, Bram Aerts, Joost Vennekens
    This code is licensed under GNU GPLv3 license (see LICENSE) for more
    information.
    This file is part of the cDMN solver.
"""
from typing import List, Dict
import re


def merge_definitions(idp: str) -> str:
    """
    In cDMN, it is possible to create different tables that each define
    the same concept.
    In cases where relations are defined, this can be problematic.
    E.g., in the `Vacation_Days_Advanced_old` example, we define the `Employee
    eligible for Rule` relation in 5 different tables, each for a different
    value of `Rule`.
    In IDP, a definition is expected to be complete: all possible values for
    the defined concept should be defined. All other values are implicitly
    impossible. Because the cDMN implementation creates 5 different
    definitions, each defining a different value, this results in an unsat in
    IDP.

    The solution to this problem is to merge all tables defining the same
    concept.
    """
    rules = re.findall(r"\n(.+?)(?=<-)(.+?)(?=\.\n)", idp)
    new_idp = re.sub(r"\n(.+?)(?=<-)(.+?)(?=\.\n)", "", idp)
    # comments = re.findall(r"\t//(.*?)\n\t{(\.*?)\n(.*?)}", new_idp)
    # comments = [x[0] for x in comments]
    defined_concepts: Dict[str, str] = {}
    # Go over every rule and try to find the head.
    for head, body in rules:
        rule = head + body + ".\n"
        try:  # Find all rules with quantifiers.
            defined_concept = re.findall(r": (.*?)\(", rule)[0]
        except IndexError:  # Find all rules without quantifiers.
            defined_concept = re.findall(r"\t(.*?)\(", rule)[0]
        if defined_concept in defined_concepts:
            defined_concepts[defined_concept] += rule
        else:
            defined_concepts[defined_concept] = rule
    new_idp = re.sub(r"\t//(.*?)\n\t{(\.*?)\n(.*?)}", "", new_idp)
    for key, val in defined_concepts.items():
        new_idp += "\t{\n"
        new_idp += val
        new_idp += "\t}\n"
    return new_idp
