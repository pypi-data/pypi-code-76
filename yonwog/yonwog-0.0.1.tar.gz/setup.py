from setuptools import setup
#from distutils.core import setup
setup(
  name = 'yonwog',
  packages = ['yonwog'],
  version = '0.0.1',
  license='yon',
  description = 'a python 3 games cli package project for school',
  author = 'Yonatan shani',
  author_email = 'sth@sth.com',
  keywords=['yonwog'],
  install_requires=[
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)