import sys
from io import open

from setuptools import find_packages, setup

needs_wheel = {"bdist_wheel"}.intersection(sys.argv)
wheel = ["wheel"] if needs_wheel else []

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fontgen", # Replace with your own username
    version="0.0.2",
    author="Rahul Gajjar",
    author_email="rahulgajjar20@gmail.com",
    description="Python package for generating fonts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itfoundry/fontgen",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    packages=find_packages("Lib"),
    package_dir={"": "Lib"},
    entry_points={"console_scripts": ["fontgen = fontgen.__main__:main"]},
    python_requires='>=3.6',
    install_requires=[
        "fontmake",
        "fontParts",
    ],
)