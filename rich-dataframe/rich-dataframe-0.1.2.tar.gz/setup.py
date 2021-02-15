# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_dataframe']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0', 'rich>=9.10.0,<10.0.0']

setup_kwargs = {
    'name': 'rich-dataframe',
    'version': '0.1.2',
    'description': 'Create animated and prettify Pandas dataframe',
    'long_description': None,
    'author': 'khuyentran1401',
    'author_email': 'khuyentran1476@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khuyentran1401/rich-dataframe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.7.8',
}


setup(**setup_kwargs)
