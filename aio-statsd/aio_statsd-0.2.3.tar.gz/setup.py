# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_statsd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aio-statsd',
    'version': '0.2.3',
    'description': 'Simple and fast statsd client',
    'long_description': "## aiostasd\nan asyncio-based client for send metric to `StatsD`, `Graphite.carbon` and `DogStatsD`.\n\n## Installation\n```Bash\npip install aio_statsd\n```\n## Usage\n### Usage Client\nCreate connection and send gauge metric.\naiostatsd client will automatically send messages in the background when the loop is running\n```Python\nimport asyncio\nfrom aio_statsd import StatsdClient\n\n\nloop = asyncio.get_event_loop()\nclient = StatsdClient()\nloop.run_until_complete(client.connect())\nclient.gauge('test.key', 1)\nloop.run_forever()\n```\nUse context manager\n```Python\nimport asyncio\nfrom aio_statsd import StatsdClient\n\n\nasync def main():\n    async with StatsdClient() as client:\n        client.gauge('test.key', 1)\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\n### Client param\n- host: default value 'localhost', Statsd Server ip\n- port: default value 8125, Statsd Server port\n- protocol: default value ProtocolFlag.udp, Transport Layer Prrotocol, Select Tcp:`ProtocolFlag.udp` or Udp:`ProtocolFlag.tcp` \n- timeout: default value 0, send msg timeout, if timeout==0, not enable timeout\n- debug: default value False, enable debug\n- close_timeout: default value 5, Within a few seconds after the client is closed, continue to send messages which in the queue\n- create_timeout: default value 5, Create connection timeout\n- max_len: default value 10000, deque length\n- sample_rate(Use in StatsD Client, DogStatsD Client): default value 1, use sample rate in Statsd or DogStatsD\n### send metric\n```Python\nimport asyncio\nfrom aio_statsd import StatsdClient\n\n\nasync def main():\n    async with StatsdClient() as client:\n        client.gauge('test.key', 1)\n        client.counter('test.key', 1)\n        client.sets('test.key', 1)\n        client.timer('test.key', 1)\n        with client.timeit('test'):\n            pass  # run your code\n        \n        # all metric support sample rate\n        client.gauge('test1.key', 1, sample_rate=0.5)\n        \n        # mutli metric support(not support sample rate, the sample rate will always be set to 1)\n        from aio_statsd import StatsdProtocol\n        metric = StatsdProtocol()   \n        metric.gauge('test2.key', 1)\n        metric.sets('test2.key', 1)\n        client.send_statsd(metric)     \n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\n### Other Client\n#### Graphite(carbon)\n```python\nimport asyncio\nfrom aio_statsd import GraphiteClient\n\n\nloop = asyncio.get_event_loop()\nclient = GraphiteClient()\nloop.run_until_complete(client.connect())\nclient.send_graphite('test.key', 1) # Multiple clients timestamp interval synchronization\nloop.run_forever()\n```\n#### DogStatsD\n>Note: Not tested in production\n```python\nimport asyncio\nfrom aio_statsd import DogStatsdClient\n\n\nasync def main():\n    async with DogStatsdClient() as client:\n        client.gauge('test.key', 1)\n        client.distribution('test.key', 1)\n        client.increment('test.key',1)\n        client.histogram('test.key', 1)\n        client.timer('test.key', 1)\n        with client.timeit('test'):\n            pass  # run your code\n        \n        # all metric support sample rate and DogStatsD tag\n        client.gauge('test1.key', 1, sample_rate=0.5, tag_dict={'tag': 'tag1'})\n        \n        # mutli metric support(\n        #   DogStatsdProtocol will store the message in its own queue and\n        #   DogStatsDClient traverses to read DogStatsdProtocol's message and send it\n        # )\n        from aio_statsd import DogStatsdProtocol\n        metric = DogStatsdProtocol()   \n        metric.gauge('test2.key', 1, tag_dict={'tag': 'tag1'})\n        metric.histogram('test2.key', 1)\n        client.send_dog_statsd(metric, sample_rate=0.5)\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\n### Use in web frameworks\n[fast_tools example](https://github.com/so1n/fast-tools/blob/master/example/statsd_middleware.py)",
    'author': 'So1n',
    'author_email': 'qaz6803609@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/so1n/aiostatsd',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
