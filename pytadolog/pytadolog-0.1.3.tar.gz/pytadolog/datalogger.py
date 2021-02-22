#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Contains datalogger classes for PyTado.'''

import concurrent.futures
import getpass
import json
import logging
import multiprocessing
import pathlib
import sched
import time
from urllib.error import HTTPError, URLError

import keyring
import numpy as np

from .datastores import DataStore, MPDataStore
from .extended_interface import TadoExtended
from .utils import nexttick, loglistener, setuplogger, setupoutdir


_LOGGER = logging.getLogger(__name__)


class TadoLogger:
    '''Periodically requests TaDo data and passes to dataframe.'''
    CREDPATH = pathlib.Path.home() / '.tado_credentials'

    def __init__(self, outdir=None, update_period=30, last_day='sun', multiproc=True, loglevel=logging.WARNING):
        '''Constructs TaDo logger to update at update_periods.

        Args:
            outdir (path like, optional): Output direct to store csvs and logs.
                Defaults to None which places files in <home>/Documents/TadoLogs/.
            update_period (int, optional): Time in seconds between update.
                Defaults to 30.
            last_day (str, optional): Three letter weekday string indicating
                last day of week stored in csv files. Defaults to 'sun'.
            multiproc (bool, optional): Run datastore in another process. 
                Defaults to True.
            loglevel (logging level, optional): Level to log at. Defaults to
                logging.WARNING.
        '''
        self.update_period = update_period
        self.lastday = last_day
        self._multiproc = multiproc
        self._loglevel = loglevel
        self._outdir = setupoutdir(outdir)
        self.event = None  # Will hold next update event
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self._logqueue = multiprocessing.Queue(-1)
        self._stopev = multiprocessing.Event()
        self._loglistener = multiprocessing.Process(
            target=loglistener,
            args=(self._outdir, self._logqueue, self._stopev, self._loglevel),
            )
        self._loglistener.start()
        setuplogger(_LOGGER, self._logqueue, self._loglevel)
        _LOGGER.info('---STARTED TADOLOGGER---')
        self.variables = {
            'Weather': ('Outside Temp (°C)', 'Solar Int. (%)', 'Weather'),
            'Zones': (
                'Temp (°C)', 'R.H. (%)',
                'Set Temp (°C)', 'Heating Power (%)',
                'Open Window'
                ),
            }
        _LOGGER.info('Logging into TaDo server')
        self.login()
        self.zones = sorted(self.home.getZones(), key=lambda z: z["id"])
        _LOGGER.debug('Found %s zones in home', len(self.zones))

        if self._multiproc:
            self._q = multiprocessing.JoinableQueue()
            self.pdstore = MPDataStore(
                self.variables,
                self.zones,
                self._outdir,
                self.update_period,
                self.lastday,
                self._logqueue,
                self._loglevel,
                self._q,
                self._stopev,
                )
        else:
            self.pdstore = DataStore(
                self.variables,
                self.zones,
                self._outdir,
                self.update_period,
                self.lastday,
                self._logqueue,
                self._loglevel,
                )
    
    def __enter__(self):
        _LOGGER.debug('PyTadoLog context manager entered')
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        _LOGGER.debug('PyTadoLog context manager exiting')
        if exc_type is not None:
            _LOGGER.exception(
                'Error encountered during operation',
                exc_info=(exc_type, exc_value, exc_traceback),
                )
        self.close()

    def login(self):
        '''Log in to TaDo mobile server.

        Check if credentials are stored using default OS credentials manager
        and prompts for new credentials if required.
        '''
        if not self.CREDPATH.exists():
            _LOGGER.error(
                'Credentials file cannot be found - Enter Tado credentials',
                )
            self.setcredentials()
        
        loggedin = False
        while not loggedin:
            try:
                with open(self.CREDPATH, mode='r') as f:
                    credentials = json.load(f)
            except json.decoder.JSONDecodeError:
                _LOGGER.error(
                    'Credentials file is corrupted - reenter Tado credentials',
                    )
                self.setcredentials()
            else:
                try:
                    self.home = TadoExtended(
                        credentials['username'],
                        keyring.get_password(
                            credentials['service'], 
                            credentials['username']
                            )
                        )
                except HTTPError:
                    _LOGGER.error(
                        'Tado username or password is incorrect - reenter credentials',
                        )
                    self.setcredentials()
                else:
                    loggedin = True
                    _LOGGER.debug('Logged into TaDo server')

    def setcredentials(self, service='tado'):
        '''Prompt user to enter TaDo login credentials.

        Args:
            service (str, optional): Name of TaDo service in default OS 
                credentials manager. Defaults to 'tado'.
        
        Stores the service name and username in self.CREDPATH.
        '''
        _LOGGER.debug('Requesting TaDo username from user')
        username = str(input('Enter Tado username: '))
        with open(self.CREDPATH, 'w') as f:
            _LOGGER.debug(
                'Saving TaDo credentials details to %s', self.CREDPATH
                )
            json.dump({'service': service, 'username': username}, f)
        keyring.set_password(service, username, getpass.getpass())
        _LOGGER.debug('TaDo credentials stored in OS credentials manager')
    
    def update(self, t):
        '''Get new data and append to dataframe then schedule next update.

        Args:
            t (datetime.datetime): Scheduled time of current update.
        '''
        if self._multiproc:
            self._q.put((t, self.getnewdata()))
        else:
            self.pdstore.update(t, self.getnewdata())

        # Schedule the next update
        start_time = nexttick(self.update_period)
        _LOGGER.debug('Update scheduled for %s', start_time)
        print(f'Next update scheduled for {start_time}', end='\r', flush=True)
        self.event = self.scheduler.enterabs(
            time.mktime(start_time.timetuple()),
            1,
            self.update,
            argument = (start_time, ),
            )
    
    def getnewdata(self):
        '''Get latest data from TaDo server and add to dataframe.
        
        Uses multithreaded pool to get data simultaneously.
        '''
        with concurrent.futures.ThreadPoolExecutor(
                max_workers = len(self.zones) + 1
                ) as executor:
            # Load the operations then wait for them all to complete
            futures = [executor.submit(self.getweatherdata)]
            futures.extend(
                [executor.submit(self.getzonedata, zone) for zone in self.zones]
                )
            futures, _ = concurrent.futures.wait(futures, timeout=30)
            return [future.result() for future in futures]
    
    def getzonedata(self, zone):
        '''Get data on requested zone from TaDo server.

        Args:
            zone (int): ID for TaDo Zone.

        Returns:
            tuple: Tuple containing Zone data.

        Uses try/except clauses to handle server hiccups.
        '''
        try:
            climate = self.home.getClimate(zone['id'])
        except URLError:
            # If the server doesn't respond continue running
            _LOGGER.warning('Could not get climate for %s', zone["name"])
            climate = {'temperature': np.nan, 'humidity': np.nan}
        try:
            state = self.home.getHeatingState(zone['id'])
        except URLError:
            # If the server doesn't respond continue running
            _LOGGER.warning('Could not get heating state for %s', zone["name"])
            state = {'temperature': np.nan, 'power': np.nan}
        try:
            window = self.home.getOpenWindow(zone['id'])
        except URLError:
            # If the server doesn't respond continue running
            _LOGGER.warning('Could not get window state for %s', zone["name"])
            window = np.nan
        
        _LOGGER.debug('Got all data for %s', zone["name"])
        out = (
            zone['name'], (
                climate['temperature'],
                climate['humidity'],
                state['temperature'],
                state['power'],
                window,
                ),
            )
        return ('Zones', out)
    
    def getweatherdata(self):
        '''Get weather data from TaDo server.

        Returns:
            tuple: TaDo weather data.
        
        Uses try/except clauses to handle server hiccups.
        '''
        try:
            data = self.home.getWeather()
            dataout = (
                data['outsideTemperature']['celsius'],
                data['solarIntensity']['percentage'],
                data['weatherState']['value'],
                )
        except URLError:
            # If the server doesn't respond continue running
            _LOGGER.debug('Could not get weather data')
            dataout = (np.nan, np.nan, np.nan)
        out = ('Weather', dataout)
        return ('Weather', out)

    def start(self):
        '''Start running the data logger.

        Sets up the dataframe and schedules the first update.
        '''
        start_time = nexttick(self.update_period)
        self.event = self.scheduler.enterabs(
            time.mktime(start_time.timetuple()),
            1,
            self.update,
            argument = (start_time, ),
            )
        _LOGGER.info('First data point scheduled for %s', start_time)
        if self._multiproc:
            self.pdstore.start()
        self.scheduler.run()

    def close(self):
        '''Clean up any scheduled events.'''
        if self.scheduler is not None:
            if not self.scheduler.empty():
                _LOGGER.debug('Cancelling scheduled event')
                self.scheduler.cancel(self.event)
        
        if self._multiproc:
            self._stopev.set()
            _LOGGER.debug('Set stop event')
            self._q.join()
            _LOGGER.debug('Datastore process stopped')


if __name__ == '__main__':
    import datetime as dt
    
    with TadoLogger() as tl:
        tl.start()
    print(f'Logging ended at {dt.datetime.now()}')
