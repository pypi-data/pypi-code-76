from vade_api_src.vade_enums import *
from vade_api_src.spot_structs import *
import requests
import json


class VadeRealtimeAPI:

    api_key: str
    production_level: ProductionLevel

    def __init__(self, api_key: str, production_level: ProductionLevel):
        self.production_level = production_level
        self.api_key = api_key

    def get_zone_occupancy(self, zone_id: str)->[VadeSpotRealtime]:
        url = "https://realtime.{}.inf.vadenet.org/v1/zones/{}".format(self.production_level.value, zone_id)
        header = {"apiKey": self.api_key}
        resp = requests.get(url, headers=header)
        try:
            resp_obj = json.loads(resp.text)
            spot_data = resp_obj["spots"]
            ret_spots:[VadeSpotRealtime] = []
            for spot in spot_data:
                new_spot = VadeSpotRealtime.from_json(spot)
                if new_spot:
                    ret_spots.append(new_spot)
            return ret_spots
        except Exception as e:
            print("Error getZoneOccupancy: {}".format(resp.text))
            return None

    def get_geo_occupancy(self, latitude: float, longitude: float, radius: int = 1000, page_size: int = 50, page_number: int = 1) -> [VadeSpotRealtime]:
        url = "https://realtime.{}.inf.vadenet.org/v1/geo?pageSize={}&pageNumber={}&latitude={}&longitude={}&distance={}".format(self.production_level.value, page_size, page_number, latitude, longitude, radius)
        header = {"apiKey": self.api_key}
        resp = requests.get(url, headers=header)
        try:
            resp_obj = json.loads(resp.text)
            spot_data = resp_obj["spots"]
            ret_spots: [VadeSpotRealtime] = []
            for spot in spot_data:
                new_spot = VadeSpotRealtime.from_json(spot)
                if new_spot:
                    ret_spots.append(new_spot)
            return ret_spots

        except Exception as e:
            print("Error getGeoOccupancy: {}".format(resp.text))
            return None

    def get_spot_occupancy(self, spot_id: str) -> [VadeSpotRealtime]:
        url = "https://realtime.{}.inf.vadenet.org/v1/spots/{}".format(self.production_level.value, spot_id)
        header = {"apiKey": self.api_key}
        resp = requests.get(url, headers=header)
        try:
            if resp.status_code == 200 or resp.status_code == 201:
                resp_obj = json.loads(resp.text)
                new_spot = VadeSpotRealtime.from_json(resp_obj)
                if new_spot:
                    return new_spot
            else:
                return None
        except Exception as e:
            print("Error getSpotOccupancy: {}".format(resp.text))
            return None
