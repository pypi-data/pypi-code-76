import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='s3-log-query',
                 version='v1.0.0',
                 author='Mike Thoun',
                 author_email='mikethoun@gmail.com',
                 description='Query S3 Log Files',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='https://github.com/mikethoun/s3-log-query',
                 license='Apache License 2.0',
                 packages=setuptools.find_packages(),
                 classifiers=['Programming Language :: Python :: 3',
                              'License :: OSI Approved :: Apache Software License',
                              ],
                 install_requires=['boto3~=1.17.12',
                                   'python-dateutil~=2.8.1',
                                   'setuptools~=53.0.0',
                                   'pandas~=1.2.2',
                                   ])
