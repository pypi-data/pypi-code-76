#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Litao Yang, Yanan Wang
# Mail: litao.yang@monash.edu, yanan.wang1@monash.edu
# Created Time:  2021-2-1 21:40:00
#############################################
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="octid",
    version="1.1.3",
    author="Litao Yang, Yanan Wang",
    author_email="litao.yang@monash.edu, yanan.wang1@monash.edu",
    description="One-Class learning-based tool for Tumor Image Detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Environment :: GPU :: NVIDIA CUDA"
    ],
    python_requires='>=3.6',
    platforms = "any",
    install_requires=[
        "torch",
        "torchvision",
        "matplotlib",
        "numpy",
        "sklearn",
        "pandas",
        "umap-learn"    
    ]
)
