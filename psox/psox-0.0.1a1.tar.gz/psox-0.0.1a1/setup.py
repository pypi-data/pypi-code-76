import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psox",
    version="0.0.1a1",
    author="SLP",
    author_email="byteleap@gmail.com",
    description="Sound processing toolkit with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GaoangLiu/pspt",
    packages=setuptools.find_packages(),
    install_requires=[
        'smart-open'
    ],
    # entry_points={
    #     'console_scripts': ['sli=dofast.argparse_helper:parse_arguments'],
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
