import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    version="0.0.1.2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "netmiko"
    ]
)
