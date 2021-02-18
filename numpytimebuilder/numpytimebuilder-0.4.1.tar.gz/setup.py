import sys

from os import path
from setuptools import setup, find_packages

NUMPY_REQUIREMENT = 'numpy>=1.20.0'

PY2 = sys.version_info[0] == 2
PY34 = sys.version_info[0] == 3 and sys.version_info[1] == 4
PY35 = sys.version_info[0] == 3 and sys.version_info[1] == 5
PY36 = sys.version_info[0] == 3 and sys.version_info[1] == 6

if PY2 or PY34:
    NUMPY_REQUIREMENT = 'numpy<1.17.0'
elif PY35:
    NUMPY_REQUIREMENT = 'numpy<1.19.0'
elif PY36:
    NUMPY_REQUIREMENT = 'numpy<1.20.0'

with open(path.join('numpytimebuilder', 'version.py')) as f:
    exec(f.read())

THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, 'README.rst')) as f:
    README_TEXT = f.read()

setup(
    name='numpytimebuilder',
    version=__version__,
    description='A library for using the NumPy datetime API with aniso8601',
    long_description=README_TEXT,
    long_description_content_type='text/x-rst',
    author='Brandon Nielsen',
    author_email='nielsenb@jetfuse.net',
    url='https://bitbucket.org/nielsenb/numpytimebuilder',
    install_requires=[
        'aniso8601>=9.0.0,<10.0.0',
        NUMPY_REQUIREMENT
    ],
    packages=find_packages(),
    test_suite='numpytimebuilder',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='iso8601 numpy aniso8601 datetime',
    project_urls={
        'Documentation': 'https://numpytimebuilder.readthedocs.io/',
        'Source': 'https://bitbucket.org/nielsenb/numpytimebuilder',
        'Tracker': 'https://bitbucket.org/nielsenb/numpytimebuilder/issues'
    }
)
