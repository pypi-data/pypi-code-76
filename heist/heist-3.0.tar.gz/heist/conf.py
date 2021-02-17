import os
from typing import Dict


def _get_defaults() -> Dict[str, str]:
    defaults = {
        "posix": {
            "config": "/etc/heist/heist.conf",
            "rosters": "/etc/heist/rosters",
            "artifacts": "/var/tmp/heist/artifacts",
        },
        "nt": {
            "config": "C:\\heist\\heist.conf",
            "rosters": "C:\\heist\\rosters",
            "artifacts": "C:\\heist\\artifacts",
        },
    }.get(os.name, {})

    return defaults


OS_DEFAULTS = _get_defaults()

CLI_CONFIG = {
    "config": {"options": ["-c"], "subcommands": ["_global_"]},
    "acct_profile": {"subcommands": ["_global_"]},
    "artifacts_dir": {"subcommands": ["_global_"]},
    "roster": {"subcommands": ["_global_"]},
    "roster_dir": {"subcommands": ["_global_"]},
    "roster_file": {"options": ["-R"], "subcommands": ["_global_"]},
    "checkin_time": {"subcommands": ["_global_"]},
    "dynamic_upgrade": {"subcommands": ["_global_"]},
    "renderer": {"subcommands": ["_global_"]},
    "target": {"options": ["--tgt", "-t"], "subcommands": ["_global_"]},
    "artifact_version": {"options": ["-a, --artifact"], "subcommands": ["_global_"]},
    "service_plugin": {"options": ["-s", "--service"], "subcommands": ["_global_"]},
    # ACCT options
    "acct_file": {"source": "acct", "os": "ACCT_FILE", "subcommands": ["_global_"]},
    "acct_key": {"source": "acct", "os": "ACCT_KEY", "subcommands": ["_global_"]},
}
CONFIG = {
    "config": {
        "default": OS_DEFAULTS.get("config"),
        "help": "Heist configuration location",
    },
    "acct_profile": {
        "default": "default",
        "help": "The specific named profile to read from encrypted acct files",
    },
    "artifacts_dir": {
        "default": OS_DEFAULTS.get("artifacts"),
        "help": "The location to look for artifacts that will be sent to target systems",
    },
    "roster": {
        "default": None,
        "help": "The type of roster to use to load up the remote systems to tunnel to",
    },
    "roster_dir": {
        "default": OS_DEFAULTS.get("rosters"),
        "help": "The directory to look for rosters",
    },
    "roster_file": {
        "options": ["-R"],
        "default": "",
        "help": "Use a specific roster file, "
        "if this option is not used then the roster_dir will be used to find roster files",
    },
    "checkin_time": {
        "default": 60,
        "type": int,
        "help": "The number of seconds between checking to see if the managed system needs to get an updated binary "
        "or agent restart.",
    },
    "dynamic_upgrade": {
        "default": False,
        "action": "store_true",
        "help": "Tell heist to detect when new binaries are available and dynamically upgrade target systems",
    },
    "renderer": {
        "default": "yaml",
        "help": "Specify the renderer to use to render heist roster files",
    },
    "target": {
        "options": ["--tgt", "-t"],
        "default": "",
        "help": "target used for multiple rosters",
    },
    "artifact_version": {
        "default": "",
        "help": "Version of the artifact to use for heist",
    },
    "roster_defaults": {
        "default": {},
        "type": dict,
        "help": "Defaults options to use for all rosters. CLI options will"
        "override these defaults",
    },
    "service_plugin": {
        "default": "",
        "help": "The type of service to use when managing the artifacts service status",
    },
}
SUBCOMMANDS = {
    # The manager determines how you want to create the tunnels and if you want to deploy
    # ephemeral agents to the remote systems
    "grains": {x: "" for x in ("help", "desc")}
}
DYNE = {
    "acct": ["acct"],
    "artifact": ["artifact"],
    "heist": ["heist"],
    "roster": ["roster"],
    "service": ["service"],
    "tunnel": ["tunnel"],
}
