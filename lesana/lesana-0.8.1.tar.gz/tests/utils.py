import shutil
import sys


def copytree(src, dest, dirs_exist_ok=False):
    """
    Helper function to remove existing directories

    Used in the tests for compatibility with python < 3.8
    """
    if sys.version_info >= (3, 8):
        shutil.copytree(src, dest, dirs_exist_ok=dirs_exist_ok)
    else:
        if dirs_exist_ok:
            if not dest.startswith('/tmp'):
                raise ValueError("Refusing to delete a directory outside /tmp")
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
