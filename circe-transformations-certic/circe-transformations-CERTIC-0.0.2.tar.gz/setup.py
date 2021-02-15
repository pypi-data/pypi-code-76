import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="circe-transformations-CERTIC",
    version="0.0.2",
    author="Mickaël Desfrênes",
    author_email="mickael.desfrenes@unicaen.fr",
    description="Circe tranformations library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.unicaen.fr/certic/circe-transformations",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["weasyprint", "mammoth", "markdown2", "pypandoc"],
    python_requires='>=3.6',
)

