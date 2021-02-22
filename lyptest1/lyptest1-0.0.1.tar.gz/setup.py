#!/usr/bin/env python
from setuptools import setup, find_packages
setup( name = 'lyptest1',
       version = '0.0.1', description = 'library ', long_description = 'library ', author = 'pylyp456', author_email = '25506871@qq.com', url = 'https://github.com/ligaopan/lgp-library', license = 'MIT Licence', keywords = 'testing testautomation', platforms = 'any', python_requires = '>=3.7.*', install_requires = [], package_dir = {'': 'src'}, packages = find_packages('src') )