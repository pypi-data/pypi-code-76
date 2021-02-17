#!/usr/bin/env python

from pathlib import Path
import argparse

from .shared import (
    SECTION_NAMES,
    SECTION_DELIMITER,
    SECTION_FILE_SUFFIX,
    DEFAULT_SECTION_DIR,
    check_split,
)


def split_nlogo_file(nlogo_file_path, sections_dir=None):
    """Split a .nlogo file into its component sections and store the sections
    as separate files in a specified output directory
    
    Arguments:
      nlogo_file_path: path to source nlogo file
      sections_dir: path to directory in which to store section files
    """
    # parse the given paths and create a storage directory if necessary
    npath = Path(nlogo_file_path).resolve()
    stem = npath.stem
    parent = npath.parent
    if sections_dir is None:
        sections_dir = Path(parent, DEFAULT_SECTION_DIR % stem)
    else:
        sections_dir = Path(sections_dir).resolve()
    sections_dir.mkdir(exist_ok=True)

    # read the nlogo file and split it into sections
    with open(nlogo_file_path, "r") as fh:
        contents = fh.read()

    sections_content = contents.split(SECTION_DELIMITER)

    check_split(sections_content)

    # write each of the sections to separate files
    for sname, scontents in zip(SECTION_NAMES, sections_content):
        sfile_path = Path(sections_dir, sname + SECTION_FILE_SUFFIX)
        with open(sfile_path, "w") as fh:
            fh.write(scontents)


def main():
    """Parse the command line arguments and call the appropriate functions
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input-file",
        required=True,
        dest="input_file",
        help="path to .nlogo file",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        help="path to .nlogo section directory",
    )
    args = parser.parse_args()
    split_nlogo_file(args.input_file, args.output_dir)


if __name__ == "__main__":
    main()
