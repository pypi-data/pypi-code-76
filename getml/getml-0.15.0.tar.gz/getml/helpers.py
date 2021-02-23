# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Collection of helper classes that are relevant
for many submodules.
"""

# --------------------------------------------------------------------


def _check_parameter_bounds(parameter, parameter_name, bounds):
    """Checks whether a particular parameter does lie within the provided
    `bounds`.

    Args:
        parameter (numeric): Particular value of an instance variable.
        key_name (string): Name of the parameter used for an
            expressive Exception
        bounds (list[numeric]): Numerical list of length 2
            specifying the lower and upper bound (in that order)
            of `parameter`.

    Raises:
        ValueError: If `parameter` does not is not within `bounds`.

    """
    if parameter < bounds[0] or parameter > bounds[1]:
        raise ValueError(
            "'"
            + parameter_name
            + "' is only defined between ["
            + str(bounds[0])
            + ","
            + str(bounds[1])
            + "]"
        )


# --------------------------------------------------------------------


def _str(obj_dict):
    """
    Represents a predictor or feature_learner in scikit-learn-style.
    """
    # ------------------------------------

    assert "type" in obj_dict, "Expected type"

    # ------------------------------------

    repr_str = ""

    new_line = ""

    new_line += obj_dict["type"] + "("

    # ------------------------------------

    if len(obj_dict) == 1:
        return new_line + ")"

    # ------------------------------------

    skip = "\n" + " " * len(new_line)

    # ------------------------------------

    for key, value in obj_dict.items():

        if key == "type":
            continue

        if key[0] == "_":
            continue

        if isinstance(value, str):
            new_elem = key + "='" + value + "'"
        else:
            new_elem = key + "=" + str(value)

        new_elem += ", "

        if len(new_line) + len(new_elem) > 80:
            repr_str += new_line
            new_line = skip + new_elem
        else:
            new_line += new_elem

    # ------------------------------------

    repr_str += new_line

    repr_str = repr_str[:-2]

    repr_str += ")"

    # ------------------------------------

    return repr_str


# --------------------------------------------------------------------


def _html(obj_dict):
    """
    Represents a predictor or feature_learner in scikit-learn-style,
    but for _repr_html_
    """
    html = _str(obj_dict)

    html = html.replace("\n", "<br>")

    html = "<pre>" + html + "</pre>"

    return html
