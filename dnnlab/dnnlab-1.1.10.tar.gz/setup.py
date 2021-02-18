from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# Semantic Versioning
# -------------------
# MAJOR: new API-incompatible changes.
# MINOR: new API-compatible functionality.
# PATCH: Bugfixes.
setup(
    name="dnnlab",
    # MAJOR.MINOR.PATCH
    version="1.1.10",
    author="Tobias Hoefer, Kevin Hirschmann Frederik Weishaeupl",
    author_email=
    "tobias.hoefer.hm@gmail.com,  kevin.hirschmann@noventi.de, Frederik.Weishaeupl@noventi.de",
    description="DnnLab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    # Library Dependencies.
    install_requires=[
        "Cython", "numpy", "pycocotools>=2.0.2", "Click>=7.0",
        "opencv_python==4.4.0.42", "imgaug==0.4.0", "matplotlib==3.1.3",
        "Pillow==7.2.0"
    ],
    # Developement Dependencies. Versioning is specific!
    extras_require={
        "dev": [],
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
