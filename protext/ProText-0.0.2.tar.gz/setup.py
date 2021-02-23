import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ProText", # Replace with your own username
    version="0.0.2",
    author="Rajanna",
    author_email="krajanna@gmail.com",
    description="A text Preprocessing & Feature extraction package for NLP applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rajanna-AI/",
    install_requires=['nltk','textblob','wordcloud','matplotlib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)