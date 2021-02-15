import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DFL168A", # Replace with your own username
    version="1.0.0",
    author="Jack Xia",
    author_email="techsupport@dafulaielectronics.com",
    description="The python module for OBD2/J1939/J1708 Interpreter IC: DFL168A from Dafulai Electronics Inc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dafulai/DFL168A_Python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)