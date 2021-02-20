import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='LexaPureToolbox',
    version='1.0.13',
    description='Collection of tools developed for LexaPure',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/paulo-lexapure/LexaPuretoolbox',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    packages=['LexaPureToolbox'],
    include_package_data=True,
    install_requires=[
        'requests',
        'slacker',
        'datetime',
        'pymysql'
    ]
)
