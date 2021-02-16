import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="baseXtoY",
    version="0.3",
    author="L. Pham-Trong",
    author_email="spam@lucasanss.xyz",
    description="A simple base converter in python3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toto112358/base-converter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
