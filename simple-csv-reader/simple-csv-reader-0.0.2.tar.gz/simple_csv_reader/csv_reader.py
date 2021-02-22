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

class CSVReader:

    column_structs = OrderedDict()
    raw_data = []

    def __init__(self, file_path, missing_header, separator, callback=lambda: None):
        
        # check some basic file_path requirements
        if not file_path:
            raise Exception("path of the file is a mandatory input")
        if not os.path.exists(file_path):
            raise Exception("The path does not exists")
        if not os.path.isfile(file_path):
            raise Exception("The path does not point to a valid file")

        # try to parse csv file guessing the delimiter and requesting user input if header is missing
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            
            # request user input for missing headers
            if missing_header:
                for e in range(len(next(csv_reader))):
                    while True:
                        column_name = input("Type name of column #{}: ".format(e + 1))
                        if column_name in self.columns:
                            print("Error: {} already exists, please use another column name".format(column_name))
                        else:
                            self.__init_column(column_name)
                            break
                csv_file.seek(0)
            else:
                for column_name in next(csv_reader):
                    self.__init_column(column_name)

            # parse it
            for line_count, row in enumerate(csv_reader):
                self.raw_data += [{column: row[index] for index, column in enumerate(self.columns)}]
                percentage = line_count / 5000000 * 100
                callback(percentage)

    def toggle_column(self, column_name):
        self.column_structs[column_name]['visible'] = not self.column_structs[column_name]['visible']

    def add_filter(self, column_name, afilter):
        if afilter not in self.column_structs[column_name]['filters']:
            self.column_structs[column_name]['filters'] += [afilter]

    def clear_filter(self, column_name):
        self.column_structs[column_name]['filters'] = []

    def __init_column(self, column_name):
        self.column_structs[column_name] = {
            "filters": [],
            "visible": True
        }

    @property
    def columns(self):
        return list(self.column_structs.keys())

    @property
    def data(self):
        return list(filter(lambda e: all([all([f in v for f in self.column_structs[k]['filters']]) for k, v in e.items()]), self.raw_data))
            
    def get_data(self, page, page_size):
        return self.data[page * page_size:(page + 1) * page_size]

def main():
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
                    print({key: value for key,value in e.items() if csv_reader.column_structs[key]['visible']})
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
            
if __name__ == "__main__":
    main()

