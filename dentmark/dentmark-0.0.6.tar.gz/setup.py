import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dentmark",
    version="0.0.6",
    author="Ryli Dunlap",
    author_email="ryli@transvec.com",
    description="An indentation-delimited, configurable markdown language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.transvec.com/dentmark",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
