#!/usr/bin/env python3
from setuptools import setup

def get_readme():
    with open('README.md', 'r') as readme:
        return readme.read()

setup(
    name='bonnibel',
    description='Build script generator for the jsix operating system',
    version='3.0.1',
    url='https://github.com/justinian/bonnibel',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    keywords=['build', 'ninja', 'generator'],
    author='Justin C. Miller',
    author_email='justin@justin.cm',

    license='MIT',
    packages=['bonnibel'],
    scripts=['bin/pb'],
    install_requires=['click', 'ninja', 'toml'],

    include_package_data=True,
    package_data={'': ["*.ninja"]},

    zip_safe=False
)
