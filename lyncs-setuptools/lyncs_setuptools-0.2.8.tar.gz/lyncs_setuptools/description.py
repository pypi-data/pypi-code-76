"""
Utils for finding description on the package
"""

__all__ = [
    "find_readme",
    "find_description",
    "get_keywords",
]


import codecs
import os
from itertools import product
from .data_files import add_to_data_files


def find_readme():
    """Search for a README file"""
    base = ["README", "readme", "description"]
    ext = ["", ".txt", ".md", ".rst"]
    options = ["".join(parts) for parts in product(base, ext)]

    for filename in options:
        if os.path.isfile(filename):
            return filename
    return None


def find_description(readme=None):
    """
    Gets package description from the README
    """

    if readme:
        if not os.path.isfile(readme):
            raise IOError("Given readme does not exist")
    else:
        readme = find_readme()

    if not readme:
        return None, None, None

    if readme.endswith(".md"):
        dtype = "text/markdown"
    elif readme.endswith(".rst"):
        dtype = "text/x-rst"
    else:
        dtype = "text/plain"

    with codecs.open(readme, encoding="utf-8") as _fp:
        add_to_data_files(readme, directory=".")
        dlong = _fp.read()

    dshort = ""
    for line in dlong.split("\n"):
        if line.split():
            dshort = line
            break

    if "markdown" in dtype:
        while dshort.startswith("#"):
            dshort = dshort[1:]

    return dshort.strip(), dlong, dtype


def get_keywords(string):
    "Select keywords from a string"
    if string is None:
        return None

    keywords = []
    for word in string.split():
        if sum(1 for c in word if c.isupper()) > 1:
            keywords.append(word)
            continue
        if len(word) < 5:
            # skipping
            continue
        keywords.append(word)
    return set(keywords)
