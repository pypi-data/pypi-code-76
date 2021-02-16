import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    setuptools.setup(
        name="pogmake",  # Replace with your own username
        version="0.0.2",
        scripts=['pog', 'pogm', 'pog.bat'],
        author="Peter Li",
        author_email="peterlimail47@gmail.com",
        description="I needed a cross platform makefile",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/peterino/pmake",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            "markdown",
            "colorama",
        ],
        python_requires=">=3.6",
    )
