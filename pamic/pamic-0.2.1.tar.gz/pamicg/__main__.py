from importlib import metadata

from .app import App
from os.path import dirname

import sys


def main():
    setup = {}

    try:
        m = metadata.metadata('pamic')
        setup["name"] = m['Name']
        setup["description"] = m['Summary']
        setup["version"] = m['Version']

    except metadata.PackageNotFoundError:
        setup["name"] = "pamicg (dev version)"
        setup["description"] = "this will come from setup.cfg"
        setup["version"] = setup["description"]

    setup['gladefile'] = dirname(__file__) + "/pamicg.glade"

    for arg in sys.argv[1:]:
        if arg == "--load-cl" or arg == "--no-gui":
            setup[arg[2:]] = True

    pamicg = App(setup)
    pamicg.run()


if __name__ == "__main__":
    main()
