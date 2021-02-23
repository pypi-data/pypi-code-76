from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '1.1.1'
DESCRIPTION = 'Es un paquete que brinda la posibilidad a las clases de almacenar los pasos que se siguen en esta.'

# Setting up
setup(
    name="log_helper-bit3",
    version=VERSION,
    author="Mauricio Montoya Medrano",
    author_email="mcubico33@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bitcubico/LogHelperPy",
    packages=find_packages(),
    keywords=['python', 'log', 'helper', 'mcubico', 'bitcubico technology'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
    ],
    python_requires='>=3.8',
)
