import ast
import codecs
import re
from os import path

from setuptools import find_packages, setup

requires = [
  'aniso8601',
]


here = path.abspath(path.dirname(__file__))


def read(*parts):
    with codecs.open(path.join(here, *parts), 'r') as fp:
        return fp.read()


_version_re = re.compile(r"__version__\s+=\s+(.*)")


def find_version(*where):
    return str(ast.literal_eval(_version_re.search(read(*where)).group(1)))


with codecs.open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

with codecs.open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='strainer-2020',
    version=find_version('src', 'strainer', '__init__.py'),
    description='Fast functional serializers',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    author='Alex Kessinger',
    author_email='voidfiles@gmail.com',
    maintainer='Jarek Zgoda',
    maintainer_email='jarek.zgoda@gmail.com',
    url='http://github.com/zgoda/strainer',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable',
    ],
    python_requires='~=3.6'
)
