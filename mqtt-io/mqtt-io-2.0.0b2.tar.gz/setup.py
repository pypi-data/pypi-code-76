# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mqtt_io',
 'mqtt_io.config',
 'mqtt_io.config.validation',
 'mqtt_io.modules',
 'mqtt_io.modules.gpio',
 'mqtt_io.modules.sensor',
 'mqtt_io.modules.stream',
 'mqtt_io.tests.features',
 'mqtt_io.tests.features.steps']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.2,<2.0.0',
 'PyYAML>=5.3.1',
 'hbmqtt>=0.9.6,<0.10.0',
 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

setup_kwargs = {
    'name': 'mqtt-io',
    'version': '2.0.0b2',
    'description': 'Expose GPIO modules (Raspberry Pi, Beaglebone, PCF8754, PiFace2 etc.), digital sensors (LM75 etc.) and serial streams to an MQTT server for remote control and monitoring.',
    'long_description': None,
    'author': 'Ellis Percival',
    'author_email': 'mqtt-io@failcode.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
