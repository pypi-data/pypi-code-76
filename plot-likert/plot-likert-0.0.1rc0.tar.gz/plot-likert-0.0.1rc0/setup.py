import setuptools

setuptools.setup(
    name="plot-likert",
    version="0.0.1rc0",
    author="nmalkin",
    description="Library to visualize results from Likert-style survey questions",
    long_description="The package is properly called plot_likert (`pip install plot_likert`). This package exists in case there's some confusion about the name.",
    long_description_content_type="text/plain",
    keywords = 'plot graph visualize likert survey matplotlib',
    url="https://github.com/nmalkin/plot-likert",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    python_requires='>=3.6',
    install_requires=[
        'plot_likert',
    ],
)
