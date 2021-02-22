from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="string-locator",
    version="1.1.0",
    description="A python package to find the files that contain a given string inside a given path",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/sriragjayakumar/string-locator.git",
    author="Srirag Jayakumar",
    author_email="sriragjayakumar@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["string_locator"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "string-locator=string_locator.main:locator",
        ]
    },
)