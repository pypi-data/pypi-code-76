import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="py_tzone",
    version="1.5.0",
    description="Python Package to get all the information about a Time Zone",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/prkhrv/py_tzone",
    author="prkhrv",
    author_email="contact.prkhrv@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["py_tzone"],
    include_package_data=True,
    install_requires=[],
)
