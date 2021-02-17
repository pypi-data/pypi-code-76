import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anapass-python", # Replace with your own username
    version="2.0.0.7",
    author="hthwang",
    author_email="hthwang@anapass.com",
    description="Anapass Python Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.anapass.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    data_files=["AnapassTComm.dll", "AnapassTComm32.dll", "AnapassTModule.dll", "AnapassTModule32.dll", "AnapassTParser.dll", "AnapassTParser32.dll" ]
)

