from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="pyoctonion",
    version="3.5",
    description="Octonion Number System",
    packages=["pyoctonion"],
    author="Kalpa Madawa & Charith Atapattu",
    author_email="charithnisanka@gmail.com",
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
