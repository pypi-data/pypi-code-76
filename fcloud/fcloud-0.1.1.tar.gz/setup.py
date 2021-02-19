
from setuptools import setup, find_packages


# with open("DESCRIPTION.md", "r") as DESCRIPTION:
#     long_description = DESCRIPTION.read()

setup(
    name="fcloud",
    version="0.1.1",
    author="Nandanunni A S",
    author_email="asnqln@gmail.com",
    description="[DEV]",
    long_description="## [DEV]",
    long_description_content_type="text/markdown",
    url="https://github.com/Nandan-unni",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)