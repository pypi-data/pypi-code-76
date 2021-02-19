import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name         = 'nnmeta',
    version      = '1.4.6',
    author       = 'Alexander D. Kazakov',
    author_email = 'alexander.d.kazakov@gmail.com',
    description  = 'NNMeta based on Schnetpack [https://github.com/atomistic-machine-learning/schnetpack].',
    license      = 'MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url          = 'https://github.com/AlexanderDKazakov/nnmeta',
    packages     =  setuptools.find_packages(),
    keywords     = ['neural network'],
    classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      ],
    python_requires='>=3.7',
    install_requires=[
        "storer",
    ],
)

