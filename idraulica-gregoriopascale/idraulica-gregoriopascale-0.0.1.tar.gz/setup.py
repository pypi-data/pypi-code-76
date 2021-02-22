import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="idraulica-gregoriopascale",  # Replace with your own username
    version="0.0.1",
    author="pascale gregorio",
    author_email="gregoriopascale@gmail.com",
    description="Modulo per la progettazione impianti idrico sanitari.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/idraulica",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)