import setuptools as st

st.setup(
    name="NightWindAudioLib",
    author="Nova_NightWind0311",
    version="0.0.1",
    author_email="",
    description="Some little games of audio",
    long_description_content_type="text/markdown",
    url="https://github.com/",
    include_package_data=True,
    packages=st.find_packages(),
    install_requires=[
        "pydub>=0.24",
        "simpleaudio>=1.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)