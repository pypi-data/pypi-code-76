from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    LONG_DESCRIPTION = "\n" + fh.read()

DESCRIPTION = "A lightweight and basic maths interpreter"
VERSION = "1.0.2"

setup(
    name="mathterpreter",
    version=VERSION,
    author="pjones123",
    url="https://github.com/pjones123/mathterpreter",
    license="MIT",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['dataclasses'],
    keywords=['python', 'math', 'maths'],
    classifiers=[
        "Programming Language :: Python :: 3.7"
    ],
    entry_points = {
        "console_scripts": ["mathterpreter=mathterpreter.__main__:main"]
    }
)
