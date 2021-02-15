import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="noelnetwork",
    version="1.0.3",
    description="Create and use Neural Networks",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/noel-friedrich/neural",
    author="Noel Friedrich",
    author_email="noel.friedrich@outlook.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
)
