# coding:utf-8
# author caturbhuja
# date   2020/9/4 11:00 上午
# wechat chending2012
import os
import pypandoc

from setuptools import setup, find_packages

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def long_description(filename="to_git.md"):
    if os.path.isfile(os.path.expandvars(filename)):
        ld = pypandoc.convert_file(filename, "rst")
    else:
        ld = ""
    return ld


long_description = long_description("Readme.md")

setup(
    name='DbFactory',
    version='1.0.12',
    description='Easy Connection, A module for all db!',
    # long_description=long_description,
    packages=find_packages(),
    author='Caturbhuja',
    author_email='caturbhuja@foxmail.com',
    url='',
    install_requires=[
        'pymysql>=0.10.0',
        # 'elasticsearch>=7.10.0',
        'redis>=3.5.3',
        'redis-py-cluster>=2.1.0',
        'DBUtils>=1.0.2',
        'kafka-python>=2.0.1',
        'cacheout>=0.11.2',
        # 'dlog==1.0.5',
    ],
    license='MIT'
)

# os.system('rm -rf README.rst')
