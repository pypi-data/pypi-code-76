import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DynaTMT-py", 
    version="0.0.3",
    author="Kevin Klann",
    author_email="klann@em.uni-frankfurt.de",
    description="Python package to analyse pSILAC TMT data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bobbyhaze/DynaTMT-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)