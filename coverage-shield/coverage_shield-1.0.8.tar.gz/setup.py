import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('README.md') as f:
    README = f.read()

setup(
    name='coverage_shield',
    packages=['coverage_shield'],
    include_package_data=True,
    version='1.0.8',
    description='Uploads total coverage for displaying badge',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=['coverage'],
    author='Samuel Carlsson',
    author_email='samuel.carlsson@volumental.com',
    url='https://github.com/Volumental/badges',
    keywords=['coverage', 'badge', 'shields.io'],
)
