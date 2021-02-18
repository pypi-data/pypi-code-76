from setuptools import find_packages, setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='roktools',
    version_cc='{version}',
    setup_requires=['setuptools-git-version-cc'],
    author='Rokubun',
    author_email='info@rokubun.cat',
    description='Set of tools used in internal Rokubun projects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='http://opensource.org/licenses/MIT',
    url="https://www.rokubun.cat",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cl = roktools.cl:entry_point',
            'tensorial = roktools.tensorial:entry_point'
        ]
    },
    install_requires=[
        'setuptools >= 8.0',
        'numpy'
    ]
)
