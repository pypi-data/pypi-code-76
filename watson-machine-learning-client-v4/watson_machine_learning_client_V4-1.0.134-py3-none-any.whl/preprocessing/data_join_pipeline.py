__all__ = [
    'DataJoinPipeline',
    'OBMPipelineGraphBuilder'
]

import re
from operator import itemgetter
from collections import defaultdict
from typing import Tuple, List, Union, Dict, TYPE_CHECKING
from graphviz import Digraph
from .templates import pretty_print_template
from ..utils.autoai.utils import is_ipython, check_graphviz_binaries
from ..utils.autoai.enums import VisualizationTypes

if TYPE_CHECKING:
    from ..helpers.connections.connections import DataConnection


class DataJoinPipeline:
    """
    Class representing abstract data join pipeline.

    Parameters
    ----------
    preprocessed_data_connection: DataConnection, required
        Populated DataConnection with preprocessed data join information.
    optimizer: RemoteAutoPipeline, required
        Optimizer with initialized pipeline metadata, required for running an OBM training in predict method.
    """
    VisualizationTypes = VisualizationTypes

    def __init__(self, preprocessed_data_connection: 'DataConnection', optimizer: 'RemoteAutoPipelines') -> None:
        self._pipeline_json = preprocessed_data_connection._download_obm_json_from_cos()['Pipeline']
        self._obm_pipeline_graph_builder = OBMPipelineGraphBuilder(self._pipeline_json)
        self._graph_json, self._graph = self._obm_pipeline_graph_builder.build_graph()
        self._optimizer = optimizer

    @check_graphviz_binaries
    def visualize(self, astype: 'VisualizationTypes' = VisualizationTypes.INPLACE) -> None:
        """Display graph in the notebook or as a rendered image.

        Parameters
        ----------
        astype: VisualizationTypes, optional
            Specify a type of visualization for this graph. Default is VisualizationTypes.INPLACE
            (when in notebook env, picture will be displayed in the cell output).
            VisualizationTypes.PDF indicates to render a pdf document with visualization.
        """
        if is_ipython():
            if astype == VisualizationTypes.PDF:
                self._graph.render(view=True)

            else:
                import IPython.display
                IPython.display.display(self._graph)

        else:
            self._graph.render(view=True)

    # def predict(self,
    #             *,
    #             training_data_reference: List['DataConnection'],
    #             training_results_reference: 'DataConnection' = None,
    #             background_mode=False) -> 'DataFrame':
    #     """
    #     Run an OBM training process on top of the training data referenced by DataConnection.
    #
    #     Parameters
    #     ----------
    #     training_data_reference: List[DataConnection], required
    #         Data storage connection details to inform where training data is stored.
    #
    #     training_results_reference: DataConnection, optional
    #         Data storage connection details to store pipeline training results. Not applicable on CP4D.
    #
    #     background_mode: bool, optional
    #         Indicator if fit() method will run in background (async) or (sync).
    #
    #     Returns
    #     -------
    #     pandas.DataFrame contains dataset from remote data storage.
    #     """
    #     self._optimizer.fit(training_data_reference=training_data_reference,
    #                         training_results_reference=training_results_reference,
    #                         background_mode=background_mode)
    #
    #     return self._optimizer.get_preprocessed_data_connection().read()

    def pretty_print(self, ipython_display: bool = False) -> None:
        """
        Prints code which generates OBM data preprocessing.

        Parameters
        ----------
        ipython_display: bool, optional
            If method executed in jupyter notebooks/ipython set this flag to true in order to get syntax highlighting.
        """
        params = self._optimizer.get_params()
        data_join_graph = params["data_join_graph"]

        nodes = ""
        for node in data_join_graph.nodes:
            if node.table.timestamp_format and node.table.timestamp_column_name:
                nodes += f"data_join_graph.node(name=\"{node.table.name}\"," \
                         f" timestamp_column_name=\"{node.table.timestamp_column_name}\"," \
                         f" timestamp_format=\"{node.timestamp_format}\")\n"
            else:
                nodes += f"data_join_graph.node(name=\"{node.table.name}\")\n"

        edges = "\n".join([f"data_join_graph.edge(from_node=\"{edge.from_node}\", to_node=\"{edge.to_node}\",\n"
                           f"\t\t\t\t\t from_column={edge.from_column}, to_column={edge.to_column})"
                           for edge in data_join_graph.edges])


        join_indices = [it - 1 for it in self._obm_pipeline_graph_builder.get_join_iterations()]
        paths = "\n".join(["# - " + re.search(r"\[(.*)\]", msg["message"]["text"]).group()
                           for msg in itemgetter(*join_indices)(self._pipeline_json)])
        nb_of_features = re.search(r"\d", self._pipeline_json[-1]["message"]["text"]).group()

        pretty_print = pretty_print_template.template.format(
                        nodes=nodes, edges=edges,
                        name=f"\"{params['name']}\"",
                        prediction_type=f"\"{params['prediction_type']}\"",
                        prediction_column=f"\"{params['prediction_column']}\"",
                        scoring=f"\"{params['scoring']}\"",
                        paths=paths,
                        nb_of_features=nb_of_features)

        if ipython_display:
            import IPython.display
            markdown = IPython.display.Markdown(f'```python\n{pretty_print}\n```')
            IPython.display.display(markdown)
        else:
            print(pretty_print)


class OBMPipelineGraphBuilder:
    """
    Class for extracting particular elements from OBM output json with pipeline description.

    Parameters
    ----------
    pipeline_json: dict, required
        Dictionary with loaded obm.json file.
    """
    def __init__(self, pipeline_json: dict) -> None:
        self.pipeline_json = pipeline_json
        self.last_non_join_iteration = self.get_last_non_join_iteration()
        self.selection_iteration = self.get_selection_iteration()
        self.join_iterations = self.get_join_iterations()
        self.graph_json = {'nodes': [], 'edges': defaultdict(set)}
        self.graph = Digraph(comment='Data Preprocessing Steps Graph',
                             node_attr={'color': 'lightblue2', 'style': 'filled'})

    @staticmethod
    def get_step_details(msg_json) -> Tuple[str, int, str]:
        """
        Getting particular step name, iteration number and step description.
        """
        name = msg_json['feature_engineering_components']['obm'][0]['step_name'].split(':')[1]
        iteration = msg_json['feature_engineering_components']['obm'][0]['iteration']
        text = msg_json['message']['text']
        return name, iteration, text

    def get_step_types(self) -> List[str]:
        """For all steps return their types."""
        return [message['feature_engineering_components']['obm'][0]['step_type'] for message in self.pipeline_json]

    def get_last_non_join_iteration(self) -> int:
        """Returns a number of the last step before join."""
        return self.get_step_types().index('join')

    def get_selection_iteration(self) -> int:
        """Returns feature selection step number."""
        return self.get_step_types().index('feature selection') + 1

    def get_join_iterations(self) -> List[int]:
        """Returns list of join step numbers."""
        steps_types = [message['feature_engineering_components']['obm'][0]['step_type'] for message in self.pipeline_json]
        return [i + 1 for i, x in enumerate(steps_types) if x == "join"]

    @staticmethod
    def get_join_extractors(msg_json: dict) -> Union[dict, None]:
        """Returns extractors if exist."""
        return msg_json['feature_engineering_components']['obm'][0].get('extractors')

    @staticmethod
    def get_extractor_columns(extractor_json: dict) -> List[str]:
        """Returns all columns names from particular extractor."""
        return extractor_json['columns']

    @staticmethod
    def get_extractor_transformations(extractor_json: dict) -> Dict[str, str]:
        """Returns a dictionary with all transformations names."""
        return extractor_json['transformations']

    def build_extractors_subgraph(self, msg_json: dict, join_iteration: int) -> None:
        """Creates sub-graph for extractors representation."""
        extractors = self.get_join_extractors(msg_json)
        join_iteration = str(join_iteration)

        if extractors is not None:
            for ext, i in zip(extractors, range(len(extractors))):
                self.graph.attr('node', color='lightgray')
                ext_index = join_iteration + str(i)

                self.graph.node(ext_index, ext)
                self.graph.edge(join_iteration, ext_index)
                self.graph_json['nodes'].append(ext_index)
                self.graph_json['edges'][join_iteration].add(ext_index)

                columns = self.get_extractor_columns(extractors[ext])
                transformations = self.get_extractor_transformations(extractors[ext])

                for j, column in enumerate(columns):
                    self.graph.attr('node', color='lightgreen')
                    col_index = join_iteration + str(i) + str(j)

                    self.graph.node(col_index, column)
                    self.graph.edge(ext_index, col_index)
                    self.graph_json['nodes'].append(col_index)
                    self.graph_json['edges'][ext_index].add(col_index)

                    self.graph.attr('node', color='lightblue2')
                    for transformation in transformations:
                        self.graph.edge(col_index, transformation)
                        self.graph.edge(transformation, str(self.selection_iteration))
                        self.graph_json['edges'][col_index].add(transformation)
                        self.graph_json['edges'][transformation].add(str(self.selection_iteration))

    def build_graph(self) -> Tuple[dict, 'Digraph']:
        """Creates a graphviz Digraph with pipeline representation."""
        for msg in self.pipeline_json:
            name, iteration, text = self.get_step_details(msg)
            self.graph.node(str(iteration), name, tooltip=text)
            self.graph_json['nodes'].append(str(iteration))

            if 1 < iteration <= self.last_non_join_iteration:
                self.graph.edge(str(iteration - 1), str(iteration))
                self.graph_json['edges'][str(iteration - 1)].add(str(iteration))
            elif iteration in self.join_iterations:
                self.graph.edge(str(self.last_non_join_iteration), str(iteration))
                self.graph_json['edges'][str(self.last_non_join_iteration)].add(str(iteration))
                self.build_extractors_subgraph(msg, iteration)
            elif iteration > self.selection_iteration:
                self.graph.edge(str(iteration - 1), str(iteration))
                self.graph_json['edges'][str(iteration - 1)].add(str(iteration))

        return self.graph_json, self.graph
