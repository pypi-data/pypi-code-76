#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Contains utilities for the TadoLogger package.'''

import datetime as dt
import logging
import logging.handlers
import pathlib

import pandas as pd


def setupoutdir(outdir=None):
    '''Create directory structure for csvs and logs.

    Args:
        outdir (path like, optional): Path to top level directory. Defaults to None.
    
    If outdir is None <home>/Documents/TadoLogs/ is used.
    '''
    if outdir is None:
        outdir = pathlib.Path.home() / 'Documents' / 'TadoLogs'
    else:
        outdir = pathlib.Path(outdir)
    outdir.mkdir(exist_ok=True)
    return outdir


def setuplogger(logger, queue, level=logging.WARNING):
    '''Sets up the TadoLogger logging object.

    Args:
        logger (logging.logger): Python logging object to log to.
        queue (multiprocessing.Queue): Queue to log events to.
        level (logging.level, optional): Global level to log to. Defaults to
            logging.WARNING.
    '''
    logger.setLevel(level)
    logger.addHandler(logging.handlers.QueueHandler(queue))


def getnextday(day='sun'):
    '''Gets date of next occurence of day.

    Args:
        day (str, optional): Three letter weekday to get. Defaults to 'sun'.

    Returns:
        datetime.date: Date of next occurence of day.
    '''
    days = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
    today = dt.date.today()
    offset = (days.index(day.lower()) - today.weekday()) % 7
    # Add 30 seconds so next Sun is returned if it is between Sat 23:59:30 and
    # Sat 23:59:59
    return today + dt.timedelta(days=offset, seconds=30)


def ceildt(inp_dt, delta=30):
    '''Round the input up to the nearest delta in seconds.

    Args:
        inp_dt (datetime.datetime: Input datetime object to round.
        delta (int, optional): Seconds to round the input to. Defaults to 30.

    Returns:
        datetime.datetime: Rounded up datetime.

    Taken from https://stackoverflow.com/a/32724959
    '''
    return inp_dt + (dt.datetime.min - inp_dt) % delta


def nexttick(delta):
    '''Get the next time rounded to delta.

    Returns:
        datetime.datetime: Next time rounded to delta.
    '''
    return ceildt(dt.datetime.now(), dt.timedelta(seconds=delta))


def csv2excel(inpath, outpath=None, dropna=True):
    '''Convert TaDo CSV to Excel file.

    Args:
        inpath (path like): Path to csv file to be converted.
        outpath (path like, optional): Path to output Excel file.
            Defaults to None which uses input file path.
        dropna (bool, optional): Drop NaN rows on save. Defaults to True.
    '''
    df = pd.read_csv(inpath, header=[0, 1], index_col=0, parse_dates=True)
    if outpath is None:
        inpath = pathlib.Path(inpath)
        outpath = inpath.parent / inpath.with_suffix('.xlsx')
    if dropna:
        df.dropna(how='all').to_excel(outpath, freeze_panes=(2, 1))
    else:
        df.to_excel(outpath, freeze_panes=(2, 1))


def loglistener(outdir, queue, stopev, loglevel=logging.INFO):
    '''Collate logs from multiple processes.

    Args:
        outdir (path like): Top level directory in which to store log files.
        queue (Queue): Queue containing logging messages.
        stopev (Event): Event indicating that the process should be closed.
        loglevel (logging.level, optional): Level to log at. Defaults to 
            logging.INFO.
    
    Log files are stored in outdir/logs.
    '''
    outdir = outdir / 'logs'
    outdir.mkdir(exist_ok=True)
    root = logging.getLogger()
    h = logging.handlers.RotatingFileHandler(outdir / 'PyTadoLog.log', 'a', 500e3, 10)
    f = logging.Formatter(
        '[%(asctime)s] [%(processName)-15.15s] [%(name)-10.10s] '
        '[%(levelname)-8s] [%(funcName)-12.12s] %(message)s',
        '%Y-%m-%d %H:%M:%S')
    h.setFormatter(f)
    root.addHandler(h)
    root.setLevel(loglevel)

    while not stopev.is_set():
        try:
            record = queue.get()
            logger = logging.getLogger(record.name)
            logger.handle(record)
        except:
            root.exception('Exception encountered while handling logs')
