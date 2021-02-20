# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_tooltips']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs>=1.1.2,<2.0.0']

entry_points = \
{'mkdocs.plugins': ['tooltips = mkdocs_tooltips.plugin:Tooltips']}

setup_kwargs = {
    'name': 'mkdocs-tooltips',
    'version': '0.1.0',
    'description': 'Add and customize tooltips in MkDocs.',
    'long_description': None,
    'author': 'Nathanaël',
    'author_email': 'roipoussiere@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
