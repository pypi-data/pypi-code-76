import requests
import pprint

class Weather:
    """
    Creates a weather object
    """
    def __init__(self, api_key, city=None, lon=None, lat=None):
        units = "metric"
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?" \
                  f"q={city}&appid={api_key}&units={units}"
            r = requests.get(url)
            self.data = r.json()

        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?" \
                  f"lat={lat}&lon={lon}&appid={api_key}&units={units}"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("Provide a city or a latitude and longitude")

        if self.data["cod"] != "200":
            raise ValueError(self.data['message'])

    def next_12_hrs(self):
        """Returns 3 hour data
        """
        return self.data['list'][:4]

    def next_12_hrs_simplified(self):
        """Returns 12 hour simplified data
        """
        simple_data = []
        for dicty in self.data['list'][:4]:
            simple_data.append((dicty['dt_txt'], dicty['main']['temp'],
                                dicty['weather'][0]['description'], dicty['weather'][0]['icon']))
        return simple_data



