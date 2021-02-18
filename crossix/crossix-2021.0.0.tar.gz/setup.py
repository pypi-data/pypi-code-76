#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import re
import subprocess

from setuptools import setup, find_packages
from setuptools.command import build_py

root_dir = os.path.abspath(os.path.dirname(__file__))


def get_version(package_name):
    version_re = re.compile(r"^__version__ = [\"']([\w_.-]+)[\"']$")
    package_components = package_name.split('.')
    init_path = os.path.join(root_dir, *(package_components + ['__init__.py']))
    with codecs.open(init_path, 'r', 'utf-8') as f:
        for line in f:
            match = version_re.match(line[:-1])
            if match:
                return match.groups()[0]
    return ''


class BuildWithMakefile(build_py.build_py):
    """Custom 'build' command that runs 'make build' first."""
    def run(self):
        subprocess.check_call(['make', 'build'])
        return super().run()


PACKAGE = 'crossix'


setup(
    # Contents
    name=PACKAGE,
    packages=find_packages(exclude=['dev', 'tests*']),
    include_package_data=True,
    scripts=['bin/crossixctl'],
    cmdclass={'build_py': BuildWithMakefile},
    zip_safe=False,

    # Metadata
    version=get_version(PACKAGE),
    description="Simple website for Cross triangulaire registration.",
    long_description=''.join(codecs.open('README.rst', 'r', 'utf-8').readlines()),
    author="Raphaël Barrois",
    author_email='raphael.barrois+%s@polytechnique.org' % PACKAGE,
    url='https://git.xelnor.net/%s/' % PACKAGE,
    keywords=['crossix'],
    license='MIT',

    # Dependencies
    install_requires=[
        'Django>=3.1',
        'django-sendfile2>=0.6.0',
        'getconf>=1.3.0',
        'markdown',
    ],

    # Misc
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
