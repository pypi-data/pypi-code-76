import setuptools

with open("README.md") as f:
    long_description = f.read()
f.close()

setuptools.setup(
    name="nlp-900",
    version="1.0.0",
    description="NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/red-56/t9-nlp.git",
    install_requires=[
        "click",
        "vext",
        "vext.gi",
        "nltk",
        "spacy",
        "gTTS",
        "playsound",
        "SpeechRecognition",
        "pyaudio",
        "langdetect",
    ],
    entry_points={"console_scripts": ["nlp-900 = src.cli:cli"]},
    packages=setuptools.find_packages(),
    package_data={
        # If any package contains *.txt files, include them:
        "": ["data/*"],
        # And include any *.dat files found in the "data" subdirectory
        # of the "mypkg" package, also:
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
