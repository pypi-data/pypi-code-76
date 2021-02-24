import setuptools
with open("README.md","r") as fh:
    long_description=fh.read()

setuptools.setup(
    name="miniProjet-pkg-your-samiraoumami",
    version="0.0.2",
    author= "samira oumami",
    author_email="samira.oumami@gmail.com",
    description= "Mini Projet GCP",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/miniProjetSam",
    packages=setuptools.find_packages()
   
)
