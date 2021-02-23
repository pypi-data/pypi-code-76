#!/usr/bin/env python3

import codecs
from os import path
from setuptools import setup

pwd = path.abspath(path.dirname(__file__))
with codecs.open(path.join(pwd, 'README.md'), 'r', encoding='utf8') as input:
	long_description = input.read()

version='1.38'
	
setup(
	name='Swapsies',
	version=version,
	license='MIT',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url='https://github.com/eddo888/Swapsies',
	download_url='https://github.com/eddo888/Swapsies/archive/%s.tar.gz'%version,
	author='David Edson',
	author_email='eddo888@tpg.com.au',
	packages=[
		'Swapsies'
	],
	install_requires=[
		'argcomplete',
		'xlrd',
		'xlwt',
		'pyxb',
		'python-docx',
		'vobject',
		'xmltodict',
		'Baubles',
		'Perdy',
		'Argumental',
		'GoldenChild',
	],
	scripts=[
		'bin/ref2type.py',
		'bin/OPML.py',
		'bin/text2opml.py',
		'bin/wsdl2file.py',
		'bin/pdf2text.py',
		'bin/email2vcard.py',
		'bin/contact2vcard.py',
		'bin/xls2dict.py',
		'bin/COD.py',
		'bin/tree2xmi.py',
		'bin/cdata2xml.py',
		'bin/xls2opml.py',
		'bin/outlines.py',
		'bin/xml2cdata.py',
	],
)
