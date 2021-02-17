# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gg_scrape']

package_data = \
{'': ['*']}

install_requires = \
['anytree>=2.8.0,<3.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'requests>=2.25.1,<3.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['ggs = gg_scrape.main:app']}

setup_kwargs = {
    'name': 'gg-scrape',
    'version': '0.1.2',
    'description': 'A little Python CLI app that provides a League champion runes/build from mobalytics.gg and the recommended skill order from champion.gg',
    'long_description': "# gg-scrape\nA little Python CLI app that provides a League champion runes/build from mobalytics.gg and the recommended skill order from champion.gg\n\nThe goal was to not have to open a browser tab to check a build.\nThe HTML is requested and parsed sequentially, so it's rather slow.\n\n## Installation\n```\npython -m pip install gg-scrape\n```\n\n## Usage\n```\nggs CHAMPION [ROLE]\n```\n\n![screenshot of the app in use](img/Capture.PNG)\n\n## Requirements\nDepends on the anytree, beautifulsoup4, typer, and requests Python libraries.\n",
    'author': 'Alex Whittington',
    'author_email': 'alexmw777@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/teauxfu/gg-scrape',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
