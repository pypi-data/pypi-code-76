# dir_clean.py
# Dependencies: None

import os
import os.path


def dir_clean(folder_path=""):
    """
    -------------------------------------------------------
    Removes all excel and csv files from given directory
    -------------------------------------------------------
    Parameters:
        folder_path : string
            (Optional) Path to directory containing files to delete
            If not specified, deletes from current directory
    Returns:
       NONE
    Side Effects:
        Deletes all .xlsx and .csv files from local dir
    ------------------------------------------------------
    """

    # Cwd (Default)
    files_in_directory = os.listdir(os.getcwd())

    # Chosen directory to clean
    if not (folder_path == ""):
        files_in_directory = os.listdir(os.path.normpath(folder_path))

    # Remove all .xlsx files
    filtered_files = [file for file in files_in_directory if file.endswith(".xlsx")]
    for file in filtered_files:
        path_to_file = os.path.join('', file)
        os.remove(path_to_file)

    # Remove all .csv files
    filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
    for file in filtered_files:
        path_to_file = os.path.join('', file)
        os.remove(path_to_file)

    print("\nTemporary files deleted from local machine!")
