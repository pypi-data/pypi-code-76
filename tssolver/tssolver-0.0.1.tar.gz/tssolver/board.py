"""Set up a sudoku board and query and set its values.

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
from typing import List, Tuple


class Board():
    """Represent a sudoku board.

    Notes
    -----
    The board is represented as a 2D grid. The available methods allow
    for changing values and checking valid arrangements of values.

    """
    def __init__(self, grid: List[List[int]]) -> None:
        """Construct a sudoku board.

        Parameters
        ----------
        grid : list of ints
            A 2D list containing the entries in the puzzle.

        Returns
        -------
        None

        """
        self.grid = copy.deepcopy(grid)
        self._valid_entity = [i for i in range(1, 10)]
        self._set_sections()
        self._set_all_coordinates()
        self._set_all_sections()
        self._set_valid_spaces()

    def __repr__(self):
        """Represent the object as a convenient string.

        This string can be used to recreate the object.

        Parameters
        ----------
        None

        Returns
        -------
        str
            A string that represents the object.

        """
        return "{self.__class__.__name__}({self.grid})".format(self=self)

    def change_value(
        self,
        coordinates: Tuple[int, int],
        new_value: int
    ) -> None:
        """Change the value at the given coordinates to a new value.

        Parameters
        ----------
        coordinates : tuple of two ints
            The coordinates of the value to be changed.
        new_value : int
            A value between 1 and 9 to replace the current value.

        Returns
        -------
        None

        """
        self.grid[coordinates[0]][coordinates[1]] = new_value

    def get_value(self, coordinates: Tuple[int, int]) -> int:
        """Retrieve the value at the given coordinates.

        Parameters
        ----------
        coordinates : tuple of two ints
            The coordinates of the value to be retrieved.

        Returns
        -------
        int
            A value between 1 and 9.

        """
        return self.grid[coordinates[0]][coordinates[1]]

    def is_valid_move(
        self,
        coordinates: Tuple[int, int],
        new_value: int
    ) -> bool:
        """Determine if the move being made would result in an error.

        Parameters
        ----------
        coordinates : tuple of two ints
            The coordinates of the value that is being considered.
        new_value : int
            The value that would replace the current value.

        Returns
        -------
        bool
            True if move is OK, False if move causes error.

        Notes
        -----
        A valid move in classic sudoku follows four rules:

            1. The value being added is between 1 and 9.
            2. The current row does not already contain this value.
            3. The current column does not already contain this value.
            4. The current section does not already contain this value.

        """
        row = coordinates[0]
        column = coordinates[1]
        section = self._map_to_section(coordinates)
        # Only numbers between 1 and 9 are allowed.
        if not self._is_valid_value(new_value):
            return False
        # Place the new value in this spot so that it can be checked.
        # Keep the old value around for when the check is done.
        old_value = self.grid[row][column]
        self.grid[row][column] = new_value
        row_items = self._get_row(row)
        # Make sure there are no duplicates in this row.
        row_items = [item for item in row_items if item != 0]
        if len(set(row_items)) != len(row_items):
            self.grid[row][column] = old_value
            return False
        column_items = self._get_column(column)
        # Make sure there are no duplicates in this column.
        column_items = [item for item in column_items if item != 0]
        if len(set(column_items)) != len(column_items):
            self.grid[row][column] = old_value
            return False
        section_items = self._get_section(section)
        # Make sure there are no duplicates in this section.
        section_items = [item for item in section_items if item != 0]
        if len(set(section_items)) != len(section_items):
            self.grid[row][column] = old_value
            return False
        self.grid[row][column] = old_value
        return True

    def is_win(self) -> bool:
        """Check the board for a win scenario.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True if the board is in a winning state, False if not.

        Notes
        -----
        A winning sudoku board will have a value in every space where
        any given value is between 1 and 9 and is unique to that
        value's row, column, and section.

        """
        for row in range(0, 9):
            row_items = self._get_row(row).copy()
            row_items.sort()
            if row_items != self._valid_entity:
                return False
            for column in range(0, 9):
                column_items = self._get_column(column).copy()
                column_items.sort()
                if column_items != self._valid_entity:
                    return False
                current_section = self._map_to_section((row, column))
                section_items = self._get_section(current_section).copy()
                section_items.sort()
                if section_items != self._valid_entity:
                    return False
        return True

    def print_board(self) -> None:
        """Print the sudoku board to terminal in a grid-like format.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        for row in range(0, 9):
            for column in range(0, 9):
                if column != 8:
                    print(self.grid[row][column], end=" ")
                elif column == 8:
                    print(self.grid[row][column], end="\n")

    def _get_column(self, column: int) -> List[int]:
        column_items = []
        for index, row in enumerate(self.grid):
            for index, item in enumerate(row):
                if index == column:
                    column_items.append(item)
        return column_items

    def _get_row(self, row: int) -> List[int]:
        return self.grid[row]

    def _get_section(self, section: int) -> List[int]:
        section_items = []
        section_coordinates = getattr(self, "section_" + str(section))
        # Each section contains 9 spaces.
        for coordinates in range(0, 9):
            grid_row = section_coordinates[coordinates][0]
            grid_column = section_coordinates[coordinates][1]
            section_items.append(self.grid[grid_row][grid_column])
        return section_items

    def _is_valid_value(self, value: int) -> bool:
        if value not in self._valid_entity:
            return False
        else:
            return True

    def _map_to_section(self, coordinates: Tuple[int, int]) -> int:
        for section in range(0, 9):
            if coordinates in self.all_sections[section]:
                break
        return section

    def _set_all_coordinates(self) -> None:
        self.all_coordinates = []
        for row in range(9):
            all_coordinates_row = []
            for column in range(9):
                all_coordinates_row.append((row, column))
            self.all_coordinates.append(all_coordinates_row)

    def _set_all_sections(self) -> None:
        self.all_sections = []
        for section in range(9):
            self.all_sections.append(getattr(self, "section_" + str(section)))

    def _set_sections(self) -> None:
        """Create attributes for each section of the board.

        Notes
        -----
        The board is layed-out in a 9x9 grid. Each section is a 3x3
        grid within the main grid. The sections are layed-out like so:

            0 1 2
            3 4 5
            6 7 8

        The attribute for any given section holds the coordinates that
        that section contains. The attributes are created
        programatically, therefore, type checker is disabled for lines
        that reference these attributes.

        """
        for section in range(9):
            setattr(self, "section_" + str(section), [])
        for row in range(9):
            for column in range(9):
                # See the docstring for why type checking is disabled.
                if row in [0, 1, 2] and column in [0, 1, 2]:
                    self.section_0.append((row, column))  # type: ignore
                elif row in [0, 1, 2] and column in [3, 4, 5]:
                    self.section_1.append((row, column))  # type: ignore
                elif row in [0, 1, 2] and column in [6, 7, 8]:
                    self.section_2.append((row, column))  # type: ignore
                elif row in [3, 4, 5] and column in [0, 1, 2]:
                    self.section_3.append((row, column))  # type: ignore
                elif row in [3, 4, 5] and column in [3, 4, 5]:
                    self.section_4.append((row, column))  # type: ignore
                elif row in [3, 4, 5] and column in [6, 7, 8]:
                    self.section_5.append((row, column))  # type: ignore
                elif row in [6, 7, 8] and column in [0, 1, 2]:
                    self.section_6.append((row, column))  # type: ignore
                elif row in [6, 7, 8] and column in [3, 4, 5]:
                    self.section_7.append((row, column))  # type: ignore
                elif row in [6, 7, 8] and column in [6, 7, 8]:
                    self.section_8.append((row, column))  # type: ignore

    def _set_valid_spaces(self) -> None:
        """Define which spaces the solver is allowed to change.

        When the user enters values into the board, those values are
        considered static - the solver cannot change them.

        """
        valid_spaces = []
        for row in range(0, 9):
            for column in range(0, 9):
                if self.grid[row][column] == 0:
                    valid_spaces.append((row, column))
        setattr(self, "valid_spaces", valid_spaces)
