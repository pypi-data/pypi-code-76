# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['agarilog', 'agarilog.handlers', 'agarilog.handlers.web']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.7.3,<4.0.0', 'pydantic[dotenv]>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'agarilog',
    'version': '0.2.0',
    'description': 'simple logger for message services.',
    'long_description': 'agarilog\n========\n\n|PyPI version| |Python Versions|\n\n.. |PyPI version| image:: https://badge.fury.io/py/agarilog.svg\n    :target: https://pypi.org/project/agarilog/\n    :alt: PyPI version\n\n.. |Python versions| image:: https://img.shields.io/pypi/pyversions/agarilog.svg\n    :target: https://pypi.org/project/agarilog/\n    :alt: Python versions\n\n\nThis is simple logger for message service.\n\n想定用途\n==========\n\n| 長時間のバッチ処理やサービスのデモなどのloggerを想定。\n| 他から呼ばれることを想定したライブラリなどには向きません。\n\n\nInstallation\n------------\n\n.. code-block::\n\n    pip install agarilog\n\nFeatures\n--------\n\nUse .env file.\n##############################\n\n.. code-block:: python\n\n    >>> import agarilog as logger\n    >>> logger.info("Hello agarilog!")\n\nUse any .env file.\n##########################\n\n.. code-block:: python\n\n    >>> from agarilog import get_logger\n    >>> logger = get_logger(name=__name__, env_file="dev.env")\n    >>> logger.info("Hello agarilog!")\n\nThis is use :code:`dev.env` file.\n\nTelegram\n########\n\n.. image:: https://github.com/sakuv2/agarilog/blob/main/img/telegram_sample.png?raw=true\n\nSlack\n#####\n\n.. image:: https://github.com/sakuv2/agarilog/blob/main/img/slack_sample.png?raw=true\n\nChatwork\n########\n\n.. image:: https://github.com/sakuv2/agarilog/blob/main/img/chatwork_sample.png?raw=true\n\nTerminal\n########\n\n.. image:: https://github.com/sakuv2/agarilog/blob/main/img/terminal_sample.png?raw=true\n\nEnvironment\n-----------\n\n| 環境変数にサービスごとの設定を登録する。\n| もしくは実行パスと同じ場所の :code:`.env` ファイルに記述する。\n| importの方法を変えることで任意のファイルを読み込むこともできる。(上記参照)\n\n**Environment variables will always take priority over values loaded from a dotenv file.**\n\nLOG_XXXX_LEVEL: ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]\n\nTelegram\n########\n\n.. code-block::\n\n    LOG_TELEGRAM_TOKEN=XXXXXXXXX:YYYYYYYYYYYYYYYYYYYYYYYYYYYY\n    LOG_TELEGRAM_CHAT_ID=XXXXXXXX\n    LOG_TELEGRAM_LEVEL=WARNING # default is warning\n\nSlack\n#####\n\n.. code-block::\n\n    LOG_SLACK_TOKEN=xxxx-YYYYYYYYYYYY-YYYYYYYYYYYY-xxxxxxxxxxxxxxxxxxxxx\n    LOG_SLACK_CHANNEL=XXXXXXXXXXX\n    LOG_SLACK_LEVEL=WARNING # default is warning\n\nChatwork\n########\n\n.. code-block::\n\n    LOG_CHATWORK_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n    LOG_CHATWORK_ROOM_ID=XXXXXXXXX\n    LOG_CHATWORK_LEVLE=WARNING # default is warning\n\nTerminal\n########\n\n.. code-block::\n\n    LOG_TERMINAL_TYPE=COLOR # default is COLOR\n    LOG_TERMINAL_LEVEL=WARNING # default is warning\n\nLOG_TERMINAL_TYPE: ["NONE", "PRINT", "NORMAL", "COLOR"]\n\n\nDevelopment\n-----------\n\n| :code:`git clone` したら最初に実行すること。\n| 仮想環境作成と :code:`pre-commit` のインストールが行われる。\n\n.. code-block::\n\n    $ make init\n',
    'author': 'agari',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sakuv2/agarilog',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
