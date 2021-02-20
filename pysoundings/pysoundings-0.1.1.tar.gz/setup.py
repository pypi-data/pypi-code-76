# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysoundings']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'lxml>=4.6.2,<5.0.0',
 'pandas>=1.2.1,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pysoundings',
    'version': '0.1.1',
    'description': "This is just a simple little module designed to pull atmospheric sounding data from the University of Wyoming, College of Engineering, Department of Atmospheric Science's website. All you need is the station number and the date and this module will return a pandas.DataFrame containing the sounding data. You may still want to go to the website to determine what stations are available, but there are data from a lot of stations in the United States.",
    'long_description': "# pysoundings\n\n**pysoundings** is just a simple little module designed to pull atmospheric sounding data from the [University of Wyoming, College of Engineering, Department of Atmospheric Science's website](http://weather.uwyo.edu/upperair/sounding.html). All you need is the station number and the date and this module will return a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) containing the sounding data. You may still want to go to the website to determine what stations are available, but there are data from a lot of stations in the United States.\n\n## Installation\n\nThe package is available on [PyPi](https://pypi.org/):\n\n```bash\n$ pip install pysoundings\n```\n",
    'author': 'dkllrjr',
    'author_email': 'dg.kllr.jr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dkllrjr/pysoundings',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
