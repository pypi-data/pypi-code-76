import setuptools
from setuptools import setup 

def readme():
    with open('README.md') as f:
        README= f.read()
    return README
 
setup(
    #Here is the module name.
    name="InstallMyScript",
 
    #version of the module
    version="0.0.2",
 
    #Name of Author
    author="Vijay kumar Bestha",
 
    #your Email address
    author_email="Someone@domain.com",
 
    #Small Description about module
    description="adding two numbers",
 
    long_description= "This is to add two given numbers. Ex a= 30 and b= 40 so c= 70.",
 
    #Specifying that we are using markdown file for description
    long_description_content_type="text/markdown",
 
    #Any link to reach this module, if you have any webpage or github profile
    #url="https://github.com/VijaykumarBestha/InstallMyScript",
    packages=['InstallMyScript'],
    
    include_package_date=True,
    
    install_requires=[],
 
    #classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
