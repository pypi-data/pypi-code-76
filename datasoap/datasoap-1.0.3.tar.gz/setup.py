# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datasoap']

package_data = \
{'': ['*']}

install_requires = \
['pandas']

entry_points = \
{'console_scripts': ['datasoap = datasoap:main']}

setup_kwargs = {
    'name': 'datasoap',
    'version': '1.0.3',
    'description': 'Supplementary library for pandas that processes dataframes derived from CSV files.',
    'long_description': '# datasoap\n\n## What is it?\n\ndatasoap is a supplementary library for pandas that processes dataframes derived from CSV files. The module checks cell data for correct numerical formatting and converts mismatched data to the correct data type (ex. str > float64).\n\n## Main Features\n\n- Strips unnecessary characters from numerical data fields in pandas dataframes to ensure consistent data formatting\n- Provides before and after representations of dataframes to allow for comparison\n\n## Repository\n\nSource code is hosted on: [github.com/snake-fingers/data-soap](https://github.com/Snake-Fingers/datasoap)\n\n## Dependencies\n\npandas - Python package that provides fast, flexible, and expressive data structures designed to make working with “relational” or “labeled” data both easy and intuitive.\n\n## Installation\n\n```\npoetry add datasoap\n```\n\n## Documentation\n\nDocumentation to come.\n\n## Background\n\ndatasoap originated from a Code Fellows 401 Python midterm project. The project team includes Alex Angelico, Grace Choi, Robert Carter, Mason Fryberger, and Jae Choi. After working with a few painful datasets using, we wanted to create a library that allows users to more efficiently manipulate clean datasets extracted from CSVs that may have inconsistent formatting.\n',
    'author': 'Grace Choi',
    'author_email': 'choi.g.330@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Snake-Fingers/datasoap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
