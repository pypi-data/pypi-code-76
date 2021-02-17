from termcolor import colored
import re
from typing import Any
from ast import literal_eval

table = {"danger": "red", "info": "blue", "warning": "yellow"}


def translate(value: Any, table: dict):
    """ """
    for k, v in table.items():
        if k == value:
            return v
    return value


def eprint(text: str) -> str:
    """ """
    matches = re.findall("[^\s]+`\w+`", text)
    coloreds = []
    for match in matches:
        m = match.split("`")
        word = m[0]
        qualifier = m[1]
        color = translate(qualifier, table)
        coloreds.append(colored(word, color))
        text = re.sub(match, "||||", text)
    texts = text.split("||||")
    for t, c in zip(texts, coloreds):
        print(t, end="")
        print(c, end="")
    print()
