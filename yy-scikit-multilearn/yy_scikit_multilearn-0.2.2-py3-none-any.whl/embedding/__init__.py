"""
The :mod:`yyskmultilearn.embedding` module provides implementations of label space embedding methods and a general
embedding based classifier.


+--------------------------------------------------------+---------------------------------------------------------------+
| Name                                                   | Description                                                   |
+========================================================+===============================================================+
| :class:`~yyskmultilearn.embedding.CLEMS`                 | Cost-Sensitive Label Embedding with Multidimensional Scaling  |
+--------------------------------------------------------+---------------------------------------------------------------+
| :class:`~yyskmultilearn.embedding.OpenNetworkEmbedder`   | Label Network Embedding for Multilabel Classification         |
+--------------------------------------------------------+---------------------------------------------------------------+
| :class:`~yyskmultilearn.embedding.SKLearnEmbedder`       | Wrapper for scikit-learn embedders                            |
+--------------------------------------------------------+---------------------------------------------------------------+
| :class:`~yyskmultilearn.embedding.EmbeddingClassifier`   | A general embedding-based classifier                          |
+--------------------------------------------------------+---------------------------------------------------------------+

"""

from .clems import CLEMS
from .skembeddings import SKLearnEmbedder
from .classifier import EmbeddingClassifier
import sys, platform

__all__ = [
    'CLEMS',
    'SKLearnEmbedder',
    'EmbeddingClassifier'
]

if not (sys.version_info[0] == 2 or platform.architecture()[0] == '32bit'):
    from .openne import OpenNetworkEmbedder

    __all__.append('OpenNetworkEmbedder')
