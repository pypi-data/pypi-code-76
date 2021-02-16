import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="abdesign",
    version="0.0.3",
    author="Jannis Köckritz",
    author_email="jannis.koeckritz@helmholtz-muenchen.de",
    description="Antibody humanization framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SchubertLab/ABDesign",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix"
    ],
    python_requires='>=3.6',
    install_requires=['pandas>=1.0.3','biopython']
)