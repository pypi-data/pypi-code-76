from .grow import grow
from .resize import resize
from .sortify import sortify
from ..objects.lilyblock import block


class ColumnBuilder:
    def __init__(
        self, column_count=0, total_width=80, align="left", min_spacing=3
    ):
        self.column_count = column_count
        self.total_width = total_width
        self.align = align
        self.min_spacing = min_spacing

    def make_columns(self, iterable, sort=True, horizontal=False):
        if not iterable:
            return block("")

        iterable = [grow(item) for item in iterable]
        column_count = self._get_column_count(iterable)
        entries_per_column, remainder = divmod(len(iterable), column_count)
        if remainder > 0:
            entries_per_column += 1

        if sort:
            iterable = sortify(iterable)
        iterable = self._resize_all(iterable, column_count)

        if horizontal:
            rows = self._make_rows_horizontally(
                iterable, column_count, entries_per_column
            )
        else:
            rows = self._make_rows_vertically(
                iterable, column_count, entries_per_column
            )

        return self._merge_rows_to_lilyblock(rows)

    def _make_rows_horizontally(
        self, iterable, column_count, entries_per_column
    ):
        rows = []
        for i in range(entries_per_column):
            start = column_count * i
            stop = start + column_count
            rows.append(iterable[start:stop])
        return rows

    def _make_rows_vertically(
        self, iterable, column_count, entries_per_column
    ):
        rows = []
        for i in range(entries_per_column):
            rows.append(iterable[i::entries_per_column])
        return rows

    def _get_column_count(self, iterable):
        if self.column_count != 0:
            return self.column_count

        longest_item_size = max([len(item) for item in iterable])
        columns = self.total_width // (longest_item_size + self.min_spacing)

        # If we have fewer items than columns, we aren't going to
        # fill all of the columns.
        if len(iterable) < columns:
            columns = len(iterable)
        if columns == 0:
            return 1
        return columns

    def _resize_all(self, iterable, column_count):
        total_spacing = self.min_spacing * (column_count - 1)
        usable_width = self.total_width - total_spacing
        max_cell_size = usable_width // column_count
        max_item_size = max([len(item) for item in iterable])
        item_size = min([max_cell_size, max_item_size])
        return [resize(s, item_size, align=self.align) for s in iterable]

    def _merge_rows_to_lilyblock(self, rows):
        space = grow(" " * self.min_spacing)
        rows = [space.join(row) for row in rows]
        return block(rows)


def columnify(
    iterable,
    columns=0,
    width=80,
    align="left",
    sort=True,
    min_spacing=3,
    horizontal=False,
):
    builder = ColumnBuilder(
        column_count=columns,
        total_width=width,
        align=align,
        min_spacing=min_spacing,
    )
    return builder.make_columns(iterable, sort=sort, horizontal=horizontal)
