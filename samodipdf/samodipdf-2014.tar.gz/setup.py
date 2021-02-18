import setuptools
from pathlib import Path

setuptools.setup(
    name="samodipdf",
    version=2014,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests","data"])
)