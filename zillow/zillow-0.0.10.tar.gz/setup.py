import setuptools, os

readme_path = os.path.join(os.getcwd(), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r") as f:
        long_description = f.read()
else:
    long_description = 'zillow'

setuptools.setup(
    name="zillow",
    version="0.0.10",
    author="Kristof",
    description="zillow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kopnt/zillow",
    packages=setuptools.find_packages(),
    install_requires=[
        'jsoncodable>=0.0.12',
        'kffmpeg>=0.2.39',
        'ksimpleapi>=0.0.38',
        'kstopit>=0.0.10',
        'm3u8>=0.8.0',
        'randomua>=0.0.7',
        'simple-multiprocessing>=0.0.13'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)