import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="bibimbap",
    version="1.0.2",
    description="selenium based visual automation testing tool",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sh1223/bibimbap",
    author="Seonghwan KIM",
    author_email="seonghwankim86@gmail.com",
    license="",
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    packages=["bibimbap"],
    include_package_data=True,
    install_requires=["selenium", "Pillow"],
)