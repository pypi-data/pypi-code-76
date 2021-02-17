"""AWS static website with Auth0

This package contains the modules for deploying a simple AWS static website with Auth0.

It is part of the educational repositories (https://github.com/pandle/materials)
to learn how to write stardard code and common uses of the CI/CD.

Package contents two classes: one for the website and one for the lambdas and API Gateway.
They extended the core.Stack class of aws_cdk package.

    >>> import aws_static_website
    >>> help(aws_static_website)
    >>> import aws_static_website.website_stack as WebsiteStack
    >>> help(WebsiteStack)

# license MIT
# support https://github.com/bilardi/aws-static-website/issues
"""
__version__ = '0.0.1'
__author__ = 'Alessandra Bilardi'
