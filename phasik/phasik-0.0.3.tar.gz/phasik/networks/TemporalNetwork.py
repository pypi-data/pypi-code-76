import numpy as np
import pandas as pd
import teneto
import copy
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sb
from matplotlib import animation
from matplotlib.lines import Line2D

from networkx.drawing.nx_agraph import graphviz_layout
from phasik.utils.graphs import standard_node_params

class TemporalNetwork:
    """
    A wrapper class around teneto's TemporalNetwork class

    The main reason for doing this is that teneto requires that the time points in the temporal network start at zero.
    Since it is often more useful to use the actual time points from the underlying dataset, we create a wrapper class,
    exposing/adding a few other methods/properties too.
    """

    def __init__(self, teneto_network, time_shift=0, node_ids_to_names=None, temporal_edges=None):
        """
        Parameters
        ----------
        teneto_network : teneto.TemporalNetwork
            A temporal network
        time_shift : float
            How much we've shifted the data's time points by in order to start at zero
        node_ids_to_names : dict
            Dictionary mapping node IDS (integers) to more descriptive names (str) for nodes.
        """

        self.teneto_network = teneto_network
        self.time_shift = time_shift
        self.node_ids_to_names = node_ids_to_names
        self.temporal_edges = temporal_edges
        
        if self.temporal_edges!=None:
            self.temporal_nodes = np.unique(self.temporal_edges).tolist()
        else: 
            self.temporal_nodes = None

        # Keep track of the 'true' times, even though we've shifted to start at 0
        if teneto_network.sparse:
            self.times = np.array(sorted(set(self.teneto_network.network['t'])))
        else:
            self.times = np.array(range(teneto_network.T))
        self.true_times = self.times + time_shift


    def T(self):
        """Returns the number of time points in the temporal network"""

        # tried 
        #return len(self.true_times) 
        # to deal with timesteps different from 1, but yields inconsistencies because we use many teneto functions such as to_df()
        # the teneto definition for times=[0, 10, 20, 30] would yield T=31, we want 4

        return self.teneto_network.T
        
    def info(self):
        """Return summary information about the temporal network"""
        
        T = self.T()
        N = self.teneto_network.N
        G = self.get_aggregated_network()
        n_edges = len(G.edges)
        n_temporal_edges = len(self.temporal_edges)
        
        message = f"{N} nodes, {n_edges} edges (of which {n_temporal_edges} temporal), over {T} time points."
        return message
        
    def get_snapshots(self, t_ax=0):
        """Returns the representation of the network as a sequence of adjacency matrices, one for each time point"""

        array = self.teneto_network.df_to_array() if self.sparse() else self.teneto_network.network
        # Make 'time' the 0th axis
        if t_ax==0:
            snapshots = np.swapaxes(array, 0, 2)
        elif t_ax==2:
            snapshots = array
        else:
            print("ERROR: wrong axis for time, must be 0 or 2")
        return snapshots
    
    def get_df_tedges(self, add_labels=False, sort_by=None):
        """Return the representation of the network as a pandas.DataFrame of tedges, with columns ['i', 'j', 't', 'weight']"""
        
        # option addlabels exists due to not good handling of node labels in phasik and teneto
        if self.sparse:
            df_tedges = copy.deepcopy(self.teneto_network.network)
            # replace index labels by name labels
            if add_labels:
                df_tedges['i'] = df_tedges['i'].apply(lambda col: self.node_ids_to_names[col])
                df_tedges['j'] = df_tedges['j'].apply(lambda col: self.node_ids_to_names[col])
                
            if sort_by=='ij':
                df_tedges = df_tedges.sort_values(by=['i', 'j'])
            elif sort_by=='t':
                df_tedges = df_tedges.sort_values(by=['t'])
            else:
                pass
                
            return df_tedges
        else: 
#            print("ERROR: network is sparse and encoded as snapshots")
            df_tedges = snapshots2tedges(self.get_snapshots(t_ax=2))
            df_tedges = copy.deepcopy(copy.deepcopy)
            # replace index labels by name labels
            if add_labels:
                df_tedges['i'] = df_tedges['i'].apply(lambda col: self.node_ids_to_names[col])
                df_tedges['j'] = df_tedges['j'].apply(lambda col: self.node_ids_to_names[col])
                
            if sort_by=='ij':
                df_tedges = df_tedges.sort_values(by=['i', 'j'])
            elif sort_by=='t':
                df_tedges = df_tedges.sort_values(by=['t'])
            else:
                pass
                                
            return df_tedges
            

    def sparse(self):
        """Return True if teneto_network is of type 'sparse', False otherwise (see teneto documentation)"""
        return self.teneto_network.sparse

    def node_name(self, id):
        """
        Get descriptive node name

        Parameters
        ----------
        id : int 
            ID of the node

        Returns
        -------
        The more descriptive name for this node, defaulting to 'id' if no descriptive name exists.
        """

        if self.node_ids_to_names is None or id not in self.node_ids_to_names:
            return id
        else:
            return self.node_ids_to_names[id]

    def get_constant_edges(self): 
        """Return list of edges for which there is no temporal information"""
        all_static_edges = self.get_aggregated_network().edges()
        return set(all_static_edges).difference(self.temporal_edges)
    
    def get_temporal_edges(self, node=None):
        """Return dict with temporal nodes as keys, and a list of their temporal edges as values
        
        Parameters
        ----------
        node : int or str, optional
            Name of a node with temporal edges. If None, return dict for all temporal nodes
        
        Returns
        -------
        dict 
            
        """
        dict_ = {node : [edge for edge in self.temporal_edges if node in edge] for node in self.temporal_nodes}
        if node is None:
            return dict_
        else:
            return {node : dict_[node]}
            
    def get_temporal_connectivity(self, node=None):
        """Return dict with temporal nodes as keys, and the number of their temporal edges as values
        
        Parameters
        ----------
        node : int or str, optional
            Name of a node with temporal edges. If None, return dict for all temporal nodes
        
        Returns
        -------
        dict 
            
        """
        temporal_edges_dict = self.get_temporal_edges(node)
        
        return {node : len(edges) for node, edges in temporal_edges_dict.items()}
        
    def get_aggregated_network(self, type_='weighted', t_in=None, t_fi=None, averaged=True) :
        """Return aggregated network as a networkx Graph
        
        Parameters
        ----------
        type_ : {'weighted', 'normalised', binary'}, optional
            Type of aggregation, defaults to "weighted" 
        t_in : int, optional
            Initial time index at which to start the aggregation (included). Defaults to 0.
        t_fi : int, optional
            Final time index at which to end the aggregation (excluded). Defaults to T.
                      
        Returns
        -------
        networkx.Graph
        """
        
        snapshots = self.get_snapshots()
        T = len(snapshots)
        if t_in==None:
            t_in = 0
        if t_fi==None:
            t_fi = T
        n_t = t_fi - t_in
            
        # aggregate over defined time window
        aggregated_adj = snapshots[t_in:t_fi].sum(axis=0) # aggregate ajdancency matrices
        
        if type_=='weighted':
            if averaged: # divide by number of timepoints in timewindow
                aggregated_adj /= n_t 
        elif type_=='binary': # unweighted, weights can only be 0 or 1
            tol = 1e-3
            aggregated_adj[aggregated_adj>tol] = 1 # set to 1 any non-zero weight
        elif type_=='normalised': # all weights between 0 and 1
            aggregated_adj /= np.max(aggregated_adj) 

        aggregated_network = nx.Graph(aggregated_adj)
        aggregated_network = nx.relabel_nodes(aggregated_network, self.node_ids_to_names) # replace node numbers by labels
        return aggregated_network
        
    def get_network_at_time(self, i, type_='weighted') :
        """Return network at i-th timepoint as a networkx Graph
        
        Parameters
        ----------
        type_ : {'weighted', binary'}, optional
            Type of network weights, defaults to "weighted" 
            
        Returns
        -------
        networkx.Graph
        """
        
        snapshot_adj = self.get_snapshots()[i]
        if type_=='weighted':
            pass
        elif type_=='binary': # unweighted, weights can only be 0 or 1
            tol = 1e-3
            snapshot_adj[snapshot_adj>tol] = 1 # set to 1 any non-zero weight
    
        snapshot_network = nx.Graph(snapshot_adj)
        snapshot_network = nx.relabel_nodes(snapshot_network, self.node_ids_to_names) # replace node numbers by labels
        return snapshot_network 
        
    def is_edge(self, node_i, node_j):
        """Return True if (node_i, node_j) is an edge of the TemporalNetwork, False otherwise
        node_i and node_i can be nodes indices (e.g. 0) or node names ('APC')."""
        
        i, j, by_label = convert_input_to_indices(node_i, node_j, self)
        
        df_tedges = self.get_df_tedges()
        df_edges = df_tedges.drop_duplicates(['i', 'j'])[['i', 'j']]
        return [i,j] in df_edges.to_numpy().tolist()
        
    def is_temporal_edge(self, node_i, node_j):
        """Return True if (node_i, node_j) is an edge of the TemporalNetwork, with temporal information, False otherwise
        node_i and node_i can be nodes indices (e.g. 0) or node names ('APC')."""
        
        i, j, by_label = convert_input_to_indices(node_i, node_j, self)
        
        if not is_edge(node_i, node_j): 
            return False
        else: 
            if self.temporal_edges is None :
                print("No list of temporal edges available")
                return None
            else: 
                if edge in self.temporal_edges:
                    return True
                else: 
                    print(f'INFO: {edge} is a static edge of the network, but no temporal information is available for it')
                    return False
            
    def select_tedges(self, node_i, node_j):
        """Return DataFrame with tedges, corresponding to edge (node_i, node_j)"""
        i, j, by_label = convert_input_to_indices(node_i, node_j, self)
        
        if self.is_edge(node_i, node_j):
            # filter DataFrame
            df_tedges = self.get_df_tedges()
            return (df_tedges['i'] == i) & (df_tedges['j'] == j)
        else: 
            print(f"WARNING: ({node_i},{node_j}) is not an edge in the temporal network")
            
    def select_tedges_of_node(self, node_i):
        """Return DataFrame with all tedges including node_i"""
        i, _, by_label = convert_input_to_indices(node_i, node_i, self)
        
        #todo: add check if node exists
        df_tedges = self.get_df_tedges()
        return (df_tedges['i'] == i) | (df_tedges['j'] == i)
            
    # under construction
    def switch_off_edge(self, node_i, node_j, value=1, reverse=False):
        """Return new TemporalNetwork with weight of given static edge (i,j) set to constant value "value" """

        i, j, by_label = convert_input_to_indices(node_i, node_j, self)
        
        
        df_tedges = self.get_df_tedges(add_labels=True)
        tedges_to_switch_off = self.select_tedges(node_i, node_j)
        
        df_tedges_modified = df_tedges.copy(deep=True)
    
        if reverse: # switch off all links but the input one
            tedges_to_switch_off =  np.logical_not(tedges_to_switch_off)
            
        df_tedges_modified.loc[tedges_to_switch_off, 'weight'] = value
        
        # replace index labels by name labels (might be done earlier in the get_df_tedges, but check)
#        df_tedges_modified['i'] = df_tedges_modified['i'].apply(lambda col: self.node_ids_to_names[col])
#        df_tedges_modified['j'] = df_tedges_modified['j'].apply(lambda col: self.node_ids_to_names[col])
        
        print(f"Static edge {i,j}: {len(df_tedges[tedges_to_switch_off])} tedges set to constant value {value}")
        
        return TemporalNetwork.from_edge_list_dataframe(df_tedges_modified, normalise=None, threshold=0, binary=False)

    def switch_off_edges_of_node(self, node_i, value=1, reverse=False):
        """Return new TemporalNetwork with weight of all edges of node_i set to constant value "value" """

        i, _, by_label = convert_input_to_indices(node_i, node_i, self)
        
        df_tedges = self.get_df_tedges(add_labels=True)
        tedges_to_switch_off = self.select_tedges_of_node(node_i)
        
        df_tedges_modified = df_tedges.copy(deep=True)
    
        if reverse: # switch off all links but the input one
            tedges_to_switch_off =  np.logical_not(tedges_to_switch_off)
            
        df_tedges_modified.loc[tedges_to_switch_off, 'weight'] = value
        
        # replace index labels by name labels (might be done earlier in the get_df_tedges, but check)
#        df_tedges_modified['i'] = df_tedges_modified['i'].apply(lambda col: self.node_ids_to_names[col])
#        df_tedges_modified['j'] = df_tedges_modified['j'].apply(lambda col: self.node_ids_to_names[col])

        n_links_switchoff = len(df_tedges_modified[tedges_to_switch_off])
        
        print(f"Edges of node {node_i}: {n_links_switchoff // self.T()} edges across {self.T()} timepoints, set to constant value {value}")
        
        return TemporalNetwork.from_edge_list_dataframe(df_tedges_modified, normalise=None, threshold=0, binary=False)

    @classmethod
    def from_snapshots_numpy_array(_class, snapshots, node_ids_to_names=None):
        """
        Create a TemporalNetwork from snapshots

        Parameters
        ----------
        snapshots : ndarray, dim (T, N, N)
            Adjacency matrices corresponding to each timepoint
        node_ids_to_names : dict
            Dictionary mapping node IDs (integer) to more descrptive names for nodes (any type).
            
        Returns
        -------
        phasik.TemporalNetwork.TemporalNetwork
        """

        array = np.swapaxes(snapshots, 0, 2)
        return _class.from_numpy_array(array, node_ids_to_names)

    @classmethod
    def from_numpy_array(_class, array, node_ids_to_names=None):
        """
        Create a TemporalNetwork from an array representation of the network

        Parameters
        ----------
        array : ndarray, dim (N, N, T)
            Snapshot representation of a temporal network
        node_ids_to_names : dict
            Dictionary mapping node IDs (integer) to more descrptive names for nodes (any type).
            
        Returns
        -------
        phasik.TemporalNetwork.TemporalNetwork            
        """

        teneto_network = teneto.TemporalNetwork(from_array=array)
        return _class(teneto_network, node_ids_to_names=node_ids_to_names)

    @classmethod
    def from_edge_list_dataframe(_class, edges, normalise=None, threshold=0, binary=False, temporal_edges=None):
        """Create a TemporalNetwork from a DataFrame of edges over time

        Parameters
        ----------
        edges : pandas.DataFrame 
            With columns representing source node, target node, time and (optionally) weight
        normalise : {'local', 'global', None}, optional 
            Value determining what (if any) normalisation is applied (default None). If 'normalise' is 'global', all weights
            will be divided through by the max weight across all edges. If 'normalise' is 'local', all weights
            corresponding to an edge (i,j) at some time will be divided through by the max weight of the edge (i,j)
            across all times. To skip normalisation, set to None.
        threshold : float, optional 
            Any edges with weight < 'threshold' (after normalising) will not be included in the temporal network (default 0.0)
        binary : bool, optional
            If True, all positive weights (after thresholding) will be set to 1. If False, does nothing. (Default False)
        temporal_edges : list of str or int, optional 
            List of edges for which we have temporal information (default None)
            
        Returns
        -------
        phasik.TemporalNetwork.TemporalNetwork
        """

        number_of_columns = edges.shape[1]
        if number_of_columns == 3:
            edges['weight'] = 1
        elif number_of_columns != 4:
            raise ValueError('Edge list requires either 3 or 4 columns')
        edges.columns = ['i', 'j', 't', 'weight']

        if normalise == 'global':
            min_weight = edges['weight'].min()
            difference = edges['weight'].max() - min_weight
            edges['weight'] = (edges['weight'] - min_weight) / difference
        if normalise == 'local':
            # Sort first two columns; we only care about *unordered* pairs (i,j), not ordered pairs.
            edges[['i', 'j']] = np.sort(edges[['i', 'j']], axis=1)
            grouped = edges.groupby(['i', 'j'])['weight']
            maxes = grouped.transform('max')
            mins = grouped.transform('min')
            edges['weight'] = (edges['weight'] - mins) / (maxes - mins)
            # In cases where max = min we'll have a division by zero error.
            edges['weight'] = edges['weight'].fillna(0.5)
        edges = edges[edges['weight'] >= threshold]
        if binary:
            edges.loc[edges['weight'] > 0, 'weight'] = 1

        edges, ids_to_names = replace_nodes_with_ids(edges)
        edges = edges.sort_values('t')
        start_time = edges['t'].iloc[0]
        if start_time != 0:
            # For compatibility with teneto, shift all times so that we start at time 0
            edges['t'] -= start_time

        teneto_network = teneto.TemporalNetwork(from_df=edges)
        return _class(teneto_network, start_time, node_ids_to_names=ids_to_names, temporal_edges=temporal_edges)

    @classmethod
    def from_static_network_and_edge_list_dataframe(
            _class,
            static_network,
            edges,
            normalise=None,
            threshold=0,
            binary=False,
            static_edges_default=None):
        """Create a TemporalNetwork from a static network and a DataFrame of temporal edges

        Given a static network and a set of edges across different times, we can create a temporal network by including
        temporal edge (i,j,t) if edge the static network contains an edge (i,j).

        Parameters
        ----------
        static_network : networkx.Graph 
            Underlying static network
        edges :pandas.DataFrame 
            Rows of time-edges, with columns representing source node, target node, time and (optionally) weight
        normalise : {'local', 'global', None}, optional
            A value determining what (if any) normalisation is applied. If 'normalise' is 'global', all weights
            will be divided through by the max weight across all edges. If 'normalise' is 'local', all weights
            corresponding to an edge (i,j) at some time will be divided through by the max weight of the edge (i,j)
            across all times. To skip normalisation, set to None (default).
        threshold : float, optional
            Any edges with weight < 'threshold' (after normalising) will not be included in the temporal network (default 0.0)
        binary : bool, optional
            If True, all positive weights (after thresholding) will be set to 1. If False (default), does nothing.
        static_edges_default : int or None, optional 
            If there are edges in the static network that aren't present in 'edges' then
            'static_edges_default' determines what to do with these. If set to None (default), these static edges are simply
            ignored. If set to a numerical value k, these static edges are given weight k across all time points.
            
        Returns
        -------
        phasik.TemporalNetwork.TemporalNetwork
        """

        if len(edges.columns) == 3:
            edges['weight'] = 1
        elif len(edges.columns) != 4:
            raise ValueError('Edge list should have either 3 or 4 columns.')
        edges.columns = ['i', 'j', 't', 'weight']
        
        # Our fastest option throughout this method is to merge DataFrames. So begin by converting static network's
        # edges to a DataFrame.
        static_network_edges = pd.DataFrame(static_network.edges)
        static_network_edges.columns = ['static_i', 'static_j']

        # Sort the first two columns of each DataFrame so that edges are pairs (i, j) with i <= j. This allows
        # us to merge DataFrames together without regard for the direction of the edges (i.e. whether we have an
        # edge (i,j) or (j,i)).
        static_network_edges[['static_i', 'static_j']] = np.sort(static_network_edges[['static_i', 'static_j']], axis=1)
        edges[['i', 'j']] = np.sort(edges[['i', 'j']], axis=1)

        # Merge edges from static network into our temporal edge list.
        if static_edges_default is None:
            # We only want edges that appear in both the temporal edge list and the static network. We could do this
            # with an inner join, but we want to inform the user of edges in the temporal edge list that weren't
            # matched to any in the static network. So we use a left join initially.
            edges = edges.merge(static_network_edges, how='left', left_on=['i', 'j'], right_on=['static_i', 'static_j'])
        else:
            # We want edges that appear in both the temporal edge list and the static network, and we additionally
            # want to add constant temporal data for edges in the static network but not in the temporal edge list.
            edges = edges.merge(static_network_edges, how='outer', left_on=['i', 'j'], right_on=['static_i', 'static_j'])
            # Rows in the DataFrame with no value in column i are those from the static network that had no
            # corresponding edge in the temporal data.
            message = f'The following static edges have no temporal data and will have default weight ' \
                      f'{static_edges_default} across all time points'
            edges, static_missing_edges = remove_missing_edges(edges, 'i', ['static_i', 'static_j'], message)
                        
        message = 'The following edges were not found in the static network'
        edges, _ = remove_missing_edges(edges, 'static_i', ['i', 'j'], message)
        edges = edges[['i', 'j', 't', 'weight']]
        # At this point, "edges" contains tedges of static edges for which we have temporal information
        # We keep track of the names of those edges in the static network
        temporal_edges_names = edges[['i', 'j']].apply(tuple, axis=1).drop_duplicates().to_list()
        
        if static_edges_default is not None and not static_missing_edges.empty:
            # Add default weights across all timepoints for the static edges that have no temporal data.
            times = edges['t'].drop_duplicates().to_frame().assign(weight=static_edges_default)
            temporal_static_edges = static_missing_edges[['static_i', 'static_j']].assign(weight=static_edges_default)
            temporal_static_edges = temporal_static_edges.merge(times, on='weight')[['static_i', 'static_j', 't', 'weight']]
            temporal_static_edges.columns = ['i', 'j', 't', 'weight']
            edges = pd.concat([edges[['i', 'j', 't', 'weight']], temporal_static_edges], ignore_index=True)

        return _class.from_edge_list_dataframe(edges, normalise, threshold, binary, temporal_edges=temporal_edges_names)

    @classmethod
    def from_static_network_and_node_list_dataframe(
            _class,
            static_network,
            nodes,
            combine_node_weights=lambda x, y: x * y,
            normalise=None,
            threshold=0,
            binary=False,
            static_edges_default=None):
        """Create a TemporalNetwork from a static network and a DataFrame of temporal nodes

        Given a static network and a set of nodes across different times, we can create a temporal network by including
        temporal edge (i,j,t) if edge the static network contains an edge (i,j).

        Parameters
        ----------
        static_network : networkx.Graph 
           Underlying static network
        nodes : pandas.DataFrame
            Rows of values associated to node, with columns representing node, time and (optionally) weight
        combine_node_weights : lambda function, optional 
            A lambda determining how to combine two nodes' weights together to give the weight of
            the corresponding edge. NOTE: this is applied to whole columns at a time, for efficiency. Therefore any
            unvectorizable lambda functions will raise an exception.
        normalise : {'local', 'global', None}, optional 
            A value determining what (if any) normalisation is applied. If 'normalise' is 'global', all weights
            will be divided through by the max weight across all edges. If 'normalise' is 'local', all weights
            corresponding to an edge (i,j) at some time will be divided through by the max weight of the edge (i,j)
            across all times. To skip normalisation, set to None (default).
        threshold : float, optional 
            Any edges with weight < 'threshold' (after normalising) will not be included in the temporal network (default 0.0)
        binary : bool, optional 
            If True, all positive weights (after thresholding) will be set to 1. If False (default), does nothing.
        static_edges_default : float or None, optional 
            If there are edges in the static network that aren't present in 'edges' then
            'static_edges_default' determines what to do with these. If set to None (default), these static edges are simply
            ignored. If set to a numerical value k, these static edges are given weight k across all time points.
            
        Returns
        -------
        phasik.TemporalNetwork.TemporalNetwork    
        """

        if len(nodes.columns) == 2:
            nodes['weight'] = 1
        elif len(nodes.columns) != 3:
            raise ValueError('Node list must have either 2 or 3 columns.')
        nodes.columns = ['i', 't', 'weight']

        # Our fastest option throughout this method is to merge DataFrames. So begin by converting static network's
        # nodes to a DataFrame.
        static_network_nodes = pd.DataFrame(static_network.nodes)
        static_network_nodes.columns = ['static_i']
        nodes = nodes.merge(static_network_nodes, how='left', left_on='i', right_on='static_i')

        # Rows in the DataFrame with no value in static_i are exactly those that had no corresponding node in the
        # static network. So remove these edges, informing the user of this fact.
        missing_nodes_indices = nodes['static_i'].isnull()
        if missing_nodes_indices.any():
            missing_nodes = nodes[missing_nodes_indices]
            print(f'WARNING: The following {len(missing_nodes["i"].values)} nodes were not found in the static network:\n{missing_nodes["i"].values}')

        # Only keep nodes that are present in the static network
        nodes = nodes[~missing_nodes_indices][['i', 't', 'weight']]
        # Merge nodes with themselves to form temporal edge data
        edges = nodes.merge(nodes, left_on='t', right_on='t', suffixes=('_1', '_2'))
        # Remove duplicates and self-loops
        edges = edges[edges['i_1'] < edges['i_2']]
        # Add column for combined weight
        edges['r'] = combine_node_weights(edges['weight_1'], edges['weight_2'])
        edges = edges[['i_1', 'i_2', 't', 'r']]

        return _class.from_static_network_and_edge_list_dataframe(
            static_network, edges, normalise, threshold, binary, static_edges_default)

    @classmethod
    def from_static_network_and_node_table_dataframe(
            _class,
            static_network,
            node_table,
            combine_node_weights=lambda x, y: x * y,
            normalise=None,
            threshold=0,
            binary=False,
            static_edges_default=None):
        """Create a TemporalNetwork from a static network and a DataFrame of temporal nodes

        Given a static network and a set of nodes across different times, we can create a temporal network by including
        temporal edge (i,j,t) if edge the static network contains an edge (i,j).

        Parameters
        ----------
        static_network : networkx.Graph 
            Underlying static network
        node_table : pandas.DataFrame
            Time series of nodes, as columns. Columns represent the nodes of the graph, and rows
            contain the temporal data for those nodes. The DataFrame should be indexed by time points, which should
            be numeric values.
        combine_node_weights : lambda function, optinal
            A lambda determining how to combine two nodes' weights together to give the weight of
            the corresponding edge. NOTE: this is applied to whole columns at a time, for efficiency. Therefore any
            unvectorizable lambda functions will raise an exception.
        normalise : {'local', 'global', None}, optional  
            A value determining what (if any) normalisation is applied. If 'normalise' is 'global', all weights
            will be divided through by the max weight across all edges. If 'normalise' is 'local', all weights
            corresponding to an edge (i,j) at some time will be divided through by the max weight of the edge (i,j)
            across all times. To skip normalisation, set to None (default).
        threshold : float, optional 
            Any edges with weight < 'threshold' (after normalising) will not be included in the temporal network (default 0)
        binary : bool, optional 
            If True, all positive weights (after thresholding) will be set to 1. If False (default), does nothing.
        static_edges_default : float or None, optional 
            If there are edges in the static network that aren't present in 'edges' then
            'static_edges_default' determines what to do with these. If set to None (default), these static edges are simply
            ignored. If set to a numerical value k, these static edges are given weight k across all time points.
            
        Returns
        -------
        phasik.TemporalNetwork.TemporalNetwork            
        """

        def get_node_list(node_table, node):
            # Turn the column representing a particular node into a list of temporal edges.
            node_list = node_table[node].to_frame()
            node_list['i'] = node
            node_list['t'] = node_list.index
            node_list = node_list[['i', 't', node]]
            node_list.columns = ['i', 't', 'weight']
            return node_list

        # For each node in the table, create a list of temporal edges for that node, then concatenate all such lists
        # together to create the total edge list.
        node_lists = [get_node_list(node_table, node) for node in node_table.columns]
        node_list = pd.concat(node_lists, ignore_index=True)

        return _class.from_static_network_and_node_list_dataframe(
            static_network, node_list, combine_node_weights, normalise, threshold, binary, static_edges_default)
            
    #TODO complete documentation   
    @classmethod
    def from_static_network_and_edge_table_dataframe(
            _class,
            static_network,
            edge_table,
            normalise=None,
            threshold=0,
            binary=False,
            static_edges_default=None):
        """Create a TemporalNetwork from a static network and a DataFrame of temporal nodes
        """

        tedges = all_series2tedges(edge_table)
        
        return _class.from_static_network_and_edge_list_dataframe(
            static_network, tedges, 
            normalise, threshold, binary, static_edges_default)
            
    def animate_highlight_temporal(self, frames=None, filepath=None, fps=5) : 
        """Return animation of the temporal network evolving over time
        
        Parameters
        ----------
        frames : int
            Number of frames of the animation (should be at most the number of timepoints (default))
        filepath : str, optional
            Filepath to save the animation to. If None, the animation is not saved (default)

        Returns
        -------
        matplotlib.animation
        """
        
        if frames is None: 
            frames = self.T()        
                
        aggregated_network = self.get_aggregated_network("normalised")
        pos = graphviz_layout(aggregated_network, prog='neato')

        fig, ax = plt.subplots(figsize=(15, 12))

        def update_network(i) : 
            ax.clear()
            
            colour_constant = "silver"
            colour_active = "red"
            params = standard_node_params(colour_constant)
            params_active = standard_node_params(colour_active)
            width_scale = 1.5 # scale width of edges
            
            snapshot_network = self.get_network_at_time(i, type_="weighted")
            
            # unchanged elements
            nx.draw_networkx_nodes(aggregated_network, pos=pos, ax=ax, **params)
            nx.draw_networkx_labels(aggregated_network, pos=pos, ax=ax, **params)
        #     nx.draw_networkx_edges(snapshot_network, edgelist=temporal_network.temporal_edges, pos=pos, ax=ax, **params)
            nx.draw_networkx_edges(snapshot_network, edgelist=self.get_constant_edges(), width=width_scale, pos=pos, ax=ax, **params)

            # changing edges
            weights = np.array([w for u,v,w in snapshot_network.edges.data("weight") if (u,v) in self.temporal_edges])
            width_min =  0.4 # set minimum width for visualisation
            widths = np.maximum(weights * width_scale, width_min)
            nx.draw_networkx_edges(snapshot_network, edgelist=self.temporal_edges, width=widths, pos=pos, ax=ax, **params_active)
            
            ax.set_title(f"Time: {i} min")
            sb.despine(left=True, bottom=True)
            
            custom_lines = [Line2D([0], [0], color=colour_constant, lw=width_scale), 
                            Line2D([0], [0], color=colour_active, lw=width_scale)]

            ax.legend(custom_lines, ['Constant edges', 'Temporal eges'])
            
        ani = animation.FuncAnimation(fig, update_network, frames=frames, interval=20, blit=False)
        
        if filepath!=None: # save animation
            # saving the animation is often time and memory consuming, visualise first without saving 
            ani.save(filepath, fps=fps)
    
        return ani


def remove_missing_edges(edges, null_column, print_columns, message):
    """Removes unwanted edges from a DataFrame based on their value in a certain column

    Parameters
    ----------
    edges : pandas.DataFrame 
        Whose columns include null_column and every column in print_columns
    null_column : 
        Name n of the column such that if a row has a null value in column n then it will be removed
    print_columns : 
        Columns whose values to zip together when printing the list of edges removed
    message : str 
        Text to preface the list of edges removed

    Returns
    -------
    edges : pandas.DataFrame
        New dataframe with required edges removed
    missing_edges : pandas.DataFrame
        Dataframe containing all the edges that were removed
    """

    missing_edges_indices = edges[null_column].isnull()
    missing_edges = edges[missing_edges_indices]
    if not missing_edges.empty:
        printable_missing = list(zip(*[missing_edges[column] for column in print_columns]))
        print(f'{message} ({len(missing_edges)} edges):\n{printable_missing}')
        edges = edges[~missing_edges_indices]
    return edges, missing_edges


def replace_nodes_with_ids(edges):
    """Replace node names with integer IDs

    Parameters
    ----------
    edges : pandas.DataFrame
        DataFrame with nodes in columns 'i' and 'j'

    Returns
    -------
    edges : pandas.DataFrame
        Updated DataFrame with names replaced by IDs
    ids_to_names : dict 
        Dictionary mapping the new IDs to the old names
    """

    unique_nodes = pd.concat([edges['i'], edges['j']]).to_frame().drop_duplicates(ignore_index=True)
    unique_nodes.reset_index(inplace=True)
    unique_nodes.columns = ['id', 'name']
    ids_to_names = unique_nodes.to_dict()['name']

    # Replace all occurrences of a node name with its new numeric ID. We do this using merges for efficiency purposes.
    # Merge unique nodes onto our original edge list twice - once for when the node is the source node of an edge, and
    # again for when the node is the target node of an edge.
    edges = edges.merge(unique_nodes, how='left', left_on='i', right_on='name')
    edges = edges.merge(unique_nodes, how='left', left_on='j', right_on='name')
    # Now restrict to four columns again, but now using node IDs instead of node names.
    edges = edges[['id_x', 'id_y', 't', 'weight']]
    edges.columns = ['i', 'j', 't', 'weight']

    return edges, ids_to_names
    
def series2tedges(edge_series, idx) :

    """
    Convert an edge time series (idx-th row of a pandas.DataFrame) to a list of tedges
    
    Parameters
    ----------
    edge_series : pandas.DataFrame 
        Edge time series, with edge names ('A-B') as rows and time points as columns
    idx : int 
        Index of edge (row) to convert to tedges

    Returns
    -------
    df : pandas.DataFrame 
        Time-edge dataframe, with the idx-th time series, with columns ['i', 'j', 't', 'weight'] and rows as time points. 
    """
    df = edge_series.iloc[idx].to_frame()
    df["i"] = df.columns[0].split("-")[0]
    df["j"] = df.columns[0].split("-")[1]
    times = edge_series.columns.to_list()
    df["t"] = times
    df.rename(columns={df.columns[0] : 'weight'}, inplace=True)

#     print(df)
    df = df[["i", "j", "t", 'weight']]

    return df
    
def convert_input_to_indices(node_i, node_j, temporal_network):

    """Convert input (which can be labels or indices, to indices)"""
    # create inverse dictionary
    node_names_to_ids = {value : key for key, value in temporal_network.node_ids_to_names.items()}

    if isinstance(node_i, int) and isinstance(node_j, int):
        by_label = False
        i = node_i 
        j = node_j
    elif isinstance(node_i, str) and isinstance(node_j, str):
        by_label = True
        try:
            i = node_names_to_ids[node_i]
            j = node_names_to_ids[node_j]
        except KeyError:
            print("ERROR: node not in network")
            
    else: 
        print("ERROR: invalid node inputs")
            
    return i, j, by_label
    

def snapshots2tedges(snapshots): 
    """Return tedge DataFrame with columns ['i', 'j', 't', 'weight'], from snapshots array of dimensions (N,N,T)"""
    tedges = []
    
    N, _, T = np.shape(snapshots)

    for i in range(N) :
        for j in range(i) : # assume undirected
            for t in range(T) : 
                w = snapshots[i,j,t]
                tedges.append((i,j,t, w))
    return pd.DataFrame(tedges, columns=['i', 'j', 't', 'weight'])

def all_series2tedges(edge_series) : 
    
    """
    Convert a DataFrame of a set of edge time series to a list of tedges
    
    Parameters
    ----------
    edge_series : pandas.DataFrame 
        Containing multiple edge time series, with edge names ('A-B') as rows and time points as columns
    #times - time corresponding to the time points

    Returns
    -------
    df : pandas.DataFrame 
        Time series, with columns ['i', 'j', 't', 'weight'] and rows as time points. 
    """
    
    tedges = []
    n_edges = len(edge_series.index)
    for i in range(n_edges) :
        tedges_i =  series2tedges(edge_series, i)
        tedges.append(tedges_i)
        
    return pd.concat(tedges, ignore_index=True)    
