"""CLI and GUI solvers for sudoku puzzles.

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

import copy
import time
from typing import List, Tuple


class GraphicSolver():
    """Solve a sudoku puzzle and display its solution using tkinter.

    The solution is performed in-place and the results are displayed
    in real-time on the tkinter graphic user interface.

    """
    def __init__(self, toolbar, puzzle) -> None:
        """Construct a solver object for graphic user interfaces.

        Parameters
        ----------
        toolbar : object of the Toolbar class
            Represent the commands that are called by the interface.
        puzzle : object of the Puzzle class
            Represent the sudoku board and its values.

        Attributes
        ----------
        previous_spaces : 2D list of tuples containing ints
            Hold the spaces that the solver has visited already.
        next_spaces : 2D list of tuples containing ints
            Hold the spaces that the solver needs to visit.
        next_value : int
            The value that follows the current space's value.
        current_coordinates : tuple of ints
            The space that the solver is currently visiting.

        """
        self.toolbar = toolbar
        self.puzzle = puzzle
        self.previous_spaces: List[List[Tuple[int]]] = []
        self.next_spaces = copy.deepcopy(self.puzzle.board.valid_spaces)
        # The spaces closest to (0,0) need to be at top of the stack.
        self.next_spaces.reverse()
        # This ensures the first is_valid_move check fails.
        self.next_value = 0
        self.current_coordinates = self.next_spaces.pop()
        self._set_speed()
        self._set_palette()
        self._map_coordinates_to_widgets()
        self._configure_preset_spaces()

    def __repr__(self) -> str:
        """Display the object in a convenient string representation.

        """
        return (
            "{self.__class__.__name__}"
            "({self.toolbar}, {self.puzzle})"
        ).format(self=self)

    def interface_solver(self) -> None:
        """Solve a sudoku puzzle and display it with a tkinter GUI.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        This function implements a depth-first search algorithm to
        solve the puzzle.

        The algorithm starts at the top-left of the board. It fills in
        the space with the first number that does not cause an error
        and then moves on to the next space filling spaces in the same
        manner. If an irresolvable error occurs, the algorithm backs
        up to a previous space and changes its value and then
        continues forward.

        To control the position in the board (i.e. what is the previous
        space and what is the next space), two stacks are used.

        The first stack holds all of the valid spaces (i.e. spaces that
        do not contain values at the start). They are in sequential
        order from right-to-left, top-to-bottom. The second stack holds
        all of the spaces that have been visited.

        When it is time to move to the next space, the current
        coordinates are appended to the `previous_spaces` stack. The
        coordinates of the next space are popped off the `next_spaces`
        stack and replace the current coordinates.

        """
        while True:
            if self.toolbar.stop_indicator:
                break
            is_valid_move = self.puzzle.board.is_valid_move(
                self.current_coordinates,
                self.next_value
            )
            if is_valid_move:
                self.puzzle.board.change_value(
                    self.current_coordinates,
                    self.next_value,
                )
                self._config_success()
                # If the win check happens any later, there will be an
                # index error. `next_spaces` is empty if board solved.
                if self.puzzle.board.is_win():
                    break
                # Move to the next position.
                self.previous_spaces.append(self.current_coordinates)
                self.current_coordinates = self.next_spaces.pop()
                self.next_value = 0
                time.sleep(self.delay)
            elif not is_valid_move and self.next_value < 9:
                self.next_value += 1
            elif not is_valid_move and self.next_value >= 9:
                # Explore a different branch of the search.
                self.puzzle.board.change_value(self.current_coordinates, 0)
                self._config_fail()
                self.next_spaces.append(self.current_coordinates)
                self.current_coordinates = self.previous_spaces.pop()
                # Check subsequent numbers (e.g. if previous number was
                # a four, start checking at five).
                self.next_value = (
                    self.puzzle.board.get_value(self.current_coordinates) + 1
                )
                time.sleep(self.delay)

    def _config_fail(self) -> None:
        current_widget = self.mapping[self.current_coordinates]
        current_widget.config(highlightbackground=self.palette["fail"])
        current_widget.delete("0", "end")
        current_widget.insert("0", "")
        self.toolbar.parent.update()

    def _configure_preset_spaces(self) -> None:
        for row in range(9):
            for column in range(9):
                if self.puzzle.entry_widgets[row][column].get().isdecimal():
                    self.puzzle.entry_widgets[row][column].config(
                        highlightbackground=self.palette["success"],
                    )

    def _config_success(self) -> None:
        current_widget = self.mapping[self.current_coordinates]
        current_widget.config(highlightbackground=self.palette["success"])
        current_widget.delete("0", "end")
        current_widget.insert("0", self.next_value)
        self.toolbar.parent.update()

    def _map_coordinates_to_widgets(self) -> None:
        self.mapping = {}
        for row in range(9):
            for column in range(9):
                self.mapping[
                    self.puzzle.board.all_coordinates[row][column]
                ] = self.puzzle.entry_widgets[row][column]

    def _set_palette(self) -> None:
        colors = self.toolbar.colorblind_check.get()
        if colors == "True":
            # Contrasting blue and red.
            self.palette = {
                "success": "#0000B8",
                "fail": "#FF7070",
            }
        elif colors == "False":
            # Green and red.
            self.palette = {
                "success": "#00B300",
                "fail": "#B30048",
            }

    def _set_speed(self) -> None:
        speed = self.toolbar.speed_radio.get()
        if speed == "slow":
            self.delay = 0.01
        elif speed == "medium":
            self.delay = 0.001
        elif speed == "fast":
            self.delay = 0.0001
        elif speed == "instant":
            self.delay = 0


class TerminalSolver():
    """Solve a sudoku puzzle and display it to the terminal.

    The solution is performed in-place.

    """
    def __init__(self, board) -> None:
        """Construct a solver object for command line interfaces.

        Parameters
        ----------
        board : object of the Board class
            Represent the sudoku board and its values.

        Attributes
        ----------
        previous_spaces : 2D list of tuples containing ints
            Hold the spaces that the solver has visited already.
        next_spaces : 2D list of tuples containing ints
            Hold the spaces that the solver needs to visit.
        next_value : int
            The value that follows the current space's value.
        current_coordinates : tuple of ints
            The space that the solver is currently visiting.

        """
        self.board = board
        self.previous_spaces: List[List[Tuple[int]]] = []
        self.next_spaces = copy.deepcopy(self.board.valid_spaces)
        # The top-most spaces need to be at the top of the stack.
        self.next_spaces.reverse()
        self.current_coordinates = self.next_spaces.pop()
        # This ensures the first is_valid_move check fails.
        self.next_value = 0

    def __repr__(self) -> str:
        """Display the object in a convenient string representation.

        """
        return "{self.__class__.__name__}({self.board})".format(self=self)

    def terminal_solver(self) -> None:
        """Solve a sudoku grid and display its results in the terminal.

        The grid is solved in-place.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        This function implements a depth-first search algorithm to solve
        the puzzle.

        The algorithm starts at the top-left of the board. It fills in the
        space with the first number that does not cause an error and then
        moves on to the next space filling spaces in the same manner. If
        an irresolvable error occurs, the algorithm backs up to a previous
        space and changes its value and then continues forward.

        To control the position in the board (i.e. what is the previous
        space and what is the next space), two stacks are used.

        The first stack holds all of the valid spaces (i.e. spaces that
        do not contain values at the start). They are in sequential order
        from right-to-left, top-to-bottom. The second stack holds all of
        the spaces that have been visited.

        When it is time to move to the next space, the current coordinates
        are appended to the `previous_spaces` stack. The coordinates of
        the next space are popped off the `next_spaces` stack and replace
        the current coordinates.

        """
        while True:
            is_valid_move = self.board.is_valid_move(
                self.current_coordinates,
                self.next_value
            )
            if is_valid_move:
                self.board.change_value(
                    self.current_coordinates,
                    self.next_value
                )
                # If the win check happens any later, there will be an
                # index error. `next_spaces` is empty if board complete.
                if self.board.is_win():
                    break
                # Move to the next position.
                self.previous_spaces.append(self.current_coordinates)
                self.current_coordinates = self.next_spaces.pop()
                self.next_value = 0
            elif not is_valid_move and self.next_value < 9:
                self.next_value += 1
            elif not is_valid_move and self.next_value >= 9:
                # Move backward resetting the values to be empty.
                self.board.change_value(self.current_coordinates, 0)
                self.next_spaces.append(self.current_coordinates)
                self.current_coordinates = self.previous_spaces.pop()
                # Check subsequent numbers (e.g. if previous number was a
                # four, start checking at five).
                self.next_value = (
                    self.board.get_value(self.current_coordinates) + 1
                )
