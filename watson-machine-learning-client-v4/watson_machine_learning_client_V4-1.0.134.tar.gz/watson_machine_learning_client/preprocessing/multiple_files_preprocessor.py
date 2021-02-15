__all__ = [
    "DataJoinGraph"
]

from typing import List, Dict, Set
from graphviz import Digraph

from ..utils.autoai.enums import TShirtSize, PredictionType
from ..utils.autoai.utils import is_ipython, check_graphviz_binaries


class BaseOBMJson:
    """Base class for helper objects representation."""

    def __repr__(self):
        return self.__str__()


class Node(BaseOBMJson):
    """Node class for json representation and conversion of graphviz nodes."""

    def __init__(self, name: str, timestamp_column_name: str = None, timestamp_format: str = None):
        self.table = Table(name=name, timestamp_column_name=timestamp_column_name, timestamp_format=timestamp_format)

    def to_dict(self):
        """Convert this Node to dictionary for further REST API call."""
        return {"table_name": self.table.name}

    def __str__(self):
        return (f"\n\t\tNODE:\n"
                f"\t\t\t{self.table.__str__()}")


class Edge(BaseOBMJson):
    """Edge helper class for json representation of graphviz edge."""

    def __init__(self, from_node: str, to_node: str, from_column: List[str], to_column: List[str]):
        if not isinstance(from_column, list) or not isinstance(to_column, list):
            raise TypeError("\"from_column\" and \"to_column\" need to be of type List[str].")

        self.from_node = from_node
        self.to_node = to_node
        self.from_column = from_column
        self.to_column = to_column

    def to_dict(self):
        """Convert this Node to dictionary for further REST API call."""
        _dict = {
            "from": self.from_node,
            "to": self.to_node,
            "from_column": self.from_column,
            "to_column": self.to_column,
        }
        return _dict

    def __str__(self):
        return (f"\n\t\tEDGE:\n"
                f"\t\t\tFROM: {self.from_node}\n"
                f"\t\t\tTO: {self.to_node}\n"
                f"\t\t\tFROM COLUMN: {self.from_column}\n"
                f"\t\t\tTO COLUMN: {self.to_column}")


class Table(BaseOBMJson):
    """Table class to represent / define OBM tables."""

    def __init__(self, name: str, timestamp_column_name: str = None, timestamp_format: str = None):
        if (timestamp_column_name or timestamp_format) and not (timestamp_column_name and timestamp_format):
            print("Need to pass both column name and date format in order to mark column as timestamp type.")

        self.name = name
        self.timestamp_column_name = timestamp_column_name
        self.timestamp_format = timestamp_format
        self.source = {}

    def to_dict(self):
        """Convert this Node to dictionary for further REST API call."""
        _dict = {
            "table_source": self.source
        }
        if self.timestamp_column_name and self.timestamp_format:
            _dict.update({
                "column_format": {
                    self.timestamp_column_name: self.timestamp_format,
                },
                "timestamp_column_name": self.timestamp_column_name
            })
        return _dict

    def __str__(self):
        if self.timestamp_column_name and self.timestamp_format:
            return (f"TABLE:\n"
                    f"\t\t\t\tNAME: {self.name}\n"
                    f"\t\t\t\tSOURCE: {self.source}\n"
                    f"\t\t\t\tTIMESTAMP_COLUMN_NAME: \'{self.timestamp_column_name}\'\n"
                    f"\t\t\t\tCOLUMN_FORMAT: {{\n\t\t\t\t\t'{self.timestamp_column_name}': '{self.timestamp_format}'\n"
                    f"\t\t\t\t}}")
        else:
            return (f"TABLE:\n"
                    f"\t\t\t\tNAME: {self.name}\n"
                    f"\t\t\t\tSOURCE: {self.source}")


class DataJoinGraph(Digraph, BaseOBMJson):
    """
    DataJoinGraph class - helper class for handling multiple data sources for AutoAI experiment.

    You can define the overall relations between each of data source and see these defined relations
    in a form of string representation calling print(ObmGraph) or to leverage graphviz library
    and make entire graph visualization.

    Parameters
    ----------
    t_shirt_size: enum TShirtSize, optional
        The size of the computation POD.

    Example
    -------
    >>> data_join_graph = DataJoinGraph()
    >>> # or
    >>> data_join_graph = DataJoinGraph(t_shirt_size=DataJoinGraph.TShirtSize.L)
​
    >>> data_join_graph.node(name="main")
    >>> data_join_graph.node(name="customers")
    >>> data_join_graph.node(name="transactions")
    >>> data_join_graph.node(name="purchases")
    >>> data_join_graph.node(name="products")
​
    >>> data_join_graph.edge(from_node="main", to_node="customers",
    >>>                from_column=["group_customer_id"], to_column=["group_customer_id"])
    >>> data_join_graph.edge(from_node="main", to_node="transactions",
    >>>                from_column=["transaction_id"], to_column=["transaction_id"])
    >>> data_join_graph.edge(from_node="main", to_node="purchases",
    >>>                from_column=["group_id"], to_column=["group_id"])
    >>> data_join_graph.edge(from_node="transactions", to_node="products",
    >>>                from_column=["product_id"], to_column=["product_id"])
​
    >>> print(data_join_graph)
    >>> data_join_graph.visualize()
    """
    TShirtSize = TShirtSize
    NodeTemplate = """<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="1">
      <TR>
          <TD STYLE="ROUNDED" BGCOLOR=\"{color}\" COLSPAN=\"{colspan}\">{dataset_name}</TD>
      </TR>
      <TR>
      </TR>
    </TABLE>>"""
    ColumnsIndex = NodeTemplate.rfind("<TR>") + len("<TR>")
    ColumnTemplate = "<TD STYLE=\"ROUNDED\" PORT=\"{port}\">{column_name}</TD>"

    def __init__(self,
                 t_shirt_size: 'TShirtSize' = TShirtSize.M,
                 max_depth: int = 3,
                 data_source_type: str = "csv"):
        super().__init__(comment='Data Join Graph')

        self.t_shirt_size = t_shirt_size

        # note: these values should be provided by optimizer
        self.target_column = None
        self.__problem_type = None
        # --- end note

        self.main_node_name = None  # main node always the first one
        self.max_depth = max_depth
        self.data_source_type = data_source_type

        self.nodes: List['Node'] = []
        self.edges: List['Edge'] = []
        self.edges_to_ports: Dict[str, str] = {}
        self.node_edges: Dict[str, Set[str]] = {}

    @property
    def problem_type(self) -> 'PredictionType':
        return self.__problem_type

    @problem_type.setter
    def problem_type(self, value: 'PredictionType') -> None:
        """We need to map prediction types between KB and OBM."""
        if value == PredictionType.MULTICLASS:
            self.__problem_type = 'classification'
        else:
            self.__problem_type = value

    def node(self, name: str, timestamp_column_name: str = None, timestamp_format: str = None):
        """
        Add node to the graph. The node is representing the particular data source for training.
        The node added as first will be set as main one.

        Parameters
        ----------
        name: str, required
            The name/id of the node, it must be the same as id passed to particular linked DataConnection.
        timestamp_column_name: str, optional
            The name of the column, which includes dates.
        timestamp_format: str, optional
            Format of dates contained in column named 'timestamp_column_name'.
        Example
        -------
        >>> data_join_graph.node(name="main")
        """
        self.node_edges[name] = set()

        # note: if we do not have any nodes already added, first one will be the main node
        if not self.nodes:
            self.main_node_name = name
        self.nodes.append(Node(name=name, timestamp_column_name=timestamp_column_name,
                               timestamp_format=timestamp_format))
        # --- end note

    def edge(self, from_node, to_node, from_column: List[str], to_column: List[str]):
        """
        Add edge to the graph. The edge defines the connection between two DataConnections.
        eg. main --- from column customer_id to column customer_id --> customers

        Parameters
        ----------
        from_node: str, required
            The starting Node.

        to_node: str, required
            The ending Node

        from_column: List[str], required
            The list of columns located in the starting Node in order, these columns will be connected to
            the ending Node columns.

        to_column: List[str], required
            The list of columns located in the ending Node.

        Example
        -------
        >>> data_join_graph.edge(from_node="main", to_node="transactions",
        >>>                from_column=["transaction_id"], to_column=["transaction_id"])
        """
        self.node_edges[from_node] |= set(from_column)
        self.node_edges[to_node] |= set(to_column)

        self.edges.append(Edge(from_node=from_node, to_node=to_node, from_column=from_column, to_column=to_column))

    def _visualize_nodes(self):
        for node in self.nodes:
            name = node.table.name
            column_names = self.node_edges[name]
            self.edges_to_ports.update({f"{name}{column}": f"{name}:e{i}" for i, column in enumerate(column_names)})
            columns = ''.join(
                [self.ColumnTemplate.format(port=f"e{i}", column_name=name) for i, name in enumerate(column_names)])
            node_label = self.NodeTemplate[:self.ColumnsIndex] + columns + self.NodeTemplate[self.ColumnsIndex:]
            color = "LIGHTBLUE2" if self.main_node_name == name else "WHITE"

            super().node(name=name, label=node_label.format(color=color,
                                                            dataset_name=name,
                                                            colspan=str(len(column_names))))

    def _visualize_edges(self):
        for edge in self.edges:
            edges = [(self.edges_to_ports[edge.from_node + from_col], self.edges_to_ports[edge.to_node + to_col])
                     for from_col, to_col in zip(edge.from_column, edge.to_column)]

            super().edges(edges)

    @check_graphviz_binaries
    def visualize(self):
        super().clear()
        super().attr('node', shape='plaintext')
        super().attr('edge', minlen='2')
        super().attr('graph', nodesep='1')

        self._visualize_nodes()
        self._visualize_edges()

        """Display graph in the notebook or as a rendered image."""
        if is_ipython():
            import IPython.display
            IPython.display.display(self)

        else:
            self.render(view=True)

    def to_dict(self):
        """Convert this Node to dictionary for further REST API call."""
        _dict = {
            "id": "obm",
            "type": "execution_node",
            "op": "kube",
            "runtime_ref": "obm",
            "inputs": [{"id": node.table.name} for node in self.nodes],
            "outputs": [
                {
                    "id": "obm_out"
                }
            ],
            "parameters": {
                "stage_flag": True,
                "output_logs": True,
                "engine": {
                    "template_id": "spark-2.3.0-automl-svt-template",
                    "size": {
                        "num_workers": "10",
                        "worker_size": {
                            "cpu": 2,
                            "memory": "8g"
                        },
                        "driver_size": {
                            "cpu": 2,
                            "memory": "8g"
                        }
                    }
                },
                "obm": {
                    "Entity_Graph": {
                        "nodes": [node.to_dict() for node in self.nodes],
                        "edges": [edge.to_dict() for edge in self.edges]
                    },
                    "Tables": {node.table.name: node.table.to_dict() for node in self.nodes},
                    "Feature_Selector": {
                        "selectors": [
                            "deduplicate",
                            "consistent"
                        ]
                    },
                    "OneButtonMachine": {
                        "main_table": self.main_node_name,
                        "target_column": self.target_column,
                        "max_depth": self.max_depth,
                        "data_source": self.data_source_type,
                        "problem_type": self.problem_type,
                        "join_limit": 50,
                    }
                }
            }
        }
        return _dict

    @classmethod
    def _from_dict(cls, _dict: dict) -> 'DataJoinGraph':
        """Create data join graph object from wml pipeline parameters."""
        data_join_graph = cls()

        [data_join_graph.node(name=node['table_name']) for node in _dict['parameters']['obm']['Entity_Graph']['nodes']]
        [data_join_graph.edge(
            from_node=edge['from'],
            to_node=edge['to'],
            from_column=edge['from_column'],
            to_column=edge['to_column']) for edge in _dict['parameters']['obm']['Entity_Graph']['edges']]

        return data_join_graph

    def __str__(self):
        return (f"\nDataJoinGraph:\n"
                f"\tMAIN NODE: {self.main_node_name}\n"
                f"\tTARGET COLUMN: {self.target_column}\n"
                f"\tMAX DEPTH: {self.max_depth}\n"
                f"\tDATA SOURCE TYPE: {self.data_source_type}\n"
                f"\tPROBLEM TYPE: {self.problem_type}\n"
                f"\tNODES: {[node for node in self.nodes]}\n"
                f"\tEDGES: {[edge for edge in self.edges]}"
                )
