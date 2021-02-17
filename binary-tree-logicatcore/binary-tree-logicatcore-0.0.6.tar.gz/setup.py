import setuptools

with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="binary-tree-logicatcore", # Replace with your own username
    version="0.0.6",
    author="Sai Sharath",
    author_email="kakubalsai@gmail.com",
    description="Package comprising of binary tree data structure and its relevant algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/logicatcore/binary_tree",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
