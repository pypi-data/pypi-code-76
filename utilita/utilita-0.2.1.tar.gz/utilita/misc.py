from typing import Dict
import datetime
import argparse
import xml.etree.cElementTree as ET
from io import StringIO
import time
import pendulum
import warnings

def parse_templated(templated: Dict, map_value=lambda x:x, map_key=lambda x:x):
    assert 'templates' in templated
    assert 'keywords' in templated or 'template_dict' in templated

    if 'template_dict' in templated:
        warnings.warn(
            "`template_dict` key will be renamed in version 3, use `keywords` instead",
            PendingDeprecationWarning
        )

    keywords_compat = templated.get("keywords", templated.get("template_dict")) # fallback to old name for compat

    return {
        map_key(key): map_value(value.format(**keywords_compat))
        for key, value in templated["templates"].items()
    }

def pen2dt(pen: pendulum.Pendulum) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(pen.timestamp())

def parse_xml(xml_str):
    # Remove invalid characters in the XML
    xml_str_sanitized = xml_str.replace('&#x1A','').replace('&#x00','').replace('&#x01','')

    # convert the data from xml to an array before returning
    data = []

    for event, elem in ET.iterparse(StringIO(xml_str_sanitized)):
        if elem.tag == "row":
            data.append(elem.attrib)
            elem.clear()

    return data

def ymd_arg(date_str):
    '''parses 'yyyy-mm-dd' formatted date str into a python date object'''
    if date_str is None:
        return date_str
    else:
        try:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            msg = "Invalid date argument '{}'".format(date_str)
            raise argparse.ArgumentTypeError(msg)


def timeit(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time.time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time.time() * 1000)) - start
            print(f"⏱ timeit: {func.__module__}.{func.__name__} - [{end_ if end_ > 0 else 0} ms]")
    return _time_it