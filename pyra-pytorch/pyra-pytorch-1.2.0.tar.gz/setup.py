import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyra-pytorch", # Replace with your own username
    version="1.2.0",
    author="Vajira Thambawita",
    author_email="vlbthambawita@gmail.com",
    description="Pyramid Focus Augmentation: Medical Image Segmentation with Step Wise Focus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vlbthambawita/pyra-pytorch",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'Pillow',
  ],
)