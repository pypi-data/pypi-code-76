from setuptools import setup
import os
import sys

if "BUILD" not in os.environ:
    print("This is a palceholder package, did you mistype the package name?")
    sys.exit(-1)


setup(
    name="hostinfo",
    version="0.0.0",
    description="Placeholder package",
    author="Mario Corchero",
    author_email="mariocj89@gmail.com",
    packages=[],
)
