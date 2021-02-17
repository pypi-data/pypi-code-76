import sys
import webbrowser

from setuptools import setup


if sys.argv[1] in ('install', 'build', 'sdist', 'bdist_wheel'):
    webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


setup(name='discord.js',
      version='1.0',
      description="The Python module for discord.js.",
      long_description="The Python module that's never gonna let you down.",
      author='Swas.py',
      author_email='cwswas.py@gmail.com',
      py_modules=['djs'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Internet',
                   'Topic :: Sociology'],
      )
