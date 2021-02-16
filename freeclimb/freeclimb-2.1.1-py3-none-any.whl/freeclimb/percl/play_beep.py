import enum

class PlayBeep(enum.Enum):
    ALWAYS = "entryOnly"
    NEVER = "never"
    ENTRY_ONLY = "entryOnly"
    EXIT_ONLY = "exitOnly"