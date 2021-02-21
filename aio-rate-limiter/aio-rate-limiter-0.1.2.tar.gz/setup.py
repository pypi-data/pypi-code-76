# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_rate_limiter']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'aio-rate-limiter',
    'version': '0.1.2',
    'description': 'Rate limit a function using Redis as a backend',
    'long_description': '# aio-rate-limiter\n\n[![](https://img.shields.io/pypi/v/aio-rate-limit.svg)](https://pypi.org/pypi/aio-rate-limit/) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n\nRate limit a function using Redis as a backend. This is a smaller library modeled after [python-redis-rate-limit](https://github.com/EvoluxBR/python-redis-rate-limit) but it uses [aioredis](https://github.com/aio-libs/aioredis). Supports Python 3.6+.\n\n## Installation\n\n```bash\npip install aio-rate-limiter\n```\n\n## Example\n\n```python\nimport logging\n\nfrom aio_rate_limiter import RateLimiter, TooManyRequests\nimport aioredis\n\nasync def example():\n    pool = await aioredis.create_redis_pool("redis://localhost:6379")\n    try:\n        async with RateLimiter(\n            redis_pool,\n            # Rate limit requests to a resource\n            "name-of-external-system",\n            # Allow up to 100 requests in 60 seconds\n            max_requests=100,\n            time_window=60\n        ):\n            async do_work()\n    except TooManyRequests:\n        logging.warning("Try again later")\n```\n\n## Development\n\n```bash\n# Install poetry\npip install poetry\n\n# Install all package dependencies\npoetry install\n\n# Launch a shell with dependencies available\npoetry shell\n\n# Run tests (requires Redis server running at localhost:6379)\npytest\n\n# When you\'re ready to publish...\n# Bump version\npoetry version <version>\n# Set your pypi token\nexport POETRY_PYPI_TOKEN_PYPI=\'...\'\n# Build and publish\npoetry build\npoetry publish\n```\n',
    'author': 'Jonathan Drake',
    'author_email': 'jdrake@narrativescience.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
