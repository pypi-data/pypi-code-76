#!/usr/bin/env python
from pathlib import Path
import os
import argparse
import logging
import subprocess

from . import pypublish
from . import utils

logger = logging.getLogger(__name__)


SUFFIXES = {
    '.JPG': '.jpg',
    '.PNG': '.png',
}
SUFFIX_VIDEO_ARGS = {
    '.mov': ['-movflags', 'use_metadata_tags'],
    '.mpg': [],
}


def __main__():
    parser = argparse.ArgumentParser(description='Remove "pypublish" creations')

    parser.add_argument('--basedir',
                        type=pypublish.Directory, default=Path('.'),
                        help='Base directory to process. Defaults to `%(default)s`')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Show debug messages')
    args = parser.parse_args()

    utils.setup_logging(args.verbose)

    for p in args.basedir.iterdir():
        if p.is_file():
            if p.suffix in SUFFIXES:
                new_name = p.with_suffix(SUFFIXES[p.suffix])
                if not new_name.exists():
                    logger.debug(f'Suffix: Rename "{p}" -> "{new_name}"')
                    p.rename(new_name)
                else:
                    new_name = None
            elif p.suffix.lower() in SUFFIX_VIDEO_ARGS:
                new_name = p.with_suffix('.mp4')
                if not new_name.exists():
                    loglevel = ['-v', 'quiet']
                    if args.verbose:
                        loglevel = []
                    convert_command = [
                        'ffmpeg',
                        *loglevel,
                        '-i', p,
                        *SUFFIX_VIDEO_ARGS[p.suffix.lower()],
                        new_name,
                        '-map_metadata', '0',
                    ]
                    logger.debug(f'{p.suffix.upper()[1:]}: Convert "{p}" -> "{new_name}"')
                    convert_ret = subprocess.call(convert_command)
                    if convert_ret == 0:
                        logger.debug('- Success!')
                        old_stat = p.stat()
                        old_times = (old_stat.st_atime, old_stat.st_mtime)
                        os.utime(new_name, times=old_times)  # touch --reference=
                        p.unlink()
                    else:
                        logger.debug('- Error!')
                else:
                    new_name = None  # Skip


if __name__ == '__main__':
    import sys
    sys.exit(__main__())
