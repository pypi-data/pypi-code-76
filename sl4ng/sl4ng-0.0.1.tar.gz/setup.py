from setuptools import setup, find_packages

with open('README.md', 'r') as fob:
    long_description = fob.read()

setup(
    name='sl4ng',
    version='0.0.1',
    author='Kenneth Elisandro',
    author_email='eli2and40@tilde.club',
    url='https://tildegit.org/eli2and40/sl4ng',
    # packages=find_packages(),
    packages=['sl4ng'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='utilities productivity',
    license='MIT',
    requires=[
        'pyperclip',
        'dill',
        'psutil',
        'send2trash',
        'tqdm',
        'filetype',
    ],
    # py_modules=['sl4ng'],
    python_requires='>=3.8',

)