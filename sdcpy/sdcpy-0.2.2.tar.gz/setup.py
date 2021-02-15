#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['matplotlib', 'numpy', 'pandas', 'plotnine', 'scipy', 'seaborn', 'tqdm']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Alejandro Fontal",
    author_email='alejandrofontal92@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description="Scale dependent correlation in Python.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sdcpy',
    name='sdcpy',
    packages=find_packages(include=['sdcpy']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/AlFontal/sdcpy',
    version='0.2.2',
    zip_safe=False,
)
