import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visualife", # Replace with your own username
    version="0.8",
    author="Justyna Kryś, Dominik Gront",
    author_email="dgront@chem.uw.edu.pl",
    description="Interactive visualisation for the web",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/dgront/visualife/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
