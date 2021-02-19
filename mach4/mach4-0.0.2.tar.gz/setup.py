import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mach4",
    version="0.0.2",
    author="Cyriaque Perier",
    description="Mach4 is a Python3 API framework based on Flask. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alph4ice/Mach4",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)