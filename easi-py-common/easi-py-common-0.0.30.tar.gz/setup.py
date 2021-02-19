# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easi_py_common',
 'easi_py_common.client',
 'easi_py_common.core',
 'easi_py_common.jwt',
 'easi_py_common.s3',
 'easi_py_common.sqs']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.19,<2.0.0',
 'flask-redis>=0.4.0,<0.5.0',
 'flask-sqlalchemy>=2.4.4,<3.0.0',
 'flask-uploads>=0.2.1,<0.3.0',
 'flask-wtf>=0.14.3,<0.15.0',
 'flask>=1.1.2,<2.0.0',
 'flaskerk>=0.6.3,<0.7.0',
 'gevent>=20.9.0,<21.0.0',
 'itsdangerous>=1.1.0,<2.0.0',
 'orjson>=3.4.3,<4.0.0',
 'pydantic>=1.7.2,<2.0.0',
 'pymysql>=0.10.1,<0.11.0',
 'pytz>=2020.4,<2021.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.25.0,<3.0.0',
 'werkzeug>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'easi-py-common',
    'version': '0.0.30',
    'description': '',
    'long_description': None,
    'author': 'wangziqing',
    'author_email': 'eininst@aliyun.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://poetry.eustace.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
