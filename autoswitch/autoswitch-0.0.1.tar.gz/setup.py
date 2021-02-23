import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    version="0.0.1",
    long_description=long_description,
    install_requires=[
        "netmiko"
    ]
)
