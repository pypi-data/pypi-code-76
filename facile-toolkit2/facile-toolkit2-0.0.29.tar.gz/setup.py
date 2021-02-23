import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="facile-toolkit2",
    version="0.0.29",
    author="Vincenzo Gasparo",
    author_email="vincenzo.gasparo@gmail.com",
    description="A robotframework keywords toolkit used by Facile.it",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://www.facile.it",
    packages=["FacileToolkit2"],
    install_requires=['robotframework', 'robotframework-seleniumlibrary', "selenium"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)