#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='nonebot_plugin_wordbank',
    version='1.0.0',
    description=(
        '基于nonebot2的无数据库的轻量问答插件'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Joenothing',
    author_email='912871833@qq.com',
    license='GPL-3.0 License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/Joenothing-lst/word-bank',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
)