#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from collections import defaultdict
import graphviz
import networkx as nx

import pinecone
from pinecone.specs import service as service_specs
from pinecone.functions import Function
from pinecone.functions.model import HubFunction
from pinecone.functions.engine import namespaced
from pinecone.functions.ranker import aggregator

__all__ = ["Graph", "IndexGraph"]


class Graph(service_specs.Service):
    """The graphical representation of a service."""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)

    def dump(self, format: str = "yaml") -> str:
        """Dumps the graph as yaml or json string.

        :param format: one of {"yaml", "json"}, defaults to "yaml".
        :type format: str, optional
        :rtype: str
        """
        """Dumps current graph as yaml or json."""
        if format == "yaml":
            return self.to_yaml()
        elif format == "json":
            return self.to_json()
        else:
            raise NotImplementedError("Format {format} not supported.".format(format=format))

    def to_graph(self) -> nx.MultiDiGraph:
        """Exports to a `networkx <https://networkx.org/>`_ graph.

        Construct a multi directed graph.
        Add incoming traffic and outgoing traffic nodes to signify the traffic flow.

        :return: [description]
        :rtype: nx.MultiDiGraph
        """

        def _get_node_name(fn: "pinecone.function.Function"):
            image_name = fn.image if isinstance(fn, HubFunction) else ""
            if image_name:
                return '"{}\n<{}>"'.format(fn.name, image_name)
            else:
                return fn.name

        def _get_edge_name(path_name: str):
            return "[{}]".format(path_name)

        graph = nx.MultiDiGraph()

        for path_name, steps in self.paths.items():
            node_names = [_get_node_name(self.functions[ss]) for ss in steps]
            for start_node, end_node in zip(["incoming traffic", *node_names], [*node_names, "outgoing traffic"]):
                graph.add_edge(
                    start_node,
                    end_node,
                    label=_get_edge_name(path_name),
                    key=_get_edge_name(path_name),
                )
        return graph

    def view(self):
        """Visualizes the graph in an iPython notebook.

        .. note::
            This method requires the `graphviz <https://graphviz.org/download/>`_ package
            installed on your operating system.
        """
        multigraph = self.to_graph()
        union_labels = defaultdict(list)
        for start_node, end_node, label in multigraph.edges.data("label"):
            if label:
                union_labels[(start_node, end_node)].append(label)

        graph = nx.DiGraph()
        for start_node, end_node, path in multigraph.edges:
            labels = union_labels.get((start_node, end_node)) or []
            graph.add_edge(start_node, end_node, label="".join(labels))

        return graphviz.Source(nx.nx_pydot.to_pydot(graph))


class IndexGraph(Graph):
    """The graphical representation of an index service.

    An index service consists of *preprocessors*, the *vector index*, and *postprocessors*.
    Preprocessors modify the items before indexing them, or modify the queries before retrieving results
    from the index.
    Examples of preprocessors include matrix fatorization models for transforming movie ids into embeddings,
    and BERT transformers for text data.
    Postprocessors modify the retrieved results of queries. Examples of postprocessors include
    re-rankers for balancing recommendation fairness, or imputation functions for increasing diversity.
    """

    _default_engine = namespaced.NamespacedEngine
    _default_aggregator = aggregator.Aggregator

    def __init__(self, engine_type: str = "approximated", metric: str = "cosine", shards: int = 1, replicas: int = 1):
        """

        :param engine_type: type of engine, one of {"approximated", "exact"}, defaults to "approximated".
            The "approximated" engine uses fast approximate search algorithms developed by Pinecone.
            The "exact" engine uses accurate exact search algorithms.
            It performs exhaustive searches and thus it is usually slower than the "approximated" engine.
        :type engine_type: str, optional
        :param metric: type of metric used in the vector index, one of {"cosine", "dotproduct", "euclidean"}, defaults to "cosine".
            Use "cosine" for cosine similarity,
            "dotproduct" for dot-product,
            and "euclidean" for euclidean distance.
        :type metric: str, optional
        :param shards: the number of shards for the engine, defaults to 1.
            As a general guideline, use 1 shard per 1 GB of data.
        :type shards: int, optional
        :param replicas: the number of replicas, defaults to 1.
            Use at least 2 replicas if you need high availability (99.99% uptime) for querying.
            For every 100 QPS your service needs to support, provision a replica.
        :type replicas: int, optional
        """
        super().__init__()
        self.preprocessors = {
            "read": [],
            "write": [],
        }
        self.postprocessors = []

        # The engine and the aggregator must be specified for an index service
        self.engine = self._default_engine(engine_type, metric=metric, replicas=replicas, shards=shards, name="engine")
        self.aggregator = None if shards == 1 else self._default_aggregator(num_shards=shards, name="aggregator")
        self._update_graph()

    def add_postprocessor(self, image_uri: str = None, config: dict = None, fn: Function = None):
        """Adds a postprocessor to the graph.

        You can add mutiple postprocessors to a graph.
        Postprocessors are on the "read" path of a graph
        and modify results of a ``query`` request.

        :param image_uri: a Pinecone Model Hub docker image URI, defaults to None
        :type image_uri: str, optional
        :param config: configurations for :class:`HubFunction`, defaults to None
        :type config: dict, optional
        :param fn: an instance of a Pinecone Function, defaults to None.
            For custom functions, use :class:`HubFunction`.
            If specified, ``image_uri`` and ``config`` will be ignored.
        :type fn: :class:`Function`, optional
        """
        _fn = fn or HubFunction(image=image_uri, config=config)
        self.postprocessors.append(_fn)
        self._update_graph()

    def remove_postprocessor(self, name: str):
        """Removes a postprocessor."""
        self.postprocessors = [fn for fn in self.postprocessors if fn.name != name]
        self._update_graph()

    def add_preprocessor(self, path: str, image_uri: str = None, config: dict = None, fn: Function = None):
        """Adds a preprocessor to the given path of the graph.

        You can add multiple preprocessors to the same path in a graph.
        ``query`` requests flow through the read path of the graph,
        and ``upsert`` requests flow through the write path of the graph.

        :param path: the path in the graph to add the preprocessor to
        :type path: {"read", "write"}
        :param image_uri: a Pinecone Model Hub docker image URI, defaults to None
        :type image_uri: str, optional
        :param config: configurations for :class:`HubFunction`, defaults to None
        :type config: dict, optional
        :param fn: an instance of a Pinecone Function, defaults to None.
            For custom functions, use :class:`HubFunction`.
            If specified, ``image_uri`` and ``config`` will be ignored.
        :type fn: :class:`Function`, optional
        """
        if path not in {"read", "write"}:
            raise RuntimeError("'path' must be one of {0}".format({"read", "write"}))
        _fn = fn or HubFunction(image=image_uri, config=config)
        self.preprocessors[path].append(_fn)
        self._update_graph()

    def remove_preprocessor(self, path: str, name: str):
        """Removes a preprocessor from the given path.

        :param path: the path in the graph to remove the preprocessor from
        :type path: {"read", "write"}
        :param name: name of the preprocessor to remove
        :type name: str
        """
        if path not in {"read", "write"}:
            raise RuntimeError("'path' must be one of {0}".format({"read", "write"}))
        self.preprocessors[path] = [fn for fn in self.preprocessors[path] if fn.name != name]
        self._update_graph()

    def add_read_preprocessor(self, image_uri: str = None, config: dict = None, fn: Function = None):
        """Adds a preprocessor to the "read" path of the graph.

        See :func:`add_preprocessor` for details.
        """
        self.add_preprocessor(path="read", image_uri=image_uri, config=config, fn=fn)

    def remove_read_preprocessor(self, name: str):
        """Removes a preprocessor from the "read" path.

        See :func:`remove_preprocessor` for details.

        """
        self.remove_preprocessor(path="read", name=name)

    def add_write_preprocessor(self, image_uri: str = None, config: dict = None, fn: Function = None):
        """Adds a preprocessor to the "write" path of the graph.

        See :func:`add_preprocessor` for details.
        """
        self.add_preprocessor(path="write", image_uri=image_uri, config=config, fn=fn)

    def remove_write_preprocessor(self, name: str):
        """Removes a preprocessor from the "write" path.

        See :func:`remove_preprocessor` for details.

        """
        self.remove_preprocessor(path="write", name=name)

    def _update_graph(self):
        write_functions = [*self.preprocessors["write"], self.engine, self.aggregator]
        read_functions = [*self.preprocessors["read"], self.engine, self.aggregator, *self.postprocessors]
        self.paths["write"] = [fn.name for fn in write_functions if fn]
        self.paths["read"] = [fn.name for fn in read_functions if fn]
        self.functions = {fn.name: fn for fn in [*write_functions, *read_functions] if fn}
