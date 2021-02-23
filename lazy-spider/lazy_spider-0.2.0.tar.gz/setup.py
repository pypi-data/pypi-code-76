# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['lazy_spider',
 'lazy_spider.generic',
 'lazy_spider.generic.spider',
 'lazy_spider.parse',
 'lazy_spider.templates',
 'lazy_spider.tools',
 'lazy_spider.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.2.0,<7.3.0',
 'baidu-aip>=2.2.18.0,<2.3.0.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'fonttools>=4.16.1,<4.17.0',
 'html2text>=2020.1.16,<2020.2.0',
 'lxml>=4.6.2,<4.7.0',
 'peewee>=3.14.0,<3.15.0',
 'pytest>=6.2.0,<6.3.0',
 'requests>=2.25.1,<2.26.0']

setup_kwargs = {
    'name': 'lazy-spider',
    'version': '0.2.0',
    'description': 'A lazy spider tools which intergrate lxml, requests, peewee......',
    'long_description': None,
    'author': 'notnotype',
    'author_email': '2056369669@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
