# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['servergrimoire', 'servergrimoire.operation']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.1.2,<8.0.0',
 'dnspython>=2.1.0,<3.0.0',
 'pyOpenssl>=20.0.1,<21.0.0',
 'python-whois>=0.7.3,<0.8.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.10.0,<10.0.0']

entry_points = \
{'console_scripts': ['servergrimoire = servergrimoire.__main__:launcher']}

setup_kwargs = {
    'name': 'servergrimoire',
    'version': '1.8.3',
    'description': 'Package for record and store info about servers and their stuffs',
    'long_description': '```\n.d8888b.\nd88P  Y88b\nY88b.\n "Y888b.    .d88b.  888d888 888  888  .d88b.  888d888\n    "Y88b. d8P  Y8b 888P"   888  888 d8P  Y8b 888P"\n      "888 88888888 888     Y88  88P 88888888 888\nY88b  d88P Y8b.     888      Y8bd8P  Y8b.     888\n "Y8888P"   "Y8888  888       Y88P    "Y8888  888\n\n\n\n .d8888b.          d8b                        d8b\nd88P  Y88b         Y8P                        Y8P\n888    888\n888        888d888 888 88888b.d88b.   .d88b.  888 888d888 .d88b.\n888  88888 888P"   888 888 "888 "88b d88""88b 888 888P"  d8P  Y8b\n888    888 888     888 888  888  888 888  888 888 888    88888888\nY88b  d88P 888     888 888  888  888 Y88..88P 888 888    Y8b.\n "Y8888P88 888     888 888  888  888  "Y88P"  888 888     "Y8888\n```\n\n[![Maintainability](https://api.codeclimate.com/v1/badges/4aece0d4c29b48cfcea4/maintainability)](https://codeclimate.com/github/fundor333/servergrimoire/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/4aece0d4c29b48cfcea4/test_coverage)](https://codeclimate.com/github/fundor333/servergrimoire/test_coverage)\n![PyPI - License](https://img.shields.io/pypi/l/servergrimoire)\n![PyPI](https://img.shields.io/pypi/v/servergrimoire)\n![PyPI - Status](https://img.shields.io/pypi/status/servergrimoire)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/servergrimoire)\n\nThis module gives you some command to check URLs, domains, dns rocords and other things in an automatied way.\n\nAll config and data are saved as dotfiles in your home directory and it works on Windows, Mac, and Linux systems granted\nyou have Python installed.\n\n# Command\n\nThis is a partial table of commands. For the complete one we suggest you to launch the --help command\n\n|        Command        | Option   | Explanation                              |\n|:---------------------:|----------|------------------------------------------|\n| servergrimoire --help |          | Print the help of the program            |\n| servergrimoire run    | --u, --c | Run the command for the url described    |\n| servergrimoire add    | --u      | Add the URL into the file for running    |\n| servergrimoire remove | --u      | Remove the url from the file for running |\n| servergrimoire stats  | --u,--c  | Print the stats of the last run made     |\n\nFor now we have the following commands\n\n| Command     | What does it?                                   |\n|-------------|-------------------------------------------------|\n| ssl_check   | Check if the domain has a valid SSL certificate |\n| dns_lookup  | Save the DNS lookup for the domain              |\n| dns_checker | Make a whois and save the domain expiration day |\n\n# Files\n\nServer Grimoire has two file to work with:\n\n* A config file .servergrimoire/config.json\n* A data file .servergrimoire/data.json\n\nThey are .json file if you want to edit them.\n',
    'author': 'Fundor333',
    'author_email': 'fundor333@fundor333.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fundor333.com/servergrimoire/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
