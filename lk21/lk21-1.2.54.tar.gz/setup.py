#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['lk21', 'lk21.extractors']

package_data = \
{'': ['*']}

install_requires = \
['PyInquirer', 'bs4', 'requests', 'colorama']

entry_points = \
{'console_scripts': ['lk21 = lk21:main']}

setup(name='lk21',
      version='1.2.54',
      description='cari film dan anime lewat terminal',
      author='Val',
      author_email='apklover76@gmail.com',
      url='https://github.com/zevtyardt',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      entry_points=entry_points,
     )
