import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="convertbase",
    version="0.1.2",
    author="Johan Lahti",
    author_email="ccie60702@gmail.com",
    description="Convert between bases, initailly intended for RFC4648 base32",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johan-lahti/convertbase",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires='>=3.8',
)
