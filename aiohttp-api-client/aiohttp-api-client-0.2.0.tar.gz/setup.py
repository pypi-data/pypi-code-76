# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_api_client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3,<4']

setup_kwargs = {
    'name': 'aiohttp-api-client',
    'version': '0.2.0',
    'description': 'aiohttp based api client',
    'long_description': 'aiohttp-api-client\n===\n\nRequires: python 3.6+, aiohttp.\n\nExample:\n```python\nimport aiohttp\nfrom aiohttp_api_client.json_api import \\\n    JsonApiClient, JsonApiRequest, JsonApiError, JsonApiDetails\n\nasync def run(http_client: aiohttp.ClientSession):\n    api_client = JsonApiClient(http_client)\n\n    response = await api_client(JsonApiRequest(\'GET\', \'https://example.com/api/\'))\n    assert response.json == {\'ok\': True}\n\n    try:\n        await api_client(JsonApiRequest(\'GET\', \'https://example.com/api/bad-request/\'))\n    except JsonApiError as e:\n        assert e.details == JsonApiDetails(\n            http_status=400, http_reason=\'Bad Request\', content_type=\'application/json\',\n            bytes=b\'{"ok": false}\', text=\'{"ok": false}\',\n        )\n    else:\n        assert False\n```\n',
    'author': 'xppt',
    'author_email': '21246102+xppt@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xppt/py-aiohttp-api-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
