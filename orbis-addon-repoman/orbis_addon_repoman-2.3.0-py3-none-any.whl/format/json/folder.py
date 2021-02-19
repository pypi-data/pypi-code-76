import pathlib
import json


def iterate_over_json_files(download_destination):
    folder = pathlib.Path(download_destination)
    for file in list(folder.glob('*.json')):
        with open(file, "r") as open_file:
            yield json.load(open_file), file
