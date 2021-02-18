import math
import numpy as np
import theano.tensor as tt


def create_mask_matrix(shape, indices):
    """
    Create mask matrix of the specified shape with 1's in positions defined in `indices`
    and 0's elsewhere

    :param shape: tuple of integers
    :param indices: iterable of tuples
    :return: mask matrix
    """

    m = np.zeros(shape)
    for i, j in indices:
        m[i, j] = 1
    return m


def create_mask_vector(length, indices):
    """
    Create mask vector of the specified length with 1's in positions defined in `indices`
    and 0's elsewhere

    :param length: integer
    :param indices: iterable of integers
    :return: mask vector
    """

    v = np.zeros(length)
    for i in indices:
        v[i] = 1
    return v


def fill_vector(*args):
    """
    Create a vector as a Theano tensor object.
    In the context of a PyMC3 model, can be used to create a vectorial
    deterministic variable from other model variables

    :param args: sequence of objects representing scalars
     and corresponding to the elements of the constructed vector
    :return: vector as a Theano tensor object, formed from elements of `*args`
    """

    n = len(args)

    res = tt.nlinalg.matrix_dot(create_mask_vector(n, (0,)), args[0])
    for i in range(1, n):
        mask_v = create_mask_vector(n, (i,))
        res += tt.nlinalg.matrix_dot(mask_v, args[i])

    return res


def fill_correlation_matrix(c_vec):
    """
    Create a Theano tensor object representing a correlation matrix
    of a multivariate normal distribution.

    :param c_vec: PyMC3 model variable corresponding to the `LKJCorr` prior
                  on  elements of the correlation matrix
    :return: correlation matrix as a Theano tensor object
    """

    n = c_vec.tag.test_value.shape[0]
    n_layers = n - 1

    m = np.zeros((n, n))
    res = tt.nlinalg.matrix_dot(m, 1)

    ind = 0

    for layer in range(n_layers):
        start_col = layer + 1
        for j in range(start_col, n):
            m[layer, j] = 1
            m[j, layer] = 1
            res += tt.nlinalg.matrix_dot(m, c_vec[ind])

            ind += 1
            m[layer, j] = 0
            m[j, layer] = 0

    res = tt.fill_diagonal(res, 1.)
    return res


def fill_cov_matrix(*args):
    """
    Create a Theano tensor object representing a covariance matrix
    of a multivariate normal distribution.

    :param args: PyMC3 variables, each representing upper triagular elements
                 of a covariance matrix
    :return: covariance matrix as a Theano tensor object
    """

    n = len(args)
    s = (math.sqrt(8 * n + 1) - 1) / 2

    s = int(s)
    if (s * (s + 1)) / 2 != n:
        raise Exception('The number supplied components does not allow to construct a square matrix')

    m = np.zeros((s, s))
    res = tt.nlinalg.matrix_dot(m, 1)

    ind = 0
    for i in range(s):
        for j in range(i, s):
            m[i, j] = 1
            m[j, i] = 1
            res += tt.nlinalg.matrix_dot(m, args[ind])

            ind += 1
            m[i, j] = 0
            m[j, i] = 0

    return res
