import setuptools

setuptools.setup(
    name='testrexx',
    version='0.3.9',
    author='Guilherme Cartier',
    description='Python library for REXX automated testing',
    packages=['trexx',
              'trexx.utilities',
              'trexx.rexx_lib'],
    install_requires=['pyrexx',
                      'mkrexx',
                      'python-decouple',
                      'zowe-zos-files-for-zowe-sdk',
                      'zowe-zos-jobs-for-zowe-sdk'],
    package_data={'': ['*.rex']},
    include_package_data=True,
    python_requires='>=3.6'
)
