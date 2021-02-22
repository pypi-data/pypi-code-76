import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

f = open("requirements.txt", "r")
setuptools.setup(
    name="odb2psql", # Replace with your own username
    version="0.0.2",
    author="Eko S. Wibowo",
    author_email="swdev.bali@gmail.com",
    description="Converter from OpenOffice *.odb to PostgreSQL *.sql",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/remoteworkerid/odb2psql",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    python_requires='>=3.6',
    install_requires= [line.rstrip('\n') for line in f]
)
f.close()
