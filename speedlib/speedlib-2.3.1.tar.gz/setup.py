import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speedlib",
    version="2.3.1",
    author="Fabrice Dedo & Damien Marchal",
    author_email="komla-sam-fabrice.dedo@polytech-lille.net",
    description="A python library to operate 'Speed' devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CRIStAL-PADR/Speed",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
