#!/usr/bin/env python3

import re
import os
import sys
import getopt
import shutil
import json

# Insert the wrapper project dir path into sys.path
sys.path.insert(0,
                os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import tweet_manager.lib.json2csv as jsontoolkit   # noqa: E402
import tweet_manager.lib.msg_printer as printer    # noqa: E402
import tweet_manager.lib.filesystem as filesystem  # noqa: E402

#############################
#     GLOBAL  VARIABLES     #
#############################

# Build OS portable paths for the project and input/output dirs
filepath = os.path.realpath(__file__)
projectpath = os.path.dirname(filepath)
output_dir = os.path.join(projectpath, "output")


# OS portable paths for default filters
default_exclude_filter = os.path.join(projectpath, "data", "filters",
                                      "default_exclude_filter.txt")
default_include_filter = os.path.join(projectpath, "data", "filters",
                                      "default_include_filter.txt")
include_filter = None
exclude_filter = None

# Tasks table (task_list)
tasks_file = os.path.join(projectpath, "task_list.csv")

# Valid execution modes
execution_modes = ["split", "flatten", "flat2csv", "jsoncollection2csv",
                   "singlejson2csv"]

# Default execution mode
mode = "jsoncollection2csv"

# Interactive menus mode
interactive = False

# Verbosity and silence flags
verbose = False
silent = False

# Array compression mode (for CSV conversion)
array_compression = False
compression_depth = 0
# Remove dollar terminations inserted by Mongo
remove_dollars = False
# Keep intermediate files flag
keep_files = False


#############################
#    AUXILIAR FUNCTIONS     #
#############################
def change_execution_mode(mode):
    """
    If specified by the user, change execution mode. Else, default is
    jsoncollection2csv
    """

    if mode in execution_modes:
        if verbose:
            print("Mode of execution set to", mode)
        return mode
    else:
        if not silent:
            print("The selected mode of execution does not exist. Stopping")
        sys.exit(2)


##############################
#      ERROR HANDLERS        #
##############################
def handle_existing_collection(output_path, silent):
    """
    Use this to handle the exception thrown when the system detects an
    already existent split collection with the same path that the one we
    are going to create. Given that case, prompt the user for a
    decission on overwriting
    """

    if not silent:
        print("\nThe directory you selected as output for the new " +
              "collection does already contain one with the same name.")
    if input("Do you really want to overwrite it and lose the previous " +
             "files?(Y/N) > ").lower().startswith('y'):

        shutil.rmtree(output_path)
        parent_dir = os.path.dirname(output_path)
        new_dir = os.path.basename(os.path.normpath(output_path))
        return filesystem.create_subdir(parent_dir, new_dir)
    else:
        if not silent:
            print("Aborting...")
        sys.exit(1)


def handle_existing_split_collection(input_, output, collection_path, silent):
    """
    Use this to handle the exception thrown when the system detects an
    already existent split collection with the same path that the one we
    are going to create. Given that case, prompt the user for a
    decission on overwriting
    """

    if not silent:
        print("\nThe directory you selected as output for the new " +
              "split collection does already contain one with the same name.")
    if input("Do you really want to overwrite it and lose the previous " +
             "files?(Y/N) > ").lower().startswith('y'):

        shutil.rmtree(collection_path)
        return jsontoolkit.split_collection(input_, output)
    else:
        if not silent:
            print("Aborting...")
        sys.exit(1)


def handle_existing_flat_collection(input_, output, collection_path, silent):
    """
    Use this to handle the exception thrown when the system detects an
    already existent flat collection with the same path that the one we
    are going to create. Given that case, prompt the user for a
    decission on overwriting
    """

    if not silent:
        print("\nThe directory you selected as output for the new " +
              "flat collection does already contain one with the same name.")
    if input("Do you really want to overwrite " +
             "it and lose the previous files? (Y/N) > ").lower().\
            startswith('y'):

        shutil.rmtree(collection_path)
        return jsontoolkit.flatten_dir_files(input_, output)
    else:
        if not silent:
            print("Aborting...")
        sys.exit(1)


def handle_existing_csv_collection(input_, output,
                                   include_filter, exclude_filter,
                                   collection_path, compression_depth,
                                   remove_dollars, array_compression, silent):
    """
    Use this to handle the exception thrown when the system detects an
    already existent CSV collection with the same path that the one we
    are going to create. Given that case, prompt the user for a
    decission on overwriting
    """

    if not silent:
        print("\nThe directory you selected as output for the new " +
              "CSV collection does already contain one with the " +
              "same name.")
    if input("Do you really want to overwrite " +
             "it and lose the previous files? (Y/N) > ").lower().\
            startswith('y'):

        shutil.rmtree(collection_path)
        return jsontoolkit.convert_dir_json2csv(input_, output,
                                                array_compression,
                                                compression_depth,
                                                remove_dollars,
                                                include_filter,
                                                exclude_filter)
    else:
        if not silent:
            print("Aborting...")
        sys.exit(1)


def handle_existing_csv_file(input_, output, include_filter, exclude_filter,
                             previous_file, silent):

    if not silent:
        print("\nThe file that was going to be created does already exist")
    if input("Do you really want to overwrite " +
             "it and lose the previous file? (Y/N) > ").lower().\
            startswith('y'):
        os.remove(previous_file)
        return singlejson2csv_mode(input_, output, include_filter,
                                   exclude_filter)
    else:
        if not silent:
            print("Aborting...")
        sys.exit(1)


##############################
#      INTERACTIVE MENUS     #
##############################
def intro_art():
    """
    Just some ASCII art
    """

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") # noqa
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") # noqa
    print("++    #######                                                                                   ++") # noqa
    print("++       #    #    # ###### ###### #####    #    #   ##   #    #   ##    ####  ###### #####     ++") # noqa
    print("++       #    #    # #      #        #      ##  ##  #  #  ##   #  #  #  #    # #      #    #    ++") # noqa
    print("++       #    #    # #####  #####    #      # ## # #    # # #  # #    # #      #####  #    #    ++") # noqa
    print("++       #    # ## # #      #        #      #    # ###### #  # # ###### #  ### #      #####     ++") # noqa
    print("++       #    ##  ## #      #        #      #    # #    # #   ## #    # #    # #      #   #     ++") # noqa
    print("++       #    #    # ###### ######   #      #    # #    # #    # #    #  ####  ###### #    #    ++") # noqa
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") # noqa
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") # noqa


def main_menu():
    """
    This is the menu shown when the user invokes the program in the interactive
    mode
    """

    # Intro
    print("")
    print("***************")
    print("*  Main menu  *")
    print("***************")
    print("")
    # Options
    print("\t1. Format or convert a tweet collection")
    print("\t2. Get help")
    print("\n\t0. Quit the program")
    print("")

    # Selection loop
    while True:
        choice = input("> ")

        if choice in ["0", "1", "2"]:
            break

        print("Please, enter a valid option!")

    if choice == "1":
        formatting_menu()
    elif choice == "2":
        help_menu()
    elif choice == "0":
        print("Bye!")
        sys.exit()


def formatting_menu():
    """
    Menu for the tweet formatting facilities
    """

    # Intro
    print("")
    print("*********************************")
    print("*  Tweet formatting facilities  *")
    print("*********************************")
    print("")

    # Options
    print("\t1. Split collection")
    print("\t2. Flatten a single tweet")
    print("\t3. Flatten a collection of tweets")
    print("\t4. Convert a flat tweet to CSV")
    print("\t5. Convert a collection of flat tweets to CSV")
    print("\t6. Convert a single tweet to CSV")
    print("\t7. Split, flatten and convert to CSV a collection of tweets")
    print("\n\t0. Go back to main menu")

    # Selection loop
    while True:
        choice = input("> ")

        if choice in ["0", "1", "2", "3", "4", "5", "6", "7"]:
            break

        print("Please, enter a valid option!")

    global silent, verbose
    global mode
    global keep_files, remove_dollars, array_compression, compression_depth

    # Split collection
    if choice == "1":
        mode = "split"
        silent, verbose = select_verbosity()
        input_file = select_input_file()
        output_dir = select_output_dir(input_file)

        split_mode(input_file, output_dir)

    # Flatten one tweet
    elif choice == "2":
        mode = "flatten"
        silent, verbose = select_verbosity()
        input_file = select_input_file()
        output_dir = select_output_dir(input_file)

        flatten_mode(input_file, output_dir)

    # Flatten a dir of tweets
    elif choice == "3":
        mode = "flatten"
        silent, verbose = select_verbosity()
        input_dir = select_input_dir()
        output_dir = select_output_dir(input_dir)

        flatten_mode(input_dir, output_dir)

    # Convert one flat tweet to CSV
    elif choice == "4":
        mode = "flat2csv"
        silent, verbose = select_verbosity()
        array_compression, compression_depth = select_array_compression()
        remove_dollars = select_remove_dollars()
        include_filter, exclude_filter = select_filters()
        input_file = select_input_file()
        output_dir = select_output_dir(input_file)

        flat2csv_mode(input_file, output_dir, include_filter, exclude_filter)

    # Convert a dir of flat tweets to CSV
    elif choice == "5":
        mode = "flat2csv"
        silent, verbose = select_verbosity()
        array_compression, compression_depth = select_array_compression()
        remove_dollars = select_remove_dollars()
        include_filter, exclude_filter = select_filters()
        input_dir = select_input_dir()
        output_dir = select_output_dir(input_dir)

        flat2csv_mode(input_dir, output_dir, include_filter, exclude_filter)

    # Convert a single not-flattened tweet to CSV
    elif choice == "6":
        mode = "singlejson2csv"
        silent, verbose = select_verbosity()
        array_compression, compression_depth = select_array_compression()
        remove_dollars = select_remove_dollars()
        keep_files = select_keep_files()
        include_filter, exclude_filter = select_filters()
        input_file = select_input_file()
        output_dir = select_output_dir(input_file)

        singlejson2csv_mode(input_file, output_dir, include_filter,
                            exclude_filter)

    # Convert a full non-split collection to CSV
    elif choice == "7":
        mode = "jsoncollection2csv"
        silent, verbose = select_verbosity()
        array_compression, compression_depth = select_array_compression()
        remove_dollars = select_remove_dollars()
        keep_files = select_keep_files()
        include_filter, exclude_filter = select_filters()
        input_file = select_input_file()
        output_dir = select_output_dir(input_file)

        jsoncollection2csv_mode(input_file, output_dir, include_filter,
                                exclude_filter)

    # Go back to main menu
    elif choice == "0":
        main_menu()

    # This should not be reached
    else:
        print("FATAL ERROR")
        sys.exit()


def help_menu():
    """
    Menu for the help and manual options
    """

    # Intro
    print("")
    print("******************")
    print("*  Help options  *")
    print("******************")
    print("")

    # Options
    print("\t1. Command line syntax and invocation")
    print("\n\t0. Go back to main menu")

    # Selection loop
    while True:
        choice = input("> ")

        if choice in ["0", "1"]:
            break

        print("Please, enter a valid option!")

    if choice == "1":
        printer.print_help()
    elif choice == "0":
        main_menu()
    else:
        print("FATAL ERROR")
        sys.exit()


def select_verbosity():
    """
    Set verbosity/silent options from interactive mode
    Returns a boolean tuple-2 with the form:
        (silent, verbose)
    """

    print("Select one of the three modes:")
    print("\tN - Normal mode (by default). Prints the most relevant messages")
    print("\tV - Verbose mode. Prints info often about the running processes")
    print("\tS - Silent mode. Almost never prints any message")

    choice = input("> ")
    if choice in ["s", "S"]:
        return (True, False)
    elif choice in ["v", "V"]:
        return (False, True)
    else:
        return (False, False)


def select_array_compression():
    """
    Activate or deactivate array compression from interactive mode and select
    the number of levels
    Returns a tuple with the form:
        (array_compression, compression_depth)
    """

    print("Select how many levels of nested arrays you want to flatter")
    print("\t* Choose 0 if you want no array compression (default option)")
    print("\t* Select an arbitrarily large number for full flattening")

    choice = input("> ")
    if re.search(r'^\d+$', choice) and choice != '0':
        return (True, int(choice))
    else:
        return(False, 0)


def select_remove_dollars():
    """
    Activate or deactivate the removing of dollar terminations inserted by
    MongoDB.
    Returns a boolean value for the variable remove_dollars
    """

    print("Would you like to remove the dollar-like terminations?" +
          "(e.g. $date, $oid...)")
    print("Select Y/N (default No)")

    choice = input("> ")
    if choice in ["y", "Y", "yes", "Yes"]:
        return True
    else:
        return False


def select_keep_files():
    """
    Activate or deactivate the keep_files option, to keep the intermediate
    files generated in the modes that create several different types of files
    Returns a boolean value for the variable keep_files
    """

    print("Would you like to keep the intermediate files generated in the " +
          "process?")
    print("Select Y/N (default Yes)")

    choice = input("> ")
    if choice in ["n", "N", "No", "no"]:
        return False
    else:
        return True


def select_filters():
    """
    Activate the include or the exclude filter or tell the program to use no
    filters at all.
    Returns a tuple of already compiled regex filters in the form:
        (include_filter, exclude_filter)
    Where at least one of them will be None.
    """

    global include_filter
    global exclude_filter

    print("Do you want use a file to filter the results?")
    print("\tI - Include filter. Defines the data that will be included in " +
          "the output file (default)")
    print("\tE - Exclude filter. Defines data that will be excluded from " +
          " the output file")
    print("\tN - No filter at all. Include all the info")

    regex_include_filter = None
    regex_exclude_filter = None

    choice = input("> ")

    # If user selects no filter, leave them empty
    if choice in ["n", "N"]:
        pass

    # Load an exclude filter and compile it
    elif choice in ["e", "E"]:
        print("Enter the path to a exclude filter (leave blank to use the " +
              "default one)")
        # Loop until the user provides a valid filter
        while True:
            exclude_filter = input("> ").strip()
            if not exclude_filter:
                print("Using the default exclude filter")  # DEBUG
                exclude_filter = default_exclude_filter
            try:
                regex_exclude_filter = filesystem.load_filter(exclude_filter)
            except (OSError, ValueError):
                print("Please, enter the path of a filter or leave it blank!")
            else:
                break

    # Load an include filter and compile it
    else:
        print("Enter the path to a include filter (leave blank to use the " +
              "default one)")
        while True:
            include_filter = input("> ").strip()
            if not include_filter:
                print("Using the default include filter")  # DEBUG
                include_filter = default_include_filter
            try:
                regex_include_filter = filesystem.load_filter(include_filter)
            except (OSError, ValueError):
                print("Please, enter the path of a filter or leave it blank!")
            else:
                break
    # Return a tuple with the compiled filters (one will be empty
    return (regex_include_filter, regex_exclude_filter)


def select_input_file():
    """
    Ask the user to input the path of the file that is going to be processed.
    Do not accept anything else than a file. Perform some basic checks on the
    given path (to verify that it is indeed a file), although a heavier testing
    for valid files is performed afterwards in the execution funcionts
    Return the filepath
    """

    print("Please, enter a valid path pointing to the input file you want " +
          "to convert:")
    while True:
        file_path = input("> ")
        if os.path.isfile(file_path):
            break
        print("Please, enter the path for a valid file")

    return file_path


def select_input_dir():
    """
    Ask the user to input the path of the dir that is going to be processed.
    Do not accept anything else than a directory. Perform some basic checks
    Return the dirpath
    """

    print("Please, enter a valid path pointing to the input dir you want " +
          "to process:")
    while True:
        dir_path = input("> ")
        if os.path.isdir(dir_path):
            break
        print("Please, enter the path for a valid directory")

    return dir_path


def select_output_dir(input_file):
    """
    Ask the user to input the path of a valid directory to store the new
    generated files. If the answer is blank, user default output dir. There,
    generate a dedicated output folder for the collection and use that as
    output dir

    Return the path of the definitive output dir
    """

    print("Please, enter the path to a directory to store the files that " +
          "are going to be generated")
    print("(The program uses './output' in the project root as the default " +
          "output directory. Leave blank to use that one)")

    while True:
        output_path = input("> ")
        if output_path.strip() == "":
            output_path = output_dir
        if os.path.isdir(output_path):
            break
        print("Please, enter the path for a valid directory or leave blank!")

    # Create a dir to store the collection
    final_output_dir =\
        filesystem.create_collection_dir(input_file, output_path, mode, silent)

    return final_output_dir


##############################
#      EXECUTION MODES       #
##############################
def split_mode(input_, output):
    """
    If the input is a file, make a call to the JSON toolkit library to
    split the file in single JSONs and store the results in the
    specified output dir
    """

    # For splitting only files (JSON collections) are admitted
    if not os.path.isfile(input_):
        if not silent:
            print("You need to specify an input file to split")
        sys.exit(2)

    else:
        if verbose:
            print("Files from the collection:\n"
                  + os.path.realpath(input_) +
                  "\nWill be split into single JSONs and stored in:\n"
                  + os.path.realpath(output))

        try:
            output = filesystem.create_subdir(output, "Split")
        except OSError:
            output = handle_existing_collection(os.path.join(output, "Split"),
                                                silent)
        try:
            # Splitting algorithm call
            return jsontoolkit.split_collection(input_, output)

        # Handle possible exceptions
        except jsontoolkit.WrongFiletypeException:
            if not silent:
                printer.print_not_json()
            shutil.rmtree(output)
            sys.exit(1)
        except SyntaxError:
            if not silent:
                printer.print_invalid_json_syntax()
            shutil.rmtree(output)
            sys.exit(1)
        except OSError as e:
            return handle_existing_split_collection(input_, output, str(e),
                                                    silent)


def flatten_mode(input_, output):
    """
    If the input is a file or directory, make a call to the JSON toolkit
    library to flatten the file or collection and store the results in
    the specified output dir
    """

    # If path is not valid throw error
    if not (os.path.isfile(input_) or os.path.isdir(input_)):
        if not silent:
            print("You need to specify a valid path to a file or dir")
        sys.exit(2)

    # For flattening mode files are interpreted as splitted JSONs
    else:
        if verbose:
            print("Performing a flattening operation on:\n"
                  + os.path.realpath(input_) +
                  "\nAnd storing the results in:\n"
                  + os.path.realpath(output))

        # Flatten single file
        if os.path.isfile(input_):
            try:
                return jsontoolkit.flatten_file(input_, output)

            except jsontoolkit.WrongFiletypeException:
                if not silent:
                    printer.print_not_json()
                sys.exit(1)
            except json.decoder.JSONDecodeError:
                if not silent:
                    printer.print_invalid_json_syntax()
                sys.exit(1)
            except OSError as e:
                return handle_existing_flat_collection(input_, output, str(e),
                                                       silent)

        # Flatten all files in a directory
        elif os.path.isdir(input_):
            try:
                output = filesystem.create_subdir(output, "Flat")
            except OSError:
                output = handle_existing_collection(output, silent)
            try:
                return jsontoolkit.flatten_dir_files(input_, output)
            except jsontoolkit.WrongFiletypeException:
                if not silent:
                    printer.print_not_json()
                shutil.rmtree(output)
                sys.exit(1)
            except json.decoder.JSONDecodeError:
                if not silent:
                    printer.print_invalid_json_syntax()
                shutil.rmtree(output)
                sys.exit(1)
            except OSError as e:
                return handle_existing_flat_collection(input_, output, str(e),
                                                       silent)


def flat2csv_mode(input_, output, include_filter=[], exclude_filter=[]):
    """
    If the input is a file or directory, make a call to the JSON toolkit
    library to convert the file or collection from JSON to CSV format
    and store the results in the specified output dir
    """

    # If path is not valid throw error
    if not (os.path.isfile(input_) or os.path.isdir(input_)):
        if not silent:
            print("You need to specify a valid path to a file or dir")
        sys.exit(2)

    else:
        if verbose:
            print("Performing a JSON-CSV conversion on:\n"
                  + os.path.realpath(input_) +
                  "\nAnd storing the results in:\n"
                  + os.path.realpath(output))

        try:
            # Convert to CSV a single file (should be flat JSON)
            if os.path.isfile(input_):
                return jsontoolkit.convert_json2csv(
                    input_, output, array_compression, compression_depth,
                    remove_dollars, include_filter, exclude_filter)

            # Convert to CSV all files in a dir
            elif os.path.isdir(input_):
                try:
                    output = filesystem.create_subdir(output, "CSV")
                except OSError:
                    output = handle_existing_collection(output, silent)
                return jsontoolkit.convert_dir_json2csv(
                    input_, output, array_compression, compression_depth,
                    remove_dollars,
                    include_filter, exclude_filter)

        except jsontoolkit.WrongFiletypeException as e:
            if not silent:
                printer.print_not_json()

            if os.path.isdir(str(e)):
                matchObj =\
                    re.search(r'(.*)/\d{4}/\d{2}/\d{2}/?$', str(e))
                if matchObj:
                    shutil.rmtree(matchObj.group(1))
                else:
                    shutil.rmtree(str(e))

            sys.exit(1)

        # This is susceptible of being changed to another way of
        # managing the exception (perhaps redirect to flattener or ask
        # the user for a decision)
        except jsontoolkit.NotFlattenedException as e:
            if not silent:
                printer.print_not_flat()

            if os.path.isdir(str(e)):
                matchObj =\
                    re.search(r'(.*)/\d{4}/\d{2}/\d{2}/?$', str(e))
                if matchObj:
                    shutil.rmtree(matchObj.group(1))
                else:
                    shutil.rmtree(str(e))
            sys.exit(1)

        except OSError as e:
            if os.path.isdir(str(e)):
                handle_existing_csv_collection(input_, output,
                                               include_filter,
                                               exclude_filter,
                                               str(e), silent)
            elif os.path.isfile(str(e)):
                handle_existing_csv_file(input_, output,
                                         include_filter,
                                         exclude_filter, str(e),
                                         silent)


def jsoncollection2csv_mode(input_, output,
                            include_filter=[], exclude_filter=[]):
    """
    If the input is a file or directory, make a call to the JSON toolkit
    library to split the collection (if needed), flatten the file(s) and
    convert them to CSV format to finally store the results in the
    specified output dir
    """

    # If path is not valid throw error
    if not (os.path.isfile(input_) or os.path.isdir(input_)):
        if not silent:
            print("You need to specify a valid path to a file or dir")
        sys.exit(2)

    else:
        split_collection = None
        # If input_ points to a file, split
        if os.path.isfile(input_):
            # Splitting file
            try:
                split_output = filesystem.create_subdir(output, "Split")
            except OSError:
                split_output = handle_existing_collection(output, silent)
            if verbose:
                printer.splitting_collection_msg(input_, split_output)
            split_collection =\
                jsontoolkit.split_collection(input_, split_output)

        # Flattening file
        try:
            flat_output = filesystem.create_subdir(output, "Flat")
        except OSError:
            flat_output = handle_existing_collection(output, silent)
        if verbose:
            printer.flattening_collection_msg(split_collection, flat_output)
        flat_collection = jsontoolkit.flatten_dir_files(
            split_collection or input_, flat_output)

        # Finally, convert to CSV and store where needed
        try:
            csv_output = filesystem.create_subdir(output, "CSV")
        except OSError:
            csv_output = handle_existing_collection(output, silent)

        if verbose:
            printer.converting2csv_msg(flat_collection, csv_output)
        csv_collection =\
            jsontoolkit.convert_dir_json2csv(flat_collection, csv_output,
                                             array_compression,
                                             compression_depth, remove_dollars,
                                             include_filter, exclude_filter)

        if keep_files is False:
            filesystem.remove_all(split_collection)
            filesystem.remove_all(flat_collection)

        return csv_collection


def singlejson2csv_mode(input_, output, include_filter=[], exclude_filter=[]):
    """
    If the input is a single json object, make a call to the JSON toolkit
    library to flatten the file and convert it to CSV format to finally store
    the results in the specified output dir
    """

    # If path is not valid throw error
    if not os.path.isfile(input_):
        if not silent:
            print("You need to specify a valid path to a file or dir")
        sys.exit(2)

    else:
        # Make a temporal dir to store the flat file
        if verbose:
            printer.converting2csv_msg(input_, output)
        tmp_dir = os.path.join(output, "tmp")
        try:
            os.mkdir(tmp_dir)
            flat_json = jsontoolkit.flatten_file(input_, tmp_dir)
        except OSError as e:
            if not silent:
                print("The following directory is a system folder and " +
                      "should not be created by the user" + str(e))
            sys.exit(2)
        except jsontoolkit.WrongFiletypeException:
            if not silent:
                printer.print_not_json
            shutil.rmtree(tmp_dir)
            sys.exit(1)
        except json.decoder.JSONDecodeError:
            if not silent:
                printer.print_invalid_json_syntax
            shutil.rmtree(tmp_dir)
            sys.exit(1)

        try:
            csv_file =\
                jsontoolkit.convert_json2csv(flat_json, output,
                                             array_compression,
                                             compression_depth, remove_dollars,
                                             include_filter, exclude_filter)
            # If the user wants the flat file, move it to the output dir
            if keep_files:
                copy_path = os.path.join(output, os.path.basename(flat_json))
                filesystem.safe_copyfile(flat_json, copy_path)
            shutil.rmtree(tmp_dir)
            filesystem.remove_all(flat_json)

            return csv_file

        except OSError as e:
            shutil.rmtree(tmp_dir)
            return handle_existing_csv_file(input_, output, include_filter,
                                            exclude_filter, str(e), silent)

#############################
#       MAIN SCRIPT         #
#############################


def main():

    global verbose
    global silent
    global array_compression
    global compression_depth
    global remove_dollars
    global keep_files
    global mode
    global interactive
    global include_filter
    global exclude_filter

    # VARIABLE DECLARATION
    final_output_dir = output_dir
    include_filter = None
    exclude_filter = None
    regex_include_filter = []
    regex_exclude_filter = []

    # Program needs some args
    if len(sys.argv) <= 1:
        printer.bad_invocation()

    # Option & argument parsing
    try:
        opts, args = getopt.getopt(sys.argv[1:], "IkfFrusvhc:m:o:e:i:",
                                   [
                                    "interactive", "keep-files",
                                    "default-include-filter",
                                    "default-exclude-filter",
                                    "remove-dollars", "upv-compatible",
                                    "silent", "verbose", "help",
                                    "array-compression=", "mode=", "output=",
                                    "exclude", "include"
                                   ])

    except getopt.GetoptError:
        printer.bad_invocation()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printer.print_help()
        elif opt in ("-I", "--interactive"):
            interactive = True
        else:
            if opt in ('-m', "--mode"):
                mode = change_execution_mode(arg)
            if opt in ('-o', "--output"):
                final_output_dir = filesystem.change_output_dir(arg, verbose,
                                                                silent)
            if opt in ('-v', "--verbose"):
                verbose = True
            if opt in ('-s', "--silent"):
                silent = True
            if opt in ('-c', "--array-compression"):
                array_compression = True
                try:
                    compression_depth = int(arg)
                except ValueError:
                    print("Array compression option should have an integer " +
                          "value indicating depth. Invoke 'main.py -h' for " +
                          "further details")
                    sys.exit(2)

            if opt in ('-r', "--remove-dollars"):
                remove_dollars = True
            if opt in ('-u', "--upv-compatible"):
                array_compression = True
                compression_depth = 1
                remove_dollars = True
                if not include_filter:
                    include_filter = default_include_filter
            if opt in ('-e', "--exclude"):
                exclude_filter = arg
            if opt in ('-i', "--include"):
                include_filter = arg
            if opt in ('-f', "--default-include-filter"):
                if not include_filter:
                    include_filter = default_include_filter
            if opt in ('-F', "--default-exclude-filter"):
                if not exclude_filter:
                    exclude_filter = default_exclude_filter
            if opt in ('-k', "--keep-files"):
                keep_files = True

    if interactive:
        intro_art()
        main_menu()

    elif not interactive:

        input_src = sys.argv.pop()

        # Verbosity and silence are incompatible. Silence prevails
        if silent:
            verbose = False

        # Load filters, if any
        if include_filter:
            regex_include_filter = filesystem.load_filter(include_filter)
        elif exclude_filter:
            regex_exclude_filter = filesystem.load_filter(exclude_filter)

        # Create a dir to store the collection
        final_output_dir =\
            filesystem.create_collection_dir(input_src, final_output_dir,
                                             mode, silent)

        # Modes of execution
        if mode == "split":
            split_mode(input_src, final_output_dir)

        elif mode == "flatten":
            flatten_mode(input_src, final_output_dir)

        elif mode == "flat2csv":
            flat2csv_mode(input_src, final_output_dir,
                          regex_include_filter, regex_exclude_filter)

        elif mode == "singlejson2csv":
            singlejson2csv_mode(input_src, final_output_dir,
                                regex_include_filter, regex_exclude_filter)

        elif mode == "jsoncollection2csv":
            jsoncollection2csv_mode(input_src, final_output_dir,
                                    regex_include_filter, regex_exclude_filter)


#############################
#       MAIN EXECUTION      #
#############################
if __name__ == "__main__":
    main()
