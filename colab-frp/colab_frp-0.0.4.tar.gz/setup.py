import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colab_frp",
    version="0.0.4",
    author="argszero",
    author_email="argszero@gmail.com",
    description="Google colab frp connector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WassimBenzarti/colab-ssh-connector.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)