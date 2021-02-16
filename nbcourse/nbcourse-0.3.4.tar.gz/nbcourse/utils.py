import shutil
from pathlib import Path
from zipfile import ZipFile
import inspect
import os
import re

IGNORED = '__pycache__'


def update_material(src: Path, dst: Path):
    """Remove dst tree then update with src"""
    shutil.rmtree(dst, ignore_errors=True)
    try:
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(IGNORED))
    except NotADirectoryError:
        try:
            shutil.copy(src, dst)
        except FileNotFoundError:
            Path(dst.parent).mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)


def get_file_list(path: Path, relative=True, ignore: list = None):
    """Return a list of file paths relative to path"""
    ignored = set([IGNORED]) | {ignore}

    def get_path(obj):
        """return a relative or absolute path"""
        return obj.relative_to(path) if relative else obj

    return [get_path(obj) for obj in path.glob('**/*')
            if (obj.is_file() and ignored.isdisjoint(obj.parts))]


def clean_tree(target: Path):
    """Clean tree ignoring errors"""

    def remove_parent(path: Path):
        """Remove parent directory recursively if empty"""
        parent = path.parent
        if str(parent) != '.' and not os.listdir(parent):
            parent.rmdir()
            remove_parent(parent)

    if target.is_file():
        target.unlink()
        remove_parent(target)

    else:
        shutil.rmtree(target, ignore_errors=True)


def update_dict(current: dict, new: dict):
    """Update current multi-level dict with new dict"""
    for k, v in new.items():
        if k in current and type(current[k]) is dict and type(v) is dict:
            # Update current entry by descending into sub dict
            update_dict(current[k], v)
        else:
            # Add new entry or update with new value
            current[k] = v


def zip_files(zip_file_name: Path, paths_to_zip: list,
              ref_to_arc: tuple = None):
    """
    Archive files_to_zip in zip file

    :param paths_to_zip: a list of files to be archived
    :param zip_file_name: the archive filename
    :param ref_to_arc: a ('refpath', 'arcdir') tuple
    """
    if ref_to_arc:
        refpath = ref_to_arc[0]
        arcdir = ref_to_arc[1]

    with ZipFile(zip_file_name, 'w') as zf:
        for path in paths_to_zip:
            # Convert refpath/file in arcdir/file if asked
            arcpath = arcdir / path.relative_to(refpath) \
                      if ref_to_arc else None
            zf.write(path, arcname=arcpath)


def get_functions(namespace, pattern: str) -> list:
    """
    Return the list of functions in namespace that match the regex pattern
    """
    all_functions = inspect.getmembers(namespace, inspect.isfunction)
    p = re.compile(pattern)
    functions = []
    for function, dummy in all_functions:
        m = p.match(function)
        if m:
            functions.append(m.group(1))
    return functions
