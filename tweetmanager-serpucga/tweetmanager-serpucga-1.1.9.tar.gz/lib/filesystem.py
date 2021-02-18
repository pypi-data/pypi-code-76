"""
                            FILESYSTEM FUNCTIONS
                          ------------------------
This library contains different functionalities related to the manipulations
of the filesystem, such as creation, modification or removal of directories or
files and other related actions.

"""


import sys
import os
import math
import re
import shutil
import ast

from . import msg_printer as printer


#############
#   FILES   #
#############
def load_filter(filter_path):
    """
    Load the file specified in the argument and compile its regexes.
    Return the list of compiled regexes that form the ready-to-use
    filter
    """

    temporary_filter = []
    with open(filter_path, 'r') as dictionary_file:
        filter_dict = ast.literal_eval(dictionary_file.read())

    for item in filter_dict:
        temporary_filter.append(re.compile(item))

    return temporary_filter


def safe_copyfile(copiable_item, copy_path):
    """
    Given a path where a file is going to be copied (including the filename),
    add an underscore symbol followed by a number. To chose the number iterate
    numbers from 0 to infinite until it finds a free name. For example, if
    foo.txt exists in the destination path and so do foo_1.txt and foo_2.txt,
    this function should return foo_3.txt
    """

    i = 1

    if os.path.isfile(copy_path):
        new_copy_path = copy_path
        copy_path = None

        # Matches patterns such as: '/home/user/foo.json' or '/bin/foo.tar.gz'
        # Grouping '/bin/foo' in group 1 and '.tar.gz' in group 2
        matchObj =\
            re.search(r'(.*[\\\/][^\\\/\.]+)(\.[^\\\/]+)$',
                      new_copy_path)
        new_copy_path = matchObj.group(1) + "_" + str(i) +\
            matchObj.group(2)

        while os.path.isfile(new_copy_path):
            # Same match than before but including a parethesized number before
            # the extension. For example, '/bin/foo(4).tar.gz
            matchObj =\
                re.search(r'(.*[\\\/][^\\\/\.]+)(_\d+)(\.[^\\\/]+)$',
                          new_copy_path)
            new_copy_path = matchObj.group(1) + "_" + str(i) +\
                matchObj.group(3)
            i += 1

    shutil.copyfile(copiable_item, copy_path or new_copy_path)


#################
#  DIRECTORIES  #
#################
def copy_dir_tree(input_dir, output_dir, depth=math.inf):
    """
    Given input and output paths this function copies a directory
    subtree of n-levels of depth to an output directory. The input root
    directory is copied too. If no depth is specified, the function
    copies the complete subtree. Files are ignored.
    """

    if depth >= 0:

        # Copy the current directory. In case it already exists, simply
        # ignore it (don't overwrite) and proceed with execution
        newdir_name = os.path.split(input_dir)[1]
        newdir_path = os.path.join(output_dir, newdir_name)
        try:
            os.mkdir(newdir_path)
        except OSError:
            pass

        # Apply recursively to all the subdirectories
        for directory in os.listdir(input_dir):
            nextdir = os.path.join(input_dir, directory)
            if os.path.isdir(nextdir):
                copy_dir_tree(nextdir, newdir_path, depth-1)


def remove_all(path):
    if path is not None:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)


def change_output_dir(output, verbose, silent):
    """
    Change the final directory where the output will be saved if the
    user specified so. However, intermediate results will still be
    stored in the traditional dirs
    """

    if os.path.isdir(output):
        if verbose:
            print("The resulting files will be stored at",
                  os.path.abspath(output))
        return output
    else:
        if not silent:
            print("The specified output is not an existing system " +
                  "directory. Check the spelling or create the " +
                  "folder if it doesn't exist yet.")
        sys.exit(2)


def create_collection_dir(input_file, final_output_dir, mode, silent):
    """
    Given the input file (either a file of JSONs, a single JSON, a collection
    of JSONs or a collection of flat JSONs) and an output directory, create a
    new folder in that directory with the name of the collection. This will be
    the top of the new tree of files
    """

    if os.path.isfile(input_file) and mode in ("split", "jsoncollection2csv"):

        # Use regex to get only the basename of the file and build an output
        # path. If there is no match, file isn't a JSON. Throw error
        matchObj = re.search(r'.*[/\\](.*)\.json$', input_file)

        if not matchObj:
            if not silent:
                printer.print_not_json()
            sys.exit(1)

        basename = matchObj.group(1)
        collection_path = os.path.join(final_output_dir, basename)

        try:
            os.mkdir(collection_path)
        except OSError:
            pass

    elif os.path.isfile(input_file) and mode not in ("split"):
        collection_path = final_output_dir

    elif os.path.isdir(input_file):
        collection_name = decide_collection_name(input_file)
        collection_path = os.path.join(final_output_dir, collection_name)

        try:
            os.mkdir(collection_path)
        except OSError:
            pass

    else:
        print("Path " + input_file +
              " does not point to a file nor a directory")
        sys.exit(2)

    return collection_path


def decide_collection_name(input_dir):
    """
    Decide in a smart way what is going to be the name of the new collection
    """

    original_dir = os.path.normpath(input_dir)
    matchObj = re.search(r'^.*[/\\]([^/\\]+)[/\\]([^/\\]+)$', original_dir)
    if matchObj.group(2) in ("Split", "Flat"):
        collection_name = matchObj.group(1)
    else:
        collection_name = matchObj.group(2)

    return collection_name


def create_subdir(output_dir, dir_name=""):
    """
    This is used to create the three subfolders present in each collection:
    "Split", "Flat" and "CSV".
    """

    if dir_name:
        output_dir = os.path.join(output_dir, dir_name)

    # Create a new directory for the collection unless it already exists
    os.mkdir(output_dir)

    return output_dir
