import getpass
import os
import urllib.parse
import urllib.request
from collections import namedtuple
from distutils.util import strtobool
from urllib.error import HTTPError

import geopandas as gpd
import pandas as pd
from dateutil.parser import parse as date_parse

from epiw import (
    dwf,
    type
)


def desc(station_type):
    category, period = station_type

    url = f'https://aggregate.epinet.kr/station/{category}/{period}/csv/'
    req = urllib.request.urlopen(url)
    rep = req.read().decode('utf-8')
    rows = rep.splitlines()
    header, body = rows[0], rows[1:]

    Field = namedtuple('Field', header)

    return tuple(Field(*row.split(',')) for row in body)


def time_converter_by_interval(interval):
    return {
        'daily': lambda x: date_parse(x).date(),
        'hourly': date_parse
    }[interval]


def convert(field_name, value, time_converter):
    if not value:
        return None

    converter = {
        'tm': time_converter,
        'ws_gst_tm': date_parse,
        'stn_id': int,
        'src': str,
        'ir': lambda x: bool(strtobool(x)),
        'ix': lambda x: bool(strtobool(x)),
        'rda_id': str,
    }.get(field_name, float)

    try:
        return converter(value)
    except ValueError as e:
        raise ValueError(f'Can not found a converter: field_name:{field_name}, value:{value}') from e


def register(api_key=None):
    if not api_key:
        api_key = getpass.getpass('Input api key: ')
    os.environ['EPIW_API_KEY'] = api_key


def read(category, interval, begin, until=None, *, stations='', fields='', lonlat='', crs='', api_key=''):
    api_key = api_key or os.environ['EPIW_API_KEY']

    if not until:
        until = begin

    if isinstance(begin, str):
        begin = date_parse(begin)

    if isinstance(until, str):
        until = date_parse(until)

    if isinstance(fields, str):
        fields = fields.split(',')

    if isinstance(stations, str):
        stations = stations.split(',')
    elif isinstance(stations, int):
        stations = [stations]

    if isinstance(lonlat, str):
        lonlat = lonlat.split(',')

    stations = ','.join(map(str, stations))
    fields = ','.join(map(str, fields))
    lonlat = ','.join(map(str, lonlat))

    begin = begin.strftime('%Y%m%d%H%M%S')
    until = until.strftime('%Y%m%d%H%M%S')

    time_converter = time_converter_by_interval(interval)

    url = f'https://aggregate.epinet.kr/station/{category}/{interval}/'
    param = urllib.parse.urlencode(dict(
        begin=begin,
        until=until,
        stn_id=stations,
        field=fields,
        lonlat=lonlat,
        crs=crs,
        api_key=api_key,
    ))
    try:
        req = urllib.request.urlopen(f'{url}?{param}')
    except HTTPError as e:
        content = e.fp.read().decode('utf-8')
        print(f'# URL: {url}')
        print(f'# content: {content}')
        raise e
    rep = req.read().decode('utf-8')
    rows = rep.splitlines()
    header, body = rows[0], rows[1:]

    header = header.split(',')

    Field = namedtuple('Field', header)

    body = [row.split(',') for row in body]
    body = [[convert(*hr, time_converter=time_converter) for hr in zip(header, row)] for row in body]

    return tuple(Field(*row) for row in body)


def read_as_gpd(category, interval, begin, *args, **kwargs):
    data = read(category, interval, begin, *args, **kwargs)
    data = pd.DataFrame(data)
    if data.empty:
        return gpd.GeoDataFrame([])
    data = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.lon, data.lat))
    return data


def daily_weather_desc():
    return desc(type.STATION_WEATHER_DAILY)


def hourly_weather_desc():
    return desc(type.STATION_WEATHER_HOURLY)


def hourly_weather(begin, *args, **kwargs):
    return read('weather', 'hourly', begin, *args, **kwargs)


def daily_weather(begin, *args, **kwargs):
    return read('weather', 'daily', begin, *args, **kwargs)


def hourly_rda(begin, *args, **kwargs):
    return read('rda', 'hourly', begin, *args, **kwargs)


def daily_rda(begin, *args, **kwargs):
    return read('rda', 'daily', begin, *args, **kwargs)


def latest_dwf(lon, lat):
    return dwf.latest_dwf(lon, lat)
