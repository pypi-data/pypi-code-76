import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trieres", 
    
    version="0.5.0",
    author="Dionysios Diamantopoulos",
    author_email="did@zurich.ibm.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cloudFPGA/trieres",
    # this package contains one module,
    # which resides in the subdirectory mymodule
    packages=setuptools.find_packages(),

    # make sure the shared library is included
    package_data={'trieres': ['_trieres.so']},
    include_package_data=True,
    
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.7',
)
