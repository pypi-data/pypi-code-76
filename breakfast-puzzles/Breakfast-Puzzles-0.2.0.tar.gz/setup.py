#!/usr/bin/env python3
import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="Breakfast-Puzzles",
    version="0.2.0",
    author="Tom Fryers",
    description=(
        "Breakfast Puzzles is a script for laying out a selection of "
        "Simon Tatham’s Puzzles onto a page."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Tom_Fryers/breakfast-puzzles",
    py_modules=["breakfast_puzzles"],
    entry_points={"console_scripts": "breakfast-puzzles = breakfast_puzzles:main"},
    classifiers=[
        "Development Status :: 4 - Beta",
        (
            "License"
            " :: OSI Approved"
            " :: GNU General Public License v3 or later (GPLv3+)"
        ),
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
)
