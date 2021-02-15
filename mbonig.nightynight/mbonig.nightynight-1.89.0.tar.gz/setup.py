import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "mbonig.nightynight",
    "version": "1.89.0",
    "description": "A CDK construct that will automatically stop a running EC2 instance at a given time.",
    "license": "Apache-2.0",
    "url": "https://github.com/mbonig/nightynight",
    "long_description_content_type": "text/markdown",
    "author": "Matthew Bonig<matthew.bonig@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mbonig/nightynight"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "mbonig.nightynight",
        "mbonig.nightynight._jsii"
    ],
    "package_data": {
        "mbonig.nightynight._jsii": [
            "nightynight@1.89.0.jsii.tgz"
        ],
        "mbonig.nightynight": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-autoscaling==1.89.0",
        "aws-cdk.aws-ec2==1.89.0",
        "aws-cdk.aws-events-targets==1.89.0",
        "aws-cdk.aws-events==1.89.0",
        "aws-cdk.aws-iam==1.89.0",
        "aws-cdk.aws-lambda-nodejs==1.89.0",
        "aws-cdk.aws-lambda==1.89.0",
        "aws-cdk.aws-rds==1.89.0",
        "aws-cdk.core==1.89.0",
        "cdk-iam-floyd>=0.113.0, <0.114.0",
        "constructs>=3.2.27, <4.0.0",
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
    "scripts": [
        "src/mbonig/nightynight/_jsii/bin/nightynight"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
