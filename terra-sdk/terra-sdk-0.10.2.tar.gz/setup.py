# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terra_sdk',
 'terra_sdk.client',
 'terra_sdk.client.lcd',
 'terra_sdk.client.lcd.api',
 'terra_sdk.core',
 'terra_sdk.core.auth',
 'terra_sdk.core.auth.data',
 'terra_sdk.core.bank',
 'terra_sdk.core.distribution',
 'terra_sdk.core.gov',
 'terra_sdk.core.market',
 'terra_sdk.core.msgauth',
 'terra_sdk.core.oracle',
 'terra_sdk.core.params',
 'terra_sdk.core.slashing',
 'terra_sdk.core.staking',
 'terra_sdk.core.staking.data',
 'terra_sdk.core.treasury',
 'terra_sdk.core.wasm',
 'terra_sdk.key',
 'terra_sdk.util']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'attrs>=20.3.0,<21.0.0',
 'bech32>=1.2.0,<2.0.0',
 'bip32utils>=0.3.post4,<0.4',
 'ecdsa>=0.16.1,<0.17.0',
 'mnemonic>=0.19,<0.20',
 'nest-asyncio>=1.5.1,<2.0.0',
 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'terra-sdk',
    'version': '0.10.2',
    'description': 'The Python SDK for Terra',
    'long_description': '![logo](./docs/img/logo.png)\n',
    'author': 'Terraform Labs, PTE.',
    'author_email': 'engineering@terra.money',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docs.terra.money/sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
