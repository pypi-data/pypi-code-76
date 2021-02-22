# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['exec_notifier']
install_requires = \
['requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['exec_notifier = exec_notifier:main']}

setup_kwargs = {
    'name': 'exec-notifier',
    'version': '0.1.23',
    'description': 'Tool to notify you when command will be executed.',
    'long_description': '# Execution Notifier\n[![PyPI](https://img.shields.io/pypi/v/exec-notifier)](https://pypi.org/project/exec-notifier/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Actions Status](https://github.com/tikerlade/exec-notifier/workflows/Deploy%20Bot/badge.svg)](https://github.com/tikerlade/exec-notifier/actions/)\n[![Actions Status](https://github.com/tikerlade/exec-notifier/workflows/Release%20to%20PyPI/badge.svg)](https://github.com/tikerlade/exec-notifier/actions/)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/tikerlade/exec-notifier/master.svg)](https://results.pre-commit.ci/latest/github/tikerlade/exec-notifier/master)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/exec-notifier)\n\nThis tool provides you ability to send yourself information about looong executed command when it is done. Information will be sent using Telegram Bot. Logs and error messages (if they\'ll occur) will be delivered too.\n\nIf your log will be too long (longer 1_000_000 signs we\'ll not send it).\n\n## Prerequisites\n\n1. Python 3.4 or higher\n2. Telegram ID - get it from [@exec_notifier_bot](https://telegram.me/exec_notifier_bot) by using `/start` command.\n\n## Installation and running\nYou need to run your commands in quotes(`""`) when passing script to run.\n\n```shell\n>>> pip install exec-notifier\n>>> exec_notifier config --telegram_id=YOUR_TELEGRAM_ID\n>>> exec_notifier notify "[your_command_here]"\n```\n\n## Examples\n\n```shell\n>>> exec_notifier notify "ls -l | head"\n>>> exec_notifier notify "ls -l > output.txt"\n>>> exec_notifier notify "ls -l && sleep 3 && ps"\n>>> exec_notifier notify "zip Downloads"\n```\n\n## Future\n* Your own bot support will be added\n',
    'author': 'Ivan Kuznetsov',
    'author_email': 'tikerlade@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tikerlade/exec-notifier',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
