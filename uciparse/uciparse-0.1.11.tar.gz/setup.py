# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['uciparse']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ucidiff = uciparse.cli:diff',
                     'uciparse = uciparse.cli:parse']}

setup_kwargs = {
    'name': 'uciparse',
    'version': '0.1.11',
    'description': 'Parse and emit OpenWRT uci-format files',
    'long_description': "# UCI Parse Library\n\n[![pypi](https://img.shields.io/pypi/v/uciparse.svg)](https://pypi.org/project/uciparse/)\n[![license](https://img.shields.io/pypi/l/uciparse.svg)](https://github.com/pronovic/uci-parse/blob/master/LICENSE)\n[![wheel](https://img.shields.io/pypi/wheel/uciparse.svg)](https://pypi.org/project/uciparse/)\n[![python](https://img.shields.io/pypi/pyversions/uciparse.svg)](https://pypi.org/project/uciparse/)\n[![Test Suite](https://github.com/pronovic/uci-parse/workflows/Test%20Suite/badge.svg)](https://github.com/pronovic/uci-parse/actions?query=workflow%3A%22Test+Suite%22)\n[![docs](https://readthedocs.org/projects/uci-parse/badge/?version=stable&style=flat)](https://uci-parse.readthedocs.io/en/stable/)\n[![coverage](https://coveralls.io/repos/github/pronovic/uci-parse/badge.svg?branch=master)](https://coveralls.io/github/pronovic/uci-parse?branch=master)\n\nPython 3 library and command line tools to parse, diff, and normalize OpenWRT\n[UCI](https://openwrt.org/docs/guide-user/base-system/uci) configuration files.\n\nThese tools were written to ease OpenWRT upgrades, making it easier to see the\ndifferences between two config files.  As of this writing (mid-2020), OpenWRT\nupgrades often don't normalize upgraded config files in the same way from\nversion to version.  For instance, the new version from `opkg upgrade` (saved\noff with a `-opkg` filename) might use single quotes on all lines, while the\noriginal version on disk might not use quotes at all.  This makes it very\ndifficult understand the often-minimal differences between an upgraded file and\nthe original file.\n\n## Installing the Package\n\nInstalling this package on your OpenWRT router is not as simple as it could be.\nA lot of routers do not have enough space available to install a full version\nof Python including `pip` or `setuptools`.  If yours does have lots of space,\nit's as simple as this:\n\n```\n$ opkg update\n$ opkg install python3-pip\n$ pip3 install uciparse\n```\n\nIf not, it gets a little ugly.  First, install `wget` with support for HTTPS:\n\n```\n$ opkg update\n$ opkg install wget libustream-openssl20150806 ca-bundle ca-certificates\n```\n\nThen, go to [PyPI](https://pypi.org/project/uciparse/#files) and copy the\nURL for the source package `.tar.gz` file.  Retrieve the source package \nwith `wget` and then manually extract it:\n\n```\n$ wget https://files.pythonhosted.org/.../uciparse-0.1.2.tar.gz\n$ tar zxvf uciparse-0.1.2.tar.gz\n$ cd uciparse-0.1.2\n```\n\nFinally, run the custom install script provided with the source package:\n\n```\n$ sh ./scripts/install\n```\n\nThis installs the OpenWRT `python3-light` package, then copies the Python\npackages into the right `site-packages` directory and the `uciparse` and\n`ucidiff` scripts to `/usr/bin`.\n\n## Using the Tools\n\nOnce you have installed the package as described above, the `uciparse` and\n`ucidiff` tools will be available in your path.  \n\n### ucidiff\n\nThe `ucidiff` tool is probably the tool you'll use most often when updating\nyour router.  It reads two UCI configuration files from disk, normalizes both in\nmemory (without making changes on disk), and then compares them.  The result is\na unified diff, like `diff -Naur`.  This gives you a way to understand the real\ndifferences between two files without ever having to change anything on disk.\n\n```\n$ ucidiff --help\nusage: ucidiff [-h] a b\n\nDiff two UCI configuration files.\n\npositional arguments:\n  a           Path to the first UCI file to compare\n  b           Path to the second UCI file to compare\n\noptional arguments:\n  -h, --help  show this help message and exit\n\nThe comparison is equivalent to a 'diff -Naur' between the normalized versions\nof the files. If either file can't be parsed, then an error will be returned\nand no diff will be shown.\n```\n\n### uciparse\n\nIf you would prefer to clean up and normalize your configuration files on disk,\nthen you can use the `uciparse` tool.  It reads a UCI config file from disk or\nfrom `stdin`, parses it, and prints normalized output to `stdout`.  \n\n```\n$ uciparse --help\nusage: uciparse [-h] uci\n\nParse and normalize a UCI configuration file.\n\npositional arguments:\n  uci         Path to the UCI file to normalize, or '-' for stdin\n\noptional arguments:\n  -h, --help  show this help message and exit\n\nResults will be printed to stdout. If the file can't be parsed then an error\nwill be returned and no output will be generated.\n```\n\nBefore using ``uciparse``, you should make a backup of any config file that you\nare going to normalized.\n",
    'author': 'Kenneth J. Pronovici',
    'author_email': 'pronovic@ieee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/uciparse/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
