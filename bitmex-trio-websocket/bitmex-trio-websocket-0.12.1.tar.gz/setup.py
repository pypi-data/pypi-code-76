# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitmex_trio_websocket']

package_data = \
{'': ['*']}

install_requires = \
['async_generator>=1.10,<2.0',
 'pendulum>=2.0.5,<3.0.0',
 'slurry-websocket>=0.2.7,<0.3.0',
 'sortedcontainers>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'bitmex-trio-websocket',
    'version': '0.12.1',
    'description': 'Websocket implementation for BitMEX cryptocurrency derivatives exchange.',
    'long_description': '# BitMEX Trio-Websocket\n\n\n[![PyPI](https://img.shields.io/pypi/v/bitmex_trio_websocket.svg)](https://pypi.python.org/pypi/bitmex-trio-websocket)\n[![Build Status](https://img.shields.io/travis/com/andersea/bitmex-trio-websocket.svg)](https://travis-ci.com/andersea/bitmex-trio-websocket)\n\nWebsocket implementation for BitMEX cryptocurrency derivatives exchange.\n\n* Free software: MIT license\n\n## Features\n\n* Supports authenticated connections using api keys.\n* Uses SortedDict as backend storage for easy and fast table searching.\n* Fully async using async generators. No callbacks or event emitters.\n* Based on [Slurry](https://slurry.readthedocs.io/en/latest/) and [Slurry-websocket](https://github.com/andersea/slurry-websocket). \n\n## Installation\n\nThis library requires Python 3.6 or greater. \n\nTo install from PyPI:\n\n    pip install bitmex-trio-websocket\n\n## Client example\n\n    import trio\n    from async_generator import aclosing\n\n    from bitmex_trio_websocket import open_bitmex_websocket\n\n    async def main():\n        async with open_bitmex_websocket(\'testnet\') as bws:\n            async with aclosing(bws.listen(\'instrument\')) as agen:\n                async for msg in agen:\n                    print(f\'Received message, symbol: \\\'{msg["symbol"]}\\\', timestamp: \\\'{msg["timestamp"]}\\\'\')\n\n    if __name__ == \'__main__\':\n        trio.run(main)\n\nThis will print a sequence of dicts for each received item on inserts (including partials) or updates.\n\n## API\n\n![async def](https://img.shields.io/badge/async%20with-open__bitmex__websocket(network%2C%20api__key%2C%20api__secret%2C%20*%2C%20dead_mans_switch)-blue)\n\nCreates a new websocket object.\n\nThis is an async context manager, so it needs to be used with the `async with .. as ..:` construct. The returned value is a BitMEXWebsocket object.\n\n**`network`** str\n\nNetwork to connect to. Options: \'mainnet\', \'testnet\'.\n\n**`api_key`** Optional\\[str\\]\n\nApi key for authenticated connections. \n\n**`api_secret`** Optional\\[str\\]\n\nApi secret for authenticated connections.\n\n**`dead_mans_switch`** Optional\\[bool\\]\n\nWhen enabled, the websocket will periodically send cancelAllAfter messages with a timeout of 60 seconds. The timer is refreshed every 15 seconds.\n\nSee: https://www.bitmex.com/app/wsAPI#Dead-Mans-Switch-Auto-Cancel\n\n![bitmex__trio__websocket.BitMEXWebsocket](https://img.shields.io/badge/class-bitmex__trio__websocket.BitMEXWebsocket-blue?style=flat-square)\n\n\n![await listen](https://img.shields.io/badge/await-listen(table,%20symbol=None)-green)\n\nSubscribes to the channel and optionally a specific symbol. It is possible for multiple listeners\nto be listening using the same subscription.\n\nReturns an async generator object that yields messages from the channel.\n\n**`table`** str\n\nChannel to subscribe to.\n\n**`symbol`** Optional[str]\n\nOptional symbol to subscribe to.\n\n![storage](https://img.shields.io/badge/attribute-storage-teal)\n\nThis attribute contains the storage object for the websocket. The storage object caches the data tables for received\nitems. The implementation uses SortedDict from [Sorted Containers](http://www.grantjenks.com/docs/sortedcontainers/index.html),\nto handle inserts, updates and deletes.\n\nThe storage object has two public attributes `data`, and `keys`.\n\n`data` contains the table state for each channel as a dictionary with the table name as key. The tables are sorted dictionaries, stored with key tuples generated from each item using the keys schema received in the initial partial message.\n\n`data[\'orderBookL2\']` is a special state dictionary for the orderBookL2 table. It is a double nested defaultdict, with a SortedDict containing each price level. The nested dictionaries are composed like this:\n\n    # Special storage for orderBookL2\n    # dict[symbol][side][id]\n    self.data[\'orderBookL2\'] = defaultdict(lambda: defaultdict(SortedDict))\n\n`keys` contains a mapping for lists of keys by which to look up values in each table.\n\nIn addition the following helper methods are supplied:\n\n`make_key(table, match_data)` creates a key for searching the `data` table. Raises `ValueError` if `table == \'orderBookL2\'`, since this table needs special indexing.\n\n`parse_timestamp(timestamp)` static method for converting BitMEX timestamps to datetime with timezone (UTC).\n\n## Credits\n\nThanks to the [Trio](https://github.com/python-trio/trio) and [Trio-websocket](https://github.com/HyperionGray/trio-websocket) libraries for their awesome work.\n\nThe library was originally based on the [reference client](https://github.com/BitMEX/api-connectors/tree/master/official-ws), but is now substantially redesigned.\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.\n',
    'author': 'Anders Ellenshøj Andersen',
    'author_email': 'andersa@ellenshoej.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andersea/bitmex-trio-websocket',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
