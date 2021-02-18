import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "p6-namer",
    "version": "0.7.38",
    "description": "Sets the AWS IAM Account Alias with a Custom Resource",
    "license": "Apache-2.0",
    "url": "https://github.com/p6m7g8/p6-namer.git",
    "long_description_content_type": "text/markdown",
    "author": "Philip M. Gollucci<pgollucci@p6m7g8.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/p6m7g8/p6-namer.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "p6_namer",
        "p6_namer._jsii"
    ],
    "package_data": {
        "p6_namer._jsii": [
            "p6-namer@0.7.38.jsii.tgz"
        ],
        "p6_namer": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-lambda-nodejs>=1.86.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.86.0, <2.0.0",
        "aws-cdk.core>=1.86.0, <2.0.0",
        "aws-cdk.custom-resources>=1.86.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.17.1, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
