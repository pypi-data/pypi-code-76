#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'requests>=2.0.0', 'pandas>=0.25.3', 'numpy>=1.18.0']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Yasser Mahfoud",
    author_email='yassermahfoud1995@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A package needed to participate i's Hackathon",
    entry_points={
        'console_scripts': [
            'linchackathon=linchackathon.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='linchackathon',
    name='linchackathon',
    packages=find_packages(include=['linchackathon', 'linchackathon.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/YasserMahfoud/linchackathon',
    version='0.1.3',
    zip_safe=False,
)
