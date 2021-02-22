import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name="jerome",
    version="0.2.0",
    author="Patrick Shechet",
    author_email="patrick.shechet@gmail.com",
    description=("String Processing Tools"),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kajuberdut/jerome",
    license="BSD",
    packages=find_packages(exclude=["js"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
