#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`aether_sphinx` lives on `invent.kde.org`_.

.. _invent.kde.org: https://invent.kde.org/websites/aether-sphinx

"""

import os
import subprocess
import distutils.cmd
import setuptools.command.build_py
from io import open
from setuptools import setup


class BuildSasscCommand(setuptools.command.build_py.build_py):

    """Prefix Python build with Webpack asset build"""

    def run(self):
        subprocess.run(['sassc', 'src/sass/theme.scss', 'aether_sphinx/static/css/theme.css'], check=True)
        setuptools.command.build_py.build_py.run(self)

class UpdateTranslationsCommand(distutils.cmd.Command):

    description = "Run all localization commands"

    user_options = []
    sub_commands = [
        ('extract_messages', None),
        ('update_catalog', None),
        ('transifex', None),
        ('compile_catalog', None),
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)


class TransifexCommand(distutils.cmd.Command):

    description = "Update translation files through Transifex"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.run(['tx', 'push', '--source'], check=True)
        subprocess.run(['tx', 'pull'], check=True)


setup(
    name='aether_sphinx',
    version='2.3.0',
    url='https://invent.kde.org/websites/aether-sphinx',
    license='MIT',
    author='Janet Blackquill, Carl Schwan, Dave Snider, Read the Docs, Inc., KDE & contributors',
    author_email='uhhadd@gmail.com',
    description='Aether theme for Sphinx',
    long_description=open('README.rst', encoding='utf-8').read(),
    cmdclass={
        'update_translations': UpdateTranslationsCommand,
        'transifex': TransifexCommand,
        'build_py': BuildSasscCommand,
    },
    zip_safe=False,
    packages=['aether_sphinx'],
    package_data={'aether_sphinx': [
        'theme.conf',
        '*.html',
        'static/css/*.css',
        'static/css/fonts/*.*'
        'static/js/*.js',
    ]},
    include_package_data=True,
    # See http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
    entry_points = {
        'sphinx.html_themes': [
            'aether = aether_sphinx',
        ]
    },
    install_requires=[
       'sphinx'
    ],
    tests_require=[
        'pytest',
    ],
    extras_require={
        'dev': [
            'transifex-client',
            'sphinxcontrib-httpdomain',
        ],
    },
    classifiers=[
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Theme',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
)
