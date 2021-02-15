#!/usr/bin/env python3

# Note!
# ' are required, do not use any ".

# setup.
from setuptools import setup, find_packages
setup(
	name='ssht00ls',
	version='1.8.6',
	description='Some description.',
	url="http://github.com/vandenberghinc/ssht00ls",
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	install_requires=[
		"asgiref",
		"certifi",
		"chardet",
		"cl1",
		"Django",
		"fil3s",
		"idna",
		"pexpect",
		"ptyprocess",
		"pytz",
		"r3sponse",
		"requests",
		"sqlparse",
		"urllib3",
	],)