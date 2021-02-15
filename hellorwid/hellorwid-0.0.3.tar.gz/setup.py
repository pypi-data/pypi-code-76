import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hellorwid", # Replace with your own username
    version="0.0.3",
    author="Eko S. Wibowo",
    author_email="swdev.bali@gmail.com",
    description="A hello world for all fellows of Remote Worker Indonesia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/remoteworkerid/hellorwid",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    python_requires='>=3.6',
)