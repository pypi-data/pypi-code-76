from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Python addon for NAStJA'
LONG_DESCRIPTION = 'A python addon for the NAStJA Framework (https://gitlab.com/nastja/nastja).'

# Setting up
setup(
    name="nastja",
    version=VERSION,
    author="T3GD1F (Felix Hoffmann)",
    author_email="<felixhoffmann07@gmx.de>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib'],
    keywords=['python', 'nastja', 'framework', 'simulation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Scientists",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
    ]
)