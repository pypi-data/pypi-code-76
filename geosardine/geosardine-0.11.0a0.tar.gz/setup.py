# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geosardine', 'geosardine.interpolate']

package_data = \
{'': ['*']}

install_requires = \
['GDAL==3.0.4',
 'affine>=2.3.0,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'fiona>=1.8.13,<2.0.0',
 'gdal>=3.0.4,<3.1.4',
 'numba>=0.51.2,<0.52.0',
 'numpy>=1.18,<1.19.4',
 'opencv-python>=4.4.0,<5.0.0',
 'pip>=20.0.0',
 'rasterio>=1.1.2,<2.0.0',
 'shapely>=1.6.4,<2.0.0',
 'tqdm>=4.48.2,<5.0.0']

entry_points = \
{'console_scripts': ['dine = geosardine.__main__:main']}

setup_kwargs = {
    'name': 'geosardine',
    'version': '0.11.0a0',
    'description': 'Spatial operations extend fiona and rasterio',
    'long_description': '# Geo-Sardine :fish:\n![python package](https://github.com/sahitono/geosardine/workflows/python%20package/badge.svg)\n[![codecov](https://codecov.io/gh/sahitono/geosardine/branch/master/graph/badge.svg)](https://codecov.io/gh/sahitono/geosardine)\n[![Maintainability](https://api.codeclimate.com/v1/badges/e7ec3c08fe42ef4b5e19/maintainability)](https://codeclimate.com/github/sahitono/geosardine/maintainability)\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/geosardine)\n![PyPI](https://img.shields.io/pypi/v/geosardine)\n![Conda](https://img.shields.io/conda/v/sahitono/geosardine)\n\nSpatial operations extend fiona and rasterio.\nCollection of spatial operation which i occasionally use written in python:\n - Interpolation with IDW (Inverse Distance Weighting) Shepard\n - Drape vector to raster\n - Spatial join between two vector\n - Raster wrapper, for better experience. ie: math operation between two raster, resize and resample\n\n:blue_book: documentation: https://sahitono.github.io/geosardine\n## Setup\ninstall with pip\n```pip install geosardine```\n\nor anaconda\n```conda install -c sahitono geosardine```\n\n## How to use it\n\n#### Drape and spatial join\n```python\nimport geosardine as dine\nimport rasterio\nimport fiona\n\nwith rasterio.open("/home/user/data.tif") as raster, fiona.open("/home/user/data.shp") as vector:\n    draped = dine.drape_geojson(vector, raster)\n    joined = dine.spatial_join(vector, raster) \n```\n#### IDW Interpolation\n```python\nimport numpy as np\nimport geosardine as dine\nxy = np.array([\n        [106.8358,  -6.585 ],\n        [106.6039,  -6.7226],\n        [106.7589,  -6.4053],\n        [106.9674,  -6.7092],\n        [106.7956,  -6.5988]\n])\nvalues = np.array([132., 127.,  37.,  90., 182.])\n\n"""\nif epsg not provided, it will assume that coordinate is in wgs84 geographic\nFind your epsg here https://epsg.io/\n"""\ninterpolated = dine.interpolate.idw(xy, values, spatial_res=(0.01,0.01), epsg=4326)\n\n# Save interpolation result to tiff\ninterpolated.save(\'idw.tif\')\n\n# shapefile or geojson can be used too\ninterp_file = dine.interpolate.idw("points.shp", spatial_res=(0.01,0.01), column_name="value")\ninterp_file.save("idw.tif")\n\n# The result array can be accessed like this\nprint(interpolated.array)\n"""\n[[ 88.63769859  86.24219616  83.60463194 ... 101.98185127 103.37001289\n  104.54621272]\n [ 90.12053232  87.79279317  85.22030848 ... 103.77118852 105.01425289\n  106.05302554]\n [ 91.82987695  89.60855271  87.14722258 ... 105.70090081 106.76928067\n  107.64635337]\n ...\n [127.21214817 127.33208302 127.53878268 ...  97.80436475  94.96247196\n   93.12113458]\n [127.11315081 127.18465002 127.33444124 ...  95.86455668  93.19212577\n   91.51135399]\n [127.0435062  127.0827023  127.19214624 ...  94.80175756  92.30685734\n   90.75707134]]\n"""\n\n\n```\n\n\n## Raster Wrapper\nGeosardine include wrapper for raster data. The benefit are:\n1. math operation (addition, subtraction, division, multiplication) between rasters of different size, resolution and reference system.\n   The data type result is equal to the first raster data type\n\n   for example:\n   ```\n   raster1 = float32 and raster2 = int32\n   raster3 = raster1 - raster2\n   raster3 will be float32\n   ```\n   \n\n2. resample with opencv\n3. resize with opencv\n4. split into tiled\n   \n\n```python\nfrom geosardine import Raster\n\n\n"""\nminimum parameter needed to create raster are \n1. 2D numpy array, example: np.ones(18, dtype=np.float32).reshape(3, 3, 2)\n2. spatial resolution, example:  0.4 or ( 0.4,  0.4)\n3. left coordinate / x minimum\n4. bottom coordinate / y minimum\n"""\nraster1 = Raster(np.ones(18, dtype=np.float32).reshape(3, 3, 2), resolution=0.4, x_min=120, y_max=0.7)\n\n## resample\nresampled = raster.resample((0.2,0.2))\n## resize\nresized = raster.resize(height=16, width=16)\n\n## math operation between raster\nraster_2 = raster + resampled\nraster_2 = raster - resampled\nraster_2 = raster * resampled\nraster_2 = raster / resampled\n\n## math operation raster to number\nraster_3 = raster + 2\nraster_3 = raster - 2\nraster_3 = raster * 2\nraster_3 = raster / 2\n\n```\n\n\n\n## Geosardine CLI\nYou can use it through terminal or command prompt by calling **dine**\n\n```\n$ dine --help\nUsage: dine [OPTIONS] COMMAND [ARGS]...\n\n  GeoSardine CLI\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  drape         Drape vector to raster to obtain height value\n  info          Get supported format\n  join-spatial  Join attribute by location\n  idw           Create raster with Inverse Distance Weighting interpolation\n```\n\n### License\n[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n',
    'author': 'Sahit Tuntas Sadono',
    'author_email': '26474008+sahitono@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sahitono/geosardine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
