# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vps_network',
 'vps_network.vps_api',
 'vps_network.vps_ping',
 'vps_network.vps_quick',
 'vps_network.vps_speed',
 'vps_network.vps_trace']

package_data = \
{'': ['*']}

install_requires = \
['click>=7,<8',
 'icmplib>=2.0,<3',
 'pydantic>=1.7,<2.0',
 'requests>=2.25,<3',
 'rich>=9.11,<10',
 'speedtest-cli>=2.1,<3']

setup_kwargs = {
    'name': 'vps-network',
    'version': '0.2.2',
    'description': 'VPS Network Speed Test',
    'long_description': '# VPS 网络测试工具\n\n![pytest](https://github.com/QiYuTechDev/vps_network/workflows/pytest/badge.svg)\n![Pylama Lint](https://github.com/QiYuTechDev/vps_network/workflows/Pylama%20Lint/badge.svg)\n![CodeQL](https://github.com/QiYuTechDev/vps_network/workflows/CodeQL/badge.svg)\n![Black Code Format Check](https://github.com/QiYuTechDev/vps_network/workflows/Black%20Code%20Format%20Check/badge.svg)\n![docker build](https://github.com/QiYuTechDev/vps_network/workflows/docker%20build/badge.svg)\n![docker release](https://github.com/QiYuTechDev/vps_network/workflows/docker%20release/badge.svg)\n\n网络速度测试工具箱\n\n## 警告\n\n    这是一款商业软件，使用之前请联系开发人员获取授权(admin@qiyutech.tech)\n    个人允许免费使用(仅允许用来测试属于自己的机器，并且不允许分享测试结果给第三方)。\n    禁止复刻(Fork)。\n\n## GitHub Action\n\n在 GitHub action 上需要设置 `VPS_API_KEY` 环境变量\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://vps.qiyutech.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
