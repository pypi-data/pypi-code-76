import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyconductor_grpc",
    version="0.0.6",
    author="Joseph",
    author_email="joseph.solomon@invitae.com",
    description="A GRPC Library for Netflix Conductor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        "grpcio",
        "protobuf",
    ],
    python_requires=">=3.6",
)
