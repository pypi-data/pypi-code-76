import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NXTfusion", # Replace with your own username
    version="0.0.5",
    author="Daniele Raimondi",
    author_email="daniele.raimondi@kuleuven.be",
    description="Non linear data fusion over Entity Relation graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/eddiewrc/nxtfusion/src/master/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
	install_requires=['numpy', "scipy", "multipledispatch", "torch", "torchvision"],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
