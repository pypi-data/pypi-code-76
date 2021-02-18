import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrecipepuppy",
    version="0.0.1",
    author="Crinela Potinteu",
    author_email="potinteu.crinela@gmail.com",
    description="A simple Python wrapper for the Recipe Puppy API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crinela/pyrecipepuppy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
requires = [
    'requests>=2.25.0',
]
