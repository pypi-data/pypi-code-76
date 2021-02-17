#!/usr/bin/env python

from pathlib import Path
import argparse

from .shared import (
    SECTION_NAMES,
    SECTION_DELIMITER,
    SECTION_FILE_SUFFIX,
    SEC_NAMES_STRING,
    find_section_index,
)


def replace_nlogo_section(
    nlogo_file_path, section_name, section_file_path, output_file_path
):
    """Replace a section of a .nlogo file and with the contents of a separate section file
    
    Arguments:
      nlogo_file_path: path to source nlogo file
      section_name: name of the section of the file to be replaced
      section_file_path: path to the section file to be used as the replacement
      output_file_path: path to the nlogo file containing the replaced section
    """

    # parse the given paths and create a storage directory if necessary
    sindex = find_section_index(section_name)
    npath = Path(nlogo_file_path).resolve()
    output_file_path = Path(output_file_path).resolve()

    # read the nlogo file and split it into sections
    with open(npath, "r") as fh:
        contents = fh.read()

    all_sections = contents.split(SECTION_DELIMITER)

    if len(all_sections) != len(SECTION_NAMES):
        raise ValueError(
            f"Error: File '{nlogo_file_path}' does not have the required number of sections."
        )

    with open(section_file_path, "r") as fh:
        replacement_contents = fh.read()

    all_sections[sindex] = replacement_contents

    # write the file
    with open(output_file_path, "w") as fh:
        contents = SECTION_DELIMITER.join(all_sections)
        fh.write(contents)


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
        help=f"name of the .nlogo section to be replaced. valid names are {SEC_NAMES_STRING}",
    )
    parser.add_argument(
        "-s",
        "--section-file",
        dest="section_file",
        help="path to .nlogo replacement section file",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output-file",
        dest="output_file",
        help="path to .nlogo file with replaced section",
        required=True,
    )
    args = parser.parse_args()
    replace_nlogo_section(
        args.input_file, args.section_name, args.section_file, args.output_file
    )


if __name__ == "__main__":
    main()
