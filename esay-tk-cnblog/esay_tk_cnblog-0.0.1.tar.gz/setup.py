import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="esay_tk_cnblog", # Replace with your own username
    version="0.0.1",
    author="2Or3InTheMorning",
    author_email="ponsekika@gmail.com",
    description="目前仅作为测试使用，并未设置功能",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)