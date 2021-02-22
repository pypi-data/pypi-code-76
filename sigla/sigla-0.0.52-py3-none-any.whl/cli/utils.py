import json
import os
import textwrap
from pathlib import Path
from shutil import copyfile

from core import ensure_dirs, load_xml_from_file
from core.outputs.OutputFile import OutputFile
from core.importers import import_from_xml_string


def new_definition_template(name):
    return textwrap.dedent(
        f"""\
    <root>
        <file to="output/{name}[.ext]">
            <{name}>
                [...]
            </{name}>
        </file>
    </root>
"""
    )


def cli_run_definition(p):
    print(f":: Reading {p}")

    with open(p, "r") as h:
        str_xml = h.read()

    print("|> before stuff")

    stuff = import_from_xml_string(str_xml)()
    print("|> stuff", stuff)

    for s in stuff:
        if isinstance(s, OutputFile):
            print(f":: Saving {s.path}")
            s.save()
        else:
            print("\n" * 1)
            print(":: template to output")
            print(s.content)


def cli_read_snapshot_definition(file):
    print(f":: Loading {file}")
    doc = load_xml_from_file(file)
    print(f":: Ensure {SNAPSHOTS_DIRECTORY} exists")
    ensure_dirs(SNAPSHOTS_DIRECTORY)
    print(":: Reading tests")
    tests = []
    for test_node in doc.iter("test"):
        files = [test_node.attrib["out"]]

        for out_node in test_node.iter("out"):
            out = out_node.text.strip()
            files.append(out)

        tests.append(
            {"command": test_node.attrib["cmd"], "output_files": files}
        )
    print(f"    ‣ Loaded {len(tests)} commands")
    return tests


def cli_make_snapshots(tests):
    print(":: Making snapshots")
    for test in tests:
        print(f'    ‣ Command {test["command"]}')
        os.system(test["command"])

        for file in test["output_files"]:
            gn = SNAPSHOTS_DIRECTORY + "/" + file

            #
            # MAKING
            #
            ensure_dirs(Path(gn).parent)
            print(f"        ‣ Saving snapshot {file} to {gn}")
            copyfile(file, gn)


def cli_verify_snapshots(tests):
    print(":: Checking snapshots")
    failures = []
    for test in tests:
        print(f'    ‣ Command {test["command"]}')
        os.system(test["command"])

        for file in test["output_files"]:
            gn = SNAPSHOTS_DIRECTORY + "/" + file

            with open(file, "r") as h:
                current_result = h.read()

            #
            # TESTING
            #
            print(f"        ‣ Checking snapshot {file} against {gn}")
            with open(gn, "r") as h:
                good_result = h.read()

            if good_result != current_result:
                print("        🚩 Snapshot comparison failed")
                failures.append(test["command"])


SNAPSHOTS_DIRECTORY = ".core/snapshots"


def get_default_template_content(context):
    def default_jinja_template(dumped_context):
        return textwrap.dedent(
            f"""
            ---
            some_var: some_value
            ---

            Vars: {dumped_context}

            # render children

            {{{{ node.children() }}}}

            # or

            {{% for child in node.children %}}
                {{{{ child() }}}}
            {{% endfor %}}

            """
        ).strip()

    json_context = json.dumps(list(context.keys()))
    return default_jinja_template(json_context)