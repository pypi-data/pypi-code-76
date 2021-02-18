import shutil
import sys
import os

from . import json2csv as jsontoolkit
from ..main import singlejson2csv_mode, create_subdir


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
        return create_subdir(output_path)
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
