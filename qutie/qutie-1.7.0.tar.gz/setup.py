import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(
    name='qutie',
    version='1.7.0',
    author="Bernhard Arnold",
    author_email="bernhard.arnold@oeaw.ac.at",
    description="Yet another pythonic UI library using PyQt5",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/arnobaer/qutie',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'PyQt5>=5.12',
        'appdirs>=1.4.4'
    ],
    test_suite='tests',
    license="GPLv3",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ]
)
