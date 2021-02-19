#!/usr/bin/env python

from distutils.core import setup

from nlab_inf_engine_scripts.version import VERSION


setup(
    name='nlab_inf_engine_scripts',
    packages=['nlab_inf_engine_scripts'],
    version=VERSION,
    license='MIT',
    description='Python scripts for manipulation InfEngine.',
    author='Dmitry Makarov',
    author_email='dmakarov@nanosemantics.ru',
    install_requires=[
        'python-memcached',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            "InfEngineControl = nlab_inf_engine_scripts.InfEngineControl:main"
        ]
    }
)
