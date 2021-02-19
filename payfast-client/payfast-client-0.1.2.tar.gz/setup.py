# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['payfast_client']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2021.1,<2022.0', 'requests-futures>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'payfast-client',
    'version': '0.1.2',
    'description': 'Python client for interacting with the Payfast API',
    'long_description': '# payfast-python-client\n\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0a0a2acf5df045ceb533c8ee953d23a2)](https://app.codacy.com/gh/fergusdixon/payfast-python-client?utm_source=github.com&utm_medium=referral&utm_content=fergusdixon/payfast-python-client&utm_campaign=Badge_Grade)\n\nAsynchronous Python Client for the [Payfast API](https://developers.payfast.co.za/api)\n\nUses [requests-futures](https://github.com/ross/requests-futures)\n\n## Installation\nAvailable on [PyPi](https://pypi.org/project/payfast-client/)\n```shell\npip install payfast-client\n```\n\n## Usage\n ```python\nfrom payfast_client import PayfastClient\nclient = PayfastClient(merchant_id=123, merchant_passphrase="passphrase")\nsubscription = client.fetch_subscription(token="abc")\nprint(subscription)\n```\n```\n<Future at 0x107d88520 state=finished returned Response>\n```\n```python\nprint(subscription.result())\n```\n```\n<Response [200]>\n```\n\n## Features\n- [x] Signature Generation\n- [ ] Error Handling (Sometimes errors returned with response_code=200)\n- Endpoints\n    - [x] GET /ping\n    - Recurring Billing\n        - [x] GET   /subscriptions/:token/fetch\n        - [x] PUT   /subscriptions/:token/pause\n        - [x] PUT   /subscriptions/:token/unpause\n        - [x] PUT   /subscriptions/:token/cancel\n        - [x] PATCH /subscriptions/:token/update\n        - [ ] POST  /subscriptions/:token/adhoc\n    - Transaction History\n        - [ ] GET   /transactions/history\n        - [ ] GET   /transactions/history/daily\n        - [ ] GET   /transactions/history/weekly\n        - [ ] GET   /transactions/history/monthly\n    - Credit card transaction query\n        - [ ] GET   /process/query/:id\n',
    'author': 'Fergus Strangways-Dixon',
    'author_email': 'fergusdixon101@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fergusdixon/payfast-python-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
