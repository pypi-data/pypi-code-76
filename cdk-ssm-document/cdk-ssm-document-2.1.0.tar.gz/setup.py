import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-ssm-document",
    "version": "2.1.0",
    "description": "CDK Construct for managing SSM Documents",
    "license": "Apache-2.0",
    "url": "https://github.com/udondan/cdk-ssm-document",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Schroeder",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/udondan/cdk-ssm-document.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_ssm_document",
        "cdk_ssm_document._jsii"
    ],
    "package_data": {
        "cdk_ssm_document._jsii": [
            "cdk-ssm-document@2.1.0.jsii.tgz"
        ],
        "cdk_ssm_document": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-cloudformation>=1.47.0, <2.0.0",
        "aws-cdk.aws-iam>=1.47.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.47.0, <2.0.0",
        "aws-cdk.core>=1.47.0, <2.0.0",
        "cdk-iam-floyd==0.120.0",
        "constructs>=3.2.80, <4.0.0",
        "jsii>=1.21.0, <2.0.0",
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
