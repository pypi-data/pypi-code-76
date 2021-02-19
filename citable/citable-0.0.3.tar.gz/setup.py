import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="citable", # Replace with your own username
    version="0.0.3",
    author="Gerd Graßhoff, Florian Kotschka, Sabrina Bier",
    author_email="gerd.grasshoff@opensciencetechnology.com",
    description="Citable Loader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/biersabrina/citablePyPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['zipfile','requests','IPython','pandas','pyyaml'],
    python_requires='>=3.6',
)