import setuptools
import aws_static_website

setuptools.setup(
    name="aws_static_website",
    version=aws_static_website.__version__,
    author=aws_static_website.__author__,
    author_email="alessandra.bilardi@gmail.com",
    description="A simple AWS static website deployment",
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    url="https://aws-static-website.readthedocs.io/",
    packages=setuptools.find_packages(),
    install_requires=[
        "aws-cdk.core>=1.62.0,<=1.80.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        "Source":"https://github.com/bilardi/aws-static-website",
        "Bug Reports":"https://github.com/bilardi/aws-static-website/issues",
        "Funding":"https://donate.pypi.org",
    },

)
