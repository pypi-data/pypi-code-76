# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['upoly']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.6.0,<0.7.0',
 'httpx[brotli,http2]>=0.16.1,<0.17.0',
 'joblib>=1.0.0,<2.0.0',
 'nest-asyncio>=1.4.3,<2.0.0',
 'numpy>=1.19.5,<2.0.0',
 'orjson>=3.4.6,<4.0.0',
 'pandas-market-calendars>=1.6.1,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'upoly',
    'version': '0.1.23',
    'description': 'High performance asyncio REST client for polygon.io',
    'long_description': '# Upoly\n\n<p align="center">\n    <img src="upoly.png" alt="upoly">\n</p>\n<!-- ![upoly logo](upoly.png) -->\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Dependency Status](https://img.shields.io/librariesio/github/RileyMShea/upoly)]("")\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/RileyMShea/upoly/Tests)\n![Lines of code](https://img.shields.io/tokei/lines/github/RileyMShea/upoly)\n![GitHub issues](https://img.shields.io/github/issues-raw/RileyMShea/upoly)\n![GitHub](https://img.shields.io/github/license/RileyMShea/upoly)\n![PyPI](https://img.shields.io/pypi/v/upoly)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/upoly)\n<a href="https://codecov.io/gh/RileyMShea/upoly" target="_blank">\n<img src="https://img.shields.io/codecov/c/github/RileyMShea/upoly?color=%2334D058" alt="Coverage">\n</a>\n\nAn Asyncio based, high performance, REST client libary for interacting\nwith the polygon REST api.\n\n## Abstract\n\nThe two main python rest-client libs for polygon.io(alpaca-trade-api,\npolygonio) do not provide an effective means to gather more than 50,000 trade\nbars at once. This library aims to address that by providing an easy and\nperformant solution to getting results from timespans where the resultset\nexceeds 50,000 trade bars.\n\n## Installation\n\nThis library makes use of some high performance packages written in `C`/`Rust`\n(uvloop, orjson) so it may require `sudo apt install python3-dev` on Ubuntu or similar on\nother OS\'s. It is currently only compatible with Python 3.8.x but aims to be\ncompatible with 3.9 once it\'s dependendencies support 3.9\nand all future CPython versions moving forward.\n\npip/poetry w/ venv\n\n```bash\n#!/bin/env bash\npython3.8 -m venv .venv && source .venv/bin/activate\n\npoetry add upoly\n# or\npip install upoly\n```\n\n## Usage\n\nReccomend to create a copy of `./env.sample` as `./env`. Make sure `.env` is listed\nin `.gitignore`.\n\n```env\n# ./.env\nPOLYGON_KEY_ID=REPACEWITHPOLYGONORALPACAKEYHERE\n```\n\nMany alternatives to `.env` exist. One such alternative is exporting\nlike so:\n\n```bash\n#!/bin/env bash\nexport POLYGON_KEY_ID=REPACEWITHPOLYGONORALPACAKEYHERE\n```\n\nor adding to your shell startup script, either `.zshrc` or `.bashrc` to have\nit be globally available to all projects.\n\n```bash\n#/home/youruseraccount/.bashrc\n...\nexport POLYGON_KEY_ID=REPACEWITHPOLYGONORALPACAKEYHERE\n...\n```\n\n```python\n# ./yourscript.py\nimport pytz\nfrom dotenv import load_dotenv\nimport pandas as pd\n\n# load Polygon key from .env file\nload_dotenv()\n# alternatively run from cli with:\n# POLYGON_KEY_ID=@#*$sdfasd python yourscript.py\n\n# Not recommend but can be set with os.environ["POLYGON_KEY_ID"] as well\n\nfrom upoly import async_polygon_aggs\n\n\nNY = pytz.timezone("America/New_York")\n\n# Must be a NY, pandas Timestamp\nstart = pd.Timestamp("2015-01-01", tz=NY)\nend = pd.Timestamp("2020-01-01", tz=NY)\n\ndf = async_polygon_aggs("AAPL", start, end)\n```\n\n## TODO\n\n- [ ] unit tests\n- [ ] regression tests\n- [ ] integration tests\n- [ ] `/trade` endpoint functionality for tick data\n',
    'author': 'Riley',
    'author_email': 'rileymshea@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
