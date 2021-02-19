# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daffy']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'daffy',
    'version': '0.4.0',
    'description': 'Function decorators for Pandas Dataframe column name and data type validation',
    'long_description': '# DAFFY DataFrame Column Validator\n![PyPI](https://img.shields.io/pypi/v/daffy)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/daffy)\n![test](https://github.com/fourkind/daffy/workflows/test/badge.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## Description \n\nIn projects using Pandas, it\'s very common to have functions that take Pandas DataFrames as input or produce them as output.\nIt\'s hard to figure out quickly what these DataFrames contain. This library offers simple decorators to annotate your functions\nso that they document themselves and that documentation is kept up-to-date by validating the input and output on runtime.\n\n## Table of Contents\n* [Installation](#installation)\n* [Usage](#usage)\n* [Contributing](#contributing)\n* [Tests](#tests)\n* [License](#license)\n\n## Installation\n\nInstall with your favorite Python dependency manager like\n\n```sh\npip install daffy\n```\n\nor\n\n```sh\npoetry add daffy\n```\n\n\n## Usage \n\nStart by importing the needed decorators:\n\n```\nfrom daffy import df_in, df_out\n```\n\nTo check a DataFrame input to a function, annotate the function with `@df_in`. For example the following function expects to get\na DataFrame with columns `Brand` and `Price`:\n\n```python\n@df_in(columns=["Brand", "Price"])\ndef process_cars(car_df):\n    # do stuff with cars\n```\n\nIf your function takes multiple arguments, specify the field to be checked with it\'s `name`:\n\n```python\n@df_in(name="car_df", columns=["Brand", "Price"])\ndef process_cars(year, style, car_df):\n    # do stuff with cars\n```\n\nTo check that a function returns a DataFrame with specific columns, use `@df_out` decorator:\n\n```python\n@df_out(columns=["Brand", "Price"])\ndef get_all_cars():\n    # get those cars\n    return all_cars_df\n```\n\nIn case one of the listed columns is missing from the DataFrame, a helpful assertion error is thrown:\n\n```python\nAssertionError("Column Price missing from DataFrame. Got columns: [\'Brand\']")\n```\n\nTo check both input and output, just use both annotations on the same function:\n\n```python\n@df_in(columns=["Brand", "Price"])\n@df_out(columns=["Brand", "Price"])\ndef filter_cars(car_df):\n    # filter some cars\n    return filtered_cars_df\n```\n\nIf you want to also check the data types of each column, you can replace the column array:\n\n```python\ncolumns=["Brand", "Price"]\n```\n\nwith a dict:\n\n```python\ncolumns={"Brand": "object", "Price": "int64"}\n```\n\nThis will not only check that the specified columns are found from the DataFrame but also that their `dtype` is the expected.\n\nTo quickly check what the incoming and outgoing dataframes contain, you can add a `@df_log` annotation to the function. For\nexample adding `@df_log` to the above `filter_cars` function will product log lines:\n\n```\nFunction filter_cars parameters contained a DataFrame:columns: [\'Brand\', \'Price\']\nFunction filter_cars returned a DataFrame: columns: [\'Brand\', \'Price\']\n```\n\n## Contributing\n\nContributions are accepted. Include tests in PR\'s.\n\n## Development\n\nTo run the tests, clone the repository, install dependencies with Poetry and run tests with PyTest:\n\n```sh\npoetry install\npoetry shell\npytest\n```\n\nTo enable linting on each commit, run `pre-commit install`. After that, your every commit will be checked with `isort`, `black` and `flake8`.\n\n## License\n\nMIT\n\n## Changelog\n\n### 0.4.0\n\nAdded `@df_log` for logging.\nImproved assertion messages.\n\n### 0.3.0\n\nAdded type hints.\n\n### 0.2.1\n\nAdded Pypi classifiers. \n\n### 0.2.0\n\nFixed decorator usage.\nAdded functools wraps.\n\n### 0.1.0\n\nInitial release.\n\n',
    'author': 'Janne Sinivirta',
    'author_email': 'janne.sinivirta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fourkind/daffy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
