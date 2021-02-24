#!/usr/bin/env python

version = '0.4a5'

from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(name='couchdb-python-requests',
          version=version,
          description='CouchDB\'s Python wrapper (using requests library)',
          author='Alexey Elfman',
          author_email='elf2001@gmail.com',
          url='https://bitbucket.org/angry_elf/couchdb-python-requests',
          packages=find_packages(),
          license='GPL',
          classifiers=[
              "Development Status :: 2 - Pre-Alpha",
              "Intended Audience :: Developers",
              "License :: OSI Approved :: GNU General Public License (GPL)",
              "Natural Language :: English",
              "Programming Language :: Python",
              "Topic :: Software Development :: Libraries :: Python Modules",
              "Topic :: Database :: Front-Ends",
              ],
          install_requires=['requests'],
          entry_points={
              ## 'console_scripts': [
              ##     'couchdb-curl-pinger = couchdbcurl.pinger:main',
              ##     'couchdb-curl-dbcompact = couchdbcurl.dbcompact:main',
              ##     'couchdb-curl-viewserver = couchdbcurl.view:main',
              ##     'couchdb-curl-dump = couchdbcurl.tools.dump:main',
              ##     'couchdb-curl-load = couchdbcurl.tools.load:main',
              ##     'couchdb-curl-replicate = couchdbcurl.tools.replication_helper:main'
              ## ]
          },
          test_suite="couchdbrq.tests",
          )
