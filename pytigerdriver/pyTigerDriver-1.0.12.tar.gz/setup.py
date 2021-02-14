import setuptools

with open("README.md", "r") as rdm:
    desc = rdm.read()

setuptools.setup(
    name="pyTigerDriver",
    version="v1.0.12",
    author="Zrouga Mohamed",
    author_email="medzrouga@gmail.com",
    description="GSQL client for TigerGraph",
    long_description=desc,
    long_description_content_type="text/markdown",
    keywords=['gsql', 'client','tigergraph'],
    requires=["requests"],
    url="https://github.com/Zrouga-Mohamed/pyTigerDriver ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Topic :: Database",
    ],
    python_requires='>=3.5'
)
