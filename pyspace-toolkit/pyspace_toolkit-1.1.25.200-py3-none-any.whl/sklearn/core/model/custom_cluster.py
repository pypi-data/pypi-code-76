# %%
from minisom import MiniSom

from sklearn.base import BaseEstimator, ClusterMixin, TransformerMixin
from sklearn.metrics import classification_report
from sklearn.cluster import AgglomerativeClustering

import numpy as np
import pandas as pd

try:
    from matplotlib.gridspec import GridSpec
    import matplotlib.pyplot as plt
    from cycler import cycler
except:
    pass

import sys
from ast import literal_eval


# %%
class MinisomClustering(BaseEstimator, ClusterMixin, TransformerMixin):
    
    def __init__(self, dims=(3,3), num_iteration=1000, sigma=1.0, learning_rate=0.5, neighborhood_function='gaussian', random_seed=42):
        self.dimx = dims[0]
        self.dimy = dims[1]
        self.num_iteration = num_iteration
        self.sigma = sigma
        self.learning_rate = learning_rate
        self.neighborhood_function = neighborhood_function
        self.random_seed = random_seed
        
    def fit(self, X):
        input_len = X.shape[1]
        self.som = MiniSom(self.dimx, self.dimy, input_len=input_len, 
                           sigma=self.sigma, learning_rate=self.learning_rate,
                           neighborhood_function=self.neighborhood_function, random_seed=self.random_seed)
        self.som.pca_weights_init(X)
        self.som.train_random(X, self.num_iteration)
        
    def predict(self, X):
        clusters = [str(self.som.winner(d)) for d in X]
        return clusters
    
    def fit_predict(self, X):
        self.fit(X)
        return self.predict(X)
    
    def predict_label(self, trainX, trainLabel, testX):
        
        labels_map = self.som.labels_map(trainX, trainLabel)
        predclusters = self.predict(testX)
        
        predlabels = []
        
        default_class = np.sum(list(labels_map.values())).most_common()[0][0]
        for pred_cluster in predclusters:
            if literal_eval(pred_cluster) in labels_map:
                predlabels.append(labels_map[literal_eval(pred_cluster)].most_common()[0][0])
            else:
                predlabels.append(default_class)
        return predlabels
    
    def plot_som_marker(self, X, y):
        plt.figure(figsize=(self.dimx, self.dimy))
        plt.pcolor(self.som.distance_map().T, cmap='bone_r')
        
        markers = ['o', 's', 'D', 'x']
        colors = ['C0', 'C1', 'C2', 'C3']
        
        for cnt, xx in enumerate(X):
            w = self.som.winner(xx)
            plt.plot(w[0]+.5, w[1]+.5, markers[y[cnt]], markerfacecolor='None',
                     markeredgecolor=colors[y[cnt]], markersize=12, markeredgewidth=2)
            
        plt.axis([0, self.dimx, 0, self.dimy])
        plt.show()
        
    def plot_som_pie(self, X, y):
        
        labels_map = self.som.labels_map(X,y)
        label_names = np.unique(y)
        label_length = len(label_names)
        
        # https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
        cm = plt.get_cmap('nipy_spectral') # gist_rainbow, tab20, jet
        colors = [cm(1.*i/label_length) for i in range(label_length)]
        default_cycler = (cycler(color=colors))
        # plt.rc('axes', prop_cycle=default_cycler)
        
        plt.figure(figsize=(self.dimx, self.dimy))
        the_grid = GridSpec(self.dimy, self.dimx)
        
        for position in labels_map.keys():
            label_fracs = [labels_map[position][l] for l in label_names]
            ax = plt.subplot(the_grid[position[1], position[0]], aspect=1)
            ax.set_prop_cycle(default_cycler)
            elem_count = np.sum(label_fracs)
            # ax.text(0.5, -0.1, str(elem_count), size=12, ha="center", transform=ax.transAxes)
            ax.text(0.5,0.5, str(elem_count), size=12, horizontalalignment='center',
                    verticalalignment='center', color='white', transform=ax.transAxes)
            patches, texts = plt.pie(label_fracs)
            
        fig = plt.figure(frameon=False); ax = fig.add_axes([0, 0, 0.01, 0.01]); ax.axis('off')
        plt.legend(patches, label_names, loc='upper left', bbox_to_anchor=(0, 0), ncol=4)
        plt.show()
        
    @staticmethod
    def plot_som_quantization(X, mapx, mapy):
        som = MiniSom(mapx, mapy, X.shape[1], sigma=3, learning_rate=0.5,
                      neighborhood_function='triangle', random_seed=10)
        som.pca_weights_init(X)
        max_iter = 10000
        q_error_pca_init = []
        iter_x = []
        for i in range(max_iter):
            percent = 100*(i+1)/max_iter
            rand_i = np.random.randint(len(X)) # train_random()
            som.update(X[rand_i], som.winner(X[rand_i]), i, max_iter)
            if (i+1) % 100 == 0:
                error = som.quantization_error(X)
                q_error_pca_init.append(error)
                iter_x.append(i)
                sys.stdout.write(f'\riteration={i:2d} status={percent:0.2f}% error={error}')
                
        plt.plot(iter_x, q_error_pca_init)
        plt.ylabel('quantization error')
        plt.xlabel('iteration index')


# %%
class AgglomerativeClusteringThreshold(BaseEstimator, ClusterMixin, TransformerMixin):
    
    def __init__(self, threshold=20, *params):
        self.model = AgglomerativeClustering(*params)
        self.threshold = threshold
        
    def fit(self, X):
        self.datalength = len(X)
        self.model.fit(X)
        
    def fit_predict(self, X):
        self.fit(X)
        
        self.cut_tree()
        return self.labels_
    
    def cut_tree(self,):
        
        def get_children_count(node_id, tree): # children_tree
            children_count = 0
            for edge in tree:
                if node_id == edge[2]:
                    if edge[0] not in list(range(datalength, datalength+children_tree.shape[0])):
                        children_count += 1
                    if edge[1] not in list(range(datalength, datalength+children_tree.shape[0])):
                        children_count += 1
                    children_count += get_children_count(edge[0],tree)
                    children_count += get_children_count(edge[1],tree)
            return children_count
        
        def get_left_right_children(node_id, tree):
            for edge in tree:
                if node_id == edge[2]:
                    return edge[0], edge[1]
                
        def get_subtree(node_id, tree):
            subtree = np.empty((0,3), int)
            for edge in tree:
                if node_id == edge[2]:
                    subtree = np.append(subtree, [edge], axis=0)
                    left = get_subtree(edge[1], tree)
                    right = get_subtree(edge[0], tree)
                    if len(left) > 0:
                        subtree = np.append(subtree, left, axis=0)
                    if len(right) > 0:
                        subtree = np.append(subtree, right, axis=0)
            return subtree
        
        def get_cutting_nodes(node_id, tree, children_threshold):
            cutting_nodes = []
            if get_children_count(node_id, tree) > children_threshold:
                left, right = get_left_right_children(node_id, tree)
                subtree = get_subtree(node_id, tree)
                left = get_cutting_nodes(left, subtree, children_threshold)
                right = get_cutting_nodes(right, subtree, children_threshold)
                if len(left) > 0:
                    cutting_nodes.extend(left)
                if len(right) > 0:
                    cutting_nodes.extend(right)
            else:
                cutting_nodes.append(node_id)
            return cutting_nodes
        
        children_tree = self.model.children_.copy()
        datalength = self.datalength
        
        parent_nodes = list(range(datalength, datalength + children_tree.shape[0]))
        parent_nodes = np.array([parent_nodes]).T
        
        children_tree = np.append(children_tree, parent_nodes, axis=1)
        
        cutting_nodes = get_cutting_nodes(children_tree[-1][2], children_tree, self.threshold)
        
        labels_ = np.zeros(datalength)
        
        for cluster_id, cutting_node_id in enumerate(cutting_nodes):
            cluster = get_subtree(cutting_node_id, children_tree)
            for edge in cluster:
                for node in edge:
                    if(node not in parent_nodes):
                        labels_[node] = cluster_id
                        
        self.labels_ = labels_

