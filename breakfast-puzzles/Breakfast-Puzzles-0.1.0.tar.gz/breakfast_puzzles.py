#!/usr/bin/env python3
"""
Breakfast Puzzles is a script for laying out a selection of puzzles from
Simon Tatham’s Portable Puzzle Collection onto a page.

It outputs PostScript, which can then be printed out.
"""
import argparse
import random
import re
import subprocess
import sys

MIN_WIDTH = 5

MM_TO_PT = 360 / 127


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


PRELUDE = [
    "/Helvetica findfont dup maxlength dict dup begin exch {1 index /FID ne {def} {pop pop} ifelse} forall /Encoding ISOLatin1Encoding def /FontName /Helvetica-L1 def FontName end exch definefont",
    "/Courier findfont dup maxlength dict dup begin exch {1 index /FID ne {def} {pop pop} ifelse} forall /Encoding ISOLatin1Encoding def /FontName /Courier-L1 def FontName end exch definefont",
    "gsave",
    "1 setgray fill",
    "0 setgray stroke",
    "/Helvetica-L1 findfont 25 scalefont setfont",
    f"40 790 moveto",
    f"(Puzzles) show",
    "grestore",
]

TRANSLATE_REGEX = re.compile(rb"(-?[0-9]+) (-?[0-9]+) translate")

LINE_WIDTH_REGEX = re.compile(r"([0-9]+) setlinewidth")


def output(data):
    sys.stdout.buffer.write(data)
    sys.stdout.flush()


def trim(postscript: list[bytes]):
    if b"%%EndProlog" not in postscript:
        eprint(postscript)
    ps = postscript[postscript.index(b"%%EndProlog") + 1 : postscript.index(b"%%EOF")]
    ps[-1] = ps[-1].removesuffix(b" showpage")
    return ps


def translate(postscript: list[bytes], x=0, y=0):
    return (
        ["gsave", f"{x} {y} translate", f"{MIN_WIDTH} setlinewidth"]
        + [
            x
            for x in postscript
            if b"clippath flattenpath pathbbox" not in x and b"exch 0.5 mul" not in x
        ]
        + ["grestore"]
    )


def get_puzzle(name, position, type_code):
    while (
        result := subprocess.run(
            [f"puzzles-{name}", "--print", "1x1", "--generate", "1", type_code],
            capture_output=True,
        )
    ).returncode:
        pass
    return translate(trim(result.stdout.splitlines()), *position)


DIFFS = "GFEDCBA"


class Puzzle:
    square_size = 6
    border = 1

    def __init__(self):
        if isinstance(self.size_range[0], int):
            self.size = random.randrange(*self.size_range)
        else:
            self.size = [random.randrange(*a) for a in self.size_range]
        if self.has_diffs:
            self.get_diff()

    def get_diff(self):
        self.diff = random.choices(
            list(self.diffs.keys()), [6 ** (-diff_counts[x]) for x in self.diffs]
        )[0]

    def space_needed(self):
        size = (self.size, self.size) if isinstance(self.size, int) else self.size
        return [self.square_size * (x + self.border) for x in size]

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def puzzles_name(self):
        return self.name.casefold()

    @property
    def type_code(self):
        try:
            size_string = "x".join(str(x) for x in self.size)
        except TypeError:
            size_string = str(self.size)
        if self.has_diffs:
            return size_string + "d" + self.diffs[self.diff]
        return size_string

    @property
    def type_name(self):
        try:
            size_string = "×".join(str(x) for x in self.size)
        except TypeError:
            size_string = str(self.size)
        if self.has_diffs:
            return size_string + DIFFS[self.diff]
        return size_string

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.type_code}>"

    @property
    def has_diffs(self):
        return hasattr(self, "diffs") and self.diffs is not None


class Keen(Puzzle):
    diffs = {1: "e", 2: "n", 4: "h", 5: "x", 6: "u"}
    size_range = (4, 10)
    square_size = 9


class Dominosa(Puzzle):
    diffs = {0: "t", 1: "b", 4: "h", 5: "e"}
    size_range = (3, 7)

    def space_needed(self):
        return [6 * (x + 1.5) for x in (self.size + 2, self.size + 1)]


class Sudoku(Puzzle):
    puzzles_name = "solo"
    diffs = {0: "t", 1: "b", 2: "i", 4: "a", 5: "e", 6: "u"}
    size_range = ((2, 5), (2, 5))
    size_limits = (5, 11)
    square_size = 9

    def __init__(self):
        while True:
            self.size = [random.randrange(*i) for i in self.size_range]
            if self.size_limits[0] <= self.size[0] * self.size[1] < self.size_limits[1]:
                break

        self.get_diff()

    def space_needed(self):
        return [
            self.square_size * (self.size[0] * self.size[1] + self.border)
            for _ in range(2)
        ]


class SudokuX(Sudoku):
    name = "Sudoku X"
    diffs = {0: "tx", 1: "bx", 2: "ix", 4: "ax", 5: "ex", 6: "ux"}


class Jigsaw(Sudoku):
    name = "Jigsaw Sudoku"
    diffs = {0: "t", 1: "b", 2: "i", 4: "a", 5: "e", 6: "u"}
    size_range = (5, 11)
    __init__ = Puzzle.__init__

    space_needed = Puzzle.space_needed

    @property
    def type_code(self):
        return f"{self.size}jd{self.diffs[self.diff]}"


class Killer(Sudoku):
    diffs = {0: "tk", 1: "bk", 2: "ik", 4: "ak", 5: "ek", 6: "uk"}
    size_limits = (5, 10)


class JigsawKiller(Killer, Jigsaw):
    name = "Jigsaw Killer"
    size_limits = (5, 10)
    __init__ = Puzzle.__init__

    @property
    def type_code(self):
        return f"{self.size}jkd{self.diffs[self.diff]}"


class Galaxies(Puzzle):
    diffs = {2: "n", 6: "u"}
    size_range = ((4, 14), (4, 14))
    square_size = 8
    border = 2


class Bridges(Puzzle):
    diffs = {1: "e", 2: "m", 4: "h"}
    size_range = ((5, 15), (5, 15))
    square_size = 10


class Pearl(Puzzle):
    diffs = {1: "e", 3: "t"}
    size_range = ((5, 13), (5, 13))


class Towers(Puzzle):
    diffs = {1: "e", 4: "h", 5: "x", 6: "u"}
    size_range = (4, 7)
    square_size = 9
    border = 9 / 4


class Unequal(Puzzle):
    puzzles_name = "unequal"
    diffs = {1: "e", 3: "k", 5: "x", 6: "r"}
    size_range = (4, 7)

    def space_needed(self):
        return [10 * (self.size + (self.size - 1) / 2 + 1) for _ in range(2)]


class Adjacent(Unequal):
    diffs = {0: "t", 1: "e", 3: "k", 5: "x", 6: "r"}

    def __init__(self):
        while True:
            self.size = random.randrange(5, 9)
            self.get_diff()
            if self.size > 4 or self.diff <= 1:
                break

    @property
    def type_code(self):
        return f"{self.size}ad{self.diffs[self.diff]}"


class LatinSquare(Unequal):
    name = "Latin Square"
    size_range = (4, 8)
    diffs = None

    @property
    def type_code(self):
        return f"{self.size}dt"


class Magnets(Puzzle):
    diffs = {1: "e", 3: "t", 5: "tS"}
    border = 2 + 1 / 4
    size_range = ((5, 11), (5, 11))


class Tents(Puzzle):
    diffs = {1: "e", 3: "t"}
    size_range = (6, 15)
    border = 2


class Slant(Puzzle):
    diffs = {1: "e", 4: "h"}
    border = 2 + 1 / 4
    size_range = ((4, 13), (4, 13))


class Tracks(Puzzle):
    diffs = {1: "e", 3: "t", 4: "h"}
    size_range = ((5, 15), (5, 15))
    square_size = 7
    border = 2 + 1 / 4


class Range(Puzzle):
    square_size = 8
    size_range = ((4, 13), (4, 13))


class Unruly(Puzzle):
    diffs = {1: "e", 2: "n"}
    size_range = ((6, 12, 2), (6, 12, 2))
    square_size = 7


class Rectangles(Puzzle):
    puzzles_name = "rect"
    square_size = 5
    border = 1.5
    size_range = ((7, 15), (5, 15))


class Filling(Puzzle):
    size_range = ((4, 13), (4, 13))


class LightUp(Puzzle):
    name = "Light Up"
    puzzles_name = "lightup"
    diffs = {1: "0", 3: "1", 4: "2"}
    size_range = ((6, 14), (4, 14))


class Singles(Puzzle):
    diffs = {1: "e", 3: "k"}
    square_size = 8
    size_range = ((5, 10), (5, 10))


class Pattern(Puzzle):
    square_size = 5
    border = 4
    size_range = ((6, 20), (6, 20))

    def space_needed(self):
        return [self.square_size * (6 * x / 5 + self.border) for x in self.size]


class Map(Puzzle):
    diffs = {1: "e", 2: "n", 4: "h", 6: "u"}
    square_size = 4
    border = 2
    size_range = ((10, 30), (10, 30))

    @property
    def type_code(self):
        return f"{self.size[0]}x{self.size[1]}n{round(self.size[0] * self.size[1] / 10)}d{self.diffs[self.diff]}"


class Signpost(Puzzle):
    square_size = 13
    size_range = ((3, 5), (3, 5))

    @property
    def type_code(self):
        return super().type_code + "c"


PUZZLES = (
    Bridges,
    Dominosa,
    Filling,
    Galaxies,
    Keen,
    Killer,
    # LatinSquare,
    LightUp,
    Magnets,
    Map,
    Pattern,
    Pearl,
    Range,
    Rectangles,
    Signpost,
    Singles,
    Slant,
    Sudoku,
    SudokuX,
    Jigsaw,
    JigsawKiller,
    Tents,
    Towers,
    Tracks,
    Unequal,
    Adjacent,
    Unruly,
)

A4 = (210, 298)
MARGINS = ((12, 12), (12, 12))


def intersects(rect1, rect2):
    sides = [[(r[i], r[i] + r[i + 2]) for r in (rect1, rect2)] for i in range(2)]
    return all(d[0][1] > d[1][0] and d[1][1] > d[0][0] for d in sides)


TITLE_RECT = (0, 273, 50, 40)

MIN_AREA = 39500

TRIES = 2000
DOMINOSA_2_TRIES = 100


def generate_layout():
    global diff_counts
    area = 0
    while area < MIN_AREA:
        rects = [TITLE_RECT]
        bottomlefts = [(MARGINS[0][0], MARGINS[1][0])]
        bad_count = 0
        puzzles = []
        diff_counts = [0 for _ in range(7)]
        puzzle_counts = {p: 0 for p in PUZZLES}
        area = 0
        while bad_count < TRIES + DOMINOSA_2_TRIES:
            if bad_count < TRIES:
                puzzle = random.choices(
                    list(puzzle_counts.keys()),
                    [6 ** -x for x in puzzle_counts.values()],
                )[0]()
            else:
                puzzle = Dominosa()
                puzzle.size = 2
            position = random.choice(bottomlefts)
            size = list(puzzle.space_needed())
            real_area = size[0] * size[1]
            size[1] += 9
            if not all(
                MARGINS[x][0] <= position[x] <= A4[x] - MARGINS[x][1] - size[x]
                for x in range(2)
            ):
                bad_count += 1
                continue
            rect = list(position) + size
            if any(intersects(rect, r) for r in rects):
                bad_count += 1
                continue
            for bottomleft in bottomlefts:
                if bottomleft[0] <= position[0] and bottomleft[1] <= position[1]:
                    newrect = list(bottomleft) + size
                    if not any(intersects(newrect, r) for r in rects):
                        position = bottomleft
                        rect = newrect

            bottomlefts.remove(position)
            newright = (position[0] + size[0], position[1])
            newup = (position[0], position[1] + size[1])
            bonuses = []
            for bl in bottomlefts:
                if [newright[0], bl[1]] not in bottomlefts:
                    if (
                        bl[0] <= newright[0]
                        and bl[1] <= newright[1]
                        or newright[0] <= bl[0]
                        and newright[1] <= bl[1]
                    ):
                        bonuses.append((newright[0], bl[1]))
                if [bl[0], newup[1]] not in bottomlefts:
                    if (
                        bl[0] <= newup[0]
                        and bl[1] <= newup[1]
                        or newup[0] <= bl[0]
                        and newup[1] <= bl[1]
                    ):
                        bonuses.append((bl[0], newup[1]))
            bottomlefts += [newright, newup] + bonuses
            position = list(position)
            position[1] += size[1] - 9
            puzzles.append((position + size, puzzle))
            puzzle_counts[type(puzzle)] += 1
            try:
                diff_counts[puzzle.diff] += 1
            except AttributeError:
                pass
            rects.append(rect)
            area += real_area if bad_count < TRIES else real_area / 3
        # eprint(area)
    return puzzles, rects, bottomlefts


def make_ps(verbose=False):
    full_ps = PRELUDE
    puzzles, rects, bl = generate_layout()
    # eprint(puzzles)
    for position, puzzle in puzzles:
        position = [x * MM_TO_PT for x in position]
        full_ps += [
            "gsave",
            "1 setgray fill",
            "0 setgray stroke",
            "/Helvetica-L1 findfont 14 scalefont setfont",
            f"{position[0] + position[2] / 2} {position[1] + 2} moveto",
            f"({puzzle.name} {puzzle.type_name}) dup stringwidth pop 2 div neg 0 rmoveto show",
            "grestore",
        ]
        if verbose:
            print(f"{puzzle.name} ({puzzle.type_name})")
        data = get_puzzle(puzzle.puzzles_name, position[:2], puzzle.type_code)
        new = []
        for row in data:
            row = row.decode("latin-1") if isinstance(row, bytes) else row
            if m := LINE_WIDTH_REGEX.match(row):
                if float(m.group(1)) < MIN_WIDTH:
                    new.append(f"{MIN_WIDTH} setlinewidth")
                    continue
            new.append(row)
        full_ps += new
    if False:
        for b in bl:
            b = [x * MM_TO_PT for x in b]
            full_ps += [
                f"newpath {b[0]} {b[1]} moveto",
                f"{b[0] + 3} {b[1] - 3} lineto",
                f"{b[0]} {b[1] + 5} lineto",
                "closepath",
                "stroke",
            ]
        full_ps.append(
            "grestore",
        )
    full_ps += ["gsave", "3 setlinewidth", "0 setgray fill", "0 setgray stroke"]
    for rect in rects:
        if rect == TITLE_RECT:
            continue
        x1, y1 = [x * MM_TO_PT for x in rect[:2]]
        x2, y2 = [(rect[i] + rect[i + 2]) * MM_TO_PT for i in range(2)]
        full_ps += [
            f"newpath {x1} {y1} moveto",
            f"{x1} {y2} lineto",
            f"{x2} {y2} lineto",
            f"{x2} {y1} lineto",
            "closepath",
            "stroke",
        ]
    full_ps += ["grestore", "showpage"]
    return b"\n".join(a.encode("latin-1") if isinstance(a, str) else a for a in full_ps)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "filename", type=argparse.FileType("wb"), help="file to write to"
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args()
    ps = make_ps(verbose=args.verbose)
    args.filename.write(ps)


if __name__ == "__main__":
    main()
