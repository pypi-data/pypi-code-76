# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['appmap',
 'appmap._implementation',
 'appmap.test',
 'appmap.test.data',
 'appmap.test.data.package1',
 'appmap.test.data.package1.package2',
 'appmap.test.data.pytest']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'inflection>=0.5.1,<0.6.0', 'orjson==3.4.6']

entry_points = \
{'pytest11': ['appmap = appmap.pytest']}

setup_kwargs = {
    'name': 'appmap',
    'version': '0.1.0.dev5',
    'description': 'Create AppMap files by recording a Python application.',
    'long_description': None,
    'author': 'Alan Potter',
    'author_email': 'alan@app.land',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
