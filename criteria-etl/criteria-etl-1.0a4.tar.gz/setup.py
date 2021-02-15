import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="criteria-etl",
    version="1.0a4",
    author="Prosperia Social",
    author_email="developers.etl@prosperia.ai",
    maintainer="Rodrigo Lara Molina",
    maintainer_email="rodrigo@prosperia.ai",
    description="A library for Criteria related data wrangling.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prosper-ia/covid-response-source",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "pandas>=1", "scikit-learn"
    ]
)