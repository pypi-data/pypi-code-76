import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphericalunet",
    version="0.0.1",
    author="Fenqiang Zhao",
    author_email="zhaofenqiang0221@gmail.com",
    description="This is the code for paper Spherical U-Net on Cortical Surfaces: Methods and Applications.",
    long_description="long_description",
    long_description_content_type="text/markdown",
    url="https://github.com/zhaofenqiang/Spherical_U-Net",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

