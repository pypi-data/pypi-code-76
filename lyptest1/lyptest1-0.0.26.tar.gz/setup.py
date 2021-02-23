#!/usr/bin/env python
from setuptools import setup, find_packages
setup( name = 'lyptest1',
       version = '0.0.26', description = 'python 3.7-->3.6 ', long_description = 'library ',
       author = 'pylyp456', author_email = '25506871@qq.com', url = 'https://github.com/ligaopan/lgp-library', license = 'MIT Licence', keywords = 'testing testautomation', platforms = 'any',

       python_requires = '>=3.6.*', install_requires = [],
       package_dir = {'': 'src'}, packages = find_packages('src')
,
       entry_points = {
              'console_scripts': [
                     # 'say4 = twine2.hello:main',
                     'say4 = twine2.__main__:main',
              ],
              'lyptest1.registered_commands': [
                     'upload = twine2.commands.upload:main',
              ],
       }


       )