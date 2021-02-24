# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nsdpy']
install_requires = \
['certifi>=2020.12.5,<2021.0.0',
 'chardet>=4.0.0,<5.0.0',
 'idna>=2.10,<3.0',
 'requests>=2.25.1,<3.0.0',
 'urllib3>=1.26.2,<2.0.0']

entry_points = \
{'console_scripts': ['nsdpy = nsdpy:main']}

setup_kwargs = {
    'name': 'nsdpy',
    'version': '0.1.10',
    'description': '',
    'long_description': None,
    'author': 'RaphaelHebert',
    'author_email': 'raphaelhebert18@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
