import setuptools

setuptools.setup(
    name="niftytorch", 
    version="0.2",
    author="Farshid Sepehrband",
    author_email="fsepehrband@gmail.com",
    description="Deep Learning Library for NeuroImaging",
    long_description="""# NiftyTorch\n\n**NiftyTorch is a Python API for deploying deep neural networks for Neuroimaging research.** For documentation please visit [niftytorch.github.io](http://niftytorch.github.io/doc/).\n\n ## Developers\n\n**Adithya Subramanian** and **Farshid Sepehrband** \n INI Microstructural imaging Group ([IMG](https://www.ini.usc.edu/IMG/)), KSOM, USC""",
    long_description_content_type="text/markdown",
    url="http://niftytorch.github.io/doc/",
    packages=setuptools.find_namespace_packages(include=["niftytorch.*"]),
    include_package_data=True,
    license='This software is Copyright © 2020 The University of Southern California. All Rights Reserved. Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice, this paragraph and the following three paragraphs appear in all copies. Permission to make commercial use of this software may be obtained by contacting:  Farshid Sepehrband  farshid.sepehrband@loni.usc.edu  University of Southern California  2025 Zonal Ave, Los Angeles, CA 90033, USA. This software program and documentation are copyrighted by The University of Southern California. The software program and documentation are supplied "as is", without any accompanying services from USC. USC does not warrant that the operation of the program will be uninterrupted or error-free. The end-user understands that the program was developed for research purposes and is advised not to rely exclusively on the program for any reason. IN NO EVENT SHALL THE UNIVERSITY OF SOUTHERN CALIFORNIA BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY OF SOUTHERN CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. THE UNIVERSITY OF SOUTHERN CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND THE UNIVERSITY OF SOUTHERN CALIFORNIA HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    py_modules=['niftytorch'],
    entry_points={
        'console_scripts': ['mycli=mymodule:cli'],
    },
    python_requires='>=3.6',
    install_requires=[
        'torch==1.4.0',
        'optuna==1.4.0',
        'torchvision==0.5.0',
        'nibabel',
        'numpy==1.16.4',
        'pandas',
        'nipy',
        'colorlog',
        'alembic',
        'cliff',
        'tqdm'
    ]
)
