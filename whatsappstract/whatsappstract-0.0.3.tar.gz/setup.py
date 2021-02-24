import setuptools

setuptools.setup(
    name="whatsappstract",
    version="0.0.3",
    author="Felicia Loecherbach, Damian Trilling, Wouter van Atteveldt",
    author_email="wouter.van.atteveldt@vu.nl",
    description="Allow user to extract URLS from whatsapp messages",
    long_description_content_type="text/markdown",
    url="https://github.com/ccs-amsterdam/whatsappstract",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=['selenium'],
)
