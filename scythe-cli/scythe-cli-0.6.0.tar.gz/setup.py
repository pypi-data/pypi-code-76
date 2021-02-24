# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scythe', 'scythe.cli', 'scythe.clock', 'scythe.ui']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'arc-cli>=2.0.1,<3.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['scythe = scythe.cli:cli']}

setup_kwargs = {
    'name': 'scythe-cli',
    'version': '0.6.0',
    'description': 'A Harvest is always better with a good tool',
    'long_description': "# Scythe\nHarvests are always better with a good tool!\n\nScythe is a tool for interacting with the Harvest API\n\n\n# Installation\nThe package is available on PyPi\n```\n$ pip install scythe-cli\n```\n\n# Scripts\n`scythe help` - Displays all the help information for the CLI\n\n`scythe init` - Used to initialize the tool with the Harvest token and Account ID. The auth token can be generated [here](https://id.getharvest.com/developers). Check [here](https://help.getharvest.com/api-v2/authentication-api/authentication/authentication/) for more information.\n\n`scythe whoami` - Prints the Harvest user's information\n\n`scythe project:list` - Lists out all the projects that the user is in\n\n`scythe timer:create` - Presents an interface to create a timer based on project and task. Will automatically start the timer upon creation.\n\n`scythe timer:start` - Used to start / restart a previously created timer.\n\n`scythe timer:running` - Display the currently running timer\n\n`scythe timer:stop` - Will stop the currenlty running timer\n\n`scythe timer:delete` - Presents an interface to delete a timer from today\n\n`scythe cache` - prints out the contents of the cache\n\n`scythe cache:clear` - cleans out the cache\n\n`sycthe cache:delete KEY` - deletes the `KEY` from the cache\n\n## Atomic Jolt\nScythe comes with a namespace `atomic` for Atomic Jolt specific timers.\n\n`scythe atomic:standup` - Starts the timer for standup\n\n`scythe atomic:training` - Stats the timer for training\n\nBoth of these scripts also accept a `--launch` flag. This will open the link named `STANDUP_LINK` or `TRAINING_LINK` in the config if they exist.\n\n\n# Development\nThis project uses [Poetry](https://python-poetry.org/) for dependancy / build management\n```\n$ git clone https://github.com/seanrcollings/scythe\n$ cd scythe\n$ poetry install\n```\n\n# TODO\n- Implement a `stats` utility\n  - Show time spent per project\n  - Show time spent per project task\n- Add the ability to update a timer\n- Update the config file to use yaml\n",
    'author': 'Sean Collings',
    'author_email': 'seanrcollings@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/seanrcollings/scythe',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
