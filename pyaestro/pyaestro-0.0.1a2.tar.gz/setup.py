# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaestro',
 'pyaestro.abstracts',
 'pyaestro.data',
 'pyaestro.dataclasses',
 'pyaestro.interfaces',
 'pyaestro.interfaces.mpi',
 'pyaestro.interfaces.scheduling',
 'pyaestro.structures',
 'pyaestro.utilities']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs', 'psutil']

setup_kwargs = {
    'name': 'pyaestro',
    'version': '0.0.1a2',
    'description': 'A package of utilities structures for building workflows and workflow related tools.',
    'long_description': None,
    'author': 'Frank Di Natale',
    'author_email': 'frank.dinatale1988@gmail.com',
    'maintainer': 'Frank Di Natale',
    'maintainer_email': 'frank.dinatale1988@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.4',
}


setup(**setup_kwargs)
