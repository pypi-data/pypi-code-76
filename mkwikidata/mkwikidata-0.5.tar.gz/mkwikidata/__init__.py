"""Utility functions for working with Wikidata"""
import requests
import re

__version__ = '0.5'


def get_coordinates_from_wd_point(point_str):
    regex = re.compile("Point\(-?([\d\.]+) (-?[\d\.]+)\)")
    match = regex.match(point_str)
    if match is None:
        return None
    return match.groups()[1], match.groups()[0]


def get_wd_id_from_url(url):
    regex = re.compile("http://www.wikidata.org/entity/(Q\d+)")
    match = regex.match(url)
    if match is None:
        return None
    return match.groups()[0]


def run_wikidata_query(query):

    url = 'https://query.wikidata.org/sparql'

    r = requests.get(url, params={'format': 'json', 'query': query})
    response_json = r.json()
    return response_json
