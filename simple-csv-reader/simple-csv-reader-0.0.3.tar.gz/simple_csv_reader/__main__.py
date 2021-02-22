import os
import csv
import sys
import math
import json
import argparse
from helpers import *
from collections import OrderedDict

parser = argparse.ArgumentParser(description='CSV reader')
parser.add_argument('-f', '--file', dest='file_path', help='the path of the CSV file')
parser.add_argument('-m', '--missing-header', default=False, action='store_true', dest='missing_header', help='flag to manually input headers')
parser.add_argument('-s', '--separator', default=';', dest='separator', help='the separator used in the CSV file')

cli_helper = CliHelper()

if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])
    cli_helper.screen_clear()
    csv_reader = CSVReader(args.file_path, args.missing_header, args.separator, lambda x: cli_helper.print_percentage(x, "Loading File: "))
    cli_helper.screen_clear()
    while True:
        cli_helper.screen_clear()
        choice = cli_helper.print_menu("MAIN", {
            "1": "READ CSV FILE",
            "2": "SELECT/UNSELECT COLUMNS",
            "3": "ADD FILTERS",
            "0": "EXIT"
        })
        if choice == "1":
            page = 0
            while True:
                cli_helper.screen_clear()
                for e in csv_reader.get_data(page, cli_helper.rows - 3):
                    print({key: value for key, value in e.items() if csv_reader.column_structs[key]['visible']})
                cli_helper.print_separator()
                print("w = UP / s = DOWN / q = QUIT READING MODE")
                char = cli_helper.get_char()
                if char == 'w':
                    if page > 0:
                        page -= 1
                elif char == 's':
                    if page < math.ceil(len(csv_reader.data) / 20):
                        page += 1
                elif char == 'q':
                    break
        if choice == "2":
            while True:
                menu = {}
                cli_helper.screen_clear()
                for index, column_name in enumerate(csv_reader.columns):
                    verb = "HIDE" if csv_reader.column_structs[column_name]['visible'] else "SHOW"
                    menu[index] = "{} {} COLUMN".format(verb, column_name)
                menu["back"] = ""
                selection = cli_helper.print_menu("MAIN -> SELECT/UNSELECT COLUMNS", menu)
                if selection != "back":
                    csv_reader.toggle_column(csv_reader.columns[int(selection)])
                else:
                    break
        if choice == "3":
            while True:
                menu = {}
                cli_helper.screen_clear()
                for column_name, struct in csv_reader.column_structs.items():
                    menu[column_name] = struct["filters"]
                menu["back"] = ""
                column_name = cli_helper.print_menu("MAIN -> ADD FILTERS", menu)
                if column_name in csv_reader.columns:
                    afilter = input("Type keyword: ")
                    csv_reader.add_filter(column_name, afilter)
                if column_name == "back":
                    break

        if choice == "0":
            cli_helper.screen_clear()
            break