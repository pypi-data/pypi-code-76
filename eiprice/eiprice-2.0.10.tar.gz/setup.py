import setuptools
from setuptools import find_packages


import os

dependencies = [
    'Unidecode',
    'nest_asyncio',
    'backoff',
    'requests-html',
    'user_agent'
]

setuptools.setup(
    name='eiprice',
    version='2.0.10',
    packages=find_packages(),
    install_requires=dependencies,
)
