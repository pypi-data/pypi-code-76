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
