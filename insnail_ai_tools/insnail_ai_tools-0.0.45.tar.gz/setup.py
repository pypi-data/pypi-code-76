import setuptools

with open("README.md", "r") as fin:
    long_description = fin.read()

with open("requirements.txt", "r") as fin:
    requirements = fin.read().split("\n")

setuptools.setup(
    name="insnail_ai_tools",  # Replace with your own username
    version="0.0.22",
    author="Insnail Ai Team",
    author_email="libiao@ingbaobei.com",
    description="Insnail Ai Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/insnail_ai_tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={"console_scripts": ["snail = insnail_ai_tools.cli:main"]},
)
