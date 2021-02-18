import os
from pathlib import Path
import setuptools

PARENT_DIR = Path(__file__).resolve().parent


def set_directory():
    # CD to this directory, to simplify package finding
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)


set_directory()

with open("docs/index.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="up42-blockutils",
    version=PARENT_DIR.joinpath("blockutils/_version.txt").read_text(encoding="utf-8"),
    author="UP42",
    author_email="support@up42.com",
    description="Block development toolkit for UP42",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://www.up42.com",
    packages=setuptools.find_packages(exclude=("tests", "apiutils")),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    install_requires=[
        "geojson",
        "numpy",
        "rasterio",
        "shapely",
        "area",
        "ciso8601",
        "scipy",
        "scikit-image",
        "rio-cogeo",
        "mercantile",
        "requests",
    ],
    python_requires=">=3.6, <3.10",
)
