"""Main application called by halfling script."""
import argparse
import sys
import toml

from halfling.config import Config
from halfling.exceptions import HalflingError
from halfling.tasks import build, clean

CONFIG_FILEPATH = "halfling.toml"


def run():
    """Collects command line args and runs build/clean task according to args.
    """
    # collect command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("task", type=str, choices=[
                        "build", "clean"], help="task to be run by halfling")
    parser.add_argument("-t", "--type", type=str, choices=["debug", "release"],
                        default="release", help="controls build type; defaults to release")
    parser.add_argument("-j", "--jobs", type=int, default=None,
                        help="controls max processes to run build with; defaults to os.cpu_count()")
    args = parser.parse_args()

    try:
        # load config
        config = Config(**toml.load(CONFIG_FILEPATH))
        # run task
        if args.task == "build":
            build(config, args.type, args.jobs)
        elif args.task == "clean":
            clean(config)

    except FileNotFoundError:
        print(f"{CONFIG_FILEPATH} file not found in current directory.")
        sys.exit(1)
    except toml.TomlDecodeError as exc:
        print(f"Invalid TOML syntax found in {CONFIG_FILEPATH}:\n{exc}")
        sys.exit(1)
    except HalflingError as exc:
        print("\n" + str(exc))
        sys.exit(1)


if __name__ == "__main__":
    run()
