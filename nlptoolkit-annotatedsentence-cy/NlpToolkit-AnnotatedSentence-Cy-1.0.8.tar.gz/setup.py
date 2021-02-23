from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["AnnotatedSentence/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-AnnotatedSentence-Cy',
    version='1.0.8',
    packages=['AnnotatedSentence'],
    package_data={'AnnotatedSentence': ['*.pxd', '*.pyx', '*.c', '*.py']},
    url='https://github.com/StarlangSoftware/AnnotatedSentence-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Annotated Sentence Processing Library',
    install_requires=['NlpToolkit-WordNet-Cy', 'NlpToolkit-NamedEntityRecognition-Cy', 'NlpToolkit-PropBank-Cy', 'NlpToolkit-DependencyParser-Cy']
)
