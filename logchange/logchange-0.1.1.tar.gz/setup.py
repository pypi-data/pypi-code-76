# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logchange']

package_data = \
{'': ['*']}

install_requires = \
['newversion>=0.1.4,<0.2.0', 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'logchange',
    'version': '0.1.1',
    'description': 'Keep-a-changelog manager',
    'long_description': "# logchange - Changelog manager\n\nView, update and format your changelog anywhere!\n\n## Features\n\n- Keeps your changelog in [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) style\n- Supports version bumping from [semver](https://pypi.org/project/semver/)\n- Comes with a CLI tool `logchange`\n- Respects MarkDown\n- Created for CI and scripts\n\n## Installation\n\n```bash\npython -m pip install logchange\n```\n\n## Usage\n\n### CLI\n\n```bash\n# create CHANGELOG.md if it does not exist\n# or reformat existing (please check changes manually)\nlogchange init -f\n\n# add new release\ncat NOTES_0.1.0.md | logchange add 0.1.0\n# or\nlogchange add 0.2.0 -i `cat NOTES_0.2.0.md`\n\n# update existing or create a new section in latest release\nlogchange add latest added -i 'New feature'\n\n# set unreleased section\nlogchange set unreleased fixed -i 'Unreleased fix'\n\n# list released versions\nlogchange list\n< 0.1.0\n< 0.2.0\n\n# check release notes sections\nlogchange get 0.1.0 added\n< - New awesome feature\n< - Another feature\n```\n\n### GitHub Actions\n\nSee `workflows` folder.\n\n## Versioning\n\n`logchange` version follows [PEP 440](https://www.python.org/dev/peps/pep-0440/).\n\n## Latest changes\n\nFull changelog can be found in [Releases](https://github.com/vemel/logchange/releases).\n",
    'author': 'Vlad Emelianov',
    'author_email': 'vlad.emelianov.nz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vemel/logchange',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
