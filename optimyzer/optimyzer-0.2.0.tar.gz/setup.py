# Copyright (c) 2020-2021, Gauss Machine Learning GmbH. All rights reserved.
# This file is part of the Optimyzer Client, which is released under the BSD 3-Clause License.

"""Setup and package metadata for the Optimyzer Package."""

import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="optimyzer",
    description="A hyperparameter optimization framework that fits into every workflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gauss-ml-open/optimyzer-client",
    author="Gauss Machine Learning GmbH",
    author_email="info@gauss-ml.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="parameter optimization, machine learning, artificial intelligence, neural networks",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.5, <4",
    install_requires=[],  # no dependencies! :)
    extras_require={
        "dev": ["black", "flake8", "mypy", "pylint", "rope"],
        "test": ["flaky", "micro-ci", "pytest", "pytest-cov"],
    },
)
