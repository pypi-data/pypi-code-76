#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Contains datastore classes for PyTado.'''

import datetime as dt
import logging
import multiprocessing
import pathlib
import re

import numpy as np
import pandas as pd

from .utils import getnextday, nexttick, setuplogger


_LOGGER = logging.getLogger(__name__)


class DataStore:
    '''Class to manage pandas dataframe.

    CSV files are stored in /usr/Documents/TaDoLogs.
    '''
    DATEPATTERN = re.compile(r'\d{4}-\d{2}-\d{2}')

    def __init__(self, variables, zones, outdir, delta, lastday, logqueue, loglevel=logging.WARNING):
        '''Initialise datastore. Sets up columns based on vars and zones

        Args:
            variables (list of dicts): List of variables to use for columns.
            zones (List of dicts): List of zones in TaDo home.
            outdir (pathlib.Path): Directory to hold CSV files.
            delta (int): Time in seconds between rows in dataframe.
            last_day (str, optional): Three letter weekday string indicating 
                last day of week stored in csv files. Defaults to 'sun'.
            logqueue(multiprocessing.queue): Queue to hold logging.logger logs.
            loglevel (logging level, optional): Level to log at. Defaults to
                logging.WARNING.
        '''
        self.variables = variables
        self.zones = zones
        self.outdir = outdir
        self.delta = delta
        self.lastday = lastday
        self.csvpath = None  # Will hold path to current csv file
        self.lastindex = None  # Will hold last index in dataframe
        self.df = None  # Will hold dataframe
        setuplogger(_LOGGER, logqueue, loglevel)

        _LOGGER.debug('Creating output directory at %s', self.outdir)
        self.outdir.mkdir(exist_ok=True)
        self.setupdf()
    
    def setupdf(self):
        '''Sets up the dataframe object to hold TaDo data.

        Looks for existing suitable csv files and loads them if present.
        '''
        self.csvpath_setter()

        weather_cols = pd.MultiIndex.from_product(
            (['Weather'], self.variables['Weather']),
            names=['Zone', 'Variable'],
            )
        zone_cols = pd.MultiIndex.from_product(
            ([zone['name'] for zone in self.zones], self.variables['Zones']), 
            names=['Zone', 'Variable'],
            )
        columns = weather_cols.append(zone_cols)

        # Check if the supplied csv path is a file and in the correct format
        df_loaded = False
        if self.csvpath.exists():
            _LOGGER.debug('Found file at %s', self.csvpath)
            self.df = pd.read_csv(
                self.csvpath, 
                header = [0, 1], 
                index_col = 0, 
                parse_dates = True,
                )
            _LOGGER.debug('Loaded csv file into dataframe')
            if self.df.columns.equals(columns):
                _LOGGER.debug('Columns in csv file match expected format')
                extended_idx = pd.date_range(
                    start = self.df.index[0], 
                    end = self.lastindex,
                    freq=f'{self.delta}S',
                    )
                self.df = self.df.reindex(extended_idx)
                _LOGGER.debug('Extended dataframe index to %s', self.lastindex)
                # Add an empty row to indicate a gap at the next tick
                self.addemptyrow()
                df_loaded = True
            else:
                # Rename the old file so it is not overwritten and create a new
                # file with all required columns
                _LOGGER.warning('csv file does not match expected format')
                self.csvpath.rename(
                    self.csvpath.parent / f'{self.csvpath.stem}_old.csv'
                    )
                _LOGGER.info('Old csv file renamed to %s_old.csv', self.csvpath.stem)

        if not df_loaded:
            _LOGGER.debug('Creating new dataframe')
            index = pd.date_range(
                start = nexttick(self.delta),
                end = self.lastindex,
                freq=f'{self.delta}S',
                )
            self.df = pd.DataFrame(index=index, columns=columns)
            self.df.to_csv(self.csvpath)
        
    def update(self, t, data):
        '''Add a new entry to dataframe at row with index t.

        Args:
            t (datetime.datetime): Row index for new data.
            data (list of dicts): List of data dictionaries.
        '''
        if t > self.lastindex:
            self.setupdf()
        for d in data:
            key, result = d
            for i, var in enumerate(self.variables[key]):
                self.df.loc[t, (result[0], var)] = result[1][i]
        self.save()
        _LOGGER.debug('Saved to csv')
    
    def save(self, dropna=True):
        '''Save dataframe to csv file.

        Args:
            dropna (bool, optional): Drop NaN rows on save. Defaults to True.
        '''
        if dropna:
            self.df.dropna(how='all').to_csv(self.csvpath)
            _LOGGER.debug('Dropped NA rows from dataframe and saved to csv')
        else:
            self.df.to_csv(self.csvpath)
            _LOGGER.debug('Saved to csv')
    
    def csvpath_setter(self):
        '''Set path to csv datastore.

        Loooks for existing datastores and uses the latest one if available.
        If there are no suitable ones it will create a path to a new one.
        '''
        today = dt.date.today()
        viable_files = []
        _LOGGER.debug('Searching for viable csv files in %s', self.outdir)
        for path in self.outdir.glob('HomeData(*_to_*).csv'):
            start, end = [
                dt.datetime.strptime(date, '%Y-%m-%d').date() 
                for date in self.DATEPATTERN.findall(path.stem)
                ]
            if start <= today <= end:
                _LOGGER.debug('Found matching file with name %s', path.stem)
                viable_files += [(path, start, end)]
        if not viable_files:
            # Create a new file if there is no existing file
            _LOGGER.debug('No viable files found')
            self.lastindex = dt.datetime.combine(
                getnextday(self.lastday), 
                dt.time(23, 59, 59)
                )
            self.csvpath = self.outdir / f'HomeData({today}_to_{self.lastindex.date()}).csv'
        else:
            _LOGGER.debug('Found %s viable files', len(viable_files))
            if len(viable_files) > 1:
                viable_files = sorted(
                    viable_files,
                    reverse=True,
                    key=lambda tup: (tup[2], tup[1]),
                    )[0][0]
            self.lastindex = dt.datetime.combine(
                viable_files[0][2], 
                dt.time(23, 59, 59)
                )
            self.csvpath = viable_files[0][0]
        _LOGGER.debug('Using csv file with name %s', self.csvpath)
    
    def addemptyrow(self):
        '''Insert a row of inifinities to indicate a break in data logging.
        '''
        # Create row at previous delta time
        start_time = nexttick(self.delta) - dt.timedelta(seconds=self.delta)
        if start_time > self.lastindex:
            self.setupdf()
        elif start_time > self.df.index[0]:
            self.df.loc[start_time] = np.inf
            self.save()
            _LOGGER.debug('Added inf row to dataframe at %s', start_time)


class MPDataStore(multiprocessing.Process, DataStore):
    '''Multiprocessing version of datastore.
    '''
    def __init__(
            self,
            variables,
            zones,
            outdir,
            delta,
            lastday,
            logqueue,
            loglevel=logging.WARNING,
            q = None,
            stopev = None,
            ):
        '''Initialise multiprocessing datastore.

        Args:
            variables (list of dicts): List of variables to use for columns.
            zones (List of dicts): List of zones in TaDo home.
            outdir (pathlib.Path): Directory to hold CSV files.
            delta (int): Time in seconds between rows in dataframe.
            last_day (str, optional): Three letter weekday string indicating
                last day of week stored in csv files. Defaults to 'sun'.
            logqueue(Queue): Queue to hold logging.logger logs.
            loglevel (logging level, optional): Level to log at. Defaults to
                logging.WARNING.
            q (JoinableQueue, optional): Queue which will hold data. Defaults
                to None.
            stopev (multiprocessing.Event, optional): Event which will signal 
                to stop processing. Defaults to None.
        '''
        multiprocessing.Process.__init__(self)
        self._variables = variables
        self._zones = zones
        self._outdir = outdir
        self._delta = delta
        self._lastday = lastday
        self._logqueue = logqueue
        self._loglevel = loglevel
        self._q = q
        self._stopev = stopev
        
    def run(self):
        '''Wait for data in queue and update datastore when available.
        '''
        DataStore.__init__(self, self._variables, self._zones, self._outdir, self._delta, self._lastday, self._logqueue, self._loglevel)
        while not self._stopev.is_set():
            self.update(*self._q.get())
            self._q.task_done()
