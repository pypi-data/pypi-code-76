# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='challonge-wrapper',
    version='0.2.3',
    description='Challonge REST API wrappers',
    long_description_content_type='text/markdown',
    long_description=readme,
    author='Giuseppe Termerissa',
    author_email='linkohprismriver@gmail.com',
    url='https://github.com/Impasse52/challonge-python-wrapper',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['requests']
)