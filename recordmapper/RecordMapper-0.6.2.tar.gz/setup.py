# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['RecordMapper',
 'RecordMapper.appliers',
 'RecordMapper.avro',
 'RecordMapper.builders',
 'RecordMapper.common',
 'RecordMapper.csv',
 'RecordMapper.xml']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=4.5.4,<4.6.0',
 'dateparser>=1.0.0,<1.1.0',
 'defusedxml>=0.6.0,<0.7.0',
 'fastavro>=0.23.4,<0.24.0',
 'nose>=1.3.7,<1.4.0']

setup_kwargs = {
    'name': 'recordmapper',
    'version': '0.6.2',
    'description': 'Transform records using an Avro Schema and custom map functions',
    'long_description': '# RecordMapper\nRead, transform and write records using an Avro Schema and custom map functions.\n\n## Update PyPI version\n\n    poetry publish --build',
    'author': 'UDARealState Data engineering Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/urbandataanalytics/RecordMapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
