from setuptools import setup, find_namespace_packages

import os

version = os.environ.get('RELEASE_VERSION', '0.0.0')

setup(
    name='jonstout-actions-demo',
    version=version,
    description='Small examply for working with github actions.',
    author='Jonathan Stout',
    author_email='jonstout@globalnoc.iu.edu',
    license='Apache Software License',
    packages=find_namespace_packages(include=['jonstout.*']),
    zip_safe=False
)
