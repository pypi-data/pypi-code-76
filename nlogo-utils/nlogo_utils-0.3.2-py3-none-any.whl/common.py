"""
Shared values across package modules
"""

SECTION_DELIMITER = "@#$#@#$#@"

# {name: alias}
# names are those found in the NetLogo source code as of 20210213
# aliases are used for section files names and for the command line options
SECTIONS_NAMES = {
    "code": "code",
    "interface": "interface",
    "info": "info",
    "turtleshapes": "turtleshapes",
    "version": "version",
    "previewcommands": "previewcommands",
    "systemdynamics": "systemdynamics",
    "behaviorspace": "behaviorspace",
    "hubnetclient": "hubnetclient",
    "linkshapes": "linkshapes",
    "modelsettings": "modelsettings",
    "deltatick": "deltatick",
}

SECTION_ALIASES = SECTIONS_NAMES.values()

DEFAULT_SECTION_DIR = "%s.sections"

SECTION_FILE_SUFFIX = ".nlsec"
