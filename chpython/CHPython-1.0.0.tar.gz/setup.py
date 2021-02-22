from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.0'
DESCRIPTION = 'Programming Language'
LONG_DESCRIPTION = 'Python-based programming language.'

setup(
    name="CHPython",
    version=VERSION,
    author="ArMafer",
    author_email="<angelshaparro@outlook.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)