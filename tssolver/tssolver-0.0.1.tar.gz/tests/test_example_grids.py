"""Tests for the example_grids module.

Copyright (C) 2021 emerac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import unittest

from tssolver import example_grids as eg


class TestExampleGrids(unittest.TestCase):
    def test_blank_grid(self):
        self.assertIsInstance(
            eg.blank_grid,
            list,
        )
        self.assertEqual(
            len(eg.blank_grid),
            9,
        )
        for row in range(9):
            self.assertIsInstance(
                eg.blank_grid,
                list,
            )
            self.assertEqual(
                len(eg.blank_grid[row]),
                9,
            )
            for column in range(9):
                self.assertEqual(
                    eg.blank_grid[row][column],
                    0,
                )

    def test_example_grids(self):
        self.example_1 = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
        self.example_2 = [
            [1, 0, 0, 0, 8, 0, 0, 0, 6],
            [0, 2, 0, 4, 0, 0, 0, 7, 0],
            [0, 0, 3, 0, 0, 0, 5, 0, 0],
            [0, 0, 4, 0, 0, 7, 0, 1, 0],
            [5, 0, 0, 0, 3, 0, 0, 0, 8],
            [0, 6, 0, 2, 0, 0, 9, 0, 0],
            [0, 0, 7, 0, 0, 0, 2, 0, 0],
            [0, 8, 0, 0, 0, 9, 0, 3, 0],
            [9, 0, 0, 0, 6, 0, 0, 0, 4],
        ]
        self.example_3 = [
            [0, 0, 2, 0, 1, 0, 3, 0, 0],
            [0, 4, 0, 7, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 0, 0, 9, 0, 4],
            [0, 9, 0, 0, 0, 1, 0, 0, 0],
            [6, 0, 0, 0, 9, 0, 0, 0, 5],
            [0, 0, 0, 3, 0, 0, 0, 9, 0],
            [8, 0, 4, 0, 0, 0, 0, 0, 6],
            [0, 0, 0, 0, 0, 8, 0, 1, 0],
            [0, 0, 3, 0, 7, 0, 2, 0, 0],
        ]
        self.assertEqual(
            eg.example_1,
            self.example_1,
        )
        self.assertEqual(
            eg.example_2,
            self.example_2,
        )
        self.assertEqual(
            eg.example_3,
            self.example_3,
        )


if __name__ == "__main__":
    unittest.main()
