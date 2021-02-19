#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='netw0rk',
	version='1.1.8',
	description='Some description.',
	url='http://github.com/vandenberghinc/netw0rk',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
        install_requires=[
        'syst3m==2.2.2',
        'cl1==1.5.4',
        'fil3s==2.1.6',
        'r3sponse==2.1.1',
    ])