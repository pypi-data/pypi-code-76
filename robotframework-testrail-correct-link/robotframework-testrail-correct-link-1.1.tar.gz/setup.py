"""Setup module for Robot Framework TestRail Library package."""

# To use a consistent encoding
from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get install requires from requirements.txt
with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='robotframework-testrail-correct-link',
    version='1.1',
    description='Robot Framework library, listener and pre-run modifier for working with TestRail',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MrVeshij/robotframework-testrail-correct-link',
    author='veshij',
    author_email='veshij@bk.ru',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Robot Framework :: Library',
    ],
    py_modules = ['TestRailAPIClient', 'TestRailListener', 'TestRailPreRunModifier'],
    keywords='testing testautomation robotframework testrail correct link',
    package_dir={'': 'src'},
    install_requires=requirements,
)
