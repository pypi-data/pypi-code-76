import setuptools
from os import path, getcwd

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open(path.join(getcwd(), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="openweather-pws",
    version="1.0.2",
    author="Ilya Vereshchagin",
    author_email="i.vereshchagin@gmail.com",
    description="Open Weather PWS API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wwakabobik/openweather_pws",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests',
    ],
)
