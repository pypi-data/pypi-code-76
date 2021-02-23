import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="djraphql",
    version="0.1.6",
    author="Joel Gardner",
    author_email="joel@simondata.com",
    description="DjraphQL builds a flexible & performant GraphQL schema by examining your Django models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Radico/djraphql",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",
    install_requires=[
        "django",
        "graphene",
        "six",
    ],
    pypi={"name": "djraphql", "version": "0.1.6"},
)
