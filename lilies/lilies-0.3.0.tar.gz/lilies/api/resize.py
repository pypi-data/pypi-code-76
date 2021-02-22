from copy import deepcopy
from ..objects.lilyblock import block
from ..objects.lilystring import LilyString
from ..style import Style
from .grow import grow


class Resizer:
    def __init__(self, width, height, align, add_elipsis):
        self.width = width
        self.height = height
        self.align_x, self.align_y = self._parse_align(align)
        self.add_elipsis = add_elipsis

    def resize(self, stringlike, character=" "):
        lilyblock = block(grow(stringlike))
        if self.height == -1:
            height = lilyblock.height
        else:
            height = self.height
        lilyblock = self._resize_vertical(lilyblock, height, character)

        if self.width == -1:
            width = lilyblock.width
        else:
            width = self.width
        resized_rows = [
            self._resize_row(row, width, character) for row in lilyblock
        ]

        return grow(resized_rows)

    def _parse_align(self, align):
        if align == "center":
            return "center", "center"
        if align in ("left", "right"):
            return align, "top"
        if align in ("top", "bottom"):
            return "left", align
        align_components = align.split()
        if len(align_components) != 2:
            raise TypeError("Invalid align value: " + str(align))
        align_y, align_x = align_components
        if align_x not in ("left", "right", "center"):
            raise TypeError("Invalid horizontal align value: " + str(align_x))
        if align_y not in ("top", "bottom", "center"):
            raise TypeError("Invalid vertical align value: " + str(align_y))
        return align_x, align_y

    def _resize_row(self, lilystring, width, character):
        if lilystring.width <= width:
            return self._widen(lilystring, width, character)
        else:
            return self._truncate(lilystring, width)

    def _widen(self, lilystring, width, character):
        if len(lilystring) == width:
            return deepcopy(lilystring)

        if self.align_x == "center":
            return lilystring.center(width, character)
        elif self.align_x == "right":
            return lilystring.rjust(width, character)
        else:
            return lilystring.ljust(width, character)

    def _truncate(self, lilystring, width):
        if self.add_elipsis:
            elipsis = LilyString("..", lilystring.style_at(-1))
            if self.width <= len(elipsis):
                # no elipsis if it'd be too small
                return lilystring[:width]
            truncated = lilystring[: width - len(elipsis)]
            return truncated + elipsis
        return lilystring[:width]

    def _resize_vertical(self, lilyblock, height, character):
        if self.align_y == "center":
            return self._resize_vertical_centered(lilyblock, height, character)
        elif self.align_y == "bottom":
            return self._resize_vertical_uncentered(
                lilyblock, height, character, bottom=True
            )
        else:
            return self._resize_vertical_uncentered(
                lilyblock, height, character, bottom=False
            )

    def _resize_vertical_centered(self, lilyblock, height, character):
        height_difference = height - lilyblock.height

        # We want the top half to always have equal or less change,
        # Expanding or contracting by an odd number will cause the
        # Lower rows to be affected more than the top rows.
        # Python will always round remainders toward negative infinity.
        # Since we want it rounded towards 0, the positive remainder 1,
        # if it exists, should get added with the quotient.
        if height_difference > 0:
            top_difference = height_difference // 2
        else:
            top_difference = sum(divmod(height_difference, 2))

        resized_top_only = self._resize_vertical_uncentered(
            lilyblock,
            lilyblock.height + top_difference,
            character,
            bottom=True,
        )
        return self._resize_vertical_uncentered(
            resized_top_only, height, character
        )

    def _resize_vertical_uncentered(
        self, lilyblock, height, character, bottom=False
    ):
        height_difference = height - lilyblock.height
        if height_difference < 0:
            if bottom:
                return lilyblock[abs(height_difference) :]
            else:
                return lilyblock[:height]
        try:
            style = character.style_at(0)
        except AttributeError:
            if lilyblock.height:
                if bottom:
                    style = lilyblock._rows[0].style_at(0)
                else:
                    style = lilyblock._rows[-1].style_at(0)
            else:
                style = Style()
        if character is None:
            character = " "
        fill = block([LilyString(character, style)] * height_difference)
        if bottom:
            return fill.append(lilyblock)
        else:
            return lilyblock.append(fill)


def resize(
    stringlike,
    width=-1,
    height=-1,
    align="left",
    character=None,
    add_elipsis=True,
):
    resizer = Resizer(width, height, align, add_elipsis=add_elipsis)
    return resizer.resize(stringlike, character)
