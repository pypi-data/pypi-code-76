CLI_CONFIG = {
    # The dyne will always be heist.
    # List the subcommands that will expose this option
    "key_plugin": {"subcommands": ["salt.minion"], "dyne": "heist"},
}
CONFIG = {
    # This will show up in hub.OPT.heist.key_plugin
    "key_plugin": {
        "default": "local_master",
        "help": "Define the salt key plugin to use.",
    },
    "accept_keys": {
        "default": False,
        "action": "store_true",
        "help": "Automatically accept the salt minions keys",
    },
    "retry_key_count": {
        "default": 5,
        "help": "Amount of times to retry accepting the salt-key,"
        "while the salt minion is still starting up",
    },
}
SUBCOMMANDS = {"salt.minion": {"help": "", "dyne": "heist"}}
DYNE = {
    "artifact": ["artifact"],
    "heist": ["heist"],
    "salt": ["salt"],
    "service": ["service"],
}
