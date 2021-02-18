from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'MeBiPred'
LONG_DESCRIPTION = 'Metal Binding Predictor, using neural network'
REQUIREMENTS = [line.strip('\n') for line in open('requirements.txt','r')]

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="mymetal", 
        version=VERSION,
        author="Ariel Aptekmann",
        author_email="<arielaptekmann@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=REQUIREMENTS, # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'metal bingind prediction package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
        include_package_data=True,
        package_data={'': ['aa.csv','ModelPersistency/*','kmer_counts/*']}
)