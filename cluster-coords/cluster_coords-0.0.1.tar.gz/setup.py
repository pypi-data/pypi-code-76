import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="cluster_coords", # Replace with your own username
    version="0.0.1",
    author="Sonny Parlin",
    author_email="ask@sparl.in",
    description=("Build cluster from multiple identical longitude and latitude coordinates"),
    license = "MIT",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/sonnyparlin/cluster_coords/",
    project_urls={
        "Bug Tracker": "https://github.com/sonnyparlin/cluster_coords/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires='>=3.6',
)
