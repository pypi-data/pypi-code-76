import setuptools
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
    version='2.0.9',
    packages=["eiprice"],
    install_requires=dependencies,
)
