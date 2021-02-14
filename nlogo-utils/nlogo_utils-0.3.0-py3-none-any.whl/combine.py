#!/usr/bin/env python

from pathlib import Path
import argparse

from .common import SECTION_DELIMITER, SECTION_ALIASES, SECTION_FILE_SUFFIX

CL_OPTION_TEMPLATE = "%s-file"


def sections_to_nlogo(sections_dir, nlogo_file_path, other_section_files=None):
    """Assemble individual section files into a .nlogo file
    """
    if other_section_files is None:
        other_section_files = dict.fromkeys(SECTION_ALIASES)
    spath = Path(sections_dir).resolve()
    outfile_path = Path(nlogo_file_path).resolve()

    # find all of the section files in the specified directory
    section_files = dict.fromkeys(SECTION_ALIASES)
    for p in spath.glob(f"*{SECTION_FILE_SUFFIX}"):
        sname = p.stem
        if sname in section_files:
            section_files[sname] = p

    # update the mapping based on the other specified files
    for secname, pth in section_files.items():
        other_path = other_section_files[secname]
        if other_path is not None:
            section_files[secname] = other_path

    # assemble list of missing section files
    missing = [
        f"{secname}{SECTION_FILE_SUFFIX}"
        for secname, pth in section_files.items()
        if pth is None
    ]

    if missing:
        smissing = ", ".join(missing)
        raise FileNotFoundError(
            f"Error: The following section files appear to be missing: {smissing}"
        )

    # build .nlogo file
    all_sections = []
    for secname, pth in section_files.items():
        with open(pth, "r") as fh:
            all_sections.append(fh.read())

    with open(nlogo_file_path, "w") as fh:
        contents = SECTION_DELIMITER.join(all_sections)
        fh.write(contents)


def main():
    """Parse the command line arguments and call the appropriate functions
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input-dir",
        dest="input_dir",
        help="path to directory of .nlogo section files",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output-file",
        dest="output_file",
        help="path to the output .nlogo file",
        required=True,
    )
    for sname in SECTION_ALIASES:
        option = CL_OPTION_TEMPLATE % (sname,)
        parser.add_argument(
            f"--{option}", help=f"path to the {sname} section file",
        )

    args = parser.parse_args()
    other_section_files = dict()
    for sname in SECTION_ALIASES:
        # argparse docs: "Any internal - characters will be converted to _
        # characters to make sure the string is a valid attribute name."
        # So, we need to replace any dashes here.
        opt_name = CL_OPTION_TEMPLATE % (sname,)
        opt_name = opt_name.replace("-", "_")
        sdir = getattr(args, opt_name)
        if sdir is not None:
            sdir = Path(sdir).resolve()
        other_section_files[sname] = sdir
    sections_to_nlogo(args.input_dir, args.output_file, other_section_files)


if __name__ == "__main__":
    main()
