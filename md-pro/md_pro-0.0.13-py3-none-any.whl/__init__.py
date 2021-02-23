# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Markov Decision Process (MDP)
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

from md_pro.src.uc_mdp.uc_mdp_main import *
from scipy.spatial.distance import pdist, squareform
import argparse
import igraph as ig
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import warnings
'''
Start a MDP challenge
'''
def start_mdp(mdp_challenge):
    obj_mdp = service_MDP()
    dict_mdp = obj_mdp.start_mdp(mdp_challenge)
    logging.info(dict_mdp['pi'])
    return dict_mdp

'''
Get the points of a regular grid
'''
def get_meshgrid_points(**kwargs):
    xgrid = np.linspace(kwargs["x_min"], kwargs["x_max"], kwargs["x_grid"])
    ygrid = np.linspace(kwargs["y_min"], kwargs["y_max"], kwargs["y_grid"])
    X, Y=np.meshgrid(xgrid,ygrid)
    x=np.ravel(X)
    y=np.ravel(Y)
    z=0*y
    P={}
    points=np.transpose(np.vstack((x, y, z))).tolist()
    for idx, act_point in enumerate(points):
        P[str(idx)]=act_point
    return P


'''
Compute distance matrix
'''
def compute_distance_matrix(P):
    rtb=np.vstack(list(P.values()))
    C=squareform(pdist(rtb))
    return C

'''
Convert distance matrix to k_nearest_neigh-topology-matrix
'''
def convert_distance_knear_neigh_mat(C, k=5):
    T = np.zeros((np.size(C,0), np.size(C,1)), dtype=bool)
    idx_mat=np.argsort(C, axis=0)
    for i in range(0, np.size(C, 1)):
        act_idx=idx_mat[0:4, i]
        T[act_idx, i]=True
    return T

"""
get topology T and states for a regular grid
#states
S = ['0', '1', '2', '3']
#topology
T=np.array([[True, True, False, True],
                  [True, True, True, False],
                  [False, True, True, True],
                  [True, False, True, True]])
"""

def get_simple_topology_for_regular_grid(P, **kwargs):
    C=compute_distance_matrix(P)
    T=convert_distance_knear_neigh_mat(C)
    amount_nodes=kwargs["y_grid"]*kwargs["x_grid"]
    S=[str(i) for i in range(0, amount_nodes)]
    # T = np.zeros((amount_nodes, amount_nodes), dtype=bool)
    # T=np.eye(amount_nodes, dtype=bool)
    return T, S

'''
Topology to edge list
'''
def topology_to_edge_list(T):
    edge_list=[]
    T=T.tolist()
    for itp in range(0, len(T)):
        act_list=T[itp]
        new_ind=[idx for idx, x in enumerate(act_list) if x]
        for qrt in new_ind:
            edge_list.append((itp, qrt))
    return edge_list
'''
Plot the results
'''
def plot_the_result(dict_mdp, mdp_challenge):
    edge_list=topology_to_edge_list(mdp_challenge['T'])
    g = ig.Graph(edge_list)
    g.vs["name"] = dict_mdp['S']
    g.vs["reward"] = dict_mdp['R']
    g.vs["label"] = g.vs["name"]
    P_2D=list(mdp_challenge['P'].values())
    x_vec = [wlt[0] for wlt in P_2D]
    y_vec = [wlt[1] for wlt in P_2D]
    layout = ig.Layout(P_2D)
    g.vs["vertex_size"] = 20
    visual_style = {}
    visual_style["edge_curved"] = False
    colors = [(1, 0, 1) for i in range(0, len(dict_mdp['S']))]
    g.vs["color"] = colors
    fig = go.Figure()
    fig.add_trace(go.Scattergl(x=x_vec, y=y_vec, text=dict_mdp['S'],
                             mode='markers',
                             name='grid_points'))
    fig.add_trace(go.Scattergl(x=x_vec, y=y_vec,
                    mode='markers',
                    name='value_markers',
                    marker=dict(size=dict_mdp['U'],
                                         color=dict_mdp['U'])
                                         ))
    fig.show()

"""
Reach n-steps
"""
def next_neighbour():
    None

"""
Reachability analysis for topological spaces and n-steps
"""
def reach_n_steps(strt_pnt, mdp_challenge, dict_mdp, params, steps=3):
    reach=[]
    # first neighbours
    neigh=dict_mdp['action'][strt_pnt]
    # reachability variable
    reach.append(neigh)
    for i in range(0, steps):
        neigh = []
        # actual neighbours
        last_reach=reach[i]
        for qrt in last_reach:
            new_neigh=dict_mdp['action'][qrt]
            for wlt in new_neigh:
                neigh.append(wlt)
        neigh=np.unique(neigh)
        reach.append(neigh)
    return reach
"""
Get the trajectory for reachability analysis
"""
def get_trajectory_old(strt_pnt, dict_mdp, reach_set):
    traj=[]
    traj.append(strt_pnt)
    U=dict_mdp['U']
    for act_reach in reach_set:
        act_U=np.array([U[int(wlt)] for wlt in act_reach])
        idx=np.argmax(act_U)
        candidate=act_reach[idx]
        if(candidate in dict_mdp['action'][traj[-1]]):
            traj.append(candidate)
    return traj

"""
Get the trajectory for reachability analysis
"""
def get_deterministic_trajectory(strt_pnt, dict_mdp, steps=10):
    traj=[]
    traj.append(strt_pnt)
    U=dict_mdp['U']
    for qrt in range(0, steps):
        act_actions=np.array([np.int(wlt) for wlt in dict_mdp['action'][traj[-1]]])
        act_U=np.array([U[wlt] for wlt in act_actions])
        idx=np.argmax(act_U)
        candidate=np.str(act_actions[idx])
        traj.append(candidate)
    return traj

"""
Get the value function as a dictionary
"""
def get_U_as_dict(dict_mdp):
    U_list=dict_mdp['U']
    U_dict={str(idx): wlt for idx, wlt in enumerate(U_list)}
    return U_dict
"""
Get the values for the neighbours of one agent
"""
def get_U_for_agent_neighbours(dict_mdp, agent_str):
    U_dict=get_U_as_dict(dict_mdp)
    act_neigh=dict_mdp['action'][agent_str]
    agent_U_neigh={wlt: U_dict[wlt] for wlt in act_neigh}
    return agent_U_neigh

"""
Stochastic trajectory generation
"""
def get_stochastic_trajectory(strt_pnt, dict_mdp, steps=10):
    traj=[]
    traj.append(strt_pnt)
    U=dict_mdp['U']
    for qrt in range(0, steps):
        drt=dict_mdp['action'][traj[-1]]
        act_actions=np.array([np.int(wlt) for wlt in drt])
        act_U=np.array([U[wlt] for wlt in act_actions])
        dummy=act_U
        prob_vec=dummy/np.sum(dummy)
        idx=np.random.choice(len(prob_vec), 1, p=prob_vec)
        idx=idx[0]
        candidate=np.str(act_actions[idx])
        traj.append(candidate)
    return traj

"""
Get new states with a virtual force
"""
def get_new_states_with_virtual_force():
    None

def get_list_P(P):
    return np.array([[P[i][0], P[i][1]] for i in P])

def optimal_path_as_integers(optimal_mdp_str):
    return [np.int(i) for i in optimal_mdp_str]
'''
Get the xy coordinates from the optimal path of the MDP. Interpolate the xy coordinates
'''
def get_result_trajectories_mdp(params, optimal_mdp_str, P):
    coordinates=get_list_P(P)
    optimal_mdp=optimal_path_as_integers(optimal_mdp_str)
    act_traj=list()
    for wlt in optimal_mdp:
        x = coordinates[wlt, 0]
        y = coordinates[wlt, 1]
        act_traj.append((x,y))
    interpolated_points, points=interpolate_traj(params, act_traj)
    return interpolated_points, points


'''
    Filter obsolete path points
'''
def filter_obsolete_path_points(act_traj):
    new_traj = [act_traj[0]]
    for wlt in act_traj:
        if (new_traj[-1] != wlt):
            new_traj.append(wlt)
    x = [wlt[0] for wlt in new_traj]
    y = [wlt[1] for wlt in new_traj]
    points = np.vstack((x, y)).T
    return points
'''
    Cumulative and normalization of the points
'''
def cumulative_distance(act_traj):
    points=filter_obsolete_path_points(act_traj)
    # Linear length along the line:
    cum_distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1)))
    cum_distance=np.insert(cum_distance, 0, 0)
    normalized_distance = cum_distance / cum_distance[-1]
    return normalized_distance, points

'''
    Cumulative and normalization of the points
'''
def cumulative_distance_without_filtering(act_traj):
    points=act_traj
    dif_points=np.diff(points, axis=0)
    sum_dif=np.sum(dif_points ** 2, axis=1)
    cum_distance = np.cumsum(np.sqrt(sum_dif))
    cum_distance=np.insert(cum_distance, 0, 0)
    # x=act_traj[:, 0]
    # y=act_traj[:, 1]
    # # fig, ax = plt.subplots()
    # ax.scatter(x, y)
    #
    # for idx, txt in enumerate(cum_distance):
    #     ax.annotate(txt, (x[idx], y[idx]))
    # plt.show()
    return cum_distance

'''
    Interpolation of the trajectory in xy coordinates
'''
def interpolate_traj(params, act_traj):
    normalized_distance, points=cumulative_distance(act_traj)
    # Interpolation for different methods:
    method = 'quadratic'
    alpha = np.linspace(0, 1, params["spline_interpolation"])

    interpolated_points = {}
    interpolator = interp1d(normalized_distance, points, kind=method, axis=0)
    interpolated_points[method] = interpolator(alpha)
    return interpolated_points, points