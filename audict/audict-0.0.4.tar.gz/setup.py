#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Bamboo - 20210218Thu


from setuptools import setup, find_packages


setup(
    name='audict',
    version='0.0.4',
    description='generates subtitles for video',
    author='bamboo',
    author_email='wenzhu_art@hotmail.com',
    url='https://github.com/wenzhuart/audict',
    # packages=['audict', 'audict/autosub'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'audict = audict:main',
        ],
    },
    install_requires=[
        'google-api-python-client>=1.4.2',
        'requests>=2.3.0',
        'pysrt>=1.0.1',
        'progressbar2>=3.34.3',
        'six>=1.11.0',
    ],
)
