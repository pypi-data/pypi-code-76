import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
        name="Ideal Engine",
        version="1.0.1",
        author="Parth Krishna",
        author_email="thenerdsuperuser@gmail.com",
        description="A small project management tool",
        long_description_content_type="text/markdown",
        url="https://github.com/learnxtoday/ideal-engine",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",

            ],
        python_requires='>=3.6',
        )
