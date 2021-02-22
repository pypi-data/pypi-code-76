# coding: utf-8
import setuptools, os
import sys

packagename= "pyner"

#version = "0.0.10"
version = ""
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, packagename, "ner.py")) as f:
    for line in f.readlines():
        if "__version__" in line:
            version = line.strip().replace('"', '').split()[-1]
            break

print(version)
#sys.exit(0)

path = os.path.join(os.getcwd(),packagename, "README.md")
requiredments = os.path.join(os.getcwd(),packagename, "requirements.txt")

with open(path, "r", encoding='utf-8') as fh:
    long_description = ''.join(fh.readlines()[:-1])

with open(requiredments, "r", encoding='utf-8') as fh:
    requiredpackages = [ line.strip() for line in fh.readlines() ]

#print(requiredpackages)

setuptools.setup(
    name=packagename,
    version=version,
    author="Wang Bodhi Faqun",
    author_email="jyxz5@hotmail.com",
    description="This program is SDK of NER service API to handle one sentence or simple text file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tjnh05/ner",
    license = 'MIT',
    keywords = 'ner pyner',
    platforms = ['any'],

    packages=setuptools.find_packages(),
    package_data={
        'pyner': ['test.txt','requirements.txt']
    },
    entry_points = {
        "console_scripts": [
            "ner=pyner.ner:main"
        ]
    },
    install_requires=requiredpackages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.2',
)
