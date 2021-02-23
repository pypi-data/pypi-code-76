# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cocoro']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'fire>=0.4.0,<0.5.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['cocoro = cocoro:main']}

setup_kwargs = {
    'name': 'cocoro',
    'version': '0.1.2',
    'description': 'Utilities to use Sharp, COCORO API',
    'long_description': '# cocoro\nTools for COCORO API (SHARP products).\n\n## Appliances\n\nAPI commands were taken for Sharp, KI-JS50 (humidifying air purifier, [KI-JS50 加湿空気清浄機/空気清浄機：シャープ](https://jp.sharp/kuusei/products/kijs50/)).\n\nIt may work for other (humidifying) air purifiers.\n\n## Requirement\n\nYou need to get `appSecret` and `terminalAppIdKey` to control appliances.\n\nTo get them, you can use [mitmproxy](https://mitmproxy.org/).\n\nBy using mitmproxy, you will see following `POST` command while you are controlling COCORO in your smart phone:\n\n\n    POST https://hms.cloudlabs.sharp.co.jp/hems/pfApi/ta/setting/login/?appSecret=XXXXXXXXX…\n           ← 200 application/json 38b 308ms\n\nOpen this command and you will see:\n\n\n    2021-02-21 21:55:40 POST https://hms.cloudlabs.sharp.co.jp/hems/pfApi/ta/setting/login/?app\n                             Secret=<*************appSecret**********************>&serviceName=\n                             iClub\n                             ← 200 OK application/json 38b 308ms\n                Request                         Response                        Detail\n    Host:             hms.cloudlabs.sharp.co.jp\n    Content-Type:     application/json; charset=utf-8\n    Connection:       keep-alive\n    Accept:           */*\n    User-Agent:       smartlink_v200i Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X)\n                      AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148\n    Content-Length:   110\n    Accept-Language:  ja-jp\n    Accept-Encoding:  gzip, deflate, br\n    JSON                                                                                  [m:auto]\n    {\n        "terminalAppId":\n    "https://db.cloudlabs.sharp.co.jp/clpf/key/<************terminalAppIdKey*************>"\n    }\n\nFind `appSecret` and `terminalAppIdKey` values from above details.\n\nThen, make following configuration file as **~/.config/cocoro/config.yml**:\n\n```yml\n---\nappSecret: <*************appSecret**********************>\nterminalAppIdKey: <************terminalAppIdKey*************>\n```\n\n## Install\n\n### Using pip\n\n    $ pip install cocoro\n    $ cocoro <cmd>\n\n### Using source code\n\nUse poetry to setup the environment.\n\n    $ pip install poetry\n    $ git clone https://github.com/rcmdnk/cocoro.git\n    $ cd cocoro\n    $ poetry install\n    $ poetry run cocoro <cmd>\n\n## How to use\n\n    $ cocoro <cmd>\n\nAvailable commands are:\n\n* `on`: Switch on\n* `off`: Switch off\n* `humi_on`: Humidification on\n* `humi_off`: Humidification off\n* `mode_auto`: Set mode: Auto\n* `mode_sleep`: Set mode: Sleep\n* `mode_pollen`: Set mode: Pollen\n* `mode_quiet`: Set mode: Quiet\n* `mode_medium`: Set mode: Medium\n* `mode_high`: Set mode: High\n* `mode_recommendation`: Set mode: Recommendation\n* `mode_effective`: Set mode: Effective\n* `version`: Show version\n',
    'author': 'rcmdnk',
    'author_email': 'rcmdnk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rcmdnk/cocoro',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
