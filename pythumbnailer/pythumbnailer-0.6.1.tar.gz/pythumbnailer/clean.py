#!/usr/bin/env python
from pathlib import Path
from shutil import rmtree
import argparse
import logging

from . import pypublish

logger = logging.getLogger(__name__)


def __main__():
    parser = argparse.ArgumentParser(description='Remove "pypublish" creations')

    parser.add_argument('-f', '--rm',
                        action='store_true',
                        help='Effectively delete the files')
    args = parser.parse_args()

    if not args.rm:
        logger.info('Dry-Run, listing only the files to delete')

    for o in pypublish.OUTPUT_PATHS:
        opath = Path(o)
        if opath.exists():
            print(opath)
            if args.rm:
                # Remove the file, or folder
                if opath.is_dir():
                    rmtree(opath)
                else:
                    opath.unlink()


if __name__ == '__main__':
    import sys
    sys.exit(__main__())
