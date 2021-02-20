from sys import argv, stderr, stdout
import io


class ScoreFile:
    """Score file is a tabular data format, originally used by Rosetta to store energy values

    This class loads ``.sc`` / ``.fsc`` (these two are identical) and ``.fasc`` files;
    saves ``.sc``. Data is stored *column-wise* to facilitate plotting and conversion to JSON.

    """

    field_width = 8

    def __init__(self, input_file:str=None, **kwargs):
        """Creates an empty object

        :param input_file: input file to load once this object is constructed (optional)
        :param kwargs: see below
        :Keyword Arguments:
            * *columns* (``list(string)``) --
              provide a list of columns this score file will have; this data should be provided when new rows
              are to be added with ``add_row()`` method
            * *skip_columns* (``list(string)``) --
              when loading data from a file, skip columns given their names
            * *rename_columns* (``list(tuple(string,string)``) --
              when loading data from a file, rename given columns
        """
        self.__annotated_sequence = None
        self.__sequence = None
        self.__columns = {}
        self.__n_rows = 0
        self.__skip_from_facs = []
        self.__rename_column = []
        self.__column_names = []
        self.__tag_to_index_map = {}

        if "columns" in kwargs:
            self.__column_names.extend(kwargs["columns"])
            for c in self.__column_names:
                self.__columns[c] = []
        if "skip_columns" in kwargs:
            for col_name in kwargs["skip_columns"]: self.__skip_from_facs.append(col_name)
        if "rename_columns" in kwargs:
            for pair in kwargs["rename_columns"]: self.__rename_column.append(pair)
        if input_file:
            if input_file.endswith('.fasc'):
                self.read_fasc_file(input_file)
            else:
                self.read_score_file(input_file)

    @property
    def n_rows(self):
        """
        Provides the number of data entries (rows) in this score file

        :return: number of rows
        """
        return self.__n_rows

    def detect_pdb_name_column(self, structure_names = ["protein", "tag", "decoy", "description"]):
    
        for col_name in self.__column_names:
            for good_name in structure_names:
                if col_name.find(good_name) >= 0:
                    return col_name
        return None

    def read_score_file(self, fname):
        """Reads data in the Rosetta's score-file format

        :param fname: input file name or input data as multi-line string
        :return: None
        """

        if fname.find('\n') > 0 :       # --- it's data, not a file
            stream = io.StringIO(fname)
        else:
            stderr.write("Reading in " + fname + "\n")
            stream = open(fname)
        self.__read_score_file_data(stream)

    def column(self, col_name):
        """Returns a column by its name

        :param col_name: column name
        :return: data column
        """
        return self.__columns[col_name]

    def is_relevant_column(self,col_name):
        """Returns False if column is not relevant meaning has all values identical
        """
        val = self.column(col_name)[0]
        for i in range(1, len(self.column(col_name))):
            if val != self.column(col_name)[i]:
                return True
        return False

    def add_row(self, row):
        """ Adds a new data row to this score file
        :param row: (``iterable``) an iterable of values, that will be appended to the relevant columns
          (the values must be given in the same order as columns defined in this object)
        :return: None
        """
        if len(row) != len(self.__column_names) :
            raise Exception("wrong number of data in a given row!")

        for i in range(len(row)):
            self.__columns[self.__column_names[i]].append(row[i])
        # ---------- Record the position of a tag so the reverse lookup would be faster
        self.__tag_to_index_map[self.__columns['tag'][-1]] = self.__n_rows
        self.__n_rows += 1

    def replace_value(self, column_name, row_tag, new_value):
        """ Replaces a value in this score file table.

        The cell is represent by a tag (to identify a row) and a column name. Both tag and column must be
        already defined in this score file
        
        :param column_name: (``string``) points to the column an updated cell belong to
        :param row_tag:  (``string``) points to the row an updated cell belong to
        :param new_value: the new value
        :return: ``None``
        """
        i = self.find_row(row_tag)
        self.__columns[column_name][i] = new_value

    def row(self, index):
        """ Returns a row of data requested by its index (from 0 to n_rows - 1)
        :param index: (``int``) row index
        :return: a of row data (as a list)
        """
        r = []
        for i in range(len(self.__column_names)):
            r.append(self.__columns[self.__column_names[i]][index])
        return r

    def merge_in(self, other_sf):
        """ Merges data from ``other_sf`` into this object

        Columns from ``other_sf`` object will be added to rows of this object for these rows where ``tag`` columns
        hold the same row names
        :param other_sf: other score file object
        :return: None
        """
        for col_name in other_sf.column_names():
            if col_name not in self.__column_names:
                source_column = other_sf.column(col_name)
                destination_col = [0 for v in other_sf.column(col_name)]
                for other_idx, tag in enumerate(other_sf.column("tag")):
                    idx = self.find_row(tag)
                    if idx >= 0:
                        destination_col[idx] = source_column[other_idx]
                self.__columns[col_name] = destination_col
                self.__column_names.append(col_name)

    def find_row(self, tag):
        """Find a row identified by a given tag
        :param tag: decoy / structure / data row name
        :return: row number (``int``) or ``-1`` if this tag was not yet inserted into this score file
        """
        return self.__tag_to_index_map.get(tag, -1)

    def column_names(self):
        """Provides an `iterable` of column names
        :return: names of all the data columns
        """
        return self.__column_names

    def write(self, fname):
        """ Writes all data stored in this object in score-file format

        :param fname: output file name or an opened stream; use None to print on stdout
        :return: None
        """

        if fname is None:
            file = stdout
        else:
            if isinstance(fname, str):
                file = open(fname, "w")
            else:
                file = fname        # Assume it's an opened stream
        if self.__sequence is not None:
            file.write("SEQUENCE: " + self.__sequence + "\n")
        file.write("SCORE:")
        for col_name in self.column_names():
            fmt = " %" + str(ScoreFile.field_width) + "s"
            file.write(fmt % col_name)
        file.write("\n")
        for i in range(self.__n_rows):
            file.write("SCORE:")
            for col_name in self.column_names():
                v = self.__columns[col_name][i]
                if isinstance(v, int):
                    fmt = " %"+str(ScoreFile.field_width)+"d"
                    file.write(fmt % v)
                elif isinstance(v, float):
                    fmt = " %"+str(ScoreFile.field_width)+".2f"
                    file.write(fmt % v)
                else:
                    fmt = " %"+str(ScoreFile.field_width)+"s"
                    file.write(fmt % v)
            file.write("\n")

    def read_fasc_file(self, fname):
        """Reads a file in `.fast` (JSON) format

        :param fname: input file name
        :return: None
        """
        data = []
        for line in open(fname): data.append(eval(line.strip()))
        for col_name in data[0].keys():
            if col_name not in self.__skip_from_facs:
                self.__columns[col_name] = []
                self.__column_names.append(col_name)
        for d in data:
            self.__n_rows += 1
            for col_name in self.column_names():
                if col_name not in self.__skip_from_facs:
                    self.__columns[col_name].append(d[col_name])
        # --- rename columns
        self.__rename_columns()

    def __read_score_file_data(self, file):

        line = file.readline()
        while not line.startswith("SCORE:"):
            if line.startswith("SEQUENCE"):
                tokens = line.split()
                if len(tokens) > 1: self.__sequence = tokens[1]
            if line.startswith("ANNOTATED SEQUENCE:"):
                tokens = line.split()
                if len(tokens) > 1: self.__annotated_sequence = tokens[2]
            line = file.readline()
        col_names = line.strip().split()[1:]
        for col_name in col_names:
            if col_name not in self.__skip_from_facs:
                self.__columns[col_name] = []
                self.__column_names.append(col_name)
        for line in file:
            tokens = line.strip().split()[1:]
            self.__n_rows += 1
            for key, val in zip(col_names, tokens):
                if key not in self.__skip_from_facs:
                    try:
                        self.__columns[key].append(int(val))
                    except:
                        try:
                            self.__columns[key].append(float(val))
                        except:
                            self.__columns[key].append(val)
        # --- rename columns
        self.__rename_columns()

        # --- create tag to index map
        i = 0
        tag_column_name = self.detect_pdb_name_column()
        if tag_column_name:
            for tag in self.__columns[tag_column_name]:
                self.__tag_to_index_map[tag] = i
                i += 1
        else:
            print("No column with pdb name or unknown column name for tag, description, decoy etc.")

    def __rename_columns(self):
        for pair in self.__rename_column:
            if pair[0] in self.__columns:
                self.__columns[pair[1]] = self.__columns[pair[0]]
                del(self.__columns[pair[0]])
        for i in range(len(self.__column_names)):
            for pair in self.__rename_column:
                if self.__column_names[i] == pair[0]:
                    self.__column_names[i] = pair[1]


def filter_score_file(scorefile: ScoreFile, filter, column_name: str):
    """Filters given column in scorefile with a given filtr

    :param scorefile: object to filter
    :type scorefile: ``ScoreFile`` object
    :param filter: function to filtr
    :type filter: function
    :param column_name: name of a column to filtr
    :type column_name: string
    :return: a ``ScoreFile`` object
    """

    new_sc = ScoreFile(columns=scorefile.column_names())
    for ir in range(scorefile.n_rows):
        if filter(scorefile.column(column_name)[ir]):
            new_sc.add_row(scorefile.row(ir))

    return new_sc


def combine_score_files(*args, **kwargs):
    """Reads a number of score files and combines them by merging rows of the same tag

    :param args: a list of score file names
    :param kwargs: see constructor (``__init__()`` method)
    :return: a ``ScoreFile`` object
    """
    sf = ScoreFile(**kwargs)
    if args[0].endswith(".fasc"):
        sf.read_fasc_file(args[0])
    else:
        sf.read_score_file(args[0])
    for fname in args[1:]:
        sfi = ScoreFile(**kwargs)
        if fname.endswith(".fasc"):
            sfi.read_score_file(fname)
        else:
            sfi.read_score_file(fname)
        sf.merge_in(sfi)
    return sf


if __name__ == "__main__" :

    sf = combine_score_files("out-2.fsc", *argv[1:],
            skip_columns=["pdb_name", "decoy", "nstruct", "angle_constraint", "atom_pair_constraint", "chainbreak",
                            "dslf_ca_dih", "dslf_cs_ang", "dslf_ss_dih", "dslf_ss_dst", "ref", "dihedral_constraint",
                            "model", "rmsd"],
            rename_columns=[("filename", "tag")])
    sf.write("out.fsc")
