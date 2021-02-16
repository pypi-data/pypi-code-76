# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brewblox_service']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-apispec>=2.2.1,<3.0.0',
 'aiohttp>=3.7.3,<4.0.0',
 'aiomqtt>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'brewblox-service',
    'version': '0.32.2',
    'description': 'Scaffolding for Brewblox backend services',
    'long_description': "# Scaffolding for Brewblox service applications\n\nIn order to reduce code duplication between services, generic functionality is implemented here.\n\nFor an example on how to implement your own service based on `brewblox-service`, see <https://github.com/brewblox/brewblox-boilerplate>.\n\n`brewblox-service` can technically be launched as a standalone application, but will not be very useful.\n\n## [brewblox_service](./brewblox_service/__init__.py)\n\nSmall generic tools are defined here.\n\n`brewblox_logger` can be used for creating module-specific loggers. It is not required, but will play a bit nicer with default formatting of the log.\n\nExample:\n\n```python\nfrom brewblox_service import brewblox_logger\n\nLOGGER = brewblox_logger(__name__)\nLOGGER.info('hello')\n```\n\n## [service.py](./brewblox_service/service.py)\n\nParses commandline arguments, creates an `aiohttp` app, and runs it.\n\nThe shortest implementation is:\n\n```python\napp = service.create_app(default_name='my_service')\nservice.furnish(app)\nservice.run(app)\n```\n\nThis will get you a working web application, but it will only support the `/_service/status` health check endpoint.\n\nApplications can configure their own features, and add new commandline arguments.\n\nExample:\n\n```python\n# Separately creating the parser allows adding arguments to the default set\nparser = service.create_parser(default_name='my_service')\nparser.add_argument('--my-arg')\n\n# Now create the app\napp = service.create_app(parser=create_parser())\n\n# Add features for this service\ndevice.setup(app)\napi.setup(app)\n\n# Furnish and run\nservice.furnish(app)\nservice.run(app)\n```\n\n## [features.py](./brewblox_service/features.py)\n\nMany service features are application-scoped. Their lifecycle should span multiple requests, either because they are not request-driven, or because they manage asynchronous I/O operations (such as listening to AMQP messages).\n\nThe `ServiceFeature` class offers an abstract base class for this behavior. Implementing classes should define `startup(app)` and `shutdown(app)` functions, and those will be automatically called when the application starts up and shuts down.\n\nBoth `startup()` and `shutdown()` are called in an async context, making them the async counterparts of `__init__()` and `__del__()` functions.\n\nFeatures must be constructed after the app is created, but before it starts running. (`service.create_app()` and `service.run(app)`)\n\nThe `add()` and `get()` functions make it easy to centrally declare a feature, and then use it in any function that has a reference to the aiohttp app.\n\n## [mqtt.py](./brewblox_service/mqtt.py)\n\nThe replacement for the AMQP-based `events` module.\n\nThe major advantages over AMQP is that the protocol is simpler, and supports websocket transport.\nThis allows for it to be used outside a Brewblox network.\n\nMessages have a /-separated *topic* and a JSON-serialized body.\n\nTo publish data, all you need is the `publish(topic, message)` function.\n\nTo listen to incoming messages, you can combine `subscribe(topic)` with one or more calls to `listen(topic, callback)`.\nThe subscribe/listen functions allow for + and # wildcards to be used.\n\nFor a detailed explanation of how to use MQTT topics, see http://www.steves-internet-guide.com/understanding-mqtt-topics/.\n\nFor the Brewblox spec on how and where to publish data, see https://brewblox.netlify.app/dev/reference/event_logging.html.\n\nIncludes top-level convenience functions for `publish(topic, message)`, `listen(topic, callback)` and `subscribe(topic)`.\n",
    'author': 'BrewPi',
    'author_email': 'development@brewpi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
