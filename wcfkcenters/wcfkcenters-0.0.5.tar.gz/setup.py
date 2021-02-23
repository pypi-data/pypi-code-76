import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wcfkcenters", 
    version="0.0.5",
    author="ktstt",
    author_email="toan_stt@yahoo.com",
    description="A python package for Weighted Cluster Fuzzy-k-Centers algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)