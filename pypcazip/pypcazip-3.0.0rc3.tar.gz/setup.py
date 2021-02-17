#!/usr/bin/env python
import os
import sys
import re
import textwrap


"""Some functions for checking and showing errors and warnings."""
def _print_admonition(kind, head, body):
    tw = textwrap.TextWrapper(initial_indent='   ', subsequent_indent='   ')

    print(".. {0}:: {1}".format(kind.upper(), head))
    for line in tw.wrap(body):
        print(line)


def exit_with_error(head, body=''):
    _print_admonition('error', head, body)
    sys.exit(1)


def print_warning(head, body=''):
    _print_admonition('warning', head, body)


def check_import(pkgname, pkgver):
    """ Check for required Python packages. """
    try:
        mod = __import__(pkgname)
        if mod.__version__ < pkgver:
            raise ImportError
    except ImportError:
        exit_with_error("Can't find a local {0} installation with version >= {1}. "
                        "Pypcazip needs {0} {1} or greater to compile and run! "
                        "Please read carefully the ``README`` file.".format(pkgname, pkgver))

    print("* Found {0} {1} package installed.".format(pkgname, mod.__version__))
    globals()[pkgname] = mod


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


"""Discover the package version"""
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
VERSIONFILE = "pypcazip/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RunTimeError("Unable to find version string in {}.".format(VERSIONFILE))


"""Check Python version"""
print("* Checking Python version...")
if  sys.version_info[0:2] < (3, 4):
    exit_with_error("You need Python 3.4+ to install pyPcazip!")
print("* Python version OK!")

"""Set up pyPcazip."""
from setuptools import setup, find_packages

setup_args = {
    'name':             "pypcazip",
    'version':          verstr,
    'description':      "PCA-based molecular dynamics trajectory file compression and analysis.",
    'long_description': "PCA-based molecular dynamics trajectory file compression and analysis.",
    'author':           "The University of Nottingham & BSC",
    'author_email':     "charles.laughton@nottingham.ac.uk",
    'url':              "https://bitbucket.org/ramonbsc/pypcazip/overview",
    'download_url':     "https://bitbucket.org/ramonbsc/pypcazip/get/{}.tar.gz".format(verstr),
    'license':          "BSD license.",

    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix'
    ],

    'packages': find_packages(),
    'scripts': [
                'scripts/pyPcazip',
                'scripts/pyPcaunzip',
                ],

    'install_requires': [
                         'mdplus>0.0.4',
                         'argparse',
                         'mdtraj',
                         ],

    'zip_safe': True

}

setup(**setup_args)
