# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbf2sql', 'dbf2sql.config', 'dbf2sql.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'dataset>=1.4.1,<2.0.0',
 'dbfread>=2.0.7,<3.0.0',
 'pandas>=1.1.2,<2.0.0',
 'pefile>=2019.4.18,<2020.0.0',
 'sqlalchemy>=1.3.19,<2.0.0']

extras_require = \
{'ipy': ['ipython>=7.19.0,<8.0.0'],
 'mssql': ['pyodbc>=4.0.30,<5.0.0'],
 'nvim': ['neovim>=0.3.1,<0.4.0', 'pynvim>=0.4.2,<0.5.0']}

entry_points = \
{'console_scripts': ['dbf2sql = dbf2sql:cli']}

setup_kwargs = {
    'name': 'dbf2sql',
    'version': '0.1.1.dev1',
    'description': 'Convert DBF files to SQL tables',
    'long_description': '# dbf2sql\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n## Overview\n\nDBF2SQL is a Python CLI program that offers an interface to Convert DBF files in SQL Server tables\n\n## Pre-requirements\n\n- [Download ODBC Driver for SQL Server](https://docs.microsoft.com/es-es/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15)\n\n## License\n\nThis library is published under the terms of the MIT License. Please check the LICENSE file for more details.\n',
    'author': 'Cristian Javier Azulay',
    'author_email': 'cjadeveloper@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cjadeveloper/dbf2sql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
