#! /usr/bin/env python3


import os
import logging
from pathlib import Path


__version__ = '0.20.2'
__author__ = 'obtusescholar'

BASES = {
    'posix': '~/.config/StreamerRetriever/',
    'nt': './config/'}


def getBase():
    str_path = BASES[os.name]
    abs_path = Path.resolve(Path.expanduser(Path(str_path)))
    return abs_path


BASE = getBase()

FOLLOWS = 'follows.csv'
DB = 'streamerretriever.json'
# TWITCH = 'twitch.csv'
TWITCH = 'twitch.json'
GAME_CACHE = 'game_cache.json'
CONFIG = 'cli_conf.json'
# STREAM_LOG = 'stream.log'
# CLI_LOG = 'cli.log'
# FO_LOG = 'fo.log'
# TOOLS_LOG = 'tools.log'


def getLog(log, key):
    logs = {
        'unified': {
            # 'file': 'streamerretriever_cli.log'},
            'file': 'streamerretriever.log'},
        'stream': {
            'file': 'cli_stream.log',
            'tag':  '[STREAM]'},
        'cli': {
            'file': 'cli_cli.log',
            'tag':  '[CLI]'},
        'fo': {
            'file': 'cli_fo.log',
            'tag':  '[FO]'},
        'tools': {
            'file': 'cli_tools.log',
            'tag':  '[TOOLS]'},
        'twitch_request': {
            'file': 'twitch_request.log',
            'tag': '[TWITCH_REQUEST]'},
        'twitch_obj': {
            'file': 'twitch_obj.log',
            'tab': '[TWITCH_OBJ]'}}
    return logs[log][key]


def getLogFile(log):
    # folder = 'logs/'

    # log_folder = Path(BASES[os.name]) / Path(folder)
    log_folder = Path(BASES[os.name])
    # rel_path = log_folder / Path(getLog(log, 'file'))
    rel_path = log_folder / Path(getLog('unified', 'file'))
    abs_path = Path.resolve(Path.expanduser(rel_path))

    return abs_path


LOG_LEVEL = logging.WARNING
STREAM_LOG = getLogFile('tools')
CLI_LOG = getLogFile('gui')
FO_LOG = getLogFile('gui_tools')
TOOLS_LOG = getLogFile('follows')
TWITCH_API_LOG = getLogFile('twitch_request')
TWITCH_OBJ_LOG = getLogFile('twitch_request')


def getLogForm(log):
    log_form = '[%(asctime)s] [%(levelname)s] %(message)s'
    logger_form = '[CLI]' + ' ' + getLog(log, 'tag') + ' ' + log_form
    return logger_form


STREAM_FORM = getLogForm('stream')
CLI_FORM = getLogForm('cli')
FO_FORM = getLogForm('fo')
TOOLS_FORM = getLogForm('tools')
TWITCH_API_FORM = getLogForm('twitch_request')
TWITCH_OBJ_FORM = getLogForm('twitch_request')
