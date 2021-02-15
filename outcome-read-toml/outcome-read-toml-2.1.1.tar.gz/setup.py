# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['outcome', 'outcome.read_toml']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['read-toml = outcome.read_toml.bin:main']}

setup_kwargs = {
    'name': 'outcome-read-toml',
    'version': '2.1.1',
    'description': 'A small utility to read keys from TOML files.',
    'long_description': '# read-toml-py\n![Continuous Integration](https://github.com/outcome-co/read-toml-py/workflows/Continuous%20Integration/badge.svg) ![version-badge](https://img.shields.io/badge/version-2.1.1-brightgreen)\n\nA small utility to read keys from TOML files.\n\n## Usage\n\n### Installation\n\n```sh\npoetry add outcome-read-toml\n```\n\n### Usage\n\nThe utility reads the value specified by the key from the provided TOML file, and prints it to stdout.\n\nThe path parameter should be a \'.\' separated sequences of keys that correspond to a path in the TOML structure.\n\nExample TOML file:\n\n```toml\ntitle = "My TOML file"\n\n[info]\nversion = "1.0.1"\n\n[tools.poetry]\nversion = "1.1.2"\nfiles = [\'a.py\', \'b.py\']\n```\n\nRead standard keys:\n\n```sh\nread-toml --path my_file.toml --key title \n# "My TOML file"\n\nread-toml --path my_file.toml --key info.version\n# "1.0.1"\n```\n\nRead arrays:\n\n```sh\nread-toml --path my_file.toml --key tools.poetry.files\n# "a.py b.py"\n\nread-toml --path my_file.toml[0] --key tools.poetry.files\n# "a.py"\n```\n\nYou can\'t read non-leaf keys:\n\n```sh\nread_toml.py --path my_file.toml --key tools\n# KeyError\n```\n\nYou can check if a key exists:\n\n```sh\nread-toml --path my_file.toml --key title --check-only \n# 1\n\nread-toml --path my_file.toml --key unknown_key --check-only\n# 0\n```\n\n## Development\n\nRemember to run `./pre-commit.sh` when you clone the repository.\n',
    'author': 'Outcome Engineering',
    'author_email': 'engineering@outcome.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcome-co/read-toml-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
