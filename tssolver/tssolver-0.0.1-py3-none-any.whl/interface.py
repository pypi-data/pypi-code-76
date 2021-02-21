"""A tkinter graphic user interface for a sudoku puzzle solver.

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
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
from typing import Any, Dict, List

from tssolver import board
from tssolver import example_grids as eg
from tssolver import solver


class Dialog():
    """A basic dialog window template for delivering information.

    This class is meant to act as a template and other classes should
    inherit from it to create specific dialog windows.

    """
    def __init__(
        self,
        parent: ttk.Frame,
        textbox_options: Dict[str, Any],
    ) -> None:
        """Contruct a blank dialog window.

        Parameters
        ----------
        parent : ttk.Frame object
            Represent the frame to which the dialog window belongs.
        textbox_options : dict of str mapped to int or str
            The style configurations for the textbox in the window.

        Returns
        -------
        None

        """
        self.parent = parent
        self.dialog = tk.Toplevel(self.parent)
        self.textbox_options = textbox_options
        self.dialog.resizable(False, False)
        self.mainframe = ttk.Frame(self.dialog)
        self.textbox = tk.Text(self.mainframe, textbox_options)
        self.textbox.tag_configure(
            "all_text",
            justify="center",
        )
        self.textbox.tag_configure(
            "heading",
            font=("TkTextFont", 15),
            underline=True,
        )
        self.mainframe.grid(row=0, column=0, sticky="nsew")
        self.textbox.grid(row=0, column=0, sticky="nsew")

    def __repr__(self) -> str:
        """Represent the object as a convenient string.

        Parameters
        ----------
        None

        Returns
        -------
        str
            A string representation of the object.

        """
        return (
            "{self.__class__.__name__}"
            "({self.parent}"
            "{self.textbox_options})"
        ).format(self=self)

    def center_window(self) -> None:
        """Make sure the dialog window opens up centered on its parent.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        # Without update, the dimensions are reported incorrectly.
        self.dialog.update()
        dialog_width = self.dialog.winfo_reqwidth()
        dialog_height = self.dialog.winfo_reqheight()
        dialog_x = (
            str(int(parent_x + (parent_width / 2) - (dialog_width / 2)))
        )
        dialog_y = (
            str(int(parent_y + (parent_height / 2) - (dialog_height / 1.7)))
        )
        self.dialog.geometry("+{}+{}".format(dialog_x, dialog_y))


class AboutDialog(Dialog):
    """A dialog window describing the program.

    This class inherits from the Dialog template class and then
    customizes it.

    """
    def __init__(
        self,
        parent: ttk.Frame,
        textbox_options: Dict[str, Any],
    ) -> None:
        """Contruct an about dialog window.

        Parameters
        ----------
        parent : ttk.Frame object
            Represent the frame to which the dialog window belongs.
        textbox_options : dict of str mapped to int or str
            The style configurations for the textbox in the window.

        Returns
        -------
        None

        """
        # Let the parent class handle the basic configuration.
        super().__init__(parent, textbox_options)
        self.dialog.title("About")
        self._add_content()
        self._configure_content()
        self.center_window()

    def __repr__(self) -> str:
        """Represent the object as a convenient string.

        Parameters
        ----------
        None

        Returns
        -------
        str
            A string representation of the object.

        """
        return (
            "{self.__class__.__name__}"
            "({self.parent}"
            "{self.textbox_options})"
        ).format(self=self)

    def _add_content(self) -> None:
        self.textbox.config(state="normal")
        about_info = (
            "Sudoku Solver\n\n"
            "Solve sudoku puzzles using a depth-first\n"
            "search algorithm. Given a valid board, a\n"
            "solution will be found."
            "\n\n"
            "This program comes with absolutely no warranty."
            "\n\n"
            "This program is licensed under the GNU\n"
            "General Public License, version 3 or later.\n"
            "For the full license, please see:\n"
            "https://www.gnu.org/licenses/gpl-3.0.txt"
            "\n\n"
            "Copyright © 2021 emerac"
        )
        self.textbox.insert("end", about_info)
        self.textbox.config(state="disabled")

    def _configure_content(self) -> None:
        self.textbox.tag_add("all_text", "1.0", "end")
        self.textbox.tag_add("heading", "1.0", "1.end")


class HelpDialog(Dialog):
    """A dialog window describing how to use the program.

    This class inherits from the Dialog template class and then
    customizes it.

    """
    def __init__(
        self,
        parent: ttk.Frame,
        textbox_options: Dict[str, Any],
    ) -> None:
        """Contruct a help dialog window.

        Parameters
        ----------
        parent : ttk.Frame object
            Represent the frame to which the dialog window belongs.
        textbox_options : dict of str mapped to int or str
            The style configurations for the textbox in the window.

        Returns
        -------
        None

        """
        # Let the parent class handle the basic configuration.
        super().__init__(parent, textbox_options)
        self.dialog.title("Help")
        self._add_content()
        self._configure_content()
        self.center_window()

    def __repr__(self) -> str:
        """Represent the object as a convenient string.

        Parameters
        ----------
        None

        Returns
        -------
        str
            A string representation of the object.

        """
        return (
            "{self.__class__.__name__}"
            "({self.parent}"
            "{self.textbox_options})"
        ).format(self=self)

    def _add_content(self) -> None:
        self.textbox.config(state="normal")
        usage_info = (

            "Solving a puzzle"
            "\n\n"
            "Enter your puzzle into the grid on the main\n"
            "window, then choose 'Board -> Start Solving'\n"
            "in the toolbar. You can stop solving at anytime\n"
            "by choosing 'Stop Solving'."
            "\n\n"

            "Clearing the board"
            "\n\n"
            "To quickly clear the board, choose\n"
            "'Board -> Clear Board' in the toolbar."
            "\n\n"

            "Loading a sample puzzle"
            "\n\n"
            "Choose 'Board -> Sample Puzzles' in\n"
            "the toolbar and then choose a puzzle\n"
            "from one of the three options."
            "\n\n"

            "Configuring the solver"
            "\n\n"
            "The solver displays the solution in\n"
            "red and green. To use colorblind mode,\n"
            "choose 'Options -> Colorblind Mode'\n"
            "in the toolbar."
            "\n\n"
            "The solve speed can also be configured.\n"
            "Choose 'Options -> Solve Speed', in the\n"
            "toolbar and then choose from one of the\n"
            "four options available."
            "\n\n"

            "Quitting the program"
            "\n\n"
            "Choose 'File -> Quit' in the toolbar."
        )
        self.textbox.insert("end", usage_info)
        self.textbox.config(state="disabled")

    def _configure_content(self) -> None:
        self.textbox.tag_add("all_text", "1.0", "end")
        self.textbox.tag_add("heading", "1.0", "1.end")
        self.textbox.tag_add("heading", "8.0", "8.end")
        self.textbox.tag_add("heading", "13.0", "13.end")
        self.textbox.tag_add("heading", "19.0", "19.end")
        self.textbox.tag_add("heading", "31.0", "31.end")


class Puzzle():
    """Represent the grid of the sudoku puzzle.

    Notes
    -----
    The grid consists of 81 entry widgets inside a frame widget.

    """
    def __init__(self, parent: ttk.Frame) -> None:
        """Construct the grid for the interface.

        Parameters
        ----------
        parent : ttk.Frame object
            The frame object to which this widget belongs.

        Returns
        -------
        None

        """
        self.parent = parent
        self.board = board.Board(eg.blank_grid)
        self.entry_widgets = []
        # View the docstring for self._is_valid for a full explanation
        # of how register and validatecommand interact.
        is_valid_wrapper = (
            self.parent.register(self._is_valid),
            "%d", "%s", "%S",
        )
        # Store the widgets in a 2D list so that their position in the
        # list parallels the value they correspond to in the grid.
        for row in range(9):
            entry_row = []
            for column in range(9):
                entry = tk.Entry(
                    parent,
                    width=2,
                    font=("TkFixedFont 22"),
                    justify="center",
                    # Validatecommand will be called when entry edited.
                    validate="key",
                    validatecommand=is_valid_wrapper,
                    highlightthickness=2,
                    # Have the editing color match the border color.
                    highlightcolor="#D9D9D9",
                )
                entry.grid(row=row, column=column, sticky="nsew")
                entry_row.append(entry)
            self.entry_widgets.append(entry_row)
        self.display_board()

    def __repr__(self) -> str:
        """Represent the object as a convenient string.

        Parameters
        ----------
        None

        Returns
        -------
        str
            A string representation of the object.

        """
        return "{self.__class__.__name__}({self.parent})".format(self=self)

    def display_board(self) -> None:
        """Display the current values of the grid to the interface.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        for row in range(9):
            for column in range(9):
                self.entry_widgets[row][column].delete(
                    0,
                    "end",
                )
                # Solving changes the color, so restore it to normal.
                self.entry_widgets[row][column].configure(
                    highlightbackground="#D9D9D9",
                )
                if self.board.grid[row][column] != 0:
                    self.entry_widgets[row][column].insert(
                        0,
                        self.board.grid[row][column],
                    )
                elif self.board.grid[row][column] == 0:
                    pass

    def read_board(self) -> List[List[int]]:
        """Get the values of the board from the interface.

        Parameters
        ----------
        None

        Returns
        -------
        new_grid : list of list containing int
            A 2D list that represents the values from the interface.

        """
        new_grid = []
        for row in range(9):
            new_grid_row = []
            for column in range(9):
                entry_value = self.entry_widgets[row][column].get()
                if entry_value.isdecimal():
                    new_grid_row.append(int(entry_value))
                elif entry_value == "":
                    new_grid_row.append(0)
            new_grid.append(new_grid_row)
        return new_grid

    def _is_valid(self, action, prior_text, alter_text):
        """Determine if entry widget event is acceptable.

        Parameters
        ----------
        action : str
            Type of entry widget action. '1' if insert, '0' if delete.
        prior_text : str
            The value of the entry prior to editing.
        alter_text : str
            The string that is being inserted or deleted.

        Returns
        -------
        bool
            True if action is OK, False if not.

        Notes
        -----
        Validatecommand expects a reference to a function. When it is
        triggered, it can send information about the widget (e.g.
        what is being entered, what type of action is being
        performed, etc.) in place of percent substitutions.

        Register creates a string representation of the callable
        (function reference) along with the percent values, which
        are then passed to validatecommand. In this case, _is_valid
        is the function being referenced.

        Validatecommand substitutes the special info for the percents
        and then they get sent to the function that is called.

        The register method basically acts as a proxy.[1]

        %d - Type of action
        %s - Value of entry prior to editing
        %S - String being inserted/deleted

        There are quite a few more values available, too.[2]

        Reference
        ---------
        [1] https://stackoverflow.com/a/55231273
        [2] https://www.tcl.tk/man/tcl8.6/TkCmd/entry.htm

        """
        if (
            action == "1"
            and len(prior_text) == 0
            and alter_text.isdecimal()
        ):
            return True
        elif action == "0" and len(prior_text) == 1:
            return True
        else:
            return False


class Toolbar():
    """A toolbar menu that enables sudoku board functionality.

    """
    def __init__(self, parent: ttk.Frame, puzzle: Puzzle) -> None:
        """Construct a toolbar menu.

        Parameters
        ----------
        parent : ttk.Frame object
            The widget to which this widget belongs.
        puzzle : Puzzle object
            The sudoku board that is part of the interface.

        """
        self.colorblind_check = tk.StringVar()
        self.colorblind_check.set("False")
        self.options = {
            "background": "#F2F2F2",
            "relief": "flat",
            "borderwidth": 3,
            "activeborderwidth": 0,
        }
        self.parent = parent
        # Removes the perforated look from the cascade menus.
        self.parent.option_add("*tearOff", "false")
        self.puzzle = puzzle
        self.speed_radio = tk.StringVar()
        self.speed_radio.set("fast")
        self.stop_indicator = False
        # These methods must be called in this order.
        self._setup_mainbar_menu()
        self._setup_file_menu()
        self._setup_board_menu()
        self._setup_samples_submenu()
        self._setup_options_menu()
        self._setup_solve_speed_submenu()
        self._setup_help_menu()

    def __repr__(self) -> str:
        """Represent the object as a convenient string.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        return (
            "{self.__class__.__name__}"
            "({self.parent}, {self.puzzle})"
        ).format(self=self)

    def _display_new_board(self, choice: int) -> None:
        if choice == 0:
            self.puzzle.board.grid = eg.blank_grid
            self.puzzle.display_board()
        elif choice == 1:
            self.puzzle.board.grid = eg.example_1
            self.puzzle.display_board()
        elif choice == 2:
            self.puzzle.board.grid = eg.example_2
            self.puzzle.display_board()
        elif choice == 3:
            self.puzzle.board.grid = eg.example_3
            self.puzzle.display_board()

    def _launch_dialog(
        self,
        parent_frame: ttk.Frame,
        dialog_type: str
    ) -> None:
        if dialog_type == "help":
            options = {
                "width": 40,
                "height": 36,
                "background": "#F2F2F2",
                "borderwidth": 0,
                "relief": "flat",
                "font": "TkTextFont",
                "padx": 10,
                "pady": 10,
            }
            self.help_dialog = HelpDialog(parent_frame, options)
        elif dialog_type == "about":
            options = {
                "width": 41,
                "height": 15,
                "background": "#F2F2F2",
                "borderwidth": 0,
                "relief": "flat",
                "font": "TkTextFont",
                "padx": 10,
                "pady": 10,
            }
            self.about_dialog = AboutDialog(parent_frame, options)

    def _setup_mainbar_menu(self) -> None:
        self.mainbar = tk.Menu(
            self.parent,
            self.options,
            borderwidth=0,
        )

    def _reset_stop_indicator(self) -> None:
        self.stop_indicator = False

    def _setup_board_menu(self) -> None:
        self.board_menu = tk.Menu(
            self.mainbar,
            self.options,
        )
        self.mainbar.add_cascade(
            menu=self.board_menu,
            label="Board",
        )
        self.board_menu.add_command(
            label="Start Solving",
            command=lambda: self._solve_puzzle(),
        )
        self.board_menu.add_command(
            label="Stop Solving",
            command=lambda: self._stop_solving(),
        )
        self.board_menu.add_separator()
        self.board_menu.add_command(
            label="Clear Board",
            command=lambda: self._display_new_board(0),
        )
        self.board_menu.add_separator()

    def _setup_file_menu(self) -> None:
        self.file_menu = tk.Menu(
            self.mainbar,
            self.options,
        )
        self.mainbar.add_cascade(
            menu=self.file_menu,
            label="File",
        )
        self.file_menu.add_command(
            label="Quit",
            command=self.parent.quit,
        )

    def _setup_help_menu(self) -> None:
        self.help_menu = tk.Menu(
            self.mainbar,
            self.options,
        )
        self.mainbar.add_cascade(
            menu=self.help_menu,
            label="Help",
        )
        self.help_menu.add_command(
            label="Help...",
            command=lambda: self._launch_dialog(self.parent, "help"),
        )
        self.help_menu.add_separator()
        self.help_menu.add_command(
            label="About",
            command=lambda: self._launch_dialog(self.parent, "about"),
        )

    def _setup_options_menu(self) -> None:
        self.options_menu = tk.Menu(
            self.mainbar,
            self.options,
        )
        self.mainbar.add_cascade(
            menu=self.options_menu,
            label="Options",
        )
        self.options_menu.add_checkbutton(
            label="Colorblind Mode",
            variable=self.colorblind_check,
            onvalue="True",
            offvalue="False",
        )
        self.options_menu.add_separator()

    def _setup_samples_submenu(self) -> None:
        self.samples_menu = tk.Menu(
            self.board_menu,
            self.options,
        )
        self.board_menu.add_cascade(
            menu=self.samples_menu,
            label="Sample Puzzles",
        )
        self.samples_menu.add_command(
            label="Puzzle 1",
            command=lambda: self._display_new_board(1),
        )
        self.samples_menu.add_command(
            label="Puzzle 2",
            command=lambda: self._display_new_board(2),
        )
        self.samples_menu.add_command(
            label="Puzzle 3",
            command=lambda: self._display_new_board(3),
        )

    def _setup_solve_speed_submenu(self) -> None:
        self.solve_speed = tk.Menu(
            self.options_menu,
            self.options,
        )
        self.options_menu.add_cascade(
            menu=self.solve_speed,
            label="Solve Speed",
        )
        self.solve_speed.add_radiobutton(
            label="Slow",
            variable=self.speed_radio,
            value="slow",
        )
        self.solve_speed.add_radiobutton(
            label="Medium",
            variable=self.speed_radio,
            value="medium",
        )
        self.solve_speed.add_radiobutton(
            label="Fast",
            variable=self.speed_radio,
            value="fast",
        )
        self.solve_speed.add_radiobutton(
            label="Instant",
            variable=self.speed_radio,
            value="instant",
        )

    def _solve_puzzle(self) -> None:
        """Get the values from the interface and solve the puzzle.

        Raises
        ------
        IndexError
            If the solver cannot find a solution.

        Notes
        -----
        The solver works by moving from space to space, keeping stacks
        of the previous spaces and the next spaces. When it encounters
        an error, it backs up to a previous space and retries.

        If there are no more previous spaces, the solver will try to
        pop from an empty stack, causing an index error. This means
        that the solver was unable to find a solution.

        """
        grid = self.puzzle.read_board()
        # Creating a new object 'refreshes' the valid_spaces attribute.
        self.puzzle.board = board.Board(grid)
        try:
            puzzle_solver = solver.GraphicSolver(self, self.puzzle)
            puzzle_solver.interface_solver()
        except IndexError:
            messagebox.showinfo(
                icon="warning",
                message="No solution found.",
                detail=(
                    "The values entered do not represent a\n"
                    "valid sudoku board.\n\n"
                    "Please check the values and retry."
                )
            )

    def _stop_solving(self) -> None:
        """Change the value of the stop indicator.

        Notes
        -----
        The solver periodically checks this value to determine if it
        should discontinue solving.

        The value of the indicator needs to be reset for the next run.
        However, it cannot be reset immediately because the solver
        needs a chance to notice that the value changed.

        """
        self.stop_indicator = True
        self.parent.after(3000, self._reset_stop_indicator)


class MainApplication():
    """A sudoku solver application built using tkinter.

    This class acts as a 'controller' for the other parts of the
    application.

    """
    def __init__(self, parent: tk.Tk) -> None:
        """Construct the main application window and its widgets.

        Parameters
        ----------
        parent : tk.Tk object
            A top-level window containing all application widgets.

        Returns
        -------
        None

        """
        self.parent = parent
        self.mainframe = ttk.Frame(self.parent, padding=2)
        self.puzzle = Puzzle(self.mainframe)
        self.toolbar = Toolbar(self.mainframe, self.puzzle)

        self.parent.title("Sudoku Solver")
        self.parent.resizable(False, False)
        self.parent.config(menu=self.toolbar.mainbar)
        self.parent.geometry("+400+100")

        self.mainframe.grid(row=0, column=0)

    def __repr__(self) -> str:
        """Display the object in a convenient string representation.

        """
        return "{self.__class__.__name__}({self.parent})".format(self=self)


def main():
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
