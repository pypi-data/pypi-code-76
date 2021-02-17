"""
Shared values across package modules
"""

SECTION_DELIMITER = "@#$#@#$#@"

# {NetLogo_name, name, index)
# - NetLogo_names are those found in the NetLogo source code as of 20210213
# - names are used for section files names and for the command line options
#   these could be convenient aliases 
# - index is the section number within the .nlogo file 
SECTIONS_NAMES_MAP = [
    ("code", "code", 0),
    ("interface", "interface", 1),
    ("info", "info", 2),
    ("turtleshapes", "turtleshapes", 3),
    ("version", "version", 4),
    ("previewcommands", "previewcommands", 5),
    ("systemdynamics", "systemdynamics", 6),
    ("behaviorspace", "behaviorspace", 7),
    ("hubnetclient", "hubnetclient", 8),
    ("linkshapes", "linkshapes", 9),
    ("modelsettings", "modelsettings", 10),
    ("deltatick", "deltatick", 11),
]

SECTION_NAMES = [sn for (_, sn, _) in SECTIONS_NAMES_MAP]
SECTION_NAME_INDEX = {sn:i for (_, sn, i) in SECTIONS_NAMES_MAP}

SEC_NAMES_STRING = ", ".join((f"'{s}'" for s in SECTION_NAMES))

DEFAULT_SECTION_DIR = "%s.sections"

SECTION_FILE_SUFFIX = ".nlsec"

def check_split(sections_content):
    if len(sections_content) != len(SECTION_NAMES):
        raise ValueError(
            f"Error: File '{nlogo_file_path}' does not have the required number of sections."
        )

def find_section_index(section_name):
    section_name = section_name.strip()
    if section_name not in SECTION_NAMES:
        raise ValueError(
            f"Error: Section name {section_name} is not valid. Valid names are {SEC_NAMES_STRING}."
        )
    else:
        sindex = SECTION_NAME_INDEX[section_name]
    return sindex
