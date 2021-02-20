# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stacksearch']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'rich>=9.11.0,<10.0.0']

entry_points = \
{'console_scripts': ['stacksearch = stacksearch.__main__:main']}

setup_kwargs = {
    'name': 'stacksearch',
    'version': '2',
    'description': 'StackSearch is a python CLI and library that provides a way to search StackExchange sites.',
    'long_description': '<h1 align="center">stacksearch 🔎</h1>\n\n<p align="center">\n    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>\n    <a href="https://pypi.org/project/stacksearch/"><img src="https://img.shields.io/pypi/v/stacksearch" alt="PyPI"></a>\n    <a href="https://pypi.org/project/stacksearch/"><img src="https://img.shields.io/pypi/pyversions/stacksearch" alt="PyPI - Python Version"></a>\n    <a href="https://pypi.org/project/stacksearch/"><img src="https://img.shields.io/pypi/l/stacksearch" alt="PyPI - License"></a>\n    <a href="https://stacksearch.readthedocs.io/en/latest/"><img src="https://readthedocs.org/projects/stacksearch/badge/?version=latest" alt="Documentation Status"></a>\n    <a href="https://github.com/ThatXliner/stacksearch/actions/workflows/python-check.yml"><img src="https://github.com/ThatXliner/stacksearch/actions/workflows/python-check.yml/badge.svg" alt="PythonCI"></a>\n    <a href="https://codecov.io/gh/ThatXliner/stacksearch"> <img src="https://codecov.io/gh/ThatXliner/stacksearch/branch/master/graph/badge.svg" /> </a>\n</p>\n\n**NOTE: STACKSEARCH IS NO LONGER ACTIVELY MAINTAINED. There will still be the occasional bug fixes and updates, but not as much.**\n\n\nStackSearch is a python module that provides a way to search [StackExchange](https://stackexchange.com) sites such as [StackOverflow](https://stackoverflow.com).\n\n## Installation\n\nYou know the drill\n\n```bash\n$ pip install stacksearch\n```\n## Usage\n### CLI\n\n```bash\n$ stacksearch "This is the query"\n```\nor\n```bash\n$ python3 -m stacksearch "This is the query"\n```\n### Python API\n\n```python\n>>> from stacksearch import sync_search\n>>> sync_search("This is the query")\n```\nor the asynchronous version\n\n```python\n>>> import asyncio\n>>> from stacksearch import search\n>>> async def main():\n...    await search("This is the query")\n\n>>> asyncio.run(main())\n```\nHave fun!\n\n## Features\n\nThe benefits of this module as opposed to the other StackOverflow-searching modules is that this module provides the following:\n\n- A **markdown reverser engine** to return useful and beautiful answers\n- The ability to return a dictionary of _ALL_ the search results found, **not just the first result**\n- The ability to return results from all [StackExchange](https://stackexchange.com/) sites\n- A **beautiful command-line interface _for humans_** via [argparse](https://docs.python.org/3/library/argparse.html) and [**Rich**](https://github.com/willmcgugan/rich)\n- An optional **asynchronous Python API**\n- The ability to **crank out raw [JSON](https://www.json.org/json-en.html) data** to use\n- Fully [type hinted](https://www.python.org/dev/peps/pep-0585/)\n\n\n## Usage Examples\n\n- For creating a text editor extension built on this package\n\n- For searching StackOverflow and/or **other StackExchange websites** without leaving the Terminal (for those [Vim](https://www.vim.org/) people)\n\n- For getting lots of answers from all StackExchange sites you know\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\nPlease feel free to contribute!\n\n## Links 📎\n\n - [GitHub](https://github.com/ThatXliner/stacksearch/tree/Stable)\n - [PyPi](https://pypi.org/project/stacksearch/)\n',
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
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
