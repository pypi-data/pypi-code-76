from setuptools import setup
import iotio_client

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="iot.io-client",
    version=iotio_client.__version__,
    packages=["iotio_client"],
    author="Dylan Crockett",
    author_email="dylanrcrockett@gmail.com",
    license="MIT",
    description="A client library designed for connecting to a iot.io server instance.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dylancrockett/iot.io-client",
    project_urls={
        "Documentation": "https://iotio-client.readthedocs.io/",
        "Source Code": "https://github.com/dylancrockett/iot.io-client"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'websockets', 'websocket-client'
    ],
    python_requires='>=3.7'
)
