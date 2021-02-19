#! /usr/bin/env python3


import os
import re
import csv
import json
import logging
from pathlib import Path

from . import constants


logger = logging.getLogger(__name__)
logger.setLevel(constants.LOG_LEVEL)

file_handler = logging.FileHandler(constants.FO_LOG)
formatter = logging.Formatter(constants.FO_FORM)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class FileOperator():
    """Source file that contains items."""

    def __init__(self, path, filetype=False):
        """Initializes path."""

        logger.debug(f'[INIT] Path is: "{path}"')
        self.__path = self.__resolvePath(path)
        self.__checkFile(self.__path)
        self.__filetype = self.__getFiletype(filetype)

    def __getFiletype(self, filetype):
        """Tries to guess the filetype from filename."""

        if filetype:
            ext = filetype
            logger.debug('[GET] File extension provided')
        else:
            reg = re.compile(r'.*\.([^\s^\.]+)$')
            if reg.match(str(self.__path)):
                ext = reg.match(str(self.__path)).groups()[0]
                logger.debug('[GET] Guessed file extension')
            else:
                ext = False
                logger.debug('[GET] File extension not resolved')
        logger.debug(f'[GET] File extension: "{ext}"')
        return ext

    def __resolvePath(self, path):
        """Resolves path OS independently."""

        p = Path.resolve(Path.expanduser(Path(path)))
        logger.debug(f'[RESOLVE] Given absolute path: "{p}"')
        return p

    def __checkFile(self, path):
        """Checks that file exists and creates it and path."""

        if not Path.exists(path):
            base = path.parents[0]
            if not Path.exists(base):
                os.makedirs(base)
                logger.info(f'[CHECK] Created directory "{base}" for sources.')

            with open(path, 'a'):
                pass
            logger.info(f'[CHECK] Created file "{path}" for sources.')
        else:
            logger.debug(f'[CHECK] "{path}" found.')

    def __fileEmpty(self, path):
        """Checks if file is empty."""

        if os.stat(path).st_size == 0:
            return True
        return False

    def loadFile(self, singleLayer=False):
        """Loads data from file.

        If given or guessed filetype is found then correct method is
        used to load data from file.

        Emptry string is returned if file is empty.

        Known filetypes: json, txt, csv.
        """

        if self.__fileEmpty(self.__path):
            logger.debug('[LOAD] File is empty')
            return ''

        if self.__filetype == 'json':
            with open(self.__path, 'r') as f:
                data = json.load(f)
            logger.debug('[LOAD] json loaded')

        elif self.__filetype == 'txt':
            with open(self.__path, 'r') as f:
                data = f.read()
            logger.debug('[LOAD] txt loaded')

        elif self.__filetype == 'csv':
            with open(self.__path, 'r', newline='') as f:
                csv_data = csv.reader(f, delimiter=',')
                data = list(csv_data)
            if singleLayer:
                data = [item for sublist in data for item in sublist]
            logger.debug(f'[LOAD] csv loaded, singleLayer={singleLayer}')

        # only for extreme debug situations
        # logger.debug(f'[LOAD] data: "{data}"')
        return data

    def saveFile(self, data=False):
        """Saves data to file.

        If given or guessed filetype is found then correct method is
        used to write given data.

        Empty data can be written to any filetype.

        Known filetypes: json, txt, csv.
        """

        if data:
            if self.__filetype == 'json':
                with open(self.__path, 'w') as f:
                    json.dump(data, f)

            elif self.__filetype == 'txt':
                with open(self.__path, 'w') as f:
                    f.write(data)

            elif self.__filetype == 'csv':
                with open(self.__path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
            logger.debug(f'[SAVE] {self.__filetype} saved')

        else:
            with open(self.__path, 'w') as f:
                f.write('')
            logger.debug(f'[SAVE] "" to: "{self.__path}"')
