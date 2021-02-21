"""Tests for the solver module.

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

from tssolver import board
from tssolver import example_grids as eg
from tssolver import interface
from tssolver import solver


class TestGraphicSolver(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.main_app = interface.MainApplication(self.root)
        self.main_app.toolbar.speed_radio.set("instant")

    def tearDown(self):
        self.root.destroy()

    def test_graphic_solver_on_blank_board(self):
        self.graphic_solver = solver.GraphicSolver(
            self.main_app.toolbar,
            self.main_app.puzzle,
        )
        self.graphic_solver.interface_solver()
        self.assertTrue(self.main_app.puzzle.board.is_win())

    def test_graphic_solver_on_sample_board_1(self):
        self.main_app.puzzle.board = board.Board(eg.example_1)
        self.graphic_solver = solver.GraphicSolver(
            self.main_app.toolbar,
            self.main_app.puzzle,
        )
        self.graphic_solver.interface_solver()
        self.assertTrue(self.main_app.puzzle.board.is_win())

    def test_graphic_solver_on_sample_board_2(self):
        self.main_app.puzzle.board = board.Board(eg.example_2)
        self.graphic_solver = solver.GraphicSolver(
            self.main_app.toolbar,
            self.main_app.puzzle,
        )
        self.graphic_solver.interface_solver()
        self.assertTrue(self.main_app.puzzle.board.is_win())

    def test_graphic_solver_on_sample_board_3(self):
        self.main_app.puzzle.board = board.Board(eg.example_3)
        self.graphic_solver = solver.GraphicSolver(
            self.main_app.toolbar,
            self.main_app.puzzle,
        )
        self.graphic_solver.interface_solver()
        self.assertTrue(self.main_app.puzzle.board.is_win())

    def test_graphic_solver_on_invalid_board(self):
        self.main_app.puzzle.board = board.Board(eg.example_1)
        for row in range(9):
            for column in range(9):
                self.main_app.puzzle.board.change_value((row, column), 999)
        self.graphic_solver = solver.GraphicSolver(
            self.main_app.toolbar,
            self.main_app.puzzle,
        )
        self.assertFalse(self.main_app.puzzle.board.is_win())


class TestTerminalSolver(unittest.TestCase):
    def test_blank_board(self):
        self.board = board.Board(eg.blank_grid)
        self.terminal_solver = solver.TerminalSolver(self.board)
        self.terminal_solver.terminal_solver()
        self.assertTrue(self.board.is_win())

    def test_sample_board_1(self):
        self.board = board.Board(eg.example_1)
        self.terminal_solver = solver.TerminalSolver(self.board)
        self.terminal_solver.terminal_solver()
        self.assertTrue(self.board.is_win())

    def test_sample_board_2(self):
        self.board = board.Board(eg.example_2)
        self.terminal_solver = solver.TerminalSolver(self.board)
        self.terminal_solver.terminal_solver()
        self.assertTrue(self.board.is_win())

    def test_sample_board_3(self):
        self.board = board.Board(eg.example_3)
        self.terminal_solver = solver.TerminalSolver(self.board)
        self.terminal_solver.terminal_solver()
        self.assertTrue(self.board.is_win())

    def test_sample_invalid_board(self):
        self.board = board.Board(eg.example_1)
        self.terminal_solver = solver.TerminalSolver(self.board)
        self.terminal_solver.terminal_solver()
        for row in range(9):
            for column in range(9):
                self.board.change_value((row, column), 999)
        self.assertFalse(self.board.is_win())


if __name__ == "__main__":
    unittest.main()
