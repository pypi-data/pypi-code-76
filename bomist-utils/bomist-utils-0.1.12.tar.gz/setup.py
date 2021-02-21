# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bomist_utils']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['bomist_utils = bomist_utils:cli']}

setup_kwargs = {
    'name': 'bomist-utils',
    'version': '0.1.12',
    'description': 'BOMIST Utilities',
    'long_description': "# BOMIST Utilities\n\nThings you can do with it:\n\n- Convert legacy workspaces into BOMIST v2 workspaces\n\n## How to install\n\nThis requires Python 3 and the Python Package Installer (pip3) to be installed.\nYou can download it here:\nhttps://www.python.org/downloads/\n\nOnce you have them installed, run the following command on your terminal:\n\n```\n$ pip3 install bomist_utils\n```\n\nAfter installing `bomist_utils` through `pip3` you'll end up with it available on your terminal.\n\nOn Windows you might have to re-launch your terminal in order for the `bomist_utils` command to be recognized.\n\nTo make sure it was properly installed run the following command:\n\n```\n$ bomist_utils --help\n```\n\nYou should see the available options.\n\n## Usage\n\n### Convert legacy workspaces\n\n```\n$ bomist_utils --dump1 --ws <wspath> [--out <outpath>]\n```\n\n`wspath` is the path of the workspace you want to dump. A `.ws` file must exist in it.\n\nA `legacy.bomist_dump` file will be created on `outpath` or in the folder the command was called from if the `--out` option is not used. This file can then be imported by BOMIST v2.\n\n#### **Limitations**\n\nAt the moment this utility can only convert and keep data connections between:\n\n```\nparts, documents, labels, storage, categories\n```\n\nProjects, orders and history won't be converted.\n\nTo import projects into the new version you can export your BOMs into CSV files in the legacy version (right-click > Export) and then import them in the new version. Parts will be accordingly assigned to BOM designators, as long as those parts exists in the workspace.\n\nNeed help? [Get in touch](https://bomist.com/support/contact/)\n\n---\n\nFor more info: [bomist.com](https://bomist.com)\n",
    'author': 'Mario Ribeiro',
    'author_email': 'mario@bomist.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bomist.com',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
