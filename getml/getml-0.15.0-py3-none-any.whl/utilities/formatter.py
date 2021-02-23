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

import datetime
import itertools as it
from copy import deepcopy

from getml.data.visualization import _make_html_table

# --------------------------------------------------------------------


def _clip_lines(lines, max_cols):
    if len(lines[0]) > max_cols:
        threshold = max_cols // 2
        lines_clipped = []
        ellipses = ["..." if row[0].strip() else "   " for row in lines]
        for line, ellipsis in zip(lines, ellipses):
            line = list(line)
            lines_clipped.append(line[:threshold] + [ellipsis] + line[-threshold:])
        return lines_clipped
    return lines


# --------------------------------------------------------------------


def _get_depth(cell):
    return len(cell) if isinstance(cell, list) else 1


# --------------------------------------------------------------------


def _get_width(cell, decimal_places=None):
    if isinstance(cell, list):
        if len(cell) > 0:
            return max(_get_width(elem, decimal_places) for elem in cell)
        return 0
    if isinstance(cell, float) and decimal_places is not None:
        return len(f"{cell: .{decimal_places}f}")
    return len(str(cell))


# --------------------------------------------------------------------


def _split_lines(lines, margin, max_width):
    lines_split = []
    lines_remaining = []

    for line in lines:
        truncated = list(_truncate_line(line, margin, max_width))
        remaining = list(line[len(truncated) :])

        lines_split.append(truncated)

        if remaining:
            index = [line[0]]
            lines_remaining.append(index + remaining)

    if lines_remaining:
        lines_split.append([""])
        lines_split.extend(_split_lines(lines_remaining, margin, max_width))

    return lines_split


# --------------------------------------------------------------------


def _truncate_line(line, margin, max_width):
    widths = (len(cell) + margin for cell in line)
    cum_widths = it.accumulate(widths)

    for cell, cum_width in zip(line, cum_widths):
        if cum_width < max_width:
            yield cell


# --------------------------------------------------------------------


class Formatter:
    """A formatter for tabular output of data."""

    # ------------------------------------------------------------

    # TODO: Allow construction from dict of columns
    # TODO: Design argument checks
    # TODO: subheaders argument to supply subheaders with dict
    def __init__(self, headers=None, rows=None, columns=None):

        # the margin between columns
        self.margin = 3
        # maximum tolerable width of an output line
        self.max_width = 130
        # maximum number of output rows
        self.max_rows = 50
        # maximum number of output columns
        self.max_cols = 10

        self.data = []

        if columns is None:

            depths = [max(_get_depth(cell) for cell in row) for row in rows]

            columns = zip(*rows)
            headers = zip(*headers)

            for header, cells in it.zip_longest(headers, columns, fillvalue=[]):
                self.data.append(
                    FormatColumn(list(header), list(cells), depths, self.max_rows)
                )

        if headers == rows == None:

            columns = deepcopy(columns)

            depths = [
                max(_get_depth(cell) for cell in row) for row in zip(*columns.values())
            ]

            for header, cells in columns.items():
                self.data.append(FormatColumn([header], cells, depths, self.max_rows))

    # ------------------------------------------------------------

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key]
        if isinstance(key, str):
            try:
                return [column for column in self.data if column.name == key][0]
            except IndexError as exc:
                raise AttributeError(f"No FormatColumn with name: {key}") from exc
        raise TypeError(
            f"Formatters can only be indexed by: int, slices, or str, not {type(key).__name__}"
        )

    # ------------------------------------------------------------

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        output = [f"{'column':20}{'format':15}{'header format':15}"]
        for column in self.data:
            output.append(
                f"{column.header:20}{repr(column.format):15}{repr(column.header_format):15}"
            )
        return "\n".join(output)

    # ------------------------------------------------------------

    def _pivot(self):
        columns = [column.data for column in self.data]
        return list(zip(*columns))

    # ------------------------------------------------------------

    def render_string(self):
        columns_formatted = [column.format_cells() for column in self.data]

        headers = [column.header for column in columns_formatted]
        sub_headers = [
            list(sub_header)
            for column in columns_formatted
            for sub_header in zip(*column.sub_headers)
        ]

        columns_clipped = [column.clip() for column in columns_formatted]
        cells = [column.expand_cells() for column in columns_clipped]
        rows = [list(cell) for cell in zip(*cells)]

        lines = [headers] + sub_headers + rows
        lines_clipped = _clip_lines(lines, self.max_cols)
        lines_split = _split_lines(lines_clipped, self.margin, self.max_width)

        margin = " " * self.margin
        lines_rendered = [margin.join(line) for line in lines_split]

        return "\n".join(lines_rendered)

    # ------------------------------------------------------------

    def render_html(self):
        columns_formatted = [column.format_cells() for column in self.data]
        headers = [column.header for column in columns_formatted]

        columns_clipped = [column.clip() for column in columns_formatted]
        cells = [column.unnest_html() for column in columns_clipped]
        rows = [list(row) for row in zip(*cells)]

        return _make_html_table([headers], rows)


# --------------------------------------------------------------------


class FormatColumn:
    """A formatable column of an output table."""

    # ------------------------------------------------------------

    def __init__(self, header, cells, depths, max_length):
        self.data = cells
        self.decimal_places = 5 if self.instances_are(float) else None
        self.depths = depths
        self.formatted = False
        self.header = header[0]
        self.max_length = max_length
        self.sub_headers = []
        if len(header) > 1:
            self.sub_headers = header[1:]

        # TODO: Change attribute name
        self.format = self.default_cell_format
        self.header_format = self.default_header_format

    # ------------------------------------------------------------

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        if self.formatted:
            cells = self._unnest()[:10]
        else:
            cells = [str(cell) for cell in self._unnest()[:10]]

        return "\n".join(
            [self.header]
            + [f"{self.format:^{self.width}}"]
            + cells
            + [f"{'...':^{self.width}}"]
        )

    # ------------------------------------------------------------

    def _unnest(self):
        if self.nested:
            return [elem for cell in self.data for elem in cell]
        return self.data

    # ------------------------------------------------------------

    @property
    def default_cell_format(self):
        if self.instances_are(float):
            return "{:" f" {self.width}.{self.decimal_places}f" "}"
        if self.instances_are(int):
            return "{:>" f"{self.width}" "}"
        if self.instances_are(datetime.datetime):
            return "{:%Y-%m-%d %H:%M:%S}"
        return "{:" f"{self.width}" "}"

    # ------------------------------------------------------------

    @property
    def default_header_format(self):
        if self.instances_are(float):
            return "{:>" f"{self.width}" "}"
        if self.instances_are(datetime.datetime):
            # the default datetime format has a fixed
            # width of 19 chars
            return "{:19}"
        return self.default_cell_format

    # ------------------------------------------------------------

    def clip(self):
        if len(self.data) > self.max_length:
            column_clipped = deepcopy(self)
            head = self.data[: self.max_length // 2]
            tail = self.data[-self.max_length // 2 :]
            ellipses = (
                [self.header_format.format("...")]
                if self.header.strip()
                else [self.header_format.format("")]
            )
            if self.nested:
                ellipses = [ellipses]
            column_clipped.data = head + ellipses + tail
            return column_clipped
        return self

    # ------------------------------------------------------------

    def expand_cells(self):

        cells_expanded = []
        pad_cell = " " * self.width

        for cell, row_depth in zip(self.data, self.depths):
            cell_expanded = [cell] if not isinstance(cell, list) else list(cell)
            depth = _get_depth(cell)
            if depth < row_depth:
                remaining = row_depth - depth
                cell_expanded += [pad_cell] * remaining
            cells_expanded.extend(cell_expanded)

        return cells_expanded

    # ------------------------------------------------------------

    def format_cells(self):
        # make format-relevant params accessible as local vars
        fmt_params = {"width": self.width}

        column_formatted = deepcopy(self)

        if self.nested:
            cells_formatted = [
                [self.format.format(elem, cell=elem, **fmt_params) for elem in cell]
                for cell in self.data
            ]
        else:
            cells_formatted = [
                self.format.format(cell, cell=cell, **fmt_params) for cell in self.data
            ]

        column_formatted.data = cells_formatted
        column_formatted.header = self.header_format.format(
            self.header, head=self.header, **fmt_params
        )
        column_formatted.sub_headers = [
            self.header_format.format(sub_header, head=sub_header, **fmt_params)
            for sub_header in self.sub_headers
        ]
        column_formatted.formatted = True

        return column_formatted

    # ------------------------------------------------------------

    def instances_are(self, type_):
        if self.nested:
            return all(isinstance(elem, type_) for cell in self.data for elem in cell)
        return all(isinstance(cell, type_) for cell in self.data)

    # ------------------------------------------------------------

    @property
    def nested(self):
        return all(isinstance(cell, list) for cell in self.data)

    # ------------------------------------------------------------

    @property
    def type(self):
        # TODO Implement more sanity checks
        if self.nested:
            types = set(type(elem) for cell in self.data for elem in cell)
        else:
            types = set(type(cell) for cell in self.data)

        if len(types) == 1:
            return types.pop()

        if len(types) > 1:
            return types

        return None

    # ------------------------------------------------------------

    def unnest_html(self):
        if self.nested:
            return ["<br>".join(cell) for cell in self.data]
        return self.data

    # ------------------------------------------------------------

    @property
    def width(self):
        return max(
            _get_width(cell, self.decimal_places)
            for cell in [self.header] + self.sub_headers + self.data
        )
