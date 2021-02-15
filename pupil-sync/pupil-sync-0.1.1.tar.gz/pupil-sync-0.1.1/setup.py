from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as rm:
    long_description = rm.read()

setup(
    name="pupil-sync", 
    version="0.1.1",
    author="Alex Harston",
    author_email="alex@harston.io",
    description="A lightweight parser for triggering Pupil Labs recordings with a hardware trigger.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexharston/pupil-sync",
    license="MIT",
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=['numpy', 'argparse'],
)
