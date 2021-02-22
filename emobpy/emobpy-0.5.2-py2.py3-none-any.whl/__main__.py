import argparse

try:
    from emobpy.tools import copy_to_user_data_dir, create_project
except ImportError as exc:
    raise ImportError(
        "Couldn't import emobpy. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc


def parser():
    argcollect = argparse.ArgumentParser(description="emobpy command line")
    # add positional argument create_project and run
    argcollect.add_argument(
        "command",
        help='Start with this script "emobpy create -n [here a name]"',
        type=str,
    )
    argcollect.add_argument(
        "-n",
        "--name",
        help='Required argument for "create". A project name must be provided',
        type=str,
    )
    argcollect.add_argument(
        "-t",
        "--template",
        help="""Required argument for "create". Examples can be selected through templates,
        name of templates are eg1, eg2 ...""",
        type=str,
    )

    args = argcollect.parse_args()
    return args


def main():
    arg_option = ["create"]
    args = parser()
    if not args.command in arg_option:
        raise Exception(f"First positional argument must be {arg_option}")
    if args.command == "create":
        if args.name:
            if args.template:
                tmpl = args.template
            else:
                tmpl = "base"
            copy_to_user_data_dir()
            create_project(args.name, tmpl)
            return None
        else:
            raise Exception(
                "create is an argument that must have a project name as -n argument"
            )


if __name__ == "__main__":
    main()
