import os
import sys
from time import sleep
from getch import _Getch

class CliHelper:

    def __init__(self):
        rows, columns = os.popen('stty size', 'r').read().split()
        self.rows = int(rows)
        self.columns = int(columns)
        self._getch = _Getch()

    @staticmethod
    def screen_clear():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def get_char(self):
        return self._getch()

    def print_percentage(self, percentage, prefix=""):
        rounded = int(percentage)
        sys.stdout.write('\r')
        sys.stdout.write("%s[%-{}s] %d%%".format(self.columns-len(prefix)-7) % (prefix,'='*rounded, int(rounded)))
        sys.stdout.flush()

    def print_separator(self):
        print("─" * self.columns)

    def print_menu(self, title, menu, question="Make choice: "):
        while True:
            self.print_separator()
            print(title)
            self.print_separator()
            for menu_key, menu_label in menu.items():
                print("[{}] {}".format(menu_key, menu_label))
            self.print_separator()
            selection = input(question)
            if selection in menu.keys():
                break

    def yes_no(self, question):
        while True:
            print("\n")
            choice = input("{} [yes/no]: ".format(question))
            print("\n")
            if choice in ['yes', 'no']:
                return choice == 'yes'