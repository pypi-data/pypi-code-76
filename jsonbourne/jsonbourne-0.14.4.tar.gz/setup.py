# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['jsonbourne', 'jsonbourne.jsonlib']

package_data = \
{'': ['*']}

modules = \
['JSON', 'david_webb']
extras_require = \
{'full': ['pydantic>=1.5.0,<2.0.0',
          'python-rapidjson>=0.9.1,<1.0.0',
          'orjson>=3.0.0,<4.0.0'],
 'oj': ['orjson>=3.0.0,<4.0.0'],
 'orjson': ['orjson>=3.0.0,<4.0.0'],
 'pydantic': ['pydantic>=1.5.0,<2.0.0'],
 'rapidjson': ['python-rapidjson>=0.9.1,<1.0.0'],
 'rec': ['orjson>=3.0.0,<4.0.0'],
 'rj': ['python-rapidjson>=0.9.1,<1.0.0']}

setup_kwargs = {
    'name': 'jsonbourne',
    'version': '0.14.4',
    'description': 'EZPZ JSON',
    'long_description': None,
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
