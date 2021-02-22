import os

import dotenv

import epiw
from epiw.grid import grid, create_grid

dotenv.load_dotenv()

api_key = os.environ['EPIW_API_KEY']

epiw.register(api_key)

desc = epiw.hourly_weather_desc()

print(desc)

desc = epiw.daily_weather_desc()

print(desc)

values = epiw.hourly_weather('20200101', '20200101', api_key=api_key)

print(values)

values = epiw.read('weather', 'daily', '20180101', '20200101', lonlat='127,37', api_key=api_key)

print(values)

values = epiw.read_as_gpd('weather', 'daily', '20180101', '20200101', lonlat='127,37', api_key=api_key)
print(values)

kma_data = epiw.read_as_gpd('weather', 'daily', '20200101', '20200101', api_key=api_key)
kma_data = kma_data.set_crs(4326).to_crs(5179)
kma_data.drop(['tm'], axis=1).to_file('./tmp/output.json', driver='GeoJSON')
grid('./tmp/output.json', './tmp/output.tiff', 'tn', cell_size=10000)

create_grid('weather', 'hourly', 'tn', '20200801', './output', cell_size=1000)
create_grid('weather', 'daily', 'tn', '20200801', './output', cell_size=1000, elev_correction=lambda x: x * -0.0065, ignore_warped_dem_cache=False)

latest_dwf = epiw.latest_dwf(127, 37)
print(latest_dwf)
