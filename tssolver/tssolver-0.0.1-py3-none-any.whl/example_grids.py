"""Various sudoku grid configurations and their respective solutions.

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
blank_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

blank_grid_solution = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 1, 4, 3, 6, 5, 8, 9, 7],
    [3, 6, 5, 8, 9, 7, 2, 1, 4],
    [8, 9, 7, 2, 1, 4, 3, 6, 5],
    [5, 3, 1, 6, 4, 2, 9, 7, 8],
    [6, 4, 2, 9, 7, 8, 5, 3, 1],
    [9, 7, 8, 5, 3, 1, 6, 4, 2],
]

example_1 = [
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

example_1_solution = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]

example_2 = [
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

example_2_solution = [
    [1, 7, 5, 3, 8, 2, 4, 9, 6],
    [8, 2, 9, 4, 5, 6, 3, 7, 1],
    [6, 4, 3, 9, 7, 1, 5, 8, 2],
    [2, 3, 4, 8, 9, 7, 6, 1, 5],
    [5, 9, 1, 6, 3, 4, 7, 2, 8],
    [7, 6, 8, 2, 1, 5, 9, 4, 3],
    [3, 5, 7, 1, 4, 8, 2, 6, 9],
    [4, 8, 6, 5, 2, 9, 1, 3, 7],
    [9, 1, 2, 7, 6, 3, 8, 5, 4],
]

example_3 = [
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

example_3_solution = [
    [7, 6, 2, 9, 1, 4, 3, 5, 8],
    [3, 4, 9, 7, 8, 5, 1, 6, 2],
    [5, 1, 8, 2, 6, 3, 9, 7, 4],
    [4, 9, 7, 6, 5, 1, 8, 2, 3],
    [6, 3, 1, 8, 9, 2, 7, 4, 5],
    [2, 8, 5, 3, 4, 7, 6, 9, 1],
    [8, 7, 4, 1, 2, 9, 5, 3, 6],
    [9, 2, 6, 5, 3, 8, 4, 1, 7],
    [1, 5, 3, 4, 7, 6, 2, 8, 9],
]
