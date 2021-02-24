import requests


class Weather:
    """
    Creates a weather object
    :param apikey an API key obtainable from https://openweather.org
    :param either city or both lat and lon of where you want the weather from
    :param units either 'imperial' or 'metric', defaults to metric when no argument given

    exmple using city name:
    >>> weather = Weather(apikey="ENTER YOUR KEY HERE", city="London", units="imperial")

    or using longitude and latitude:
    >>> weather = Weather(apikey="ENTER YOUR KEY HERE", lat="51.3", lon="0.73" units="imperial")

    get complete weather for next 12h in 3 hour intervals:
    weather.next_12h()

    simplified data for next 12h
    weather.next_12h_simplified()

    url to get weather icon
    https://openweathermap.org/img/wn/{icon_code}.png

    """

    def __init__(self, apikey, city=None, lat=None, lon=None, units='metric'):

        if city:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units={units}"
        elif lat and lon:
            url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}&units={units}"
        else:
            raise TypeError("Provide either a City or Lat and Lon arguments")

        r = requests.get(url)
        self.data = r.json()

        if self.data['cod'] != '200':
            raise ValueError(self.data["message"])

    def next_12h(self):
        """
        :return: weather for next 12h in 3hr intervals as a dictionary
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """
        :return: date and time, temp, overhead conditions and a weather icon for 4 time slots 3hrs apart
        """
        simple_data = []
        for d in self.data['list'][:4]:
            simple_data.append((d['dt_txt'], d['main']['temp'], d['weather'][0]['description'], d['weather'][0]['icon']))
        return simple_data


