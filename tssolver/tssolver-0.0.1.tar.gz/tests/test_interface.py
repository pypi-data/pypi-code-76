"""Tests for the interface module.

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

import tkinter as tk
import unittest

from tssolver import example_grids as eg
from tssolver import interface


class TestMainApplication(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.main_app = interface.MainApplication(self.root)
        self.main_app.parent.update()

    def tearDown(self):
        self.root.destroy()

    def test_root(self):
        self.assertTrue(
            self.root.winfo_exists(),
        )
        self.assertEqual(
            self.root.title(),
            "Sudoku Solver"
        )


class TestToolbar(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.main_app = interface.MainApplication(self.root)
        self.main_app.toolbar.speed_radio.set("instant")

    def tearDown(self):
        self.root.destroy()

    def test_solve(self):
        self.main_app.toolbar.board_menu.invoke(0)
        self.assertEqual(
            self.main_app.puzzle.board.grid,
            eg.blank_grid_solution,
        )

    def test_clear(self):
        self.main_app.toolbar.board_menu.invoke(0)
        self.assertEqual(
            self.main_app.puzzle.board.grid,
            eg.blank_grid_solution,
        )
        self.main_app.toolbar.board_menu.invoke(3)
        self.assertEqual(
            self.main_app.puzzle.board.grid,
            eg.blank_grid,
        )

    def test_load_sample(self):
        self.main_app.toolbar.samples_menu.invoke(0)
        self.main_app.toolbar.board_menu.invoke(0)
        self.assertEqual(
            self.main_app.puzzle.board.grid,
            eg.example_1_solution,
        )

    def test_set_colorblind_mode(self):
        self.assertEqual(
            self.main_app.toolbar.colorblind_check.get(),
            "False",
        )
        self.main_app.toolbar.options_menu.invoke(0)
        self.assertEqual(
            self.main_app.toolbar.colorblind_check.get(),
            "True",
        )

    def test_set_solve_speed(self):
        self.assertEqual(
            self.main_app.toolbar.speed_radio.get(),
            "instant",
        )
        self.main_app.toolbar.solve_speed.invoke(0)
        self.assertEqual(
            self.main_app.toolbar.speed_radio.get(),
            "slow",
        )
        self.main_app.toolbar.solve_speed.invoke(1)
        self.assertEqual(
            self.main_app.toolbar.speed_radio.get(),
            "medium",
        )
        self.main_app.toolbar.solve_speed.invoke(2)
        self.assertEqual(
            self.main_app.toolbar.speed_radio.get(),
            "fast",
        )
        self.main_app.toolbar.solve_speed.invoke(3)
        self.assertEqual(
            self.main_app.toolbar.speed_radio.get(),
            "instant",
        )

    def test_help(self):
        self.main_app.toolbar.help_menu.invoke(0)
        self.assertTrue(
            self.main_app.toolbar.help_dialog.dialog.winfo_exists(),
        )

    def test_about(self):
        self.main_app.toolbar.help_menu.invoke(2)
        self.assertTrue(
            self.main_app.toolbar.about_dialog.dialog.winfo_exists(),
        )


if __name__ == "__main__":
    unittest.main()
