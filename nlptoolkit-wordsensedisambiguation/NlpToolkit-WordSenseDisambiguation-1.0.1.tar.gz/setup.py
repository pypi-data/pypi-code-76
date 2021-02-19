from setuptools import setup

setup(
    name='NlpToolkit-WordSenseDisambiguation',
    version='1.0.1',
    packages=['WordSenseDisambiguation', 'WordSenseDisambiguation.Sentence', 'WordSenseDisambiguation.ParseTree'],
    url='https://github.com/StarlangSoftware/WordSenseDisambiguation-Py',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Word Sense Disambiguation Library',
    install_requires = ['NlpToolkit-AnnotatedSentence', 'NlpToolkit-AnnotatedTree']
)
