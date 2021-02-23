import os
from pathlib import Path

PACKAGE_DATA_PATH = os.path.join(Path().absolute(), 'Data')


def get_Directory():
    if not os.path.isdir(PACKAGE_DATA_PATH):
        os.mkdir(PACKAGE_DATA_PATH)
        print("\n----------> Folder Data Did not exist... CREATED NEW ONE")

    return PACKAGE_DATA_PATH
