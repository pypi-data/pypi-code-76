# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['certdumper']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'flex-config>=2.0.0,<3.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'typer>=0.3.2,<0.4.0',
 'watchdog>=1.0.2,<2.0.0']

entry_points = \
{'console_scripts': ['certdumper = certdumper.cli:app']}

setup_kwargs = {
    'name': 'certdumper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mateusz Klos',
    'author_email': 'novopl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
