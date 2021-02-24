# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matrixctl', 'matrixctl.handlers']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.13,<4.0.0',
 'ansible-runner>=1.4.7,<2.0.0',
 'coloredlogs>=15.0,<16.0',
 'paramiko>=2.7.2,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{'docs': ['sphinx>=3.5.1,<4.0.0',
          'sphinx-autodoc-typehints>=1.11.1,<2.0.0',
          'sphinxcontrib-programoutput>=0.16,<0.17',
          'numpydoc>=1.1.0,<2.0.0']}

entry_points = \
{'console_scripts': ['matrixctl = matrixctl.application:main']}

setup_kwargs = {
    'name': 'matrixctl',
    'version': '0.8.2',
    'description': 'Controls a synapse oci-container instance via ansible',
    'long_description': '![GitHub](https://img.shields.io/github/license/MichaelSasser/matrixctl?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/matrixctl?style=flat-square)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/matrixctl?style=flat-square)\n![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/michaelsasser/matrixctl?style=flat-square)\n![GitHub Release Date](https://img.shields.io/github/release-date/michaelsasser/matrixctl?style=flat-square)\n![PyPI - Status](https://img.shields.io/pypi/status/matrixctl?style=flat-square)\n![Matrix](https://img.shields.io/matrix/matrixctl:michaelsasser.org?server_fqdn=matrix.org&style=flat-square)\n![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/michaelsasser/matrixctl?style=flat-square)\n\n# MatrixCtl\n\nMatrixCtl is a python program to control, manage, provision and deploy our\nmatrix homeserver. Instead of remembering tons of commands or having a bunch\nof shell scripts MatrixCtl does many things for you.\n\n## Command line tool\n\nMatrixCtl as a pure commandline tool. You can use it as package, if you like,\nbut breaking changes may be introduced, even in a minor version shift.\n\n```\n# matrixctl\nusage: matrixctl [-h] [--version] [-d]\n                 {adduser,deluser,adduser-jitsi,deluser-jitsi,user,users,rooms,delroom,update,upload,deploy,server-notice,start,restart,maintenance,check,version}\n              ...\n\npositional arguments:\n  {adduser,deluser,adduser-jitsi,deluser-jitsi,user,users,rooms,delroom,update,upload,deploy,server-notice,start,restart,maintenance,check,version}\n    adduser             Add a new matrix user\n    deluser             Deletes a user\n    adduser-jitsi       Add a new jitsi user\n    deluser-jitsi       Deletes a jitsi user\n    user                Get information about a specific user\n    users               Lists users\n    rooms               List rooms\n    delroom             Deletes an empty room from the database\n    update              Updates the ansible repo\n    upload              Upload a file.\n    deploy              Provision and deploy\n    server-notice       Send a server notice\n    start               Starts all OCI containers\n    restart             Restarts all OCI containers (alias for start)\n    maintenance         Run maintenance tasks\n    check               Checks the OCI containers\n    version             Get the version of the Synapse instance\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --version             show program\'s version number and exit\n  -d, --debug           Enables debugging mode.\n```\n\n## Installation\n\nMatrixCtl is written in Python. The installation is straight forward. Just run ``pip install matrixctl``. MatrixCtl will be installd from the [Python Package Index (PyPi)](https://pypi.org/project/matrixctl/).\n\nYou will find more information in the documentation.\n\n## Documentation\n\nThere is a [documentation](https://michaelsasser.github.io/matrixctl/index.html) waiting for you, showing you how everything works and howto setup matrixctl\n\n## Configuration File\n\nTo use this program you need to have this config file in\n"/etc/matrixctl/config" or in "~/.config/matrixctl/config".\n\nCheck out the documentation for more information.\n\n```toml\n[ANSIBLE]\n# The absolute path to your playbook\n#\n# Playbook="/absolut/path/to/the/playbook"\n\n[SYNAPSE]\n# The absolute path to the synapse playbook.\n# This is only used for updating the playbook.\n#\n# Playbook = "/absolut/path/to/the/playbook"\n\n[API]\n# If your matrix server is deployed, you may want to fill out the API section.\n# It enables matrixctl to run more and faster commands. You can deploy and\n# provision your Server without this section. You also can cerate a user with\n# "matrixctl adduser --ansible YourUsername" and add your privileges after\n# that.\n\n# Your domain should be something like "michaelsasser.org" without the\n# "matrix." in the front. MatrixCtl will add that, if needed. An IP-Address\n# is not enough.\n#\n# Domain = "domain.tld"\n\n# To use the server-notice feature, you need to have a contact username set.\n# If your user is "@michael:MichaelSasser.org" you set "michael" as username.\n# Keep in mind, you need to enable the server-notice feature on your\n# homeserver first.\n#\n# Username = "MyMatrixUserName"\n\n# To use the API you need to have an administrator account. Enter your Token\n# here. If you use the element client you will find it your user settings (click\n# on your username on the upper left corner on your browser) in the\n# "Help & About" tab. If you scroll down click next to "Access-Token:" on\n# "<click to reveal>". It will be marked for you. Copy it in here.\n#\n# Token= " MySuperLongMatrixToken"\n\n[SSH]\n# Here you can add your SSH configuration.\n#\n# Address = "matrix.domain.tld"\n\n# The default port is 22\n#\n# Port = 22\n\n# The default username is your current login name.\n#\n# User = "MyUserSystemAccountName"\n```\n\n## Chat\n\nIf you have any thoughts or questions, you can join the project channel ``#matrixctl:michaelsasser.org``.\n\n## Semantic Versioning\n\nThis repository uses [SemVer](https://semver.org/) for its release\ncycle.\n\n## Branching Model\n\nThis repository uses the\n[git-flow](https://danielkummer.github.io/git-flow-cheatsheet/index.html)\nbranching model by [Vincent Driessen](https://nvie.com/about/).\nIt has two branches with infinite lifetime:\n\n* [master](https://github.com/MichaelSasser/matrixctl/tree/master)\n* [develop](https://github.com/MichaelSasser/matrixctl/tree/develop)\n\nThe master branch gets updated on every release. The develop branch is the\nmerging branch.\n\n## License\nCopyright &copy; 2020 Michael Sasser <Info@MichaelSasser.org>. Released under\nthe GPLv3 license.\n',
    'author': 'Michael Sasser',
    'author_email': 'Michael@MichaelSasser.org',
    'maintainer': 'Michael Sasser',
    'maintainer_email': 'Michael@MichaelSasser.org',
    'url': 'https://michaelsasser.github.io/matrixctl/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
