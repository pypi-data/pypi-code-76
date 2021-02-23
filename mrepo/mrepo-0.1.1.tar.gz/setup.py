# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mrepo']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'parse>=1.19.0,<2.0.0', 'ruamel.yaml>=0.16.12,<0.17.0']

entry_points = \
{'console_scripts': ['echo-all-commands = mrepo.process:echo_all_commands',
                     'echo-next-command = mrepo.process:echo_next_command',
                     'run-pipeline-stage-all = '
                     'mrepo.process:run_pipeline_stage_all']}

setup_kwargs = {
    'name': 'mrepo',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Matthew Hartley',
    'author_email': 'mhartley@cantab.net',
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
