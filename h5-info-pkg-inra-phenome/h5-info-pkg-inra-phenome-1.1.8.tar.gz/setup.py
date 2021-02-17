import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="h5-info-pkg-inra-phenome",
    version="1.1.8",
    author="Eric David",
    author_email="eric.david@ephesia-consult.com",
    description="Utility package for extracting, reading and saving metadata from HDF5 Phenomobile V2 acquisition file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://forgemia.inra.fr/4p/tools/h5info",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'h5py',
        'Pillow'
    ]
)
