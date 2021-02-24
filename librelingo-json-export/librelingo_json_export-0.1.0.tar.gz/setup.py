# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['librelingo_json_export']

package_data = \
{'': ['*']}

install_requires = \
['librelingo-tools>=0.1.3,<0.2.0',
 'librelingo-types>=0.1.1,<0.2.0',
 'librelingo-utils>=0.1.2,<0.2.0',
 'python-slugify>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'librelingo-json-export',
    'version': '0.1.0',
    'description': 'Export LibreLingo courses in the JSON format used by the web app',
    'long_description': None,
    'author': 'Dániel Kántor',
    'author_email': 'git@daniel-kantor.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
