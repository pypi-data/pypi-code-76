from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='dbrlist',
    version='0.0.3',
    description='Async wrapper for DBL api',
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/ConnorTippets/dblist/',
    author='meiscool466',
    license='MIT',
    packages=["dbrlist"],
    python_requires=">=3.8",
    keywords=["async", "wrapper", "async wrapper", "dbl"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        
    ],
    zip_safe=False,
)
