import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
requirements = open("requirements.txt").read().splitlines()

setuptools.setup(
    name="media_processing_lib",
    version="0.2",
    author="Mihai Cristian Pîrvu",
    author_email="mihaicristianpirvu@gmail.com",
    description="Generic media processing lib high level library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mihaicristianpirvu/media-processing-lib/",
    keywords = ["audio", "video", "images", "media", "high level api"],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    license="WTFPL",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
