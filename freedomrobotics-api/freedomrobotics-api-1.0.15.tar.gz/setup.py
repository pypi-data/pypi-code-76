import re

from setuptools import setup

with open("freedomrobotics_api/__init__.py") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='freedomrobotics-api',
    version=version,
    packages=['freedomrobotics_api'],
    install_requires=['requests'],
)
