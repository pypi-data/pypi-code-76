#!/usr/bin/env python
import sys
import time

from setuptools import setup, find_packages

# Bump pyglet/__init__.py version as well.
VERSION = '2.2.%d' % round(time.time())

long_description = '''gracie_dictionary_api is an API wrapper for the Gracie AI platform'''

# The source dist comes with batteries included, the wheel can use pip to get the rest
is_wheel = 'bdist_wheel' in sys.argv

excluded = []
if is_wheel:
    excluded.append('extlibs.future')


def exclude_package(pkg):
    for exclude in excluded:
        if pkg.startswith(exclude):
            return True
    return False


def create_package_list(base_package):
    return ([base_package] +
            [base_package + '.' + pkg
             for pkg
             in find_packages(base_package)
             if not exclude_package(pkg)])


setup_info = dict(
    # Metadata
    name='gracie_dictionary_api',
    version=VERSION,
    author='Darshan Gencarelle',
    author_email='darshan.gencarelle@toposlabs.com',
    url='https://gracie-dictionary-api-documentation.readthedocs.io',
    download_url='https://pypi.org/project/gracie-dictionary-api/',
    description='Gracie Dictionary API python wrapper',
    long_description=open('README').read(),
    license='commercial',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # Package info
    packages=create_package_list('gracie_dictionary_api'),

    # Add _ prefix to the names of temporary build dirs
    options={
        'build': {'build_base': '_build'},
        #        'sdist': {'dist_dir': '_dist'},
    },
    zip_safe=True,
)

if is_wheel:
    setup_info['install_requires'] = ['future', 'requests']

setup(**setup_info)
