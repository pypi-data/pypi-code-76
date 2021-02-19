import pybedtools
import pandas as pnd
from copy import deepcopy
import os
import numpy as np

class GenomicRegionAnnotator():
    #############################
    # Constructors/ Destructors #
    #############################

    def __init__(self):
        '''Standard Constructor. Creates an empty GenomicRegionAnnotator.
        '''
        # Set database against which to None. Will be pandas.DataFrame
        # object containing the following columns: 
        # FILENAME: Absolute path to the file 
        # REGION.TYPE: E.g. protein.coding.genes, Enhancers, ...
        # SOURCE: E.g., Cell type from which regions are derived
        # ANNOTATION.BY: NAME | SOURCE
        # MAX.DISTANCE: If ANNOTATION.TYPE is distance, then the max
        # distance has to be defined
        # DISTANCE.TO: If ANNOTATION.TYPE is distance, then it has to
        # be defined what the location is to which the distance shall
        # be computed. Can be START | END | MID | REGION
        # N.HITS: Van be either of ALL | CLOSEST
        self.__database = None

        # Set regions that shall be annotated to None.
        # List will be filled with filename, and pybedtools.BedTool
        # object
        self.__base = None

        # Set pybedtools.BedTool object, that contains data of 
        # self.__base as bed4 BedTool object to None
        self.__base_bed = None


    ##################
    # Public methods #
    ##################

    ######################
    # Data loading methods

    def load_database_from_file(self, database_filename):
        '''Method for loading a database from a tab separated file. The database
        contains all files against which the annotation shall be performed.

        :param database_filename: Path to tab separated database file. The
            database contains all files against which the annotation shall be
            performed. Required columns are

            - FILENAME: Absolute path to the file (must be a bed like file)
            - REGION.TYPE: E.g. protein.coding.genes, Enhancers, ...
            - SOURCE: E.g., Cell type from which regions are derived
            - ANNOTATION.BY: SOURCE | NAME
            - MAX.DISTANCE: Maximal distance between base and database \
intervall, such that database intervall is anotated to base \
intervall.
            - DISTANCE.TO: If ANNOTATION.TYPE is distance, then it has to be \
defined what the location is to which the distance shall be \
computed. Can be START | END | MID | REGION.
            - N.HITS: Can be either of ALL | CLOSEST
            - NAME.COL: If ANNOTATION.BY == NAME, then you can define the \
column (0-based) in which the name is stored. If NAME.COL == NA, then it is \
assumed, that the 4th column contains the name.

        :type database_filename: str

        :return: Nothing to be returned
        :rtype: None
        '''
        self.__database = pnd.read_csv(database_filename, sep="\t",
                                        keep_default_na=False)

        # Check if __database is correctly defined
        self.__check_database()

    def load_database_from_dataframe(self, database_dataframe):
        '''Method for loading a database from a :class:`pandas.DataFrame`. The
        database contains all files against which the annotation shall be
        performed.

        :param database_dataframe: :class:`pandas.DataFrame` object. The
            database contains all files against which the annotation shall be
            performed. Required columns are

            - FILENAME: Absolute path to the file (must be a bed like file)
            - REGION.TYPE: E.g. protein.coding.genes, Enhancers, ...
            - SOURCE: E.g., Cell type from which regions are derived
            - ANNOTATION.BY: SOURCE | NAME
            - MAX.DISTANCE: Maximal distance between base and database \
intervall, such that database intervall is anotated to base \
intervall.
            - DISTANCE.TO: If ANNOTATION.TYPE is distance, then it has to be \
defined what the location is to which the distance shall be \
computed. Can be START | END | MID | REGION.
            - N.HITS: Can be either of ALL | CLOSEST
            - NAME.COL: If ANNOTATION.BY == NAME, then you can define the \
column (0-based) in which the name is stored. If NAME.COL == NA, then it is \
assumed, that the 4th column contains the name.
        :type database_dataframe: :class:`pandas.DataFrame`

        :return: Nothing to be returned
        :rtype: None
        '''
        self.__database = deepcopy(database_dataframe)

        # Check if files in __database exist
        self.__check_database()

    def load_base_from_file(self, base_filename):
        '''Function that loads base file, that will be annotated against
        annotation database.

        :param base_filename: Path to a bed-like file, that shall be annotated.
            First three columns must be bed-like, i.e. containing chromosome,
            start-, and end-position. Must contain a header. First three header
            entries must be: "#chrom", "start", "end".
        :type base_filename: str

        :return: Nothing to be returned
        :rtype: None
        '''
        self.__base = pnd.read_csv(base_filename, sep="\t", 
                                   dtype={"start": 'Int64', "end": 'Int64'})
        # Check if __base contains header and is bed-like
        self.__check_base()

        self.__base.index = [ "_".join([ str(e) for e in r.iloc[:3] ]) for i, r
                             in self.__base.iterrows() ]

        # Create pybedtools.BedTool pbject from self.__base
        self.__base_bed = self.__create_bed4(self.__base)

    def load_base_from_dataframe(self, base_dataframe):
        '''Function that loads base from a :class:`pandas.DataFrame`, that will
        be annotated against annotation database.

        :param base_dataframe: :class:`pandas.DataFrame` object, that shall be
            annotated. First three columns must be bed-like, i.e. containing 
            chromosome, start-, and end-position. Must contain columns: 
            "#chrom", "start", "end"
        :type base_dataframe: :class:`pandas.DataFrame`

        :return: Nothing to be returned
        :rtype: None
        '''
        print("Start copying!")
        self.__base = deepcopy(base_dataframe)
        print("Copy Done!")
        # Check if __base contains header and is bed-like
        self.__check_base()
        print("Check Done!")

        self.__base.index = [ "_".join([str(c), str(s), str(e) ]) for c,s,e
                             in zip(self.__base["#chrom"],
                                    self.__base["start"],
                                    self.__base["end"]) ]


        print("Indexing Done!")

        # Create pybedtools.BedTool pbject from self.__base
        self.__base_bed = self.__create_bed4(self.__base)
        print("Bed Creation Done!")

    ####################
    # Annotation methods
    def annotate(self):
        '''Method, that annotates the base region table against the ROI tables
        in the database.

        :return: Nothing to be returned.
        :rtype: None
        '''
        # Check if all necessary objects are defined
        if(self.__base is None):
            raise(RuntimeError((
                "Base regions are not defined! Please define "
                "them using either of load_base_from_file or "
                "load_base_from_dataframe method.")))
        elif(self.__database is None):
            raise(RuntimeError((
                "Database regions are not defined! Please "
                "define them using either of load_database_from_file or "
                "load_database_from_dataframe method.")))

        for index, row in self.__database.iterrows():
            max_distance = row["MAX.DISTANCE"]
            annotation_by = row["ANNOTATION.BY"]
            n_hits = row["N.HITS"]
            filename = row["FILENAME"]
            region_type = row["REGION.TYPE"]
            current_source = row["SOURCE"]
            distance_to = row["DISTANCE.TO"]
            name_col = (row["NAME.COL"] if row["NAME.COL"] == "NA" else 
                        int(row["NAME.COL"]))

            print(filename)

            # Check if annotation was already done
            if(self.__anno_done(region_type, current_source, annotation_by)):
                continue
            else:
                if(not region_type in self.__base.columns):
                    # Initiate new column if self.__base with "NA"
                    self.__base[row["REGION.TYPE"]] = (["NA"]*
                                                        len(self.__base.index))

                anno_bed = self.__create_bed6(filename,
                                              distance_to,
                                              annotation_by,
                                              source=current_source,
                                              name_col=name_col)

                # Determine closest database intervals to base intervals
                intersect_bed = self.__base_bed.sort().closest(anno_bed.sort(), 
                                                        D="ref",
                                                        k=int(n_hits),
                                                        t="all"
                                                       )
                intersect_dict = {}
                for e in intersect_bed:
                    if(e[-1] == -1):
                        continue
                    distance = int(e[-1])
                    if(abs(distance) > max_distance):
                        continue
                    db_name = e[7].split("(")[0]
                    if(not e[3] in intersect_dict):
                        intersect_dict[e[3]] = [[db_name+"("+str(distance)+")", 
                                                 distance]]
                    else:
                        intersect_dict[e[3]] += [[db_name+"("+str(distance)+")",
                                                  distance]]
                base_df_list = []
                index_tmp = []
                for c,s,e,rt in zip(self.__base["#chrom"],
                                    self.__base["start"],
                                    self.__base["end"],
                                    self.__base[region_type]):
                    idx = "_".join([str(c), str(s), str(e)])
                    if(not idx in intersect_dict):
                        continue
                    index_tmp += [idx]
                    anno_string = rt
                    overlap_list = intersect_dict[idx]
                    overlap_list_sorted = overlap_list
                    result_string = None
                    result_string = ";".join([ ol[0] for ol in
                                                  overlap_list_sorted ])
                    if(anno_string == "NA"):
                        anno_string = result_string
                    else:
                        anno_string += ";"+result_string
                    base_df_list += [ anno_string ]
                self.__base.loc[index_tmp, region_type] = base_df_list


    ###############
    # Print methods

    def print_database(self):
        '''Method that prints the database.

        :return: Nothing to be returned.
        :rtype: None
        '''
        print(self.__database)

    def print_base(self):
        '''Method that prints base.

        :return: Nothing to be returned.
        :rtype: None
        '''
        print(self.__base)

    ################
    # Getter methods

    def get_base(self):
        '''Method that return self.__base

        :return: Copy of :class:`pandas.DataFrame` object self.__base
        :rtype: :class:`pandas.DataFrame`
        '''
        return deepcopy(self.__base)

    ###############
    # Other Methods
    def set_tempdir(self, dirpath):
        '''Methods that sets temp directory for pybedtools objects

        :param dirpath: Path to temp directory.
        :type dirpath: str

        :return: Nothing to be returned.
        :rtype: None
        '''
        pybedtools.set_tempdir(dirpath)

    ###################
    # Private Methods #
    ###################

    def __check_database(self):
        '''Checks if database is consistently defined.

        :return: Nothing to be returned.
        :rtype: None
        '''
        # Check if necessary fields are defined
        columns = set(self.__database.columns)
        required_fields = ["FILENAME", "REGION.TYPE", "SOURCE", "ANNOTATION.BY",
                           "MAX.DISTANCE", "DISTANCE.TO", "N.HITS", "NAME.COL"]
        for required_field in required_fields:
            if(not required_field in columns):
                self.__database = None
                raise(RuntimeError(
                    required_field+(" is a required column in the database "
                                    "but not found. Please update your "
                                    "database!")))

        # Check if files in database exist!
        if(self.__database is None):
            print("No annotation database defined yet!")
        else:
            for index, row in self.__database.iterrows():
                filename = row["FILENAME"]
                if(not(os.path.exists(filename))):
                    raise(RuntimeError(filename+" does not exist!"))

        # Check if there are many entries for the same REGION.TYPE, that in 
        # this case ANNOTATION.BY has to be SOURCE in all cases.
        region_type_dict = {}
        for index, row in self.__database.iterrows():
            region_type = row["REGION.TYPE"]
            annotation_by = row["ANNOTATION.BY"]

            if(not region_type in region_type_dict):
                region_type_dict[region_type] = [annotation_by]
            else:
                region_type_dict[region_type] += [annotation_by]

        for region_type in region_type_dict.keys():
            if(region_type_dict[region_type].count("NAME") > 1):
                raise(RuntimeError((
                    "Database contains more than one entry with the "
                    "same REGION.TYPE ("+region_type+"), while ANNOTATION.BY " 
                    "is set to \"NAME\". Please define distinct "
                    "\"REGION.TYPE\" IDs, if you want to annotate the names of "
                    "different database intervals!")))
            elif(len(set(region_type_dict[region_type])) > 1):
                raise(RuntimeError((
                    "Database contains two entries with different "
                    "ANNOTATION.BY values for the same \"REGION.TYPE\" ID "
                    "("+region_type+")! Please define a distinct "
                    "\"REGION.TYPE\" ID for the database entry, that has "
                    "\"ANNOTATION.BY\" set to \"NAME\"!")))

    def __check_base(self):
        '''Checks if base, that will be annotated is bed-like, and
        contains a header.

        :return: Nothing to be returned.
        :rtype: None
        '''
        if(not self.__base.columns[0][0] == "#"):
            raise(RuntimeError((
                    "Base table does not contain a "
                    "valid haeder! Header has to start with \"#\"")))

        # Only Check first 100 entries
        c = 0
        for index, row in self.__base.iterrows():
            if(c > 100):
                break
            if(not(str(row.iloc[1]).isdigit() and str(row.iloc[2]).isdigit())):
                print(type(row.iloc[1]))
                raise(RuntimeError((
                        "Base table does not seem to be bed-like. "
                        "Second and third columns must be integers.")))
            elif(not(row.iloc[2] > row.iloc[1])):
                print(row)
                raise(RuntimeError((
                        "Base table does not seem to be bed-like. "
                        "Second column must be smaller or equal to third "
                        "column.")))
            c += 1

    def __create_bed4(self, df):
        '''Method that creates a bed4 pybedtools.BedTool object from df. Columns
        are: 1. Chromosome, 2. Start, 3. End, 4. Name (<chrom>_<start>_<end>)

        :param df: :class:`pandas.DataFrame` object, that will be converted
            into bed4 :class:`pybedtools.BedTool` object
        :type df: :class:`pandas.DataFrame`

        :return: :class:`pybedtools.BedTool` object derived from df
        :rtype: :class:`pybedtools.BedTool`
        '''
        bed_list = []

        for c,s,e in zip(df["#chrom"], df["start"], df["end"]):
            bed_list += [ "\t".join([ str(c), str(s), str(e) ]+
                    [ "_".join([ str(c), str(s), str(e) ]) ]) ]

        return pybedtools.BedTool("\n".join(bed_list), from_string=True)

    def __create_bed6(self, 
                      bed_filename, 
                      pos, 
                      annotation_by,
                      source=None, 
                      name_col="NA"):
        '''Create a bed6 pybedtools.BedTool object using single base
        at start-, end- or midpoint of region.

        :param bed_filename: Path to bed file used for creating BedTool object.
        :type bed_filename: str
        :param pos: base position relative to intervall used for creating the 
            BedTool object. Can be either of START | END | MID | REGION. START, 
            and END are relative to strand.
        :type pos: str
        :param annotation_by: Shall name (as defined in 4th column of
            bed_filename), or source as defined in database be used for 
            annotation. Can be either of NAME | SOURCE.
        :type annotation_by: str
        :param source: Has to be defined if annotation_by is SOURCE.
        :type source: str
        :param name_col:Column (zero-based) containing the name of the
            intervals.
        :type name:col: int

        :return: :class:`pybedtools.BedTool` object derived from bed_filename
        :rtype: :class:pybedtools.BedTool`
        '''
        bed_list = []
        bed_file = open(bed_filename, "r")
        is_bed6_like = self.__is_bed6_like(bed_filename)
        for line in bed_file:
            if(line[0] == "#"):
                continue
            split_line = line.rstrip("\r\n").split("\t")
            chrom = split_line[0]
            start = int(split_line[1])
            end = int(split_line[2])

            # Define name of interval
            name = None
            if(annotation_by == "NAME"):
                if(not name_col == "NA"):
                    name = split_line[name_col]
                else:
                    if(len(split_line) < 4):
                        name = "_".join(split_line[:3])
                    else:
                        name = split_line[3]
            else:
                name = source

            # Define strand of interval
            strand = "+"
            if(is_bed6_like):
                strand = split_line[5]

            if(pos == "START"):
                if(strand == "+"):
                    end = start+1
                else:
                    start = end-1
            elif(pos == "END"):
                if(strand == "-"):
                    start = end-1
                else:
                    end = start+1
            elif(pos == "MID"):
                start = start+int((end-start)/2)
                end = start + 1
            name += "("+"_".join([split_line[0], str(start), str(end)])+")"

            bed_list += [ "\t".join([chrom, str(start), str(end), 
                                        name, "NA", strand]) ]

        return pybedtools.BedTool("\n".join(bed_list), from_string=True)

    def __is_bed6_like(self, bed_filename):
        '''Method that checks if bed_filename is bed6 like format.

        :param bed_filename: Path to bed file
        :type bed_filename: str

        :return: True, if bed_filename is bed6 like, False otherwise.
        :rtype: bool
        '''
        bed_file = open(bed_filename, "r")
        strands = []
        # Check first 100 lines
        c = 0
        for line in bed_file:
            c += 1
            if(c >= 100):
                break
            if(line[0] == "#"):
                continue
            split_line = line.rstrip().split("\t")
            if(not(len(split_line) >= 6)):
                return False
            else:
                strands += [split_line[5]]
        bed_file.close()

        strands = set(strands)

        if(len(strands) == 2 and "+" in strands and "-" in strands):
            return True
        elif(len(strands) == 1 and ("+" in strands or "-" in strands)):
            return True
        else:
            return False

    def __anno_done(self, region_type, source, annotation_by):
        '''Method that checks if annotation is already done for region_type, 
        source, annotation_by combo.

        :param region_type: region type as given in self.__database
        :type region_type: str
        :param source: source as given in self.__database
        :type source: str
        :annotation_by: annotation_by as given in self.__database. Can be either
            of SOURCE | NAME

        :return: True, if the annotation was already performed, False otherwise.
        :rtype: bool
        '''
        if(not region_type in set(self.__base.columns)):
            return False
        elif( annotation_by == "SOURCE" ):
            sources = sum([ e.split(";") for e in 
                            self.__base.loc[:, region_type] ], [])
            sources = set( [ e.split("(")[0] for e in sources ] )
            if(not source in sources):
                return False
            else:
                return True
        else:
            return True

    def __calculate_distance(self, e):
        '''Method that calculates the distance between two intervalls.

        :param e: Object of type :class:`pybedtools.Intervall`. The following
            entries must be contained in e

            - e[0]: Chromosome base intervall
            - e[1]: Start base intervall
            - e[2]: End base intervall
            - e[3]: Name base intervall (<chrom>_<start>_<end>)
            - e[4]: Chromosome db intervall
            - e[5]: Extended start db intervall 
            - e[6]: Extended end db intervall
            - e[7]: Name db intervall (<name>(<chrom>_<start>_<end>))
            - e[8]: "NA"
            - e[9]: Strand db intervall

        :type e: :class:`pybedtools.Intervall`

        :return: Distance between two intervalls
        :rtype: int
        '''
        base_name = str(e[3])
        base_region = base_name
        base_region_split = base_region.split("_")
        base_start = int(base_region_split[1])
        base_end = int(base_region_split[2])
        db_region = str(e[7]).split("(")[1][:-1]
        db_region_split = db_region.split("_")
        db_start = int(db_region_split[1])
        db_end = int(db_region_split[2])
        db_strand = str(e[9])

        distance = 0
        if(db_end < base_start):
            distance = base_start - db_end
            if(db_strand == "-"):
                distance = -1*distance
        elif(base_end < db_start):
            distance = db_start - base_end
            if(db_strand == "-"):
                distance = -1*distance

        return distance

