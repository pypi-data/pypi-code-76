"""
Author:     LanHao
Date:       2021/2/8 14:49
Python:     python3.6

"""

from setuptools import setup, find_packages

description = "基于rabbitmq的轻量级rpc调用封装"

setup(
    name='leaves',
    version="0.1.4",
    description=description,
    long_description=description,
    author="bigpangl",
    author_email='bigpangl@163.com',
    url='https://github.com/bigpangl/leaves',
    py_modules=['leaves'],
    install_requires=[
        "aiormq"
    ],
    include_package_data=True,
    keywords='rpc',
    classifiers=[
    ],
    license="Apache License 2.0"
)
