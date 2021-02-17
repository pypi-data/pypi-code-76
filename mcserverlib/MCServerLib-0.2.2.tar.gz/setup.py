import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="MCServerLib",  # Replace with your own username
    version="0.2.2",
    author="명이",
    author_email="aiden080605@gmail.com",
    description="Minecraft Server Setup Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/myoung2namur/MCServerLib",
    packages=setuptools.find_packages(),
    install_requires=['cpython'],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
