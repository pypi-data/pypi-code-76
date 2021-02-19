#!/usr/bin/env python
#-*- coding:utf-8 -*-

import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Ming Feng",
    author_email="fengming@mail.com",
    name="fmc",
    license="MIT",
    description="fmc is a simple cli application for one's own convenience.",
    version="v0.2.0",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=['plumbum==1.6.9'],
    keywords = ["fmc", "shortcut", "alias"],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
    entry_points={
        'console_scripts': [
            'fmc = fmc.app:main',
     ],
    },
)