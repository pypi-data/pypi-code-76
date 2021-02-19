# source: https://python-packaging.readthedocs.io/en/latest/minimal.html
from setuptools import setup, find_packages
name = 'encrypti0n'
setup(
	name=name,
	version='3.9.1',
	description='Easily encrypt & decrypt files with python / through the CLI.',
	url=f"http://github.com/vandenberghinc/{name}",
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	install_requires=[
		"certifi",
		"chardet",
		"cl1",
		"fil3s",
		"idna",
		"pycryptodome",
		"requests",
		"urllib3",
	])