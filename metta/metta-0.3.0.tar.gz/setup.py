# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metta',
 'metta.common',
 'metta.nodes',
 'metta.nodes.audio',
 'metta.nodes.inference',
 'metta.nodes.video',
 'metta.nodes.video.display_sink',
 'metta.nodes.video.video_source',
 'metta.proto']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.21,<0.30.0',
 'PyYAML>=5.3.1,<6.0.0',
 'aiokafka>=0.7.0,<0.8.0',
 'aiozk>=0.28.0,<0.29.0',
 'blosc>=1.10.1,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'kafka-python>=2.0.2,<3.0.0',
 'numpy>=1.19.4,<2.0.0',
 'opencv-python>=4.5.1,<5.0.0',
 'protobuf>=3.14.0,<4.0.0',
 'pyarrow>=2.0.0,<3.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'uvloop>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'metta',
    'version': '0.3.0',
    'description': 'Micro-service framework for real-time machine learning applications',
    'long_description': None,
    'author': 'Tony Francis',
    'author_email': 'tonyfrancisv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.2,<4.0.0',
}


setup(**setup_kwargs)
