from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "Operating System :: Unix",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "License :: OSI Approved :: MIT License"
]

setup(
    name="cubituskinematics",
    version="0.0.7",
    description="Controller library for C.U.B.I.T.U.S. Robotic Arm",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/cubituskinematics/",
    author="Oliver Kudzia",
    author_email="olinox11@gmail.com",
    py_modules=["cubituskinematics"],
    include_package_data=True,
    package_data={'': ['cubituskinematics/*.xml']},
    license="MIT",
    classifiers=classifiers,
    keywords="cubitus, robotic arm, inverse kinematics, forward kinematics, tuke, kkui",
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=["numpy", "matplotlib>=3.3.3", "pyserial"]
)