#
#    (C) Quantum Computing Inc., 2020.
#
#    THIS IS UNPUBLISHED PROPRIETARY SOURCE CODE of the Copyright Holder. 
#    The contents of this file may not be disclosed to third parties, copied 
#    or duplicated in any form, in whole or in part, without the prior written
#    permission of the Copyright Holder.
#
from typing import Union, Optional
import networkx as nx
from scipy.sparse import spmatrix
import numpy as np

from .client import ClientService, get_client_kwargs
from .result import GraphResult
from .data_processing import GraphAlgorithms


__all__ = ['minimum_clique_cover', 'community_detection', 'partition']


class QGraphClient(ClientService):

    def __init__(self,
                 username: str = None,
                 password: str = None,
                 access_token: str = None,
                 url: str = 'https://api.qci-prod.com',
                 configuration: str = 'default',
                 conf_path: str = None,
                 sampler: str = 'csample',
                 braket_url: Optional[str] = None):
        """

        :param username: str
        :param password: str
        :param access_token: str
        :param url: str
        :param sampler: str, string representation of the ampler to invoke. Default = 'csample'.
        """
        super().__init__(username, password, access_token, sampler, configuration, conf_path, url, braket_url)

    def solve_graph_problem(self,
                            G: Union[nx.Graph, np.ndarray, spmatrix],
                            graph_algo: str,
                            **kwargs):
        """
        This function is typically invoked through one of the higher-level interfaces defined below.

        :param G: NetworkX Graph, np.ndarray or  sp.spmatrix.
        :param graph_algo: str, name of graph algorithm.
        :param kwargs: dict, keyword args for the specific algorithm. Eg.,
            k, alpha, beta
        :return: GraphResult
        """
        if isinstance(G, nx.Graph) and not \
            (graph_algo == GraphAlgorithms.COMMUNITY_DETECTION.value or
             graph_algo == GraphAlgorithms.BIPARTITE_COMMUNITY_DETECTION.value):
            G = nx.to_scipy_sparse_matrix(G, nodelist=sorted(set(G.nodes())), dtype=np.float).tocoo()
        # if isinstance(G, nx.Graph) and not kwargs.get('bipartite', False):
        #     G = nx.to_scipy_sparse_matrix(G, nodelist=sorted(set(G.nodes())), dtype=np.float).tocoo()
        metadata = self.process_metadata('graph', G)
        params_elements = {'graph_algo': graph_algo}
        params_elements.update(kwargs)
        params = self.process_params(params_elements)
        data_obj = self.process_data(G)
        message = {'data_obj': (self.DATA_OBJ_FNAME, data_obj, 'application/octet-stream'),
                   'metadata': (self.METADATA_FNAME, metadata, 'text/plain'),
                   'params': (self.PARAMS_NAME, params, 'text/plain')}
        res = self.sendRequest(message)
        return GraphResult.from_dict_response(res)

    def minimum_clique_cover(self,
                             G: Union[nx.Graph, np.ndarray, spmatrix],
                             chromatic_lb: int = None,
                             chromatic_ub: int = None,
                             **kwargs):
        """
        Partition vertices in an undirected graph into a cover of cliques.

        :param G: NetworkX Graph, np.ndarray or  sp.spmatrix. Undirected, with possible edge weights.
        :param chromatic_lb: int, optional. A lower bound on the chromatic number.
        :param chromatic_ub: int, optional. A upper bound on the chromatic number.
        :param kwargs: Parameters to pass to the algorithm and solver.
            Clique Cover takes 'alpha', a Lagrange multiplier.
            For sampler parameters, see documentation in the sampler module.
        :return: GraphResult
        """
        graph_algo = GraphAlgorithms.CLIQUE_COVER.value
        kwargs.update({'chromatic_lb': chromatic_lb})
        kwargs.update({'chromatic_ub': chromatic_ub})
        return self.solve_graph_problem(G, graph_algo, **kwargs)

    def community_detection(self,
                            G: Union[nx.Graph, np.ndarray, spmatrix],
                            k: int = 2,
                            bipartite: bool = False,
                            **kwargs):
        """
        Partition a graph into k disjoint community of nodes, using community detection.

        :param G: NetworkX Graph, np.ndarray or  sp.spmatrix. Undirected, with possible edge weights.
        :param k: int, number of communities
        :param bipartite: bool, Invoke bipartite community detection algorithms on a bipartite graph.
            No effort is spent determining whether G is bipartite prior to sending posting the problem to the server.
        :param kwargs: Parameters to pass to the algorithm and solver.

            * *alpha*: float. The importance of constraining each node to a single community vs modularity.
                The problem formulation is :math:`B + \\alpha  C^t C`, where B is the n x n modularity matrix and
                C the constraint matrix.

            For sampler parameters, see documentation in the sampler module.
        :return: GraphResult
        """
        if bipartite:
            graph_algo = GraphAlgorithms.BIPARTITE_COMMUNITY_DETECTION.value
            assert isinstance(G, nx.Graph), \
                "Bipartite community detection requires a NetworkX Graph with labeled bipartite nodes." \
                "See https://networkx.org/documentation/stable/reference/algorithms/bipartite.html."
        else:
            graph_algo = GraphAlgorithms.COMMUNITY_DETECTION.value
        kwargs.update({'k': k, 'bipartite': bipartite})
        return self.solve_graph_problem(G, graph_algo, **kwargs)

    def partition(self,
                  G: Union[nx.Graph, np.ndarray, spmatrix],
                  k: int = 2,
                  **kwargs):
        """
        Partition a graph into k disjoint collections of nodes.

        :param G: NetworkX Graph, np.ndarray or  sp.spmatrix. Undirected, with possible edge weights.
        :param k: int, number of partitions, default = 2.
        :param kwargs: Parameters to pass to the algorithm and solver.
            Partition takes 'alpha' and 'beta', the importance of minimizing edge cuts and
            the importance of a balanced partition, respectively.
            For sampler parameters, see documentation in the sampler module.
        :return: GraphResult
        """
        graph_algo = GraphAlgorithms.PARTITION.value
        kwargs.update({'k': k})
        return self.solve_graph_problem(G, graph_algo, **kwargs)


####################################################
# Functional calls to graph algorithms
#
def minimum_clique_cover(G: Union[nx.Graph, np.ndarray, spmatrix],
                         chromatic_lb: int = None,
                         chromatic_ub: int = None,
                         **kwargs) -> GraphResult:
    """
    Partition vertices in a graph into a clique cover with minimum cardinality.

    :param G: NetworkX Graph, np.ndarray or  sp.spmatrix. Undirected, with possible edge weights. Requirement: For NetworkX Graph, integer nodes (0-based indexing) required (i.e. - For 3-nodes graph, G.nodes = NodeView((0, 1, 2)))
    :param chromatic_lb: int, optional, default = None. A lower bound on the chromatic number.
    :param chromatic_ub: int, optional, default = None. A upper bound on the chromatic number.
    If *chromatic_up* is None, then it is estimated from

        :math:`\\min \\left( \\lambda_{\\text{max}}(A), \\left\\lceil {1 + \\sqrt{1+ 8|E|}}\\right\\rceil / 2 \\right)`,

    where :math:`A` is the adjacency matrix of :math:`G`, and :math:`\\lambda_{\\text{max}}` indicates the maximum eigenvalue.

    Similarly, if *chromatic_lb* is None, it will be computed as the *clique covering number*, see `Clique covering number <https://mathworld.wolfram.com/CliqueCoveringNumber.html>`_.

    :param kwargs: dict, Parameters and arguments for the sampler and solver algorithm.

        * *alpha* float, default = 1.0
            A factor controlling the importance of the orthogonality of the cliques to each other (see [DA]_ Alg 15).
            Empirical guidance on good values for *alpha* is being explored.
        * *access_token* str, None
            Retrieved from .qci.conf file unless provided.
        * *conf_path* str, None
            Path to .qci.conf file on local system. Defaults to `~/.qci.conf` on Linux/Mac.
        * *configuration* str, default = 'default'
            Specific configuration to use, defined in .qci.conf.
        * *url* str, default = https://api.qci-prod.com
            Url for Qatalyst web-service
        * *sampler* str, default= 'csample'
            Available classical and quantum samplers are obtainable through `utils.print_available_samplers`.
            List of available samplers: `braket_rigetti`, `braket_ionq`, `braket_dwave`, `braket_simulator`, `csample`.
                Braket's simulator comes in two flavors: SV1 (state vector simulator) and TN1 (based on tensor networks),
                the former is a general purpose quantum circuit simulator, while TN1 is only suitable for certain
                types of quantum circuits (see Braket documentation for further information).
                `braket_simulator` calls SV1 while `braket_simulator_tn1` calls TN1.
        * *optimizer* str
            We utilize algorithms found in `scipy.minimize` and additional stochastic version of such optimizers.
            If sampler is of hybrid type, defaults to 'cobyla', otherwise defaults to None.
        * *optimizer_params* dict = None
            A dictionary of options to pass to the optimizer. Default will be set in the backend if argument is None.
            Example: ` options = {'disp': False, 'maxiter': 100}`.
            If sampler is of hybrid type, defaults to {'maxiter': 5}, otherwise defaults to None.
        * *algorithm* str
            Variational algorithm to run with a hybrid 'sampler' and classical 'optimizer'. Both QAOA and VQE are
            implemented (see [FGG]_, [PM]_, [MR]_). Select with 'qaoa' or 'vqe'. Defaults to 'qaoa' when sampler is of
            hybrid type.
        * *num_shots* int
            Number of samples taken per iteration on gate-based QPU samplers.

    :return: :meth:`qatalyst.result.GraphResult`

        * *samples* list(dict)
            List of clique covers per sample
        * *energies* list
            List of QUBO energies per sample
        * *counts* list
            List of measured frequencies per sample

    :Example:

    >>> import networkx as nx
    >>> from qatalyst import qgraph as qg
    >>> num_nodes = 30
    >>> alpha = 2
    >>> G = nx.random_geometric_graph(n=num_nodes, radius=0.4, dim=2, seed=518)
    >>> res = qg.minimum_clique_cover(G, alpha=alpha, num_solutions=5)

    In addition to the classical sampler, various quantum backends are also available. For instance, setting :code:`sampler='braket_dwave'`, will construct a QUBO from the graph problem and sample the problem on D-Wave System's 2000Q processor to obtain the result in :code:`res`.

    >>> import networkx as nx
    >>> from qatalyst import qgraph as qg
    >>> G = nx.barbell_graph(3,2)
    >>> alpha = 2
    >>> res = qg.minimum_clique_cover(G, alpha=alpha, num_solutions=5, sampler='braket_dwave')

    Alternatively, a variational algorithm can be used to to sample the resultant QUBO, as detailed in the code snippet that follows:

    >>> import networkx as nx
    >>> from qatalyst import qgraph as qg
    >>> G = nx.barbell_graph(3,2)
    >>> alpha = 2
    >>> res = qg.minimum_clique_cover(G, alpha=alpha, num_solutions=5, sampler='braket_rigetti', algorithm='qaoa', optimizer='cobyla', num_shots=10, optimizer_params={'maxiter': 5})

    See :ref:`Quantum Algorithms and Devices` for more details on QPU options and available parameters.
    """
    client_kwargs, param_kwargs = get_client_kwargs(**kwargs)
    client = QGraphClient(**client_kwargs)
    return client.minimum_clique_cover(G, chromatic_lb=chromatic_lb, chromatic_ub=chromatic_ub, **param_kwargs)


def community_detection(G: Union[nx.Graph, np.ndarray, spmatrix],
                        k: int = 2,
                        bipartite: bool = False,
                        **kwargs) -> GraphResult:
    """
    Partition a graph into :math:`k` disjoint communities of nodes, maximizing modularity.

    :param G: NetworkX Graph, np.ndarray or  sp.spmatrix. Undirected, with possible edge weights.
        Requirement: For NetworkX Graph, integer nodes (0-based indexing) required
        (i.e. - For 3-nodes graph, G.nodes = NodeView((0, 1, 2)))
    :param k: int, number of communities, default = 2.
    :param bipartite: bool. Invoke bipartite community detection algorithms on a bipartite graph.
            No effort is spent determining whether G is bipartite prior to sending posting the
            problem to the server. If True, input must be a NetworkX Graph with nodes labeled with keyword 'bipartite'.
    :param kwargs: dict, Parameters and arguments for the sampler and solver algorithm.

        * *alpha* float, default=1
            The importance of constraining each node to a single community vs. modularity.
            The problem formulation is :math:`\min_{x} x^t (-B + \\alpha  C^t C)x`, where :math:`B` is the
            :math:`n \\times n` modularity matrix and :math:`C` the constraint matrix enforcing that each node is assigned
            to a single community.
            For more details, see https://arxiv.org/abs/1901.09756.
        * *access_token* str, None
            Retrieved from .qci.conf file unless provided.
        * *conf_path* str, None
            Path to .qci.conf file on local system. Defaults to `~/.qci.conf` on Linux/Mac.
        * *configuration* str, default = 'default'
            Specific configuration to use, defined in .qci.conf.
        * *url* str, default = https://api.qci-prod.com
            Url for Qatalyst web-service
        * *alpha* float, default = 1.0
            A factor controlling the importance of constraining each node to a single community, in trade for the
            importance of modularity.
        * *sampler* str, default = 'csample'
            Available classical and quantum samplers are obtainable through `utils.print_available_samplers`.
            List of available samplers: `braket_rigetti`, `braket_ionq`, `braket_dwave`, `braket_simulator`, `csample`.
                Braket's simulator comes in two flavors: SV1 (state vector simulator) and TN1 (based on tensor networks),
                the former is a general purpose quantum circuit simulator, while TN1 is only suitable for certain
                types of quantum circuits (see Braket documentation for further information).
                `braket_simulator` calls SV1 while `braket_simulator_tn1` calls TN1.
        * *optimizer* str
            We utilize algorithms found in `scipy.minimize` and additional stochastic version of such optimizers.
            If sampler is of hybrid type, defaults to 'cobyla', otherwise defaults to None.
        * *optimizer_params* dict = None
            A dictionary of options to pass to the optimizer. Default will be set in the backend if argument is None.
            Example: `options = {'disp': False, 'maxiter': 100}`.
            If sampler is of hybrid type, defaults to `{'maxiter': 5}`, otherwise defaults to None.
        * *algorithm* str
            Variational algorithm to run with a hybrid 'sampler' and classical 'optimizer'. Both QAOA and VQE are
            implemented (see [FGG]_, [PM]_, [MR]_). Select with 'qaoa' or 'vqe'. Defaults to 'qaoa' when sampler is of
            hybrid type.
        * *num_shots* int
            Number of samples taken per iteration on gate-based QPU samplers.

    :return: :meth:`qatalyst.result.GraphResult`

        * *samples* list(dict)
            List of community mappings per sample
        * *energies* list
            List of QUBO energies, plus offsets, per sample
        * *counts* list
            List of measured frequencies per sample
        * *properties* dict
            * *community_mappings* list
                List of community mappings per sample
            * *modularities* list
                List of the modularities, relative to each sample in `samples`.

    :Example:

    >>> import networkx as nx
    >>> from qatalyst import qgraph as qg
    >>> num_nodes = 30
    >>> alpha = 2
    >>> G = nx.random_geometric_graph(n=num_nodes, radius=0.4, dim=2, seed=518)
    >>> k = 3
    >>> res = qg.community_detection(G, k=k, alpha=alpha, num_solutions=5)

    In addition to the classical sampler, various quantum backends are also available. For instance, setting :code:`sampler='braket_dwave'`, will construct a QUBO from the graph problem and sample the problem on D-Wave System's 2000Q processor to obtain the result in :code:`res`.

    >>> import networkx as nx
    >>> from qatalyst import qgraph as qg
    >>> G = nx.barbell_graph(3,2)
    >>> alpha = 3
    >>> k = 2
    >>> res = qg.community_detection(G, k=k, alpha=alpha, num_solutions=5, sampler='braket_dwave')

    Alternatively, a variational algorithm can be used to to sample the resultant QUBO,
    as detailed in the code snippet that follows. Note: For :math:`N` nodes, the algorithm sets up a QUBO of
    size :math:`N` when :math:`k = 2`, and size :math:`kN` when :math:`k > 2`. For the barbell graph of size 10 below, and
    :math:`k=3`, this yields 30 qubits.

    >>> import networkx as nx
    >>> from qatalyst import qgraph as qg
    >>> G = nx.barbell_graph(3,2)
    >>> alpha = 3
    >>> k = 2
    >>> # change sampler to 'braket_rigetti' to run on Rigetti's Aspen-8 QPU, or 'braket_ionq' to run on IonQ's device.
    >>> res = qg.community_detection(G, k=k, alpha=alpha, sampler='braket_rigetti', algorithm='qaoa',
    >>>                               optimizer='cobyla', num_shots=10, optimizer_params={'maxiter': 5})

    Bipartite graph are often a more natural fit for real-world data. For instance, coauthorship networks are linked by
    articles written, which expand naturally to a bipartite network composed of 'author' and 'article' nodes. Below is
    an example using the classic *Davis Southern Women* network, run on *csample*. In this example, the nodes in the
    Davis Southern Women graph are labeled by with key 'bipartite' which takes a value of either 0 or 1.

    >>> import networkx as nx
    >>> from qatalyst import qgraph as qg
    >>> G = nx.social.davis_southern_women_graph()
    >>> k = 3
    >>> res = qg.community_detection(G, k=k, bipartite=True)

    See :ref:`Quantum Algorithms and Devices` for more details on QPU options and available parameters.
    """
    client_kwargs, param_kwargs = get_client_kwargs(**kwargs)
    client = QGraphClient(**client_kwargs)
    return client.community_detection(G, k=k, bipartite=bipartite, **param_kwargs)


def partition(G: Union[nx.Graph, np.ndarray, spmatrix],
              k: int = 2,
              **kwargs) -> GraphResult:
    """
    Partitions a graph into k disjoint collections of nodes, minimizing the number of inter-partition edges. For the QUBO formulation of the graph partition, refer to  `arXiv preprint arXiv:1705.03082`.

    Note: It is possible that no valid solution exist for a given choice of `alpha` and `beta`, in which case the GraphResult object will contain empty attributes. The user is advised to modify `alpha` and `beta` to enforce balance and cut size, respectively.

    :param G: NetworkX Graph, np.ndarray or  sp.spmatrix. Undirected, with possible edge weights. Requirement: For NetworkX Graph, integer nodes (0-based indexing) required (i.e. - For 3-nodes graph, G.nodes = NodeView((0, 1, 2)))
    :param k: int, number of partitions, default = 2.
    :param kwargs: dict, Parameters and arguments for the sampler and solver algorithm.

        * *alpha* float, default = 1.0
            A factor controlling the importance of a balanced partition.
        * *beta* float, default = 1.0
            A factor controlling the importance of minimizing edge cuts over the balance criterion.
        * *access_token* str, None
            Retrieved from .qci.conf file unless provided.
        * *conf_path* str, None
            Path to .qci.conf file on local system. Defaults to `~/.qci.conf` on Linux/Mac.
        * *configuration* str, default = 'default'
            Specific configuration to use, defined in .qci.conf.
        * *url* str, default = https://api.qci-prod.com
            Url for Qatalyst web-service
        * *sampler* str, default= 'csample'
            Available classical and quantum samplers are obtainable through `utils.print_available_samplers`.
            List of available samplers: `braket_rigetti`, `braket_ionq`, `braket_dwave`, `braket_simulator`, `csample`.
                Braket's simulator comes in two flavors: SV1 (state vector simulator) and TN1 (based on tensor networks),
                the former is a general purpose quantum circuit simulator, while TN1 is only suitable for certain
                types of quantum circuits (see Braket documentation for further information).
                `braket_simulator` calls SV1 while `braket_simulator_tn1` calls TN1.
        * *optimizer* str
            We utilize algorithms found in `scipy.minimize` and additional stochastic version of such optimizers. If sampler is of hybrid type, defaults to 'cobyla', otherwise defaults to None.
        * *optimizer_params* dict = None
            A dictionary of options to pass to the optimizer. Default will be set in the backend if argument is None.
            Example: ` options = {'disp': False, 'maxiter': 100}`.
            If sampler is of hybrid type, defaults to `{'maxiter': 5}`, otherwise defaults to None.
        * *algorithm* str
            Variational algorithm to run with a hybrid 'sampler' and classical 'optimizer'. Both QAOA and VQE are implemented (see [FGG]_, [PM]_, [MR]_). Select with 'qaoa' or 'vqe'. Defaults to 'qaoa' when sampler is of hybrid type.
        * *num_shots* int
            Number of samples taken per iteration on gate-based QPU samplers.

    :return: :meth:`qatalyst.result.GraphResult`

        * *samples* list(dict)
            List of partition mappings per valid sample
        * *energies* list
            List of QUBO energies per valid sample
        * *counts* list
            List of measured frequencies per valid sample
        * *properties* dict
            * *weighted_cut_sizes* list
                List of weighted cut sizes per valid sample. A cut size of 0.0 indicates all nodes are in a single partition. This is still considered a valid solution.
            * *balances* list
                List of partition balances per valid sample

    :Example:

    >>> import networkx as nx
    >>> from qatalyst import qgraph as qg
    >>> num_nodes = 30
    >>> alpha = 2
    >>> G = nx.random_geometric_graph(n=num_nodes, radius=0.4, dim=2, seed=518)
    >>> k = 3
    >>> res = qg.partition(G, k=k, alpha=alpha, num_solutions=5)

    In addition to the classical sampler, various quantum backends are also available. For instance, setting :code:`sampler='braket_dwave'`, will construct a QUBO from the graph problem and sample the problem on D-Wave System's 2000Q processor to obtain the result in :code:`res`.

    >>> import networkx as nx
    >>> from qatalyst import qgraph as qg
    >>> G = nx.barbell_graph(3,2)
    >>> alpha = 3
    >>> k = 2
    >>> res = qg.partition(G, k=k, alpha=alpha, num_solutions=5, sampler='braket_dwave')

    Alternatively, a variational algorithm can be used to to sample the resultant QUBO, as detailed in the code snippet that follows:

    >>> import networkx as nx
    >>> from qatalyst import qgraph as qg
    >>> G = nx.barbell_graph(3,2)
    >>> alpha = 3
    >>> k = 2
    >>> res = qg.partition(G, k=k, alpha=alpha, num_solutions=5, sampler='braket_rigetti', algorithm='qaoa', optimizer='cobyla', num_shots=10, optimizer_params={'maxiter': 5})

    See :ref:`Quantum Algorithms and Devices` for more details on QPU options and available parameters.
    """
    client_kwargs, param_kwargs = get_client_kwargs(**kwargs)
    client = QGraphClient(**client_kwargs)
    return client.partition(G, k=k, **param_kwargs)
