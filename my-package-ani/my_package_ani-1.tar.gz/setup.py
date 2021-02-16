import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my_package_ani",
    version="1",
    author="AJ",
    description="AssignmentQs2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anime-sh/SE_Lab_Python_DS_Assignment/tree/master/AssignmentQs2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
