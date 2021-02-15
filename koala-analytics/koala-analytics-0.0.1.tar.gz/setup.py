# -*- coding: utf-8 -*-
import setuptools


with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

with open('VERSION', 'r') as version_file:
    version = version_file.read()


setuptools.setup(
    name='koala-analytics',
    version=version,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=install_requires,
    author="NAV IKT",
    description="Package for fetching metrics from different analytics sources and pushing them to BigQuery.",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/navikt",
        "Documentation": "https://github.com/navikt",
        "Source Code": "https://github.com/navikt",
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
