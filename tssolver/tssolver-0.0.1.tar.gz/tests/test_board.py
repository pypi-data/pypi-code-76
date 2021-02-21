"""Tests for the board module.

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

from tssolver import board
from tssolver import example_grids as eg


class TestBlankBoard(unittest.TestCase):
    def setUp(self):
        self.blank_board = board.Board(eg.blank_grid)

    def tearDown(self):
        del self.blank_board

    def test_grid_attr(self):
        self.assertEqual(
            self.blank_board.grid,
            eg.blank_grid,
        )

    def test_valid_entity_attr(self):
        self.assertIsInstance(
            self.blank_board._valid_entity,
            list,
        )
        self.assertEqual(
            len(self.blank_board._valid_entity),
            9,
        )
        self.assertEqual(
            self.blank_board._valid_entity[0],
            1,
        )
        self.assertEqual(
            self.blank_board._valid_entity[-1],
            9,
        )

    def test_sections_attr(self):
        self.assertIsInstance(
            self.blank_board.section_0,
            list,
        )
        self.assertIsInstance(
            self.blank_board.section_0[0],
            tuple,
        )
        self.assertEqual(
            len(self.blank_board.section_0),
            9,
        )
        self.assertIn(
            (0, 0),
            self.blank_board.section_0,
        )
        self.assertIn(
            (4, 4),
            self.blank_board.section_4,
        )
        self.assertIn(
            (8, 8),
            self.blank_board.section_8,
        )

    def test_valid_spaces_attr(self):
        self.assertIsInstance(
            self.blank_board.valid_spaces,
            list,
        )
        self.assertIsInstance(
            self.blank_board.valid_spaces[0],
            tuple,
        )
        self.assertEqual(
            self.blank_board.valid_spaces[0],
            (0, 0),
        )
        self.assertEqual(
            len(self.blank_board.valid_spaces),
            81,
        )

    def test_change_value(self):
        self.blank_board.change_value((0, 0), 9)
        self.blank_board.change_value((8, 8), 9)
        self.assertEqual(
            self.blank_board.grid[0][0],
            9
        )
        self.assertEqual(
            self.blank_board.grid[8][8],
            9
        )

    def test_get_value(self):
        self.blank_board.get_value((0, 0))
        self.blank_board.get_value((8, 8))
        self.assertEqual(
            self.blank_board.grid[0][0],
            0
        )
        self.assertEqual(
            self.blank_board.grid[8][8],
            0
        )

    def test_is_valid_move(self):
        self.assertTrue(
            self.blank_board.is_valid_move((0, 0), 9),
        )
        self.assertFalse(
            self.blank_board.is_valid_move((0, 0), 10),
        )


class TestExampleBoard(unittest.TestCase):
    def setUp(self):
        self.example_board = board.Board(eg.example_1)

    def tearDown(self):
        del self.example_board

    def test_grid_attr(self):
        self.assertEqual(
            self.example_board.grid,
            eg.example_1,
        )

    def test_valid_spaces_attr(self):
        self.assertIsInstance(
            self.example_board.valid_spaces,
            list,
        )
        self.assertIsInstance(
            self.example_board.valid_spaces[0],
            tuple,
        )
        self.assertNotIn(
            (0, 0),
            self.example_board.valid_spaces[0],
        )

    def test_is_valid_move(self):
        self.assertTrue(
            self.example_board.is_valid_move((0, 2), 1),
        )
        self.assertTrue(
            self.example_board.is_valid_move((8, 6), 1),
        )
        self.assertFalse(
            self.example_board.is_valid_move((0, 2), 5),
        )
        self.assertFalse(
            self.example_board.is_valid_move((8, 6), 5),
        )


if __name__ == "__main__":
    unittest.main()
