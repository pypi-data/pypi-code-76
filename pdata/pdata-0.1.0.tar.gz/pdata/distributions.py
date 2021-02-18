import numpy as np


def estimate_mvnormal(observations):
    '''
    Perform maximum-likelihood estimation of a multivariate normal
    distribution given the observation data

    :param observations: An (m x n) NumPy array or Pandas data frame,
                         where n is the dimension of the data
                         and m is the number of observations
    :return: Mean value ((m x 1) array) and covariance matrix ((n x n array))
    '''

    mu = np.mean(observations, axis=0)
    cov = np.cov(observations, rowvar=False)

    return mu, cov


def lognormal_mode(lognorm_params):
    '''
    Given the estimated parameters of log-normal distribution (s, loc, scale),
    compute its mode (x with the peak value of PDF)
    '''

    s, loc, scale = lognorm_params

    mu = np.log(scale)

    return np.exp(mu - s ** 2) + loc
