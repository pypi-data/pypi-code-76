# type: ignore
"""This files holds utility functions from external sources."""

import os
import tempfile
from shutil import move

# The following code comes from a pull-request to Python:
# https://github.com/python/cpython/pull/14464/files
#
# The code is licensed under the Python Software Foundation License Version 2:
# https://github.com/python/cpython/blob/master/LICENSE

# This code can be removed once the functionality is available in distributed Python.


def _create_or_replace(dst, create_temp_dst):
    """Create or overwrite file `dst` atomically via os.replace.
    The file to replace `dst` is first created with a temporary pathname.
    `create_temp_dst` is a callable taking a single argument: a pathname
    where the temporary file to replace `dst` should be created.  If it
    raises FileExistsError, it will be called again with another temp pathname.
    """
    # Following import can't be at module level: to build standard modules,
    # setup.py uses argparse which uses shutil.get_terminal_size().
    # tempfile imports random which imports math which isn't available

    try:
        # Loop until successful creation of previously non-existent temp pathname
        while True:
            temp_path = ""  # Avoid later NameError if mktemp raises exception
            # Deprecated mktemp is used because the pathname must not already
            # exist in the case of os.link and os.symlink.
            temp_path = tempfile.mktemp(dir=os.path.dirname(dst))
            try:
                create_temp_dst(temp_path)
                break  # Success - no exception raised
            except FileExistsError:
                # Race condition: temporary pathname was created after generation
                pass  # Try again

        try:
            os.replace(temp_path, dst)  # If successful, POSIX guarantees atomicity
        except FileExistsError:  # Windows raises this if dst exists
            move(temp_path, dst)

    except BaseException as e:
        if os.path.lexists(temp_path):
            os.remove(temp_path)
        raise e


# pylint: disable=cell-var-from-loop
def _link_or_symlink(os_method, srcs, dst, **kwargs):
    """Create either links or symlinks based upon the value of `os_method`.
    Helper function for link and symlink.
    `os_method` must be either os.link or os.symlink
    """
    if isinstance(srcs, str) or not hasattr(srcs, "__iter__"):
        sources = [srcs]  # We have been given a single source
        dst_is_dir = False
    else:  # We have been given an iterable of sources
        sources = srcs
        dst_is_dir = True

    bool_args = {
        os.link: ("overwrite", "follow_symlinks"),
        os.symlink: ("overwrite", "target_is_directory"),
    }
    for bool_arg in bool_args[os_method]:
        if not isinstance(kwargs[bool_arg], bool):
            raise TypeError(f"{bool_arg} not a bool")
    os_method_args = {k: kwargs[k] for k in kwargs if k != "overwrite"}

    for target in sources:
        if dst_is_dir:
            link_name = os.path.join(dst, os.path.basename(target))
        else:
            link_name = dst

        def create_link_at(here):
            os_method(target, here, **os_method_args)

        if kwargs["overwrite"]:
            _create_or_replace(link_name, create_link_at)
        else:
            create_link_at(link_name)


def symlink(srcs, dst, *, overwrite=False, target_is_directory=False):
    """Create symbolic link(s) in `dst` pointing at `srcs`.
    Given a iterable of sources, `dst` must be a directory and links to
    each source are created inside `dst`.
    Given a single source, `dst` is taken to be a file, even if it is a
    symlink to a directory. This allows for:
     - Enforcing that a link is created as `dst` rather than `dst`/src
     - Replacing symlinks to directories (with `overwrite=True`)
    With `overwrite=False`, FileExistsError is raised if the destination
    pathname already exists in any form.
    With `overwrite=True`, overwrite an existing destination.
     - Raises IsADirectoryError if `dst` is a directory
     - Symlinks to directories are treated as files and overwritten
       - To dereference a linked directory, use "link/"
    On Windows, a symlink represents either a file or a directory, and does
    not morph to the target dynamically. If the target is present, the type
    of the symlink will be created to match. Otherwise, the symlink will be
    created as a directory if `target_is_directory` is True or a file
    symlink (the default) otherwise. On non-Windows platforms,
    `target_is_directory` is ignored.
    """
    _link_or_symlink(
        os.symlink, srcs, dst, overwrite=overwrite, target_is_directory=target_is_directory
    )
