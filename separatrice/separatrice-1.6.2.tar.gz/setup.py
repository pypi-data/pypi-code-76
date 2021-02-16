import os
import setuptools

with open(r"C:\projects\separatrice\README.txt") as readme_file:
    README = readme_file.read()

setuptools.setup(
     name='separatrice',  
     version='1.6.2',
     license='MIT',
     author="Constantin Werner",
     author_email="const.werner@gmail.com",
     description="Separatrice is able to split a text into sentences and a sentence into clauses (russian). See docs: github.com/constantin50/separatrice/",
     include_package_data=True,
     long_description=README,
     keywords=['tokenizer','segmentation', 'NLP', 'russian','clauses'],
     url="https://github.com/constantin50/separatrice",
     packages=setuptools.find_packages(),
     install_requires=["morpholog","nltk"],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
