from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read().strip()


setup(
    name="LibLynx",
    version="0.13",
    description="Python Library to interact with LibLynx",
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author="Etienne Posthumus",
    author_email="posthumus@brill.com",
    url="https://gitlab.com/brillpublishers/code/liblynx",
    packages=["liblynx"],
    data_files=[("", ["LICENSE"])],
)
