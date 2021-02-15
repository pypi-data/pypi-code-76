import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uqo",
    version="0.0.2.1",
    author="QAR-Lab Munich",
    author_email="Sebastian.Zielinski@ifi.lmu.de",
    description="Client of the optimization framework UQO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        'dimod==0.9.13',
        'dwave-networkx==0.8.8',
        'prettytable==2.0.0',
        'pyzmq==22.0.2',
        'matplotlib==3.3.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)