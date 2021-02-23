import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mydataframesales", # Replace with your own username
    version="0.0.1",
    author="Pascale Gregorio",
    author_email="gregoriopascale@gmail.com",
    description="Functions for sales.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/myDataFrameSales",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)