import numpy as np


def generate_mvnormal_clusters(mus, covs, sizes, seed=None):

    if seed is not None:
        np.random.seed(seed)

    n_points = sum(sizes)
    xs = np.zeros(n_points)
    ys = np.zeros(n_points)
    labels = np.zeros(n_points, dtype=int)

    start_from = 0
    lb = 0
    for mu, cov, sz in zip(mus, covs, sizes):

        x, y = np.random.multivariate_normal(mu, cov, sz).T

        next_start_from = start_from + sz

        xs[start_from:next_start_from] = x
        ys[start_from:next_start_from] = y
        labels[start_from:next_start_from] = lb

        start_from = next_start_from
        lb += 1

    return xs, ys, labels


def generate_normal_clusters(mus, stddevs, sizes, seed=None):

    if seed is not None:
        np.random.seed(seed)

    n_points = sum(sizes)
    xs = np.zeros(n_points)
    labels = np.zeros(n_points, dtype=int)

    start_from = 0
    lb = 0
    for mu, std, sz in zip(mus, stddevs, sizes):

        x = np.random.normal(mu, std, sz)

        next_start_from = start_from + sz

        xs[start_from:next_start_from] = x
        labels[start_from:next_start_from] = lb

        start_from = next_start_from
        lb += 1

    return xs, labels
