import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="country_module",
    version="1.0.1",
    author="Harshil Darji",
    author_email="darjiharshil2994@gmail.com",
    description="Python module for country codes with ISO codes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harshildarji/country",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
