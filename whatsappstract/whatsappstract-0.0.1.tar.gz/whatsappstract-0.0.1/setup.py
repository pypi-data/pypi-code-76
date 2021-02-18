import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whatsappstract",
    version="0.0.1",
    author="Felicia Loecherbach, Damian Trilling, Wouter van Atteveldt",
    author_email="wouter.van.atteveldt@vu.nl",
    description="Allow user to extract URLS from whatsapp messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ccs-amsterdam/whatsappstract",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=['selenium',
                      'dateparser',
                      'langdetect'],
)