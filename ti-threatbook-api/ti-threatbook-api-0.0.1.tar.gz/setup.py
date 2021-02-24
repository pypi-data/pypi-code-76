import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ti-threatbook-api",
    version="0.0.1",
    author="yege0201",
    author_email="yege0201@gmail.com",
    description="The unofficial Python library for ThreatBook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yege0201/ti-threatbook-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
