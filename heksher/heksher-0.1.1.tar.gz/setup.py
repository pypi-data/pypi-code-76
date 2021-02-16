# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heksher', 'heksher.clients']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.16.0,<0.17.0', 'ordered-set>=4.0.0,<5.0.0', 'orjson>=3.0.0,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['mock>=4.0.0,<5.0.0']}

setup_kwargs = {
    'name': 'heksher',
    'version': '0.1.1',
    'description': '',
    'long_description': '# heksher SDK for python\nThis is a library for using a [heksher](https://github.com/biocatchltd/Heksher) server from within python.\nCompatible with python 3.7, 3.8, and 3.9. The library contains both an asynchronous client, as well as a thread-based\nclient. Also included are stub clients to make testing without a service simple.\n\n## Example usage\n```python\n# main.py\nfrom contextvars import ContextVar\nfrom heksher import AsyncHeksherClient, Setting\n\nuser = ContextVar(\'user\', default=\'guest\')\n\nclass App:\n    ...\n    \n    async def startup(self):\n        ...\n        \n        # initialize the client, and set it as the process\' main client\n        self.heksher_client = AsyncHeksherClient(\'http://heksher.service.url\',\n                                            update_interval=60, \n                                            context_features=[\'user\', \'trust\', \'theme\'])\n        # set certain context features to be retrieved either from string constants or\n        # context variables \n        self.heksher_client.set_defaults(user = user, theme="light")\n        await self.heksher_client.set_as_main()\n    \n    async def shutdown(self):\n        await self.heksher_client.close()        \n        ...\n\ncache_size_setting = Setting(\'cache_size\', type=int, configurable_features=[\'user\', \'trust\'], default_value=10)\ndef foo(trust: str):\n    ...\n    # should be run after App.startup is completed\n    cache_size = cache_size_setting.get(trust=trust)\n    ...\n```\nThread-based client usage is nearly identical. ',
    'author': 'Biocatch LTD',
    'author_email': 'serverteam@biocatch.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/biocatchltd/heksher-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
