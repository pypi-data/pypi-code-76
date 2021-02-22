# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Markov Decision Process (MDP)
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------


from md_pro.src.uc_mdp.mdp import *

class problem(object):
    def __init__(self, mdp_challenge, **kwargs):
        self.mdp_challenge=mdp_challenge
    def get_probability_nodes(self, S, Adjenc, A):
        transition = {}
        for wlt in range(0, np.size(Adjenc, 1)):
            allActions = A[S[wlt]]
            topSet = [(S[wlt], i) for i in allActions]
            vec = Adjenc[:, wlt]
            count = 0
            for tlw in range(0, len(vec)):
                if (vec[tlw]):
                    count += 1
            for qrt in range(0, np.size(topSet, 0)):
                prob = np.zeros(len(vec))
                prob[vec] = 1 / count
                act_type = (topSet[qrt][0], topSet[qrt][1])
                prob = prob / prob.sum()
                if (np.allclose(sum(prob), 1.0, rtol=1e-05, atol=1e-08)):
                    newdict = {act_type: prob}
                    transition.update(newdict)
                else:
                    None
        return transition
    def get_actions(self, S, T):
        new_dict=dict()
        for idx, ili in enumerate(S):
            act_bool=T[idx, :]
            new_val=[i for idx, i in enumerate(S) if(act_bool[idx])]
            new_dict[ili]=new_val
        return new_dict


    def set_solver(self, mdp_challenge):
        S = self.mdp_challenge['S'] # states
        T = self.mdp_challenge['T']  # topology
        A = self.get_actions(S, T)  # actions
        P = self.get_probability_nodes(S, T, A)
        self.obj_solver=mdp()
        self.obj_solver.set_gamma(mdp_challenge['gamma'])
        self.obj_solver.set_S(S)
        self.obj_solver.set_T(T)
        self.obj_solver.set_U()
        self.obj_solver.set_action(A)
        self.obj_solver.set_init_pi()
        self.obj_solver.set_P(P)
    def start_mdp_solver(self, rewards):
        R_dict = rewards
        self.obj_solver.set_R(R_dict)
        dict_mdp = self.obj_solver.start_mdp_algorithm()
        # self.obj_solver.get_all_policy_options()
        return dict_mdp

