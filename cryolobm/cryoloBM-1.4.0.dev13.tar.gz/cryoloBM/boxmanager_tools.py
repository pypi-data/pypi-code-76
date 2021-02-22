#
# This fiel contains command line cryoloBM_tools for box management
#
import sys
import argparse

PARSER=None


def create_scale_parser(parser):
    scale_required_group = parser.add_argument_group(
        "Required arguments",
        "Scales coordinate files.",
    )

    scale_required_group.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input folder or file.",
    )

    scale_required_group.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output folder where to write the scaled coordinates.",
    )

    scale_required_group.add_argument(
        "-s",
        "--scale",
        type=float,
        required=True,
        help="Scale factor",
    )

    scale_required_group.add_argument(
        "-t",
        "--type",
        required=True,
        choices=["cbox", "coords", "box2D", "box3D","fil-seg"],
        help="Box format you want to convert.",
    )

    scale_required_group.add_argument(
        "-e",
        "--extension",
        required=True,
        help="File name extension of input data.",
    )


def create_parser():
    parent_parser = argparse.ArgumentParser(
        description="Boxmanager Tools",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parent_parser.add_subparsers(help="sub-command help")

    # Config generator
    parser_scale = subparsers.add_parser(
        "scale",
        help="Scales all sort of coordinate files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    create_scale_parser(parser_scale)

    return parent_parser


def _main_():
    global PARSER

    PARSER = create_parser()

    args = PARSER.parse_args()

    if "scale" in sys.argv[1]:
        from cryoloBM_tools import scale
        scale.scale(
            input_path=args.input,
            output_path=args.output,
            input_type=args.type,
            input_ext=args.extension,
            scale_factor=args.scale
                    )


if __name__ == "__main__":
    _main_()