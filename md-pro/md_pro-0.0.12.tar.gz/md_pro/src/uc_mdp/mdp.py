# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Markov Decision Process (MDP)
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

import logging
import igraph as ig
import numpy as np
from scipy.cluster.vq import kmeans, vq
import md_pro.util.data_input_loader as util_io

"""
Class for Markov Decision Process
"""
class mdp(object):
    def __init__(self, **kwargs):
        self.mdp_dict= {'S': None, # States
                        'T': None,  # Topology
                   'action': None, # Action set
                   'R': None, # Rewards
                   'gamma': None, # discount factor
                    }
        self.mdp_dict['P']=None # Transition
        self.mdp_dict['pi']=None
        #self.mdp_dict['multi_pi'] = {}
        self.mdp_dict['U'] = None
        self.param = {'n_optimal_trajectory': None, # optimal trajectory
                      }


    def set_limit_simulation(self, value):
        self.param["n_optimal_trajectory"]=value

    """
    Set gamma (forgetting factor) on dictionary for MDP
    """
    def set_gamma(self, gamma):
        self.mdp_dict["gamma"]=gamma

    """
    Set position list on dictionary for MDP
    """
    def set_position_list(self, position):
        self.mdp_dict['P']=position

    """
    Set transition probabilities on dictionary for MDP
    """
    def set_P(self, transition):
        self.mdp_dict['P']=transition

    """
    Set state values on dictionary for MDP
    """
    def set_U(self):
        self.mdp_dict['U'] = [0] * len(self.mdp_dict['S'])

    """
    Set action values on dictionary for MDP
    """
    def set_action(self, action):
        self.mdp_dict['action']=action

    """
    Set initial policy on dictionary for MDP
    """
    def set_init_pi(self):
        a={}
        for i in self.mdp_dict['S']:
            a[i]=self.mdp_dict['action'][i][0]
        self.mdp_dict['pi']=a

    """
    Set states on dictionary for MDP
    """
    def set_S(self, S):
        self.mdp_dict['S']=S

    """
    Set topology for MDP
    """

    def set_T(self, T):
        self.mdp_dict['T'] = T

    """
    Set rewards on dictionary for MDP
    """
    def set_R(self, dictR):
        val=list(dictR.values())
        keys=dictR.keys()
        self.mdp_dict['R']=np.zeros(len(self.mdp_dict['S']))
        for idx, q in enumerate(keys):
            self.mdp_dict['R'][int(q)]=val[idx]

    """
    Set adjacency list on dictionary for MDP
    """
    def set_adjacency_list(self, list):
        new_list=[]
        for i in list:
            a = self.mdp_dict['S'].index(i[0])
            b = self.mdp_dict['S'].index(i[1])
            new_list.append((a, b))
            new_list.append((a, a))
            #new_list.append((b, a))
        self.mdp_dict['adjacency_list']=new_list

    """
    Policy evaluation for MDP
    """
    def policy_evaluation(self):
            for kp, p in enumerate(self.mdp_dict['S']):
                state_action=(p, self.mdp_dict['pi'][p])
                prob_dict=self.mdp_dict['P'][state_action]
                bds=self.mdp_dict['gamma']*np.sum([a * b for a, b in zip(self.mdp_dict['U'], prob_dict)])
                idx=np.int(np.random.choice(len(self.mdp_dict['S']), 1, p=prob_dict))
                self.mdp_dict['U'][kp]=self.mdp_dict['R'][idx]+bds
            return self.mdp_dict['U']

    """
    Policy iteration for MDP
    """
    def policy_iteration(self):
            actual_U=self.policy_evaluation()
            for kp, p in enumerate(self.mdp_dict['S']):
                all_Us = np.zeros(len(self.mdp_dict['action'][p]))
                for ka, act_a in enumerate(self.mdp_dict['action'][p]):
                    state_action=(p, act_a)
                    prob_dict=self.mdp_dict['P'][state_action]
                    bds=self.mdp_dict['gamma']*np.sum([a * b for a, b in zip(actual_U, prob_dict)])
                    idx = np.int(np.random.choice(len(self.mdp_dict['S']), 1, p=prob_dict))
                    all_Us[ka]=self.mdp_dict['R'][idx] + bds
                self.get_new_policy(np.array(all_Us), kp)

    """
    Get new policy
    """
    def get_new_policy(self, all_Us, act_node):
        idx=np.argmax(all_Us, axis=0)
        act_node_name=self.mdp_dict['S'][act_node]
        self.mdp_dict['pi'][act_node_name]=self.mdp_dict['action'][act_node_name][idx]

    """
    Find neighbours
    """
    def find_neighbours(self, act_node):
        return self.mdp_dict["action"][act_node]

    """
    Get values for a list of nodes
    """
    def get_value_of_nodes(self, nodes):
        group=[self.mdp_dict["U"][int(wlt)] for wlt in nodes]
        return group

    """
    Get all policy options
    """
    def get_all_policy_options(self):
        for act_node in self.mdp_dict['S']:
            act_value=float(self.get_value_of_nodes(act_node)[0]) # actual value function
            act_neighbours=self.find_neighbours(act_node) # actual neighbours
            act_values_by_group=self.get_value_of_nodes(act_neighbours) # actual value function of neighbours
            bool_group=list()
            for wlt in act_values_by_group:
                if(wlt>act_value):
                    bool_group.append(True)
                else:
                    bool_group.append(True)
            self.mdp_dict['multi_pi'][act_node]=list()
            for idx, act_bool in enumerate(bool_group):
                if(act_bool==True):
                    new_cand={"neighbour": act_neighbours[idx], "difference": float(act_values_by_group[idx]-act_value)}
                    self.mdp_dict['multi_pi'][act_node].append(new_cand)


    """
    MDP: policy iteration and evaluation
    """
    def start_mdp_algorithm(self):
        count=0
        count2=0
        while(1):
            oldU=self.mdp_dict['U'][:]
            self.policy_iteration()
            if (np.sum(np.array(self.mdp_dict['U']))==0):
                count += 1
                continue
            if(np.sum(np.array(self.mdp_dict['U'])-np.array(oldU))<10e-9):
                count += 1
                count2+=1
            if(count2>10):
                # logging.info("Convergence")
                # logging.info(count)
                # logging.info(self.mdp_dict['pi'])
                # logging.info(self.mdp_dict['U'])
                break
            elif(count>1000):
                logging.info("No Convergence")
                break

            count+=1
        return self.mdp_dict

    """
    Visualization of the network after running MDP algorithms (policy iteration and -evaluation) with igraph python package
    """
    def visualize_network(self):
        g = ig.Graph(self.mdp_dict['adjacency_list'])
        g.vs["name"] = self.mdp_dict['S']
        g.vs["reward"]= self.mdp_dict['R']
        g.vs["label"] = g.vs["name"]
        # vec=np.array(self.mdp_dict['U'])
        # p=np.var(vec)
        # if(p==0):
        #     print('error')
        #     exit()
        # color_dict = {0: "blue", 1: "green", 2: "cyan", 3: "yellow", 4: "pink", 5: "orange", 6: "red"}
        # try:
        #     codebook, _ = kmeans(vec, len(color_dict))
        #     cluster_indices, _ = vq(vec, codebook)
        # except:
        #     codebook
        #
        # sel=[]
        # am_max_cluster=np.max(cluster_indices)
        # for qrti in range(0, am_max_cluster+1):
        #     tre=qrti==cluster_indices
        #     new_candi=np.max(vec[tre])
        #     sel.append(new_candi)
        # sel=np.array(sel)
        # sort_idx=np.argsort(sel)
        # new_cluster_indices=[np.nan]*len(cluster_indices)
        # for count, qrt in enumerate(sort_idx):
        #     act_idx_bool=sort_idx[count]==cluster_indices
        #     act_idx=np.where(act_idx_bool)
        #     act_idx=act_idx[0].tolist()
        #     for t in act_idx:
        #         new_cluster_indices[t]=count
        #
        # colors = [color_dict[index] for index in new_cluster_indices]
        # g.vs["color"] = colors

        g.vs["vertex_size"] = 20
        visual_style = {}
        visual_style["edge_curved"] = False
        P_2D=[(wlt[0], wlt[1]) for wlt in self.mdp_dict['P']]
        layout = ig.Layout(P_2D)
        ig.plot(g)

    """
    Based on the optimization on the MDP, get a stochastic trajectory resulting from the optimization procedure of the MDP
    """
    def get_trajectory(self, R_dict):
        params=util_io.get_params()
        start_node=self.mdp_dict['S'][params["md_pro"]["simulation"]["start_node"]]
        r_target_values=list(R_dict.keys())
        ideal_path=[]
        ideal_path.append(str(start_node))
        policy=self.mdp_dict['pi']
        count=0
        while(1):
            act_node=ideal_path[-1]
            action=policy[act_node]
            if(count>self.param['n_optimal_trajectory']):
                break
            if(act_node in r_target_values):
                break
            else:
                count+=1
            abc=self.mdp_dict['T']
            act_trans=abc[(act_node, action)]
            next_node=np.int(np.random.choice(len(self.mdp_dict['S']), 1, p=act_trans))
            ideal_path.append(self.mdp_dict['S'][next_node])
        print('ideal_path')
        print(ideal_path)
        self.visualize_network()
        return ideal_path



