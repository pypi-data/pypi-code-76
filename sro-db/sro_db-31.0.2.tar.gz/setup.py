from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='sro_db',  # Required
    version="31.0.2",  # Required
    author="Paulo Sergio dos Santo Junior",
    author_email="paulossjuniort@gmail.com",
    description="A lib to create a database based on Scrum Reference Ontology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ontologyasaservice/data/domain/scrum-reference-ontology/sro_db",
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy', 'SQLAlchemy-Utils', 'factory-boy', 'SQLAlchemy-serializer'
    ],

    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    setup_requires=['wheel'],
    
)
