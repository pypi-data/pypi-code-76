from setuptools import setup, find_packages

requirements = [
"networkx>=2.4",
"numpy>=1.18.1",
"pandas>=1.0.5",
"matplotlib>=3.1.1",
"seaborn>=0.11.0",
"scikit-learn>=0.21.3",
"scipy>=1.4.1",
"teneto==0.5.0",
]

setup(
    name="phasik",
    version="0.0.3",
    author="Maxime Lucas",
    author_email="ml.maximelucas@gmail.com",
    description="Tools to build temporal networks and infer temporal phases from them",
    long_description="Tools to build temporal networks and infer temporal phases from them. Build temporal networks from time series data. Cluster snapshots to infer the multiscale temporal organisation of the network.",
    url="https://gitlab.com/habermann_lab/phasik",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
