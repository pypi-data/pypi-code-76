# -*- coding: utf-8 -*-
'''
Created on 30 Jan 2021
@author: olivier
'''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypos3dv",
    version="0.4.0",
    author="Olivier Dufailly",
    author_email="dufgrinder@laposte.net",
    description="Wavefront files simple 3D viewer (OpenGL GLFW based)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sourceforge.net/projects/pojamas",
    
    package_dir={'': 'src'},  
    packages=setuptools.find_packages(where='src', include=('pypos3dv', 'pypos3dv.*' )),

    entry_points={
      'console_scripts': [ 'pypos3dv = pypos3dv.__main__:main' ],
      'gui_scripts': [ 'pypos3dv = pypos3dv.__main__:main' ] },
    
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=['PyOpenGL>=3.1', 'PyGLM>=1.99', 'glfw>=2.0.0', 'pypos3d>=0.4'],
    python_requires='>=3.6',
)
