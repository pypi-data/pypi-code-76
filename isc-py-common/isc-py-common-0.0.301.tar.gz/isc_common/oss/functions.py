import os
import shutil


def mekeDirs(name, logger, mode=0o777, exist_ok=False):
    try:
        os.makedirs(name=name, exist_ok=exist_ok, mode=mode)
        if not os.path.exists(name):
            logger.error(f'dirs: {name} not created.')
            return False
        return True
    except FileNotFoundError:
        logger.error(f'dirs: {name} not created.')
        return False


def copyTwo(src, dst, follow_symlinks=True):
    dir, _file = os.path.split(dst)
    os.chdir(dir)
    try:
        shutil.copy2(src=src, dst=_file, follow_symlinks=follow_symlinks)
        return True
    except FileNotFoundError:
        return False
