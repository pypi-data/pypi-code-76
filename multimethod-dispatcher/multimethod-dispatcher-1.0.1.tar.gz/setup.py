"""Pip setup for multimethod"""
import setuptools

with open("README.md", "r") as fh:
    DESC = fh.read()

setuptools.setup(
    name='multimethod-dispatcher',
    version='1.0.1',
    include_package_data=True,
    py_modules=["multimethod"],
    package_dir={"": "src"},
    author="Sanjay Patel",
    author_email="sanjay10.patel@gmail.com",
    description="A clojure style multimethod dispatcher",
    long_description=DESC,
    long_description_content_type="text/markdown",
    url="https://github.com/sanjP10/multimethod.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers"
    ],
    keywords="multimethod dispatcher functional-programming",
    extras_require={
        "dev": [
            "pylint>=2.6",
            "coverage>=5.4"
        ],
        "publishing": [
            "twine>=3.3"
        ]
    }
)
