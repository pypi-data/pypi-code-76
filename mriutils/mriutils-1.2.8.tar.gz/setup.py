#!/usr/bin/env python

import setuptools

readme = 'README.md'

setuptools.setup(
    name="mriutils",
    version="1.2.8",
    author="Mengmeng Kuang",
    keywords="MRI-Analysis",
    author_email="kuangmeng@msn.com",
    description="A simple common utils and models package",
    long_description=open(readme, 'r').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kuangmeng/MRIUtils",
    packages=setuptools.find_packages(),
    data_files=[readme],
    install_requires=["requests"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities"
    ],
    python_requires='>=3.5',
)