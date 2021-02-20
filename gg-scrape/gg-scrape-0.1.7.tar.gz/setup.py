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
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['ggs = gg_scrape.argsparse:ggs']}

setup_kwargs = {
    'name': 'gg-scrape',
    'version': '0.1.7',
    'description': 'A little Python CLI app that provides a summary of League champion build information. ',
    'long_description': "# gg-scrape\nA little Python CLI app that provides a League of Legends champion build by scraping the web.\n\nThe goal was to not have to open a browser tab (or be advertised to) to quickly check a build before a match.\nThe HTML is requested and parsed sequentially, so it's somewhat slow (but still faster than opening a browser).\n\n## Installation\n```\npython -m pip install gg-scrape\n```\n\n## Usage\n```\nggs [OPTIONS] CHAMPION [ROLE]\n```\n\n\n\n## Screenshots\n![help text](img/help.PNG)\n![screenshot of the app in use](img/demo.PNG)\n![unavailable build handling](img/default_build.PNG)\n![verbose output](img/verbose_output.PNG)\n\n## Requirements\nDepends on the anytree, beautifulsoup4, typer, and requests Python libraries.\n\n## Contributions\nThanks to [@Mycsina](https://github.com/Mycsina) for feedback and helping to improve and expand this package's functionality!\n\nPull requests are welcome! \n",
    'author': 'Alex W',
    'author_email': 'alex@southsun.tech',
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
