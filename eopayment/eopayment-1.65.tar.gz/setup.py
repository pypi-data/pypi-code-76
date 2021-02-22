#!/usr/bin/env python

'''
Setup script for eopayment
'''

import io
import os
import subprocess

import distutils
import distutils.core
from distutils.command.build import build as _build
from distutils.cmd import Command
from distutils.spawn import find_executable

import setuptools
from setuptools.command.sdist import sdist
from setuptools.command.install_lib import install_lib as _install_lib

from glob import glob
from os.path import splitext, basename, join as pjoin
import os
from unittest import TextTestRunner, TestLoader
import doctest


class TestCommand(distutils.core.Command):
    user_options = []

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        '''
        Finds all the tests modules in tests/, and runs them.
        '''
        testfiles = []
        for t in glob(pjoin(self._dir, 'tests', '*.py')):
            if not t.endswith('__init__.py'):
                testfiles.append('.'.join(
                    ['tests', splitext(basename(t))[0]])
                )

        tests = TestLoader().loadTestsFromNames(testfiles)
        import eopayment
        tests.addTests(doctest.DocTestSuite(eopayment))
        t = TextTestRunner(verbosity=4)
        t.run(tests)


class eo_sdist(sdist):

    def run(self):
        print("creating VERSION file")
        if os.path.exists('VERSION'):
            os.remove('VERSION')
        version = get_version()
        version_file = open('VERSION', 'w')
        version_file.write(version)
        version_file.close()
        sdist.run(self)
        print("removing VERSION file")
        if os.path.exists('VERSION'):
            os.remove('VERSION')


def get_version():
    '''Use the VERSION, if absent generates a version with git describe, if not
       tag exists, take 0.0.0- and add the length of the commit log.
    '''
    if os.path.exists('VERSION'):
        with open('VERSION', 'r') as v:
            return v.read()
    if os.path.exists('.git'):
        p = subprocess.Popen(['git', 'describe', '--dirty',
                              '--match=v*'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        result = p.communicate()[0]
        if p.returncode == 0:
            result = result.decode('ascii').strip()[1:]  # strip spaces/newlines and initial v
            if '-' in result:  # not a tagged version
                try:
                    real_number, commit_count, commit_hash = result.split('-', 2)
                except ValueError:
                    real_number, commit_hash = result.split('-', 2)
                    commit_count = 0
                version = '%s.post%s+%s' % (real_number, commit_count, commit_hash)
            else:
                version = result
            return version
        else:
            return '0.0.post%s' % len(
                    subprocess.check_output(
                            ['git', 'rev-list', 'HEAD']).splitlines())

    return '0.0.0'


class compile_translations(Command):
    description = 'compile message catalogs to MO files via django compilemessages'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        django_admin = find_executable('django-admin')
        if django_admin:
            os.environ.pop('DJANGO_SETTINGS_MODULE', None)
            subprocess.check_call([django_admin, 'compilemessages'])


class build(_build):
    sub_commands = [('compile_translations', None)] + _build.sub_commands


class install_lib(_install_lib):
    def run(self):
        self.run_command('compile_translations')
        _install_lib.run(self)


setuptools.setup(
    name='eopayment',
    version=get_version(),
    license='GPLv3 or later',
    description='Common API to use all French online payment credit card '
    'processing services',
    include_package_data=True,
    long_description=io.open(
        os.path.join(
            os.path.dirname(__file__),
            'README.txt'), encoding='utf-8').read(),
    long_description_content_type='text/plain',
    url='http://dev.entrouvert.org/projects/eopayment/',
    author="Entr'ouvert",
    author_email="info@entrouvert.com",
    maintainer="Benjamin Dauvergne",
    maintainer_email="bdauvergne@entrouvert.com",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    packages=['eopayment'],
    install_requires=[
        'pycrypto >= 2.5',
        'pytz',
        'requests',
        'six',
        'click',
        'zeep >= 2.5',
    ],
    cmdclass={
        'build': build,
        'compile_translations': compile_translations,
        'install_lib': install_lib,
        'sdist': eo_sdist,
    }
)
