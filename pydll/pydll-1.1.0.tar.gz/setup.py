import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydll", # Replace with your own username
    version="1.1.0",
    author="GuangYao Sun",
    author_email="3150237154@qq.com",
    description="A expansion for me",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/manage/project/MyPymods/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)