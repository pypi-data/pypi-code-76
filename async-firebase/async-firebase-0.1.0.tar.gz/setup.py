# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_firebase']

package_data = \
{'': ['*']}

install_requires = \
['google-auth>=1.26,<1.27', 'httpx>=0.16,<0.17', 'requests>=2.25.1,<2.26.0']

setup_kwargs = {
    'name': 'async-firebase',
    'version': '0.1.0',
    'description': 'Async Firebase Client - a Python asyncio client to interact with Firebase Cloud Messaging.',
    'long_description': '# Async Firebase Cloud Messaging client\n\n[![PyPI download total](https://img.shields.io/pypi/dt/async-firebase.svg)](https://pypi.python.org/pypi/async-firebase/)\n[![PyPI download month](https://img.shields.io/pypi/dm/async-firebase.svg)](https://pypi.python.org/pypi/async-firebase/)\n[![PyPI version fury.io](https://badge.fury.io/py/async-firebase.svg)](https://pypi.python.org/pypi/async-firebase/)\n[![PyPI license](https://img.shields.io/pypi/l/async-firebase.svg)](https://pypi.python.org/pypi/async-firebase/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/async-firebase.svg)](https://pypi.python.org/pypi/async-firebase/)\n[![GitHub Workflow Status for CI](https://img.shields.io/github/workflow/status/healthjoy/async-firebase/CI?label=CI&logo=github)](https://github.com/healthjoy/async-firebase/actions?query=workflow%3ACI)\n[![Codacy coverage](https://img.shields.io/codacy/coverage/b6a59cdf5ca64eab9104928d4f9bbb97?logo=codacy)](https://app.codacy.com/gh/healthjoy/async-firebase/dashboard)\n\nAsync Firebase - is a lightweight asynchronous client to interact with Firebase.\n\n  * Free software: MIT license\n  * Requires: Python 3.6+\n\n## Features\n TBD...\n\n## Installation\n```shell script\n$ pip install async-firebase\n```\n\n## Getting started\nTo send push notification to either Android or iOS device:\n```python3\nimport asyncio\n\nfrom async_firebase import AsyncFirebaseClient\n\n\nasync def main():\n    client = AsyncFirebaseClient()\n    client.creds_from_service_account_file("secret-store/mobile-app-79225efac4bb.json")\n\n    device_token = "..."\n\n    response = await client.push(\n        device_token=device_token,\n        notification_title="Store Changes",\n        notification_body="Recent store changes",\n        notification_data={\n            "discount": "15%",\n            "key_1": "value_1"\n        },\n        priority="normal",\n        apns_topic="store-updates",\n        collapse_key="push",\n        alert_text="test-alert",\n        category="test-category",\n        badge=1,\n    )\n\n    print(response)\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\nThis prints:\n```shell script\n{"name": "projects/mobile-app/messages/0:2367799010922733%7606eb557606ebff"}\n```\n\n## License\n\n``async-firebase`` is offered under the MIT license.\n\n## Source code\n\nThe latest developer version is available in a GitHub repository:\nhttps://github.com/healthjoy/async-firebase\n',
    'author': 'Aleksandr Omyshev',
    'author_email': 'oomyshev@healthjoy.com',
    'maintainer': 'Healthjoy Developers',
    'maintainer_email': 'developers@healthjoy.com',
    'url': 'https://github.com/healthjoy/async-firebase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
