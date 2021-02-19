from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="racepretextproc",
    version="0.0.3",
    author='Saby, Rakesh, Shashi, Gurushanth',
    author_email="author@example.com",
    license="MIT",
    description="Race Text processing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/race-ai01-srgs/racepretextproc",
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[            
          'regex',
          'NLTK',
          'textblob',
          'emot',
          'WordCloud',
          'matplotlib'
    ],
    python_requires='>=3.6'
)