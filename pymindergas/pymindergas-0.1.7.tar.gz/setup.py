import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymindergas", # Replace with your own username
    version="0.1.7",
    author="Robert van Bregt",
    author_email="robertvanbregt@gmail.com",
    description="A python module to post meter readings to Mindergas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/metbril/pymindergas",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)