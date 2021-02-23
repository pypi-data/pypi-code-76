"""Replace any complex model by a linear one, and compute model uncertainties from them."""
import logging
from copy import copy
from functools import reduce
from random import sample

import numpy as np
from sympy import symbols, lambdify, diff, simplify
from sympy.matrices import Matrix


# noinspection PyShadowingNames
def linear_error_modeling(data_dict, s1, s2, mdl_vars, logger=None, inp_model=None, n_max_test=500, n_max_fit=1000,
                          min_samples=100):
    """
    :param min_samples:
    :param n_max_fit:
    :param n_max_test:
    :param inp_model:
    :param data_dict: dict with keys: "tau", "sp", "wv", "I", "dtau", "dsp", "dwv", "dI" , "r",
           either ndarrays or scalar (only for differentials)
    :param s1: tuple e.g. ((1,1,1,1),)
    :param s2: tuple e.g. ((0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0))
    :param mdl_vars: list of variable names used for the modeling, e.g. ["tau", "sp","wv","I"]
    :param logger: either None or logging instance
    :return: dictionary: {"error":[ndarray],"coef":[list],"f":[str, function definition],
             "fit_quality":[tuple, (intercept, offset, norm)]}
    """
    # import here to avoid static TLS ImportError
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split

    logger = logger if logger is not None else logging.getLogger(__name__)
    dtype = float
    # generade differential variables
    mdl_dvars = ["d%s" % var for var in mdl_vars]
    logger.info("Build model based on: %s and derivatives:%s" % (str(mdl_vars), str(mdl_dvars)))
    # dependency correlation and cross correlation
    sel1, sel2 = Matrix(s1), Matrix(s2)
    # define symbols and their derivatives
    vv = symbols(" ".join(mdl_vars))  # list of symbols
    dv = symbols(" ".join(mdl_dvars))  # list of derivative derivatives
    # build model based on correlations and cross correlations
    par = Matrix([vv])
    ff = ((par * sel1.T)[0] + (par * sel2 * par.T)[0]).expand()  # expansion: a_i's
    ww = [symbols("w%i" % ii) for ii in range(len(ff.args) + 1)]  # linear coefficients w_i's
    mdl = ww[0] + sum([arg * w for arg, w in zip(ff.args, ww[1:])])  # final model w0 + sum_i(w_i*a_i)
    mdl_error = simplify(sum([abs(diff(mdl, x) * dx) for x, dx in zip(vv, dv)]))  # gaussian (total) error propagation

    finites = list(
        np.where(  # get list of integer with valid data points
            reduce(np.logical_and,  # all should be true -> reduce list of data with logical_and
                   # generator to produce list of finites in each data field -> to be consumed from logical_and
                   (np.isfinite(v.ravel()) for k, v in data_dict.items() if k in mdl_vars + ["r"])))[0])
    if len(finites) > n_max_fit + n_max_test:
        finites = sample(finites, n_max_fit + n_max_test)
    if len(finites) < min_samples:
        logger.info("Fit failed due to lack of data -> proceed with zero errors.")
        return {
            "error": np.zeros(data_dict["r"].shape, dtype=np.float16),
            "coef": "",
            "f": "",
            "fit_quality": 0.0,
            "y": "",
            "yl": "",
        }
    finites_fit, finites_test = train_test_split(finites,
                                                 test_size=int(n_max_test) / (int(n_max_fit) + int(n_max_test)))
    del finites

    # two options, 1st buld model from inp, 2nd build model from inp_model
    if inp_model is None:
        logger.info("Build model based in inp.")
        inp_deps = {k: np.array(v.ravel()[finites_fit], dtype=dtype) for k, v in data_dict.items() if k in mdl_vars}
        x = np.vstack((lambdify(args=vv, expr=arg, dummify=False)(**inp_deps) for arg in ff.args)).transpose()
        y = np.array(data_dict["r"].ravel()[finites_fit], dtype=dtype)  # reflectance
    else:
        logger.info("Build model based in inp_model.")
        inp_deps = {k: np.array(v.ravel(), dtype=dtype) for k, v in inp_model.items() if k in mdl_vars}
        x = np.vstack([lambdify(args=vv, expr=arg, dummify=False)(**inp_deps) for arg in ff.args]).transpose()
        y = np.array(inp_model["r"].ravel(), dtype=dtype)  # reflectance

    # start fitting
    lr = LinearRegression()
    lr.fit(X=x, y=y)
    # save results
    ww_v = [lr.intercept_] + list(lr.coef_)
    # evaluate model

    # prepare input for sklearn alg,e.g. ff.args=(I, sp, tau, wv, I**2) -> loop over and compute values
    inp_deps = {k: np.array(v.ravel()[finites_test], dtype=dtype) for k, v in data_dict.items() if k in mdl_vars}
    x_test = np.vstack([np.array(
        lambdify(args=vv, expr=arg, dummify=False)(**inp_deps), dtype=dtype) for arg in ff.args]).transpose()
    y_test = np.array(data_dict["r"].ravel()[finites_test], dtype=dtype)  # reflectance
    # noinspection PyArgumentList
    y_model = np.array(lr.predict(X=x_test), dtype=dtype)

    # test model -> scatter plot
    lrt = LinearRegression()
    lrt.fit(X=y_model.reshape(-1, 1), y=y_test.reshape(-1, 1))
    # offset, slope, normalized sum of squares
    fit_quality = (float(lrt.intercept_), float(lrt.coef_[0]), float(np.sum(np.abs(y_model - y_test)) / len(y_test)))
    logger.info("model quality: a0=%.5f,a1=%.5f,<a>=%.5f" % fit_quality)
    logger.info("model: y = %s" % mdl)
    logger.info("error: dy = %s" % mdl_error)
    logger.info("coefficients: w0 -> %.3f" % ww_v[0])
    for w, w_, f in zip(ww[1:], ww_v[1:], ff.args):
        logger.info("coefficients: %s -> %.3f -> %s" % (w, w_, f))
        # prepare to replace coefficients with fitted values
    mdl_error_final = copy(mdl_error)
    mdl_final = copy(mdl)
    for w, v in zip(ww, ww_v):
        mdl_error_final = mdl_error_final.replace(w, v)
        mdl_final = mdl_final.replace(w, v)
    logger.info("error = %s" % mdl_error_final)
    # prepare for numpy evaluation
    f_error = lambdify(args=(vv + dv), expr=mdl_error_final, dummify=False)
    # evaluate model, gather results
    # input values for dependencies and their errors, if numpy array (has ravel() method), then use it,
    # else assume scalar value and proceed
    inp_d_deps = {k: v.ravel() if "ravel" in dir(v) else v for k, v in
                  data_dict.items() if k in mdl_vars + mdl_dvars}

    bf = f_error(**inp_d_deps)
    try:
        error_array = np.array(bf, dtype=np.float16).reshape(data_dict["r"].shape)
    except ValueError:  # in case that bf is only scalar -> get array now
        logger.info("Resulting error field is only scalar.")
        error_array = np.ones(data_dict["r"].shape, dtype=np.float16) * np.float16(bf)
    error_array[np.isnan(data_dict["r"])] = np.NaN

    return {
        "error": error_array,
        "coef": ww_v,
        "f": str(mdl_final),
        "f_error": str(mdl_error_final),
        "fit_quality": fit_quality,
        "y_test": y_test,
        "y_model": y_model
    }


if __name__ == "__main__":
    shape = (5, 5)
    inp = {v: np.random.rand(*shape) for v in ["tau", "sp", "wv", "I", "r", "dtau", "dsp", "dwv", "dI"]}
    inp["dsp"] = 0.5
    inp["dtau"] = 0.1
    mdl_vars = ["tau", "sp", "wv", "I"]
    s1 = ((1, 1, 1, 1),)
    s2 = ((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))

    logger = logging.getLogger("w")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    er = linear_error_modeling(data_dict=inp, s1=s1, s2=s2, mdl_vars=mdl_vars, logger=logger)
    print(er)
