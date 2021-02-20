"""
The :mod:`yyskmultilearn.cluster` module gathers label space clustering methods.


+-------------------------------------------------------------+----------------------------------------------------------+
| Name                                                        | Description                                              |
+=============================================================+==========================================================+
| :class:`~yyskmultilearn.cluster.FixedLabelSpaceClusterer`     | Return a predefined fixed clustering, usually driven by  |
|                                                             | expert knowledge                                         |
+-------------------------------------------------------------+----------------------------------------------------------+
| :class:`~yyskmultilearn.cluster.MatrixLabelSpaceClusterer`    | Cluster the label space using a scikit-compatible        |
|                                                             | matrix-based clusterer                                   |
+-------------------------------------------------------------+----------------------------------------------------------+
| :class:`~yyskmultilearn.cluster.GraphToolLabelGraphClusterer` | Fits a Stochastic Block Model to the Label Graph and     |
|                                                             | infers the communities                                   |
+-------------------------------------------------------------+----------------------------------------------------------+
| :class:`~yyskmultilearn.cluster.StochasticBlockModel`         | A Stochastic Blockmodel class                            |
+-------------------------------------------------------------+----------------------------------------------------------+
| :class:`~yyskmultilearn.cluster.IGraphLabelGraphClusterer`    | Clusters label space using igraph community detection    |
+-------------------------------------------------------------+----------------------------------------------------------+
| :class:`~yyskmultilearn.cluster.RandomLabelSpaceClusterer`    | Randomly divides label space into equally-sized clusters |
+-------------------------------------------------------------+----------------------------------------------------------+
| :class:`~yyskmultilearn.cluster.NetworkXLabelGraphClusterer`  | Cluster label space with NetworkX community detection    |
+-------------------------------------------------------------+----------------------------------------------------------+

"""

from .base import LabelCooccurrenceGraphBuilder
from .fixed import FixedLabelSpaceClusterer
from .matrix import MatrixLabelSpaceClusterer
from .random import RandomLabelSpaceClusterer

__all__ = [
    'FixedLabelSpaceClusterer',
    'LabelCooccurrenceGraphBuilder',
    'MatrixLabelSpaceClusterer',
    'RandomLabelSpaceClusterer'
]

# graphtool import optional (is GPL-ed, does not work on windows)
try:
    from .graphtool import GraphToolLabelGraphClusterer, StochasticBlockModel

    __all__ += ['GraphToolLabelGraphClusterer', 'StochasticBlockModel']
except ImportError:
    pass

# python-igraph import optional (is GPL-ed)
try:
    from .igraph import IGraphLabelGraphClusterer

    __all__ += ['IGraphLabelGraphClusterer']
except ImportError:
    pass

# networkx import is optional
try:
    from .networkx import NetworkXLabelGraphClusterer

    __all__ += ['NetworkXLabelGraphClusterer']
except ImportError:
    pass
