# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Plotting the manifold
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

'''
plot the polytope
'''
def plot_polytope(**kwargs):
    ax=kwargs["ax"]
    ax.fill("x", "y",
            data={"x": kwargs["x"], "y": kwargs["y"]})
'''
solve a linear program if a point is inside a convex polygon
'''
def inside_polygon_ND(points, x):
    n_points = np.size(points, 0)
    c = np.zeros(n_points)
    A = np.r_[points.T,np.ones((1,n_points))]
    b = np.r_[x, np.ones(1)]
    lp = linprog(c, A_eq=A, b_eq=b)
    return lp.success

def compute_simple_zonotpye(point):
    val=np.tile(point[0:2], (4,1))
    new_points = val + np.array([[2.5, 2.5],
                          [-2.5, 2.5],
                          [-2.5, -2.5],
                          [2.5, -2.5]])
    return new_points
def plot_patches(P, **kwargs):
    fig, ax = plt.subplots()
    all_points=np.array([P[p] for p in P])
    for i, txt in enumerate(P):
        new_points=compute_simple_zonotpye(all_points[i, :])
        ax.fill(new_points[:, 0], new_points[:, 1], alpha=.2)
        ax.annotate(txt, (all_points[i, 0], all_points[i, 1]))
    ax.scatter(all_points[:, 0], all_points[:, 1], c="blue")