import pandas as pd
import pkg_resources
from shutil import copyfile


def load(file):
    # Ensure file has .zip extension
    file += '.zip' * (not file.endswith('.zip'))

    # Path to data relative to package
    data_path = f'data/{file}'

    # Absolute path to data
    abs_path = pkg_resources.resource_filename(__name__, data_path)

    return pd.read_csv(abs_path)


def populate_examples():
    # Get path to files relative to package
    pkg_data = pkg_resources.resource_listdir(__name__, 'data')

    # Drop compressed files
    files = [file for file in pkg_data if not file.endswith('.zip')]

    # Copy files to current dir
    for file in files:
        abs_path = pkg_resources.resource_filename(__name__, f'data/{file}')
        copyfile(abs_path, file)
        print(f'\nCreated file {file} in current directory.\n')
