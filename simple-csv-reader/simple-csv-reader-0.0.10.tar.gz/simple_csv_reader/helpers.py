import os
import sys

from simple_csv_reader.getch import _Getch

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
        rounded = percentage
        total_bricks = self.columns - len(prefix) - 7
        bricks_count = int(rounded / 100 * total_bricks)
        sys.stdout.write('\r')
        sys.stdout.write("%s[%-{}s] %d%%".format(total_bricks) % (prefix, '=' * bricks_count, int(percentage)))
        sys.stdout.flush()

    def print_separator(self):
        print("─" * self.columns)

    def print_menu(self, title, menu, question="Make choice: "):
        while True:
            self.screen_clear()
            self.print_separator()
            print(title)
            self.print_separator()
            for menu_key, menu_label in menu.items():
                print("[{}] {}".format(menu_key, menu_label))
            self.print_separator()
            selection = input(question)
            if selection in [str(e) for e in menu.keys()]:
                break

        return selection

    def yes_no(self, question):
        while True:
            print("\n")
            choice = input("{} [yes/no]: ".format(question))
            print("\n")
            if choice in ['yes', 'no']:
                return choice == 'yes'
