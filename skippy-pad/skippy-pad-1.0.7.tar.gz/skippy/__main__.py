from prettytable import PrettyTable
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import app
import config

import utils.plugin
import utils.logger


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="print the version - will not run the ui",
    )
    parser.add_argument(
        "-p",
        "--plugins",
        action="store_true",
        help="print plugin list - will not run the ui",
    )

    args = parser.parse_args()

    if args.version:
        utils.logger.log.info(f"skippy v{config.version}")
    elif args.plugins:
        table = PrettyTable()
        table.field_names = ["Alias", "Description", "Author", "Version"]
        sys.path.append(config.PLUGINS_FOLDER)
        for file in utils.plugin.PluginLoader.files():
            plugin = __import__(file).Plugin
            table.add_row(
                [plugin.__alias__, plugin.__description__, plugin.__author__, plugin.__version__]
            )
        print(table)
    else:
        utils.logger.log.info("Skippy was started...")
        app.start_ui()


if __name__ == "__main__":
    run()
