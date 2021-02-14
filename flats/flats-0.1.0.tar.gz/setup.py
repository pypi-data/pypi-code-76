from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="flats",
    version="0.1.0",
    packages=["flats",],
    install_requires=[],
    license="MIT",
    url="https://github.com/lapets/flats",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Python library for common functionalities related "+\
                "to flattening nested instances of container types.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
