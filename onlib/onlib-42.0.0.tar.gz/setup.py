#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Bo Bayles",
    author_email='bo@bbayles.com',
    python_requires='>=3.5',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    description="onlib namespace package",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + readme,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='onlib',
    name='onlib',
    packages=find_packages(include=['onlib', 'onlib.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/bbayles/onlib',
    version='42.0.0',
    zip_safe=False,
)
