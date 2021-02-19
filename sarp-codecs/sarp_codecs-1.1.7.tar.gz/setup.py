import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sarp_codecs",
    version="1.1.7",
    author="Josh Sherbrooke",
    author_email="jsherbro@gmail.com",
    description="A package to encode network communication for SARP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/SARP_UW/codecs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)