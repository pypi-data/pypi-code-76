# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_gen_files']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs>=1.0,<2.0']

entry_points = \
{'mkdocs.plugins': ['gen-files = mkdocs_gen_files.plugin:GenFilesPlugin']}

setup_kwargs = {
    'name': 'mkdocs-gen-files',
    'version': '0.3.0',
    'description': 'MkDocs plugin to programmatically generate documentation pages during the build',
    'long_description': None,
    'author': 'Oleh Prypin',
    'author_email': 'oleh@pryp.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oprypin/mkdocs-gen-files',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
