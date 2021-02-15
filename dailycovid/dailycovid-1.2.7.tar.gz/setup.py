# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dailycovid']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0.0,<4.0.0',
 'numpy>=1.0.0,<2.0.0',
 'pandas>=1.0.0,<2.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['dailycovid = dailycovid:main']}

setup_kwargs = {
    'name': 'dailycovid',
    'version': '1.2.7',
    'description': 'U.S.A daily covid information.',
    'long_description': '# dailycovid - Easily get covid updates\n\n# Pypi installation\n`pip3 install dailycovid`\n\n# Usage\n\n\n## Simplest\n\n`dailycovid --plot -s statecode`\n\n## Specific Counties in a State or Whole States\n\nYou can now use an arbitrary number of arguments with `-s` or `-sc`.\n\n`dailycovid -sc ny-albany ca-orange "California-Los Angeles"`\n\n`dailycovid -s DELAWARE MA`\n\n\nHere are three ways to do the same thing.\n\n`dailycovid -sc "California-Los Angeles"`\n\n`dailycovid -s CA -c "Los Angeles"`\n\n`dailycovid --state CA --county "Los Angeles"`\n\n## Making Plots\n\nUse `--plot` or `-p` to make the plots.\n\n## Updating Data\n\nOn the first run it will download a csv file containing the most recent data.\n\nUse `dailycovid -g` to update the cache.\n\n\n# Initial Execution Video\n\n[Full resolution video.](https://streamable.com/j3occ7)\n\n\n\n# Examples of plots\n\n\'![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_LOS-ANGELES_CA.png)\'\n\n![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_SUFFOLK_MA.png)   \n\n![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_NEW-YORK-CITY_NY.png)\n',
    'author': 'fitzy1293',
    'author_email': 'berkshiremind@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Fitzy1293/daily-covid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
