import sys

from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

version = "0.0.0"
if len(sys.argv) > 2:
    version = sys.argv[2]
    del sys.argv[2]

setup(
    name="ntdrt",
    version=version,
    author="Tomáš Kolinger",
    author_email="tomas@kolinger.name",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["ntdrt"],
    zip_safe=False
)
