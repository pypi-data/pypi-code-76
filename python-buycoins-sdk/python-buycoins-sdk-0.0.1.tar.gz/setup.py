from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = "0.0.1"
DESCRIPTION = "BUYCOINS SDK"

# Setting up
setup(
    name="python-buycoins-sdk",
    version=VERSION,
    author="Praise Ajayi",
    author_email="praiseajayi2@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/NerdPraise/python-buycoin",
    license="MIT",
    install_requires=["python-graphql-client", "requests", "python-decouple"],  # add any additional packages that
    # needs to be installed along with your package. Eg: "caer"

    keywords=["python", "SDK", "Buycoins"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.0"
)
