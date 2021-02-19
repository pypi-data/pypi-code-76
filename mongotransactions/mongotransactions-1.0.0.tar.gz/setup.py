from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mongotransactions',
    version='1.0.0',    
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vorticalbox/mongotransactions',
    author='vorticalbox',
    author_email='vorticalbox@protonmail.com',
    license='GPL-3.0',
    packages=['mongotransactions'],
    install_requires=['pymongo~=3.11.0','dnspython~=2.0.0'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)