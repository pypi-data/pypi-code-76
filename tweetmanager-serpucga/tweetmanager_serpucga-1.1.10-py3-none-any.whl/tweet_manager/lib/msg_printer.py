"""
                            MESSAGE PRINTER
                          -------------------
This library contains all the functions whose main or only function is the
printing of messages through the console. This includes informative and
verbose messaging, syntax remainders, the help page, errors, warnings, etc.
"""

import os
import sys


def bad_invocation():
    print("Unacceptable invocation. To know more about the syntax:")
    print("./main.py -h")
    sys.exit(2)


def print_help():
    """
    Basic help about usage of the program and accepted syntax that will
    be printed when the option -h or --help is received
    """

    print("Usage:\n\t./main.py [arguments] file")

    print("\nArguments:")
    print("\n\t-h | --help\n\t\tPrint help about syntax and usage")
    print("\n\t-I | --interactive\n\t\tExecute in the interactive menu mode")
    print("\n\t-m <mode> | --mode=<mode>\n\t\tSelect an execution " +
          "mode")
    print("\n\t-o <dir> | --output=<dir>\n\t\tSelect an output " +
          "directory")
    print("\n\t-c <depth> | --array-compression <depth>\n" +
          "\t\tCompress the array fields in a single list in the CSV. " +
          "Follow with\n\t\tan integer arg indicating the number of " +
          "nested arrays to compress.\n\t\tUse an arbitrarily large " +
          "number to indicate full compression")
    print("\n\t-r | --remove-dollars\n\t\tRemove the dollar-" +
          "headed terminations")
    print("\n\t-u | --upv-compatible\n\t\tEquivalent to " +
          "remove-dollars + array-compression + default include filter")
    print("\n\t-v | --verbose\n\t\tVerbose mode")
    print("\n\t-s | --silent\n\t\tSilent mode. If this flag is " +
          "present the verbose flag will be muted and\n\t\teven " +
          "the most critical messages will be silenced.")
    print("\n\t-f | --default-include-filter\n\t\tUse the " +
          "default include filter")
    print("\n\t-F | --default-exclude-filter\n\t\tUse the " +
          "default exclude filter")
    print("\n\t-k | --keep-files\n\t\tKeep the intermediate " +
          "files (split and flat) when doing full cycle JSON to " +
          "CSV conversion")
    print("\nModes:")
    print("\tsplit\t\t\t\tSplit a collection (single file) of JSON" +
          " objects in individual files")
    print("\tflatten\t\t\t\tFlatten a collection of JSON files")
    print("\tflat2csv\t\t\tConvert from flat JSON to CSV")
    print("\tjsoncollection2csv\t\tConvert a JSON collection (single file " +
          "containing multiple JSON items) to CSV")
    print("\tsinglejson2csv\t\t\tConvert a single JSON object " +
          "to CSV (doesn't generate a directory tree)")
    sys.exit()


def splitting_collection_msg(input_, output):
    print("Splitting the collection "
          + os.path.realpath(input_) +
          "\nAnd storing the results in:\n"
          + os.path.realpath(output))


def flattening_collection_msg(input_, output):
    print("\nFlattening the collection:"
          + os.path.realpath(input_) +
          "\nAnd storing the results in:\n"
          + os.path.realpath(output))


def converting2csv_msg(input_, output, array_compression, remove_dollars):
    print("\nConverting the following to CSV format:"
          + os.path.realpath(input_) +
          "\nWith compression mode = " + str(array_compression) +
          "\nAnd remove dollars mode = " + str(remove_dollars) +
          "\nAnd storing the results in:\n"
          + os.path.realpath(output))


def print_invalid_json_syntax():
    print("Something seems to be wrong with your JSON " +
          "file. Please, check its structure and syntax." +
          "\nAborting...")


def print_not_json():
    print("Please, check that the input file you specify " +
          "has a .json extension.\nAborting...")


def print_not_flat():
    print("The file you are trying to convert to CSV seems"
          + " to contain nested dictionaries.\n" +
          "Try flattening it first.")
