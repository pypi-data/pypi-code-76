from time import time
from sys import stderr
import json

import requests


BASE_API_URL = 'http://api.openweathermap.org/data/3.0'


class Station:
    def __init__(self, api_key, station_id=None):
        self.endpoint = f'{BASE_API_URL}/stations'
        self.station_id = station_id
        self.api_key = api_key
        self.measurements = Measurements(api_key=self.api_key, station_id=self.station_id)

    def register(self, external_id, name, latitude, longitude, altitude):
        payload = {
            'external_id': external_id,
            'name': name,
            'latitude': latitude,
            'longitude': longitude,
            'altitude': altitude
        }
        response = requests.post(f'{self.endpoint}?appid={self.api_key}', json=payload)
        if response.status_code != 201:
            stderr.write("Can't create station!")
        else:
            if not self.station_id:
                self.station_id = response.json()['id']
                self.measurements.station_id = self.station_id
        return response.json()['id'] if response.status_code != 201 else None

    def info(self, station_id=None):
        api_call = f'{self.endpoint}/'
        api_call += station_id if station_id else self.station_id
        api_call += f'?appid={self.api_key}'
        response = requests.get(api_call)
        if response.status_code != 200:
            stderr.write("Can't get info")
            
        return response.json()

    def update(self, station_id=None, external_id=None, name=None, latitude=None, longitude=None, altitude=None):
        payload = self.info(station_id)
        api_call = f'{self.endpoint}/'
        api_call += station_id if station_id else self.station_id
        api_call += f'?appid={self.api_key}'
        if external_id: payload['external_id'] = external_id
        if name: payload['name'] = name
        if latitude: payload['latitude'] = latitude
        if longitude: payload['longitude'] = longitude
        if altitude: payload['altitude'] = altitude

        response = requests.put(url=api_call, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        if response.status_code != 200:
            stderr.write("Can't get info")
        return response.json()

    def delete(self, station_id=None):
        api_call = f'{self.endpoint}/'
        api_call += station_id if station_id else self.station_id
        api_call += f'?appid={self.api_key}'
        response = requests.delete(api_call)
        if response.status_code != 204:
            stderr.write("Can't delete")
        return response.json()

    def all_stations(self):
        response = requests.get(f'{self.endpoint}?appid={self.api_key}')
        return response.json()

    def set_station_id(self, station_id):
        self.station_id = station_id
        self.measurements.station_id = station_id


class Measurements:
    def __init__(self, api_key, station_id=None):
        self.station_id = station_id
        self.api_key = api_key
        self.endpoint = f'{BASE_API_URL}/measurements'

    def get(self, station_id=None, meas_type=None, limit=None, time_from=None, time_to=None):
        api_call = f'{self.endpoint}/?station_id='
        api_call += station_id if station_id else self.station_id
        api_call += '&type='
        api_call += meas_type if meas_type else 'h'
        api_call += '&limit='
        api_call += limit if limit else '24'
        if time_from:
            api_call += f'&from={time_from}'
        if time_to:
            api_call += f'&time_to={time_to}'
        api_call += f'&appid={self.api_key}'
        response = requests.get(api_call)
        return response.json()

    def get_one(self, station_id=None, meas_type=None, time_from=None, time_to=None):
        response = self.get(station_id=station_id, meas_type=meas_type, limit=1, time_from=time_from,
                            time_to=time_to)
        return response[0]

    def set(self, dt=None, station_id=None, temperature=None, wind_speed=None, wind_gust=None, wind_deg=None,
            pressure=None, humidity=None, rain_1h=None, rain_6h=None, rain_24h=None, snow_1h=None, snow_6h=None,
            snow_24h=None, dew_point=None, humidex=None, heat_index=None, visibility_distance=None,
            visibility_prefix=None, clouds=None, weather=None):
        payload = dict()
        payload.update({'station_id': station_id if station_id else self.station_id })
        payload.update({'dt': dt if dt else int(time())})
        if temperature: payload.update({'temperature': temperature})
        if wind_speed: payload.update({'wind_speed': wind_speed})
        if wind_gust: payload.update({'wind_gust': wind_gust})
        if wind_deg: payload.update({'wind_deg': wind_deg})
        if pressure: payload.update({'pressure': pressure})
        if humidity: payload.update({'humidity': humidity})
        if rain_1h: payload.update({'rain_1h': rain_1h})
        if rain_6h: payload.update({'rain_6h': rain_6h})
        if rain_24h: payload.update({'rain_24h': rain_24h})
        if snow_1h: payload.update({'snow_1h': snow_1h})
        if snow_6h: payload.update({'snow_6h': snow_6h})
        if snow_6h: payload.update({'snow_24h': snow_24h})
        if dew_point: payload.update({'dew_point': dew_point})
        if humidex: payload.update({'humidex': humidex})
        if heat_index: payload.update({'heat_index': heat_index})
        if visibility_distance: payload.update({'visibility_distance': visibility_distance})
        if visibility_prefix: payload.update({'visibility_prefix': visibility_prefix})
        if clouds: payload.update({'clouds': clouds})
        if weather: payload.update({'weather': weather})

        response = requests.post(url=f'{self.endpoint}?appid={self.api_key}', json=[payload])
        return response.content

    def set_bulk(self, payload):
        response = requests.post(url=f'{self.endpoint}?appid={self.api_key}', json=payload)
        return response.content

    def set_station_id(self, station_id):
        self.station_id = station_id
