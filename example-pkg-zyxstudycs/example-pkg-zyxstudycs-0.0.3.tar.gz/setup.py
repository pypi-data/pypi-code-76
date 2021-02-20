import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="example-pkg-zyxstudycs",
    version="0.0.3",
    author="zyxstudycs",
    author_email="zhengyixing01@corp.netease.com",
    description="Try package python code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'librosa==0.8.0',
        'numba==0.45.1'
    ],
)