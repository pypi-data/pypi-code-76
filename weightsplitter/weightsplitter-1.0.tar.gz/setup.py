from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='weightsplitter',
    version='1.0',
    packages=find_packages(),
    author='PunchyArchy',
    author_email='ksmdrmvscthny@gmail.com',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=[
        'portdatasplitter',
    ],
)
