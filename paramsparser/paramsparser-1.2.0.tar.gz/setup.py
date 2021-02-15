from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='paramsparser',
    packages=['paramsparser'],

    version='1.2.0',

    license='MIT',

    install_requires=['PyYAML', 'ConfigParser'],

    author='pysan3',
    author_email='pysan3@gmail.com',

    url='https://github.com/pysan3/paramsparser.git',

    description='Parse parameters written in files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='paramsparser yaml PyYAML ConfigParser json',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)