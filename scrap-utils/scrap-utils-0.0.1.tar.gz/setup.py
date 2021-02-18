from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scrap-utils",
    version="0.0.1",
    author="Bisola Olasehinde",
    author_email="horlasehinde@gmail.com",
    description="A small package that contains commonly used codes while scraping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bizzyvinci/scrap-utils",
    packages=["scrap_utils"],
    keywords = ["scrap", "scraping", "scraper", "requests", "csv", "json"],
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)