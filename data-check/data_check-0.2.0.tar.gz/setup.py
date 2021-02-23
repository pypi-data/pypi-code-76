# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_check']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.22,<1.4.0',
 'click>=7.1.2,<7.2.0',
 'colorama>=0.4.4,<0.5.0',
 'importlib-metadata>=3.4.0,<4.0.0',
 'numpy>=1.19.5,<1.20.0',
 'pandas>=1.1.5,<1.2.0',
 'pyyaml>=5.3.1,<6.0.0']

extras_require = \
{'mssql': ['pyodbc>=4.0.30,<4.1.0'],
 'mysql': ['pymysql[rsa]'],
 'oracle': ['cx_Oracle>=8.1.0,<8.2.0'],
 'postgres': ['psycopg2-binary>=2.8.6,<2.9.0']}

entry_points = \
{'console_scripts': ['data_check = data_check.__main__:main']}

setup_kwargs = {
    'name': 'data-check',
    'version': '0.2.0',
    'description': 'simple data validation',
    'long_description': '# data_check\n\ndata_check is a simple data validation tool. Write SQL queries and CSV files with the expected result sets and data_check will test the result sets against the queries.\n\ndata_check should work with any database that works with [SQLAlchemy](https://docs.sqlalchemy.org/en/13/dialects/). Currently data_check is tested against PostgreSQL, MySQL, SQLite, Oracle and Microsoft SQL Server.\n\n## Quickstart\n\nYou need Python 3.6 or above to run data_check. The easiest way to install data_check is via [pipx](https://github.com/pipxproject/pipx):\n\n`pipx install data_check`\n\nThe data_check Git repository is also a sample data_check project. Clone the repository, switch to the folder and run data_check:\n\n```\ngit clone git@github.com:andrjas/data_check.git\ncd data_check\ndata_check\n```\n\nThis will run the tests in the _checks_ folder using the default connection as set in data_check.yml.\n\nSee the [documentation](https://andrjas.github.com/data_check) how to install data_check in different environments with additional database drivers and other usages of data_check.\n\n## Project layout\n\ndata_check has a simple layout for projects: a single configuration file and a folder with the test files. You can also organize the test files in subfolders.\n\n    data_check.yml    # The configuration file\n    checks/           # Default folder for data tests\n        some_test.sql # SQL file with the query to run against the database\n        some_test.csv # CSV file with the expected result\n        subfolder/    # Tests can be nested in subfolders\n\n## Documentation\n\nSee the [documentation](https://andrjas.github.com/data_check) how to setup data_check, how to create a new project and more options.\n',
    'author': 'Andreas Rjasanow',
    'author_email': 'andrjas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://andrjas.github.io/data_check/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
