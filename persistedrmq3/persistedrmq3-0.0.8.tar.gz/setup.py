# coding=utf8

__author__ = 'Alexander.Li'

from setuptools import setup, find_packages

version = '0.0.8'

setup(name='persistedrmq3',
      version=version,
      description="A simple MQ based on Redis pubsub, but won't lose message version 3",
      long_description="""\
A simple MQ based on Redis pubsub, but won't lose message version 2(Based on asyncio, only works on Python 3)
""",
      classifiers=[],
      keywords='MQ Redis Pubsub Persisted',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      url='https://github.com/ipconfiger/persistedRMQ3',
      license='GNU General Public License v3.0',
      packages=find_packages(exclude=['ez_setup', 'examples']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'aioredis',
      ],
      entry_points={},
      )
