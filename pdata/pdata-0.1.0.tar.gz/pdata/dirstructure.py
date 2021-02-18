import os
from glob import glob
import pandas as pd


def get_list_of_full_child_dirs(d):
    """
    For a directory d (full path), 
    return a list of its subdirectories 
    in a full path form.
    """

    children = (os.path.join(d, child) for child in os.listdir(d))
    dirs = filter(os.path.isdir, children)

    return list(dirs)


def split_full_path(full_path, base_dir):
    """
    Given a full path, return:
    
     - relative_dir: the part of the path that does not 
       include the base directory and the basename
     - basename
    """

    fname = os.path.basename(full_path)

    relative_path = full_path.split(base_dir)[-1]
    relative_dir = relative_path.split(fname)[0]
    relative_dir = relative_dir[1:-1]  # clip slashes

    return relative_dir, fname


def gather_files(base_dir, file_mask):
    """
    Walk the directory base_dir using os.walk
    and gather files that match file_mask (e.g. '*.jpg'). 
    Return the result as a Pandas dataframe with columns 
    'relative_dir' and 'basename'.
    """

    res_tuples = []

    for dir_name, subdirs, files in os.walk(base_dir):

        dir_has_files = len(files) > 0

        if dir_has_files:

            full_mask = os.path.join(dir_name, file_mask)
            mask_matches = glob(full_mask)

            res_tuples += [split_full_path(f, base_dir) for f in mask_matches]

    return pd.DataFrame(res_tuples, columns=['relative_dir', 'basename'])
