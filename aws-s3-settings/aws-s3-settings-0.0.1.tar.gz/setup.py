# encoding: utf-8
from setuptools import setup

setup(
    name='aws-s3-settings',
    version='0.0.1',
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
    }
)
