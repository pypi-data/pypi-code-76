# encoding: utf-8
from setuptools import setup
import sys

PYTHON_VERSION = ".".join([str(x) for x in sys.version_info[0:2]])

setup(
    name='aws-s3-settings',
    version='0.0.2',
    packages=['aws_s3_settings'],
    url='https://github.com/plecto/aws-s3-settings/',
    license='MIT',
    author='Kristian Øllegaard',
    author_email='kristian@plecto.com',
    description='',
    install_requires=[
        'PyYAML',
        'boto3'
    ],
    entry_points={
        'console_scripts': [
            'aws-s3-settings = aws_s3_settings:run',
        ]
    },
    options={
      'build_scripts': {
          'executable': '/usr/bin/env python%s' % PYTHON_VERSION,
      },
  }
)
