#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : setup.py
@Time  : 2021/2/7 9:57
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""


from setuptools import setup, find_packages

setup_requirements = ['pytest-runner', ]

setup(
    version='0.1',
    author="Tao Xu",
    author_email='txu2008@outlook.com',
    description='Send email with pytest execution result',
    long_description='A plugin for send email with pytest execution result once execution is completed',
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ],
    license="MIT license",
    include_package_data=True,
    keywords=[
        'pytest', 'py.test', 'email',
    ],
    name='pytest-smtp',
    packages=find_packages(include=['pytest_smtp']),
    setup_requires=setup_requirements,
    url='https://github.com/txu2k8/pytest-smtp',
    zip_safe=True,
    install_requires=[
        'pytest',
        'pytest-runner'
    ],
    entry_points={
        'pytest11': [
            'pytest-smtp = pytest_smtp.plugin',
        ]
    }
)


if __name__ == '__main__':
    pass
