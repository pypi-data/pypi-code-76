from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.1'
DESCRIPTION = 'Port Scanner'
LONG_DESCRIPTION = 'A package that allows to build a simple script for Port Scanner'

# Setting up
setup(
    name="port_scann",
    version=VERSION,
    author="CyberCommands",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['colorama', 'argparse'],
    keywords=['python', 'port', 'scan', 'port scanner', 'port scan', 'TCP scan'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
