#!/usr/bin/env python
"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Justin Richert",
    author_email="justinrichert@icloud.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Library to control Fellow Stagg Kettle EKG+",
    install_requires=["bleak>=0.10.0"],
    license="MIT License",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="fellow",
    name="fellow-py",
    packages=find_packages(include=["fellow_py", "fellow_py.*"]),
    setup_requires=["pytest-runner"],
    test_suite="tests",
    tests_require=["pytest>=3"],
    url="https://github.com/justin-richert/fellow-py",
    version="0.2.0",
    zip_safe=False,
)
