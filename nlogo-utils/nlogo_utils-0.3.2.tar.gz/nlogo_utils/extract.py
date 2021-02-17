#!/usr/bin/env python

from pathlib import Path
import argparse

from .shared import (
    SECTION_DELIMITER,
    SECTION_FILE_SUFFIX,
    SEC_NAMES_STRING,
    check_split,
    find_section_index,
)


def extract_nlogo_section(nlogo_file_path, section_name, section_file_path=None):
    """Extract a section from a .nlogo file and store in a separate file

    Arguments:
      nlogo_file_path: path to source nlogo file
      section_name: name of the section of the file to be extracted
      section_file_path: path to store the file created from the nlogo section
    """

    section_name = section_name.strip()
    # parse the given paths and create a storage directory if necessary
    sindex = find_section_index(section_name)
    npath = Path(nlogo_file_path).resolve()
    stem = npath.stem
    parent = npath.parent
    if section_file_path is None:
        fname = f"{stem}.{section_name}{SECTION_FILE_SUFFIX}"
        section_file_path = Path(parent, fname)
    else:
        section_file_path = Path(section_file_path).resolve()

    # read the nlogo file and split it into sections
    with open(npath, "r") as fh:
        contents = fh.read()

    sections_content = contents.split(SECTION_DELIMITER)

    check_split(sections_content)

    # create a {section_name: section_contents} mapping
    scontents = sections_content[sindex]

    # write the file
    with open(section_file_path, "w") as fh:
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
        "-n",
        "--section-name",
        required=True,
        dest="section_name",
        help=f"name of the .nlogo section to be extracted. valid names are {SEC_NAMES_STRING}",
    )
    parser.add_argument(
        "-o", "--output-file", dest="output_file", help="path to .nlogo section file",
    )
    args = parser.parse_args()
    extract_nlogo_section(args.input_file, args.section_name, args.output_file)


if __name__ == "__main__":
    main()
