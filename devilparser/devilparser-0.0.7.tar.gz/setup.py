import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name="devilparser",
    version="0.0.7",
    author="Drew Stinnett",
    author_email="drew@drewlink.com",
    description=
    ("Load RC type files with the ability to use shell commands like lpass to get passwords"
     ),
    install_requires=install_requirements,
    license="BSD",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    keywords="lpass secuirty config",
    packages=['devilparser'],
    scripts=['scripts/devilparser-cat.py'],
    long_description=read('README.md'),
)
