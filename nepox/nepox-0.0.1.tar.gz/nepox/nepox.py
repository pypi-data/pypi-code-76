from argparse import ArgumentParser
from json import dump
from os import mkdir, path
from subprocess import run


def argparse():
    parser = ArgumentParser(
        prog="Nepo",
        description="How many more projects do you want to start without finishing it?",
        usage=("nepox project-name"),
        epilog="Example: nepox cool-cats -e sublime --no-venv",
    )
    parser.add_argument("name", help="project name")
    parser.add_argument("-v", "--venv", help="virtual environment name", default=".env")
    parser.add_argument(
        "-e",
        "--editor",
        help="editor name to additional files",
        choices=("sublime", "sublime-terminus"),
        required=False,
    )
    parser.add_argument(
        "--no-venv", help="project with no virtual environment", action="store_true"
    )
    parser.add_argument(
        "-V",
        "--version",
        help="script version",
        action="version",
        version="nepo v0.0.1",
    )
    return parser.parse_args()


def sublime(full_path, project_name, main_file, venv_name, terminus, venv):
    return {
        "folders": [
            {
                "path": full_path,
                "folder_exclude_patterns": [venv_name],
                "file_exclude_patterns": [],
            }
        ],
        "build_systems": [
            {
                "name": project_name,
                "working_dir": "$folder",
                "cmd": ["$folder/.env/bin/python3" if venv else "python3", main_file],
            }
        ]
        if not terminus
        else [
            {
                "name": project_name,
                "title": project_name,
                "working_dir": "$folder",
                "cmd": ["$folder/.env/bin/python3" if venv else "python3", main_file],
                "target": "terminus_open",
                "cancel": "terminus_cancel_build",
                "auto_close": False,
            }
        ],
    }


def main():
    # variables
    args = argparse()
    curdir = path.abspath(path.curdir)
    full_path = path.join(curdir, args.name)
    main_file = f"{args.name.lower().replace('-', '_')}.py"
    editor = args.editor
    venv_name = args.venv

    # creation
    if not path.exists(full_path):
        mkdir(full_path)
    run(["python3", "-m", "venv", path.join(full_path, venv_name)])
    open(path.join(full_path, main_file), "w").write(
        "#!/usr/bin/env python3"
        if args.no_venv
        else f"#!{path.join(full_path,venv_name)}/bin/python3"
    )

    # editors
    if editor == "sublime":
        dump(
            sublime(
                full_path,
                args.name,
                main_file,
                venv_name,
                terminus=False,
                venv=not args.no_venv,
            ),
            open(f"{full_path}/{args.name}.sublime-project", "w"),
            indent=4,
        )
    elif editor == "sublime-terminus":
        dump(
            sublime(
                full_path,
                args.name,
                main_file,
                venv_name,
                terminus=True,
                venv=not args.no_venv,
            ),
            open(f"{full_path}/{args.name}.sublime-project", "w"),
            indent=4,
        )


if __name__ == "__main__":
    main()
