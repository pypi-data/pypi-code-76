import argparse
from .legacy import dump1


def cli():
    parser = argparse.ArgumentParser(description="BOMIST Legacy Utilities")
    parser.add_argument("--dump1", default=False, action="store_true")
    parser.add_argument("--ws", help="Workspace path")
    parser.add_argument("--out", help="Output file path")
    args = parser.parse_args()

    if args.dump1:
        if not args.ws:
            parser.error("--ws is required")
        dump1(args.ws, args.out)
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
