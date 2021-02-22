import requests
import os

from pyzipcode import ZipCodeDatabase


OPEN_WEATHER_MAP_KEY = os.getenv('OPEN_WEATHER_MAP_KEY')


def weather(*, zip_code: str, units: str = 'imperial'):
    # TODO(marcua): Internationalize.
    zcdb = ZipCodeDatabase()
    code = zcdb[zip_code]
    lat: float = code.latitude
    lon: float = code.longitude
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?'
        f'lat={lat}'
        f'&lon={lon}'
        f'&units={units}'
        f'&appid={OPEN_WEATHER_MAP_KEY}')
    results = response.json()
    today = results['daily'][0]
    descriptions = ', '.join(
        entry['description'] for entry in today['weather'])
    results['today'] = {
        'morning': {
            'temp': today['temp']['morn'],
            'feels_like': today['feels_like']['morn']
        },
        'day': {
            'temp': today['temp']['day'],
            'feels_like': today['feels_like']['day']
        },
        'evening': {
            'temp': today['temp']['eve'],
            'feels_like': today['feels_like']['eve']
        },
        'night': {
            'temp': today['temp']['night'],
            'feels_like': today['feels_like']['night']
        },
        'uvi': today['uvi'],
        'description': descriptions}
    return results


def covid(*, state: str):
    # TODO(marcua): Internationalize.
    response = requests.get(
        f'https://api.covidtracking.com/v1/states/{state}/current.json')
    results = response.json()
    positive = results.get('positiveIncrease', 0) * 1.0
    total = results.get('totalTestResultsIncrease', 0) * 1.0
    results['dayPositiveRate'] = (
        positive / total if positive and total else 'n/a')
    return results
