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
Collection of functions for visualizing tables
that are not intended to be used by
the end-user.
"""

import json

import numpy as np

import getml.communication as comm

from .helpers import _is_typed_list

# --------------------------------------------------------------------

BORDER_STYLE = "1pt solid LightGray;"
BORDER_STYLE_BOTTOM = "border-bottom:" + BORDER_STYLE
BORDER_STYLE_RIGHT = "border-right:" + BORDER_STYLE
BORDER_STYLE_TOP = "border-top:" + BORDER_STYLE

TRUNCATE_ROWS_ASCII = True
TRUNCATE_ROWS_HTML = False

# --------------------------------------------------------------------


def _add_index(lines, begin, length):
    index = np.arange(begin, begin + length).astype(str)
    return [[ix] + line for ix, line in zip(index, lines)]


# --------------------------------------------------------------------


def _check_head_and_body(head, body):
    """
    Checks whether the head and body input for a
    table is plausible.
    """

    if not isinstance(head, list) or not all(
        [_is_typed_list(elem, str) for elem in head]
    ):
        raise TypeError("'head' must be a list of a list of strings.")

    if not isinstance(body, list) or not all(
        [_is_typed_list(elem, str) for elem in body]
    ):
        raise TypeError("'body' must be a list of a list of strings.")

    if not head:
        raise ValueError("'head' cannot be empty!")

    length_set = {len(elem) for elem in head + body}

    if len(length_set) != 1:
        raise ValueError(
            """All lines in 'body' and 'head'
                             must have the same length."""
        )


# --------------------------------------------------------------------


def _extrapolate_list(rows):
    processed_rows = []
    for row in rows:
        row_depth = max(_get_depth(cell) for cell in row)
        if row_depth > 1:
            for j in range(row_depth):
                processed_rows.append(
                    [
                        _get_contents(cell, j) if j < _get_depth(cell) else ""
                        for cell in row
                    ]
                )
        else:
            processed_rows.append(["".join(cell) for cell in row])

    return processed_rows


# --------------------------------------------------------------------


def _extract_columns(lines, cols):
    extracted = []

    for line in lines:
        extracted.append([line[ix] for ix in cols])

    return extracted


# --------------------------------------------------------------------


def _find_max_lengths(head, body):

    _check_head_and_body(head, body)

    n_columns = len(head[0])

    max_lengths = np.zeros(n_columns).astype(int)

    for line in head + body:
        for i, elem in enumerate(line):
            if len(elem) > max_lengths[i]:
                max_lengths[i] = len(elem)

    return max_lengths


# --------------------------------------------------------------------


def _get_break_col(line, max_width):
    cells = []
    for index, cell in enumerate(line):
        cells.append(cell)
        width = len("   ".join(cells))
        if width >= max_width:
            return index
    return len(line)


# --------------------------------------------------------------------


def _get_column_content(col, coltype, start, length):
    """
    Returns the contents of a data frame in a format that is
    compatible with jquery.data.tables.

    Args:
        col (dict): The thisptr describing the dict.

        coltype (str): The type of the column
            (FloatColumn, StringColumn or BooleanColumn).

        start (int): The number of the first line to retrieve.

        length (int): The number of lines to retrieve.
    """

    # ------------------------------------------------------------

    if not isinstance(start, int):
        raise TypeError("'start' must be an int.")

    if not isinstance(length, int):
        raise TypeError("'length' must be an int.")

    # ------------------------------------------------------------

    cmd = dict()

    cmd["type_"] = coltype + ".get_content"
    cmd["name_"] = col["df_name_"]

    cmd["col_"] = col
    cmd["draw_"] = 1

    cmd["start_"] = start
    cmd["length_"] = length

    # ------------------------------------------------------------

    sock = comm.send_and_receive_socket(cmd)

    json_str = comm.recv_string(sock)

    if json_str[0] != "{":
        comm.engine_exception_handler(json_str)

    # ------------------------------------------------------------

    return json.loads(json_str)


# --------------------------------------------------------------------


def _get_data_frame_content(name, start, length):
    """
    Returns the contents of a data frame in a format that is
    compatible with jquery.data.tables.

    Args:
        name (str): The name of the data frame.

        start (int): The number of the first line to retrieve.

        length (int): The number of lines to retrieve.
    """

    # ------------------------------------------------------------

    if not isinstance(name, str):
        raise TypeError("'name' must be a str.")

    if not isinstance(start, int):
        raise TypeError("'start' must be an int.")

    if not isinstance(start, int):
        raise TypeError("'length' must be an int.")

    # ------------------------------------------------------------

    cmd = dict()

    cmd["type_"] = "DataFrame.get_content"
    cmd["name_"] = name

    cmd["start_"] = start
    cmd["length_"] = length

    cmd["draw_"] = 1

    # ------------------------------------------------------------

    sock = comm.send_and_receive_socket(cmd)

    json_str = comm.recv_string(sock)

    if json_str[0] != "{":
        comm.engine_exception_handler(json_str)

    # ------------------------------------------------------------

    return json.loads(json_str)


# --------------------------------------------------------------------


def _get_contents(cell, index):
    if isinstance(cell, str):
        return cell
    if isinstance(cell, list):
        return cell[index]


# --------------------------------------------------------------------


def _get_depth(cell):
    return len(cell) if isinstance(cell, list) else 1


# --------------------------------------------------------------------


def _get_truncated(lines, n_cols, has_index=True):
    if len(lines) == 0:
        return lines
    first = list(range(n_cols // 2))
    if has_index:
        first.append(n_cols // 2 + 1)
    last = list(range(len(lines[0]) - n_cols // 2, len(lines[0])))
    lines_first = _extract_columns(lines, first)
    lines_last = _extract_columns(lines, last)
    lines = [first + ["..."] + last for first, last in zip(lines_first, lines_last)]
    return lines


# --------------------------------------------------------------------


def _lines_to_string(lines, max_lengths, align_left=True):

    ascii_str = ""

    for line in lines:
        for i, elem in enumerate(line):
            filler = " " * (max_lengths[i] - len(elem))
            if align_left:
                ascii_str += elem + filler + "   "
            else:
                ascii_str += filler + elem + "   "
        ascii_str += "\n"

    return ascii_str


# --------------------------------------------------------------------


# TODO: Refactor to utilize Formatter class
# TODO: Introduce column formatting


def _make_ascii_table(head, body, cols=None, has_index=True, max_cols=8, max_width=99):
    """
    Returns a string representation of the table.
    """

    # ----------------------------------------------------------------

    if cols is not None:
        head = _extract_columns(head, cols)
        body = _extract_columns(body, cols)
    # ----------------------------------------------------------------

    assert head, "Head cannot be empty"

    # ----------------------------------------------------------------

    if any(isinstance(cell, list) for row in body for cell in row):
        body = _extrapolate_list(body)

    # ----------------------------------------------------------------

    if TRUNCATE_ROWS_ASCII and len(head[0]) > max_cols:
        head = _get_truncated(head, max_cols, has_index)
        body = _get_truncated(body, max_cols, has_index)

    # ----------------------------------------------------------------

    cols_per_row = min(_get_break_col(line, max_width) for line in head + body)

    if len(head[0]) > cols_per_row:
        cols_head = np.arange(0, cols_per_row).tolist()
        cols_tail = np.arange(cols_per_row, len(head[0])).tolist()

        if has_index:
            cols_tail = [0] + cols_tail

        ascii_str = _make_ascii_table(head, body, cols_head)
        ascii_str += "\n\n\n"
        ascii_str += _make_ascii_table(head, body, cols_tail)

        return ascii_str

    # ----------------------------------------------------------------

    max_lengths = _find_max_lengths(head, body)

    # ----------------------------------------------------------------

    ascii_str = _lines_to_string(head, max_lengths, align_left=False)

    ascii_str += _lines_to_string(body, max_lengths, align_left=True)

    # ----------------------------------------------------------------

    return ascii_str


# --------------------------------------------------------------------


def _make_html_body(body, has_index=True):

    col_ix = 1 if has_index else 0

    html_str = "<tbody>"

    for i, line in enumerate(body):
        style_top = ' style="' + BORDER_STYLE_TOP + '"' if i == 0 else ""

        style_right = ' style="' + BORDER_STYLE_RIGHT + '"'

        html_str += "<tr" + style_top + ">"

        html_str += "".join(
            [
                "<td" + style_right + "><b>" + field + "</b></td>"
                for field in line[:col_ix]
            ]
        )

        html_str += "".join(["<td>" + field + "</td>" for field in line[col_ix:]])

        html_str += "</tr>"

    html_str += "</tbody>"

    return html_str


# --------------------------------------------------------------------


def _make_head_first_line(head, col_ix):

    html_str = ""

    for line in head:
        html_str += '<tr style="' + BORDER_STYLE_BOTTOM + '">'

        html_str += "".join(
            [
                '<th style="text-align: left;'
                + BORDER_STYLE_RIGHT
                + '">'
                + field
                + "</th>"
                for field in line[:col_ix]
            ]
        )

        html_str += "".join(
            [
                '<th style="text-align: right;">' + field + "</th>"
                for field in line[col_ix:]
            ]
        )

        html_str += "</tr>"

    return html_str


# --------------------------------------------------------------------


def _make_head_other_lines(head, col_ix):

    html_str = ""

    for line in head:
        html_str += "<tr>"

        html_str += "".join(
            [
                '<th style="text-align: left;'
                + BORDER_STYLE_RIGHT
                + '">'
                + field
                + "</th>"
                for field in line[:col_ix]
            ]
        )

        html_str += "".join(
            [
                '<td style="text-align: right;"><i>' + field + "</i></td>"
                for field in line[col_ix:]
            ]
        )

        html_str += "</tr>"

    return html_str


# --------------------------------------------------------------------


def _make_html_head(head, has_index=True):

    col_ix = 1 if has_index else 0

    html_str = "<thead>"

    html_str += _make_head_first_line(head[:1], col_ix)

    html_str += _make_head_other_lines(head[1:], col_ix)

    html_str += "</thead>"

    return html_str


# --------------------------------------------------------------------


# TODO: Refactor to utilize Formatter class
def _make_html_table(head, body, has_index=True, max_cols=8):
    """
    Returns an HTML representation of the table.
    """

    # ----------------------------------------------------------------

    _check_head_and_body(head, body)

    # ----------------------------------------------------------------

    html_str = '<table class="dataframe">'

    # ----------------------------------------------------------------

    if TRUNCATE_ROWS_HTML and len(head[0]) > max_cols:
        head = _get_truncated(head, max_cols, has_index)
        body = _get_truncated(body, max_cols, has_index)

    html_str += _make_html_head(head, has_index)

    html_str += _make_html_body(body, has_index)

    # ----------------------------------------------------------------

    html_str += "</table>"

    # ----------------------------------------------------------------

    return html_str


# --------------------------------------------------------------------


def _make_link(mystr):
    if "url: " not in mystr:
        return mystr
    url = mystr.split("url: ")[1]
    link = '<a href="' + url + '" target="_blank">' + url + "</a>"
    return "url: " + link


# --------------------------------------------------------------------


def _monitor_url():

    cmd = dict()

    cmd["type_"] = "monitor_url"
    cmd["name_"] = ""

    sock = comm.send_and_receive_socket(cmd)

    return comm.recv_string(sock)


# --------------------------------------------------------------------
