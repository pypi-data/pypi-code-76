# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cgmodels', 'cgmodels.demultiplex']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0', 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'cgmodels',
    'version': '0.1.0',
    'description': 'Models used at clinical genomics',
    'long_description': '# cgmodels\n\nWork as an interface between services at Clinical Genomics. In most cases where multiple services needs access to a \ncommon API, those models should be defined here.',
    'author': 'moonso',
    'author_email': 'mans.magnusson@scilifelab.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Clinical-Genomics/cgmodels',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
