from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["WordNet/*.pyx", "WordNet/Similarity/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-WordNet-Cy',
    version='1.0.3',
    packages=['WordNet', 'WordNet.Similarity'],
    package_data={'WordNet': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'WordNet.Similarity': ['*.pxd', '*.pyx', '*.c']},
    url='https://github.com/StarlangSoftware/TurkishWordNet-Py',
    license='',
    author='olcay',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Turkish WordNet KeNet',
    install_requires=['NlpToolkit-MorphologicalAnalysis-Cy']
)
