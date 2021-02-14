# Display card output and retreive input
# Armaan Bhojwani 2021

import curses
import curses.panel
import os
from random import shuffle
import sys
import textwrap
import time

from . import runner, progress, parse


def panel_create(x, y):
    """Create popup panels to a certain scale"""
    win = curses.newwin(x, y)
    panel = curses.panel.new_panel(win)
    win.erase()
    return (win, panel)


class Quit:
    def __init__(self, outer, mlines=5, mcols=20):
        self.outer = outer
        (self.win, self.panel) = panel_create(mlines, mcols)
        self.panel.top()
        self.panel.hide()

        self.win.addstr(
            1,
            2,
            "QUIT LIGHTCARDS?",
            curses.color_pair(1) + curses.A_BOLD,
        )
        self.win.hline(2, 1, curses.ACS_HLINE, mcols)
        self.win.addstr(3, 1, "Quit? [y/n]")

        self.win.box()

    def disp(self):
        """Display quit confirmation screen"""
        (mlines, mcols) = self.outer.win.getmaxyx()
        self.win.mvwin(int(mlines / 2) - 3, int(mcols / 2) - 10)
        self.panel.show()
        if self.outer.config["quit_confirmation"]:
            while True:
                key = self.win.getkey()
                if key == "y":
                    break
                elif key == "n":
                    self.panel.hide()
                    self.outer.get_key()


class Panel:
    def __init__(self, outer, mlines, mcols):
        self.outer = outer
        (self.win, self.panel) = panel_create(mlines, mcols)
        self.panel.top()
        self.panel.hide()

    def config_get(self, setting, cut=28):
        return str(list(self.outer.config[setting][:cut])).replace("'", "")


class Help(Panel):
    def __init__(self, outer, mlines=23, mcols=52):
        """Initialize help screen"""
        super().__init__(outer, mlines, mcols)
        c = self.config_get

        text = [
            "Welcome to Lightcards. Here are some keybindings",
            "to get you started:",
            "",
            f"{c('card_prev')}: previous card",
            f"{c('card_next')}: next card",
            f"{c('card_flip')}: flip card",
            f"{c('card_star')}: star card",
            f"{c('card_first')}: go to first card",
            f"{c('card_last')}: go to last card",
            f"{c('help_disp')}: open this help menu",
            f"{c('menu_disp')}: open the control menu",
            f"{c('view_one')}: switch to view one",
            f"{c('view_two')}: switch to view two",
            f"{c('view_three')}: switch to view three",
            f"{c('quit_key')}: quit",
            "",
            "More information can be found in the man page, or",
            "by running `lightcards --help`.",
            "",
            f"Press {c('help_disp')} to go back.",
        ]

        self.win.addstr(
            1,
            int(mcols / 2) - 8,
            "LIGHTCARDS HELP",
            curses.color_pair(1) + curses.A_BOLD,
        )
        self.win.hline(2, 1, curses.ACS_HLINE, mcols)

        for i, content in enumerate(text, 3):
            self.win.addstr(i, 1, content)

        self.win.box()

    def disp(self):
        """Display help screen"""
        (mlines, mcols) = self.outer.win.getmaxyx()
        self.win.mvwin(int(mlines / 2) - 12, int(mcols / 2) - 25)
        self.panel.show()

        while True:
            key = self.win.getkey()
            if key in self.outer.config["quit_key"]:
                self.outer.leave()
            elif key in self.outer.config["help_disp"]:
                self.panel.hide()
                self.outer.get_key()


class Menu(Panel):
    def __init__(self, outer, mlines=17, mcols=44):
        """Initialize the menu with content"""
        super().__init__(outer, mlines, mcols)
        c = self.config_get

        self.win.addstr(
            1,
            int(mcols / 2) - 8,
            "LIGHTCARDS MENU",
            curses.color_pair(1) + curses.A_BOLD,
        )
        self.win.hline(2, 1, curses.ACS_HLINE, mcols)
        env = os.environ.get("EDITOR", "$EDITOR")[:15]
        text = [
            f"{c('menu_reset')}: reset stack to original state",
            f"{c('menu_alphabetize')}: alphabetize stack",
            f"{c('menu_shuffle')}: shuffle stack",
            f"{c('menu_reverse')}: reverse stack order",
            f"{c('menu_unstar')}: unstar all",
            f"{c('menu_star')}: star all",
            f"{c('menu_stars_only')}: update stack to include starred only",
            f"{c('menu_open_file')}: open the input file in {env}",
            "",
            f"{c('menu_restart')}: restart",
            f"{c('menu_disp')}: close menu",
        ]

        for i, content in enumerate(text, 3):
            self.win.addstr(i, 1, content)

        self.win.box()

    def clear_msg(self):
        for i in range(42):
            self.win.addch(15, i + 1, " ")

    def menu_print(self, string, err=False):
        """Print messages on the menu screen"""
        if err:
            color = curses.color_pair(2)
        else:
            color = curses.color_pair(1)

        self.win.addstr(15, 1, string, color)
        self.menu_grab()

    def menu_grab(self):
        """Grab keypresses on the menu screen"""
        while True:
            key = self.win.getkey()
            if (
                key
                in self.outer.config["menu_disp"]
                + self.outer.config["menu_restart"]
            ):
                self.panel.hide()
                self.outer.get_key()
            elif key in self.outer.config["quit_key"]:
                self.outer.leave()
            elif key in self.outer.config["menu_reset"]:
                self.outer.stack = runner.get_orig()[1]
                self.menu_print("Stack reset!")
            elif key in self.outer.config["menu_alphabetize"]:
                self.outer.stack.sort(key=lambda x: x.front)
                self.menu_print("Stack alphabetized!")
            elif key in self.outer.config["menu_unstar"]:
                [x.unStar() for x in self.outer.stack]
                self.menu_print("All unstarred!")
            elif key in self.outer.config["menu_star"]:
                [x.star() for x in self.outer.stack]
                self.menu_print("All starred!")
            elif key in self.outer.config["menu_reverse"]:
                self.outer.stack.reverse()
                self.menu_print("Stack reversed!")
            elif key in self.outer.config["menu_shuffle"]:
                shuffle(self.outer.stack)
                self.menu_print("Stack shuffled!")
            elif key in self.outer.config["menu_open_file"]:
                curses.endwin()
                os.system(f"$EDITOR {self.outer.input_file}"),
                (self.outer.headers, self.outer.stack) = parse.parse_html(
                    parse.md2html(self.outer.input_file),
                    self.outer.args,
                    self.outer.config,
                )
                self.outer.get_key()
            elif key in self.outer.config["menu_stars_only"]:
                # Check if there are any starred cards before proceeding, and
                # if not, don't allow to proceed and show an error message
                cont = False
                for x in self.outer.stack:
                    if x.starred:
                        cont = True
                        break

                if cont:
                    self.outer.stack = [
                        x for x in self.outer.stack if x.starred
                    ]
                    self.menu_print("Stars only!")
                else:
                    self.menu_print("ERR: None are starred!", err=True)
            elif key in self.outer.config["menu_restart"]:
                self.outer.obj.index = 0
                self.outer.get_key()

    def disp(self):
        """
        Display a menu offering multiple options on how to manipulate the deck
        and to continue
        """
        self.clear_msg()

        (mlines, mcols) = self.outer.win.getmaxyx()
        self.win.mvwin(int(mlines / 2) - 8, int(mcols / 2) - 22)
        self.panel.show()

        self.menu_grab()


class Display:
    def __init__(self, stack, headers, obj, view, args, conf):
        self.stack = stack
        self.headers = headers
        self.obj = obj
        self.view = view
        self.input_file = args.inp
        self.config = conf
        self.args = args

    def run(self, stdscr):
        """Set important options that require stdscr before starting"""
        self.win = stdscr
        curses.curs_set(0)  # Hide cursor
        curses.use_default_colors()  # Allow transparency
        curses.init_pair(1, self.config["highlight_color"], -1)
        curses.init_pair(2, self.config["error_color"], -1)
        curses.init_pair(3, self.config["starred_color"], -1)

        self.main_panel = curses.panel.new_panel(self.win)
        self.menu_obj = Menu(self)
        self.help_obj = Help(self)
        self.quit_obj = Quit(self)

        self.get_key()

    def check_size(self):
        (mlines, mcols) = self.win.getmaxyx()

        while mlines < 24 or mcols < 60:
            self.win.clear()
            self.win.addstr(
                0,
                0,
                textwrap.fill(
                    "Terminal too small! Min size 60x24", width=mcols
                ),
            )
            self.win.refresh()
            (mlines, mcols) = self.win.getmaxyx()
            time.sleep(0.1)
        else:
            self.disp_card()

    def dump(self):
        if self.config["cache"]:
            progress.dump(self.stack, runner.get_orig()[1])

    def leave(self):
        """Pickle stack and confirm before quitting"""
        self.quit_obj.disp()
        if self.obj.index + 1 == len(self.stack):
            self.obj.index = 0

        self.dump()
        sys.exit(0)

    def nstarred(self):
        """Get total number of starred cards"""
        return [card for card in self.stack if card.starred]

    def prep_bar(self):
        # Calculate percent done
        if len(self.stack) <= 1:
            percent = "100"
        else:
            percent = str(
                round(self.obj.index / (len(self.stack) - 1) * 100)
            ).zfill(3)

        # Print yellow if starred
        if self.current_card().starred:
            self.star_color = curses.color_pair(3)
        else:
            self.star_color = curses.color_pair(1)

        # Compose bar text
        self.bar_start = "["
        self.bar_middle = self.current_card().printStar()
        self.bar_end = (
            f"] [{len(self.nstarred())}/{str(len(self.stack))} starred] "
        )
        if self.view != 3:
            self.bar_end += (
                f" [{self.get_side()} ("
                f"{str(int(self.current_card().side) + 1)})]"
            )
        self.bar_end += f" [View {str(self.view)}]"

        self.progress = (
            f"[{percent}% ("
            f"{str(self.obj.index + 1).zfill(len(str(len(self.stack))))}"
            f"/{str(len(self.stack))})] "
        )

    def disp_bar(self):
        """
        Display the statusbar at the bottom of the screen with progress, star
        status, and card side.
        """
        # Put it all togethor
        (mlines, mcols) = self.win.getmaxyx()
        height = mlines - 2
        self.win.addstr(height, 0, self.bar_start, curses.color_pair(1))
        self.win.addstr(
            height, len(self.bar_start), self.bar_middle, self.star_color
        )
        self.win.addstr(
            height,
            len(self.bar_start + self.bar_middle),
            textwrap.shorten(self.bar_end, width=mcols - 20, placeholder="…"),
            curses.color_pair(1),
        )

        self.win.addstr(
            height + 1,
            0,
            self.progress,
            curses.color_pair(1),
        )

        for i in range(
            int(
                self.obj.index
                / (len(self.stack) - 1)
                * (mcols - len(self.progress))
                - 1
            )
        ):
            self.win.addch(
                height + 1,
                i + len(self.progress),
                self.config["progress_char"],
                curses.color_pair(1),
            )

        self.win.hline(mlines - 3, 0, 0, mcols)

    def wrap_width(self):
        """Calculate the width at which the body text should wrap"""
        (_, mcols) = self.win.getmaxyx()
        wrap_width = mcols - 20
        if wrap_width > 80:
            wrap_width = 80
        return wrap_width

    def get_side(self):
        if self.obj.side == 0:
            return self.headers[self.current_card().side]
        else:
            return self.headers[self.current_card().get_reverse()]

    def disp_card(self):
        (_, mcols) = self.win.getmaxyx()
        self.main_panel.bottom()
        self.prep_bar()
        num_done = str(self.obj.index + 1).zfill(len(str(len(self.stack))))

        if self.view in [1, 2, 4]:
            """
            Display the contents of the card.
            Shows a header, a horizontal line, and the contents of the current
            side.
            """
            # If on the back of the card, show the content of the front side in
            # the header
            if self.view == 1:
                self.obj.side = 0
            elif self.view == 2:
                self.obj.side = 1

            if self.current_card().side == 0:
                top = num_done + " | " + self.get_side()
            else:
                top = (
                    num_done
                    + " | "
                    + self.get_side()
                    + ' | "'
                    + str(self.current_card().get()[self.obj.get_reverse()])
                    + '"'
                )

            self.win.clear()
            self.win.addstr(
                0,
                0,
                textwrap.shorten(top, width=mcols - 20, placeholder="…"),
                curses.A_BOLD,
            )

            # Show current side
            self.win.addstr(
                2,
                0,
                textwrap.fill(
                    self.current_card().get()[self.obj.side],
                    width=self.wrap_width(),
                ),
            )

        elif self.view == 3:
            """
            Display the contents of the card with both the front and back sides.
            """
            self.win.clear()
            self.win.addstr(
                0,
                0,
                textwrap.shorten(
                    num_done,
                    width=mcols - 20,
                    placeholder="…",
                ),
                curses.A_BOLD,
            )

            # Show card content
            self.win.addstr(
                2,
                0,
                textwrap.fill(
                    self.headers[0] + ": " + self.current_card().front,
                    width=self.wrap_width(),
                )
                + "\n\n"
                + textwrap.fill(
                    self.headers[1] + ": " + self.current_card().back,
                    width=self.wrap_width(),
                ),
            )

        self.win.hline(1, 0, curses.ACS_HLINE, mcols)
        self.disp_sidebar()
        self.disp_bar()

    def current_card(self):
        """Get current card object"""
        return self.stack[self.obj.index]

    def get_key(self):
        """
        Display a card and wait for the input.
        Used as a general way of getting back into the card flow from a menu
        """
        while True:
            self.check_size()
            key = self.win.getkey()
            if key in self.config["quit_key"]:
                self.leave()
            elif key in self.config["card_prev"]:
                self.obj.back()
                self.current_card().side = 0
                self.disp_card()
            elif key in self.config["card_next"]:
                if self.obj.index + 1 == len(self.stack):
                    if self.config["show_menu_at_end"]:
                        self.menu_obj.disp()
                else:
                    self.obj.forward(self.stack)
                    self.current_card().side = 0
                    self.disp_card()
            elif key in self.config["card_flip"] and self.view != 3:
                self.current_card().flip()
                self.disp_card()
            elif key in self.config["card_star"]:
                self.current_card().toggleStar()
                self.disp_card()
            elif key in self.config["card_first"]:
                self.obj.index = 0
                self.current_card().side = 0
                self.disp_card()
            elif key in self.config["card_last"]:
                self.obj.index = len(self.stack) - 1
                self.current_card().side = 0
                self.disp_card()
            elif key in self.config["help_disp"]:
                self.help_obj.disp()
            elif key in self.config["menu_disp"]:
                self.menu_obj.disp()
            elif key in self.config["view_one"]:
                self.view = 1
            elif key in self.config["view_two"]:
                self.view = 2
            elif key in self.config["view_three"]:
                self.view = 3

    def disp_sidebar(self):
        """Display a sidebar with the starred terms"""
        (mlines, mcols) = self.win.getmaxyx()
        left = mcols - 19

        self.win.addstr(
            0,
            mcols - 16,
            "STARRED CARDS",
            curses.color_pair(3) + curses.A_BOLD,
        )
        self.win.vline(0, mcols - 20, 0, mlines - 3)

        nstarred = self.nstarred()
        for i, card in enumerate(nstarred):
            term = card.get(smart=False)[0]
            if len(term) > 18:
                term = term[:18] + "…"

            if i > mlines - 6:
                for i in range(19):
                    self.win.addch(mlines - 4, left + i, " ")

                self.win.addstr(
                    mlines - 4,
                    left,
                    f"({len(nstarred) - i - 2} more)",
                )
            else:
                self.win.addstr(2 + i, left, term)

        if len(self.nstarred()) == 0:
            self.win.addstr(2, left, "None starred")
