# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_bt_backup_tools']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'bencode.py>=4.0.0,<5.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['cat_bencode = '
                     'git_bt_backup_tools.pretty_print:pretty_print_bencoded']}

setup_kwargs = {
    'name': 'git-bt-backup-tools',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Smitten',
    'author_email': '77771103+C84186@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
