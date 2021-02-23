import setuptools as st

st.setup(
    name="NightWind3DLib",
    version="0.0.2",
    author="Nova_NightWind0311",
    author_email="",
    description="Some little 3D games",
    long_description_content_type="text/markdown",
    url="https://github.com/",
    include_package_data=True,
    packages=st.find_packages(),
    install_requires=[
        "panda3d>=1.10.7"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
