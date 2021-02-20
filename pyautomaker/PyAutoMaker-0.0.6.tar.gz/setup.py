import setuptools
from glob import glob

with open("README.md", "rt") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyAutoMaker", # Replace with your own username
    version="0.0.6",
    author="WDW",
    author_email="boa9448@naver.com",
    description="자동화를 위한 패키지",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://boa9448.tistory.com/category/PyAutoMaker%20%EC%82%AC%EC%9A%A9%EB%B2%95",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],

    packages=["PyAutoMaker"],
    data_files=[("lib\\site-packages\\PyAutoMaker\\dlls", [file for file in glob("PyAutoMaker\\dlls\\*.*")])
                , ("lib\\site-packages\\PyAutoMaker\\models", [file for file in glob("PyAutoMaker\\models\\*.*")])
                , ("lib\\site-packages\\PyAutoMaker\\imgs", [file for file in glob("PyAutoMaker\\imgs\\*.*")])],

    install_requires = ["keyboard", "mouse", "pywin32"],

    python_requires='>=3.6',
)