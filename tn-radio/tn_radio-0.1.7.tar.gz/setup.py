import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="tn_radio", # Replace with your own username
    version="0.1.7",
    author="THAVASIGTI",
    author_email="ganeshanthavasigti1032000@gmail.com",
    description="Tamil Nadu Local Online Fm Station",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/THAVASIGTI/tn_radio.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=["python-vlc"]
)