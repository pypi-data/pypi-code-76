import os
import sys

from .util import package_from_path

def show_python_paths():
    return '\n'.join(sys.path)

def add_package(path_to_package):
    package_name, package_path = package_from_path(path_to_package)

    if package_name:
        sys.path.insert(0, package_as_path)
        return package_name

    else:
        sys.stderr.write(f'Sorry, invalid package: {path_to_package}\n')
        return ''

def try_import(package_name, fallback_path=''):
    try:
        import package_name

    except:
        sys.stderr.write(f'Sorry, unable to import {package_name}\n')

    # Just return if no fallback path was provided
    if not fallback_path: return ''

    sys.stdout.write(f'Attempting fallback: {fallback_path}')

    imported_name = add_package(fallback_path)
    if not imported_name:
        sys.stdout.write('Importing fallback was unsuccessful\n')
        return ''

    else:
        sys.stdout.write(f'Successfully imported: "{imported_name}"\n')
        return imported_name
