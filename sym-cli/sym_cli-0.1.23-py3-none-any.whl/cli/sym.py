from .helpers.config import init as config_init

config_init("sym")

from .commands import import_all as command_init
from .commands.sym import sym
from .helpers.init import sym_init

command_init()
sym_init()

if __name__ == "__main__":
    sym()
